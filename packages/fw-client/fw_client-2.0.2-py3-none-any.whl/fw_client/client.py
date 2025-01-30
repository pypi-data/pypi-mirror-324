"""Flywheel HTTP API sync client."""

import os
import platform
import random
import re
import time
import typing as t
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from importlib.metadata import version as pkg_version

import backoff
import httpx
from fw_utils import AttrDict
from httpx._auth import FunctionAuth
from packaging import version

from .errors import ValidationError

METHODS = ["delete", "get", "head", "options", "patch", "post", "put"]
# regex to match api keys with (to extract the host if it's embedded)
API_KEY_RE = re.compile(
    r"(?i)"
    r"((?P<api_key_type>bearer|scitran-user) )?"
    r"((?P<scheme>https?://)?(?P<host>[^:]+)(?P<port>:\d+)?:)?"
    r"(?P<api_key>.+)"
)
KILOBYTE = 1 << 10
MEGABYTE = 1 << 20
# cache time to live (duration to cache /api/config and /api/version response)
CACHE_TTL = 3600  # 1 hour
# x-accept-feature header sent by default to core-api
CORE_FEATURES = (
    "multipart_signed_url",
    "pagination",
    "safe-redirect",
    "subject-container",
)

# global cache of drone keys (device api keys acquired via drone secret)
DRONE_DEVICE_KEYS = {}
# retry
RETRY_METHODS = ("DELETE", "GET", "HEAD", "POST", "PUT", "OPTIONS")
RETRY_STATUSES = (429, 502, 503, 504)


class FWClient(httpx.Client):
    """Flywheel HTTP API base client."""

    def __init__(  # noqa: PLR0912, PLR0913, PLR0915
        self,
        *,
        api_key: str | None = None,
        url: str | None = None,
        client_name: str | None = None,
        client_version: str | None = None,
        client_info: dict[str, str] | None = None,
        io_proxy_url: str | None = None,
        snapshot_url: str | None = None,
        xfer_url: str | None = None,
        drone_secret: str | None = None,
        device_type: str | None = None,
        device_label: str | None = None,
        defer_auth: bool = False,
        core_features: t.Sequence[str] = CORE_FEATURES,
        retry_allowed_methods: t.Sequence[str] = RETRY_METHODS,
        retry_status_forcelist: t.Sequence[int] = RETRY_STATUSES,
        retry_backoff_factor: float = 0.5,
        retry_total: int = 5,
        **kwargs,
    ):
        """Initialize FW client."""
        self._cache: dict[str, tuple[t.Any, float]] = {}
        self.core_features = core_features
        self.defer_auth = defer_auth
        self.drone_secret = drone_secret
        self.device_type = device_type or client_name
        self.device_label = device_label
        self.retry_backoff_factor = retry_backoff_factor
        self.retry_allowed_methods = retry_allowed_methods
        self.retry_status_forcelist = retry_status_forcelist
        self.retry_total = retry_total
        if not (api_key or url):
            raise ValidationError("api_key or url required")
        # extract any additional key info "[type ][scheme://]host[:port]:key"
        if api_key:
            match = API_KEY_RE.match(t.cast(str, api_key))
            if not match:  # pragma: no cover
                raise ValidationError(f"invalid api_key: {api_key!r}")
            info = match.groupdict()
            # clean the key of extras (enhanced keys don't allow any)
            api_key = info["api_key"]
            # use site url prefixed on the key if otherwise not provided
            if not url:
                if not info["host"]:
                    msg = "Invalid API key format - expected <site>:<key>"
                    raise ValidationError(msg)
                scheme = info["scheme"] or "https://"
                host = info["host"]
                port = info["port"] or ""
                url = f"{scheme}{host}{port}"
        if not url:  # pragma: no cover
            raise ValidationError("url required")
        if not url.startswith("http"):
            url = f"https://{url}"
        # strip url /api path suffix if present to accommodate other apis
        url = re.sub(r"(/api)?/?$", "", url)
        self.svc_urls = {
            "/api": url,
            "/io-proxy": io_proxy_url,
            "/snapshot": snapshot_url,
            "/xfer": xfer_url,
        }
        kwargs["base_url"] = url
        kwargs.setdefault("timeout", httpx.Timeout(10, read=30))
        kwargs.setdefault("follow_redirects", True)
        client_info = client_info or {}
        client_info |= {client_name: client_version} if client_name else {}
        user_agent = dump_useragent(**client_info)
        kwargs.setdefault("headers", {}).setdefault("User-Agent", user_agent)
        if not (sync_transport := kwargs.pop("transport", None)):
            sync_transport = httpx.HTTPTransport(http2=True, retries=0)
        if not (async_transport := kwargs.pop("async_transport", None)):
            async_transport = httpx.AsyncHTTPTransport(http2=True, retries=0)
        super().__init__(**kwargs, transport=sync_transport)
        # setup the async client
        self._async = httpx.AsyncClient(**kwargs, transport=async_transport)
        self._async._base = self._base
        # patch request methods to support auth, error handling, stream
        patch_request(self)
        patch_request_methods(self)
        # patch build request to support service prefixes and core features
        patch_build_request(self)
        # require auth (unless it's deferred via defer_auth)
        creds = api_key or self.drone_secret
        if self.defer_auth and creds:
            msg = "api_key and drone_secret not allowed with defer_auth"
            raise ValidationError(msg)
        elif not self.defer_auth and not creds:
            raise ValidationError("api_key or drone_secret required")
        if api_key:
            # careful, core-api is case-sensitively testing for Bearer...
            key_type = "Bearer" if len(api_key) == 57 else "scitran-user"
            self.headers["Authorization"] = f"{key_type} {api_key}"
        # require device_type and device_label if drone
        elif not api_key and self.drone_secret:
            if not self.device_type:  # pragma: no cover
                raise ValidationError("device_type required")
            if not self.device_label:  # pragma: no cover
                raise ValidationError("device_label required")
            api_key = self._get_device_key()
            key_type = "Bearer" if len(api_key) == 57 else "scitran-user"
            self.headers["Authorization"] = f"{key_type} {api_key}"

    def __getattr__(self, name):
        """Proxy 'a' prefixed attributes to the async client."""
        try:
            if name.startswith("a"):
                aname = name[1:] if name != "aclose" else name
                return object.__getattribute__(self._async, aname)
            return object.__getattribute__(self._base, name)
        except AttributeError:  # pragma: no cover
            msg = f"{self.__class__.__name__!r} object has no attribute {name!r}"
            raise AttributeError(msg) from None

    def _get_device_key(self) -> str:
        """Return device API key for the given drone_secret (cached)."""
        drone = (self.base_url, self.device_type, self.device_label)
        if drone not in DRONE_DEVICE_KEYS:
            # limit the use of the secret only for acquiring a device api key
            assert self.drone_secret and self.device_type and self.device_label
            headers = {
                "X-Scitran-Auth": self.drone_secret,
                "X-Scitran-Method": self.device_type,
                "X-Scitran-Name": self.device_label,
            }
            kwargs: t.Any = {"headers": headers, "auth": None}
            # core-api auto-creates new device entries based on type and label
            # however, it may create conflicting ones for parallel requests...
            # FLYW-17258 intended to fix and guard against that, to no avail
            # to mitigate, add some(0-1) jitter before the 1st connection
            if "PYTEST_CURRENT_TEST" not in os.environ:
                time.sleep(random.random())  # pragma: no cover
            # furthermore, delete redundant device entries, leaving only the 1st
            # ie. try to enforce type/label uniqueness from the client side
            type_filter = f"type={self.device_type}"
            label_filter = f"label={self.device_label}"
            query = f"filter={type_filter}&filter={label_filter}"
            url = "/api/devices"
            devices = self.get(f"{url}?{query}", **kwargs)
            for device in devices[1:]:  # type: ignore
                self.delete(f"{url}/{device._id}", **kwargs)
            # legacy api keys are auto-generated and returned on the response
            # TODO generate key if not exposed after devices get enhanced keys
            # NOTE caching will need rework and move to self due to expiration
            device = self.get(f"{url}/self", **kwargs)
            DRONE_DEVICE_KEYS[drone] = device.key
        return DRONE_DEVICE_KEYS[drone]

    def _cached_get(self, path: str) -> AttrDict:
        """Return GET response cached with a one hour TTL."""
        now = time.time()
        val, exp = self._cache.get(path, (None, 0))
        if not val or now > exp:
            val = self.get(path)
            self._cache[path] = val, now + CACHE_TTL
        return val

    @property
    def core_config(self) -> AttrDict:
        """Return Core's configuration."""
        return self._cached_get("/api/config")

    @property
    def core_version(self) -> t.Optional[str]:
        """Return Core's release version."""
        return self._cached_get("/api/version").get("release")

    @property
    def auth_status(self) -> AttrDict:
        """Return the client's auth status."""
        status = self._cached_get("/api/auth/status")
        resource = "devices" if status.is_device else "users"
        status["info"] = self._cached_get(f"/api/{resource}/self")
        return status

    def check_feature(self, feature: str) -> bool:
        """Return True if Core has the given feature and it's enabled."""
        return bool(self.core_config.features.get(feature))  # type: ignore

    def check_version(self, min_ver: str) -> bool:
        """Return True if Core's version is greater or equal to 'min_ver'."""
        if not self.core_version:
            # assume latest on dev deployments without a version
            return True
        return version.parse(self.core_version) >= version.parse(min_ver)

    def upload_device_file(
        self,
        project_id: str,
        file: t.BinaryIO,
        origin: dict | None = None,
        content_encoding: str | None = None,
    ) -> str:
        """Upload a single file using the /api/storage/files endpoint (device only)."""
        assert self.auth_status.is_device, "Device authentication required"
        url = "/api/storage/files"
        origin = origin or self.auth_status.origin
        params = {
            "project_id": project_id,
            "origin_type": origin["type"],
            "origin_id": origin["id"],
            "signed_url": True,
        }
        headers = {"Content-Encoding": content_encoding} if content_encoding else {}
        response = self.post(url, params=params, headers=headers, raw=True)
        if response.is_success:
            upload = response.json()
            headers = upload.get("upload_headers") or {}
            if hasattr(file, "getbuffer"):
                headers["Content-Length"] = str(file.getbuffer().nbytes)
            else:
                headers["Content-Length"] = str(os.fstat(file.fileno()).st_size)
            try:

                def stream():
                    while chunk := file.read(MEGABYTE):
                        yield chunk

                self.put(
                    url=upload["upload_url"],
                    auth=httpx_anon,
                    headers=headers,
                    content=stream(),
                )
            # make sure we clean up any residue on failure
            except httpx.HTTPError:
                del_url = f"{url}/{upload['storage_file_id']}"
                self.delete(del_url, params={"ignore_storage_errors": True})
                raise
        # core's 409 means no signed url support - upload directly instead
        elif response.status_code == 409:
            del params["signed_url"]
            files = {"file": file}
            upload = self.post(url, params=params, headers=headers, files=files)
        else:
            response.raise_for_status()
        return upload["storage_file_id"]

    async def aupload_device_file(
        self,
        project_id: str,
        file: t.BinaryIO,
        origin: dict | None = None,
        content_encoding: str | None = None,
    ) -> str:
        """Upload a single file using the /api/storage/files endpoint (device only)."""
        assert self.auth_status.is_device, "Device authentication required"
        url = "/api/storage/files"
        origin = origin or self.auth_status.origin
        params = {
            "project_id": project_id,
            "origin_type": origin["type"],
            "origin_id": origin["id"],
            "signed_url": True,
        }
        headers = {"Content-Encoding": content_encoding} if content_encoding else {}
        response = await self.apost(url, params=params, headers=headers, raw=True)
        if response.is_success:
            upload = response.json()
            headers = upload.get("upload_headers") or {}
            if hasattr(file, "getbuffer"):
                headers["Content-Length"] = str(file.getbuffer().nbytes)
            else:
                headers["Content-Length"] = str(os.fstat(file.fileno()).st_size)
            try:

                async def stream():
                    while chunk := file.read(MEGABYTE):
                        yield chunk

                await self.aput(
                    url=upload["upload_url"],
                    auth=httpx_anon,
                    headers=headers,
                    content=stream(),
                )
            # make sure we clean up any residue on failure
            except httpx.HTTPError:
                del_url = f"{url}/{upload['storage_file_id']}"
                await self.adelete(del_url, params={"ignore_storage_errors": True})
                raise
        # core's 409 means no signed url support - upload directly instead
        elif response.status_code == 409:
            del params["signed_url"]
            files = {"file": file}
            upload = await self.apost(url, params=params, headers=headers, files=files)
        else:
            response.raise_for_status()
        return upload["storage_file_id"]


def patch_build_request(client: FWClient) -> None:
    """Patch build request to support service prefixes and core features."""
    orig_build_request = client._base.build_request

    def build_request(method, url, **kwargs):
        # dispatch known service prefixes to cluster-internal urls
        if not url.startswith("http"):
            svc_prefix = re.sub(r"^(/[^/]+)?.*$", r"\1", url)
            # use service base url if defined
            if client.svc_urls.get(svc_prefix):
                url = f"{client.svc_urls[svc_prefix]}{url}"
            # otherwise default to self.base_url IFF looks like a domain
            elif re.match(r".*\.[a-z]{2,}", str(client.base_url)):
                url = f"{client.base_url}{url}"  # pragma: no cover
            # raise error about missing service url for known prefixes/APIs
            elif svc_prefix in client.svc_urls:
                svc_name = f"{svc_prefix[1:]}".replace("-", "_")
                msg = f"{svc_name}_url required for {svc_prefix} requests"
                raise ValueError(f"{client.__class__.__name__}: {msg}")
            # raise error about invalid path for unknown prefixes
            else:
                msg = f"invalid URL path prefix: {svc_prefix}"
                raise ValueError(f"{client.__class__.__name__}: {msg}")
        headers = kwargs["headers"] = kwargs.get("headers") or {}
        # set default feature headers for core-api
        if "/api/" in url:
            headers.setdefault("X-Accept-Feature", ", ".join(client.core_features))
        return orig_build_request(method, url, **kwargs)

    client._base.build_request = build_request


def patch_request(client: FWClient) -> None:  # noqa: PLR0915
    """Patch request to be more powerful (auth, json, raise for status, stream)."""

    def get_retries():
        def retry_when(response: httpx.Response):
            method = response.request.method in client.retry_allowed_methods
            status = response.status_code in client.retry_status_forcelist
            # only requests with byte stream can be safely retried
            byte_stream = isinstance(response.request.stream, httpx.ByteStream)
            return method and status and byte_stream

        # backoff max tries includes the initial request, so add 1
        # because 0 means infinite tries
        on_pred, on_exc, expo = backoff.on_predicate, backoff.on_exception, backoff.expo
        tries, factor = client.retry_total + 1, client.retry_backoff_factor
        retry_http = on_pred(expo, retry_when, max_tries=tries, factor=factor)
        retry_tfer = on_exc(expo, httpx.TransportError, max_tries=tries, factor=factor)
        return retry_http, retry_tfer

    def prep_request(method, url, **kwargs) -> tuple[dict, dict]:
        # send anonymous request when the auth header is explicitly set to None
        headers = kwargs["headers"] = kwargs.get("headers") or {}
        if kwargs.get("auth") is None and headers.get("Authorization", ...) is None:
            kwargs["auth"] = httpx_anon
            headers.pop("Authorization")  # httpx raises on None
        # set authorization header from simple str auth kwarg
        if isinstance(kwargs.get("auth"), str):
            headers["Authorization"] = kwargs.pop("auth")
        send_kwargs = {"auth": kwargs.pop("auth", None)}
        send_kwargs["follow_redirects"] = kwargs.pop("follow_redirects", True)
        request = client.build_request(method=method, url=url, **kwargs)
        return request, send_kwargs

    def prep_response(response: httpx.Response, raw: bool, stream: bool = False):
        # raise if there was an http error (eg. 404)
        if not raw:
            response.raise_for_status()
        if raw or stream:
            return response
        # don't load empty response as json
        if not response.content:
            return None
        return response.json()

    def request(*args, raw: bool = False, **kwargs):
        request, send_kwargs = prep_request(*args, **kwargs)
        retry_http, retry_transport = get_retries()
        response = retry_http(retry_transport(client.send))(request, **send_kwargs)
        return prep_response(response, raw)

    async def arequest(*args, raw: bool = False, **kwargs):
        request, send_kwargs = prep_request(*args, **kwargs)
        retry_http, retry_transport = get_retries()
        send = client._async.send
        response = await retry_http(retry_transport(send))(request, **send_kwargs)
        return prep_response(response, raw)

    @contextmanager
    def stream(*args, raw: bool = False, **kwargs):
        request, send_kwargs = prep_request(*args, **kwargs)
        retry_http, retry_transport = get_retries()
        send = retry_http(retry_transport(client.send))
        response = send(request, stream=True, **send_kwargs)
        try:
            yield prep_response(response, raw, stream=True)
        finally:
            response.close()

    @asynccontextmanager
    async def astream(*args, raw: bool = False, **kwargs):
        request, send_kwargs = prep_request(*args, **kwargs)
        retry_http, retry_transport = get_retries()
        send = retry_http(retry_transport(client._async.send))
        response = await send(request, stream=True, **send_kwargs)
        try:
            yield prep_response(response, raw, stream=True)
        finally:
            await response.aclose()

    client.request = request
    client.stream = stream
    client._async.request = arequest
    client._async.stream = astream


def patch_request_methods(client: FWClient) -> None:
    """Patch request methods to pass all kwargs to the underlying request method."""
    for method in METHODS:
        setattr(client, method, partial(client.request, method))
        setattr(client._async, method, partial(client._async.request, method))


def dump_useragent(*args: str, **kwargs: str) -> str:
    """Return parsable UA string for the given agent info."""
    useragent = f"fw-client/{pkg_version('fw_client')}"
    kwargs = {"platform": platform.platform()} | kwargs
    comments = list(args) + [f"{k}:{v}" if v else k for k, v in kwargs.items()]
    return f"{useragent} ({'; '.join(comments)})"


def httpx_pop_auth_header(request):
    """Pop authorization header from request to enable anonymous request."""
    request.headers.pop("Authorization", None)
    return request


httpx_anon = FunctionAuth(httpx_pop_auth_header)
