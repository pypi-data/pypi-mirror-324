import asyncio
import base64
import ctypes
import urllib.parse
import uuid
from json import dumps, loads
from typing import Any, Dict, List, Optional, Union

from .__version__ import __version__
from .cffi import request, freeMemory, destroySession
from .cookies import cookiejar_from_dict, merge_cookies, extract_cookies_to_jar
from .exceptions import TLSClientExeption
from .response import build_response, Response
from .settings import ClientIdentifiers
from .structures import CaseInsensitiveDict


class AsyncSession:
    """
    Asynchronous session to perform HTTP requests with special TLS settings and session management.

    This class provides an asynchronous session that uses a Go-based TLS client under the hood.
    It supports setting client identifiers, custom JA3 strings, HTTP/2 settings, certificate pinning,
    custom proxy usage, and more. Each session is tracked by a unique session ID, so destroying or closing
    the session frees its underlying resources.

    The session includes:

    - Standard HTTP settings (headers, proxies, cookies, etc.)
    - Advanced TLS settings (client identifiers, JA3, HTTP/2 h2_settings, supported signature algorithms, etc.)
    - HTTP/2 custom frames and priorities
    - Custom extension order and forced HTTP/1 usage if necessary
    - Debugging and panic catching (Go-based)

    Examples::

        async with AsyncSession(client_identifier="chrome_120") as session:
            response = await session.get("https://example.com")
            print(response.status_code, response.text)
    """

    def __init__(
            self,
            client_identifier: ClientIdentifiers = "chrome_120",
            ja3_string: Optional[str] = None,
            h2_settings: Optional[Dict[str, int]] = None,
            h2_settings_order: Optional[List[str]] = None,
            supported_signature_algorithms: Optional[List[str]] = None,
            supported_delegated_credentials_algorithms: Optional[List[str]] = None,
            supported_versions: Optional[List[str]] = None,
            key_share_curves: Optional[List[str]] = None,
            cert_compression_algo: Optional[str] = None,
            additional_decode: Optional[str] = None,
            pseudo_header_order: Optional[List[str]] = None,
            connection_flow: Optional[int] = None,
            priority_frames: Optional[List[dict]] = None,
            header_order: Optional[List[str]] = None,
            header_priority: Optional[List[str]] = None,
            random_tls_extension_order: Optional[bool] = False,
            force_http1: Optional[bool] = False,
            catch_panics: Optional[bool] = False,
            debug: Optional[bool] = False,
            certificate_pinning: Optional[Dict[str, List[str]]] = None,
            # -- New parameters --
            local_address: Optional[str] = None,
            server_name_overwrite: Optional[str] = None,
            request_host_override: Optional[str] = None,
            transport_options: Optional[Any] = None,
            stream_output_block_size: Optional[int] = None,
            stream_output_eof_symbol: Optional[str] = None,
            stream_output_path: Optional[str] = None,
            is_byte_response: bool = False,
            is_rotating_proxy: bool = False,
            disable_ipv6: bool = False,
            disable_ipv4: bool = False,
            with_default_cookie_jar: bool = True,
            without_cookie_jar: bool = False,
            default_headers: Optional[Dict[str, List[str]]] = None,
            connect_headers: Optional[Dict[str, List[str]]] = None,
            alpn_protocols: Optional[List[str]] = None,
            alps_protocols: Optional[List[str]] = None,
            ech_candidate_payloads: Optional[List[int]] = None,
            ech_candidate_cipher_suites: Optional[Any] = None,
    ) -> None:
        """
        Initializes the AsyncSession with various HTTP and TLS parameters.

        :param client_identifier:
            Identifies the client. For example, "chrome_103", "firefox_102", "opera_89", etc.
            Defaults to "chrome_120". See the settings file for more possible values.

        :param ja3_string:
            A JA3 string specifying TLS fingerprint details such as TLSVersion, Ciphers, Extensions,
            EllipticCurves, and EllipticCurvePointFormats.

        :param h2_settings:
            A dictionary representing HTTP/2 frame settings. Possible keys include:
            HEADER_TABLE_SIZE, SETTINGS_ENABLE_PUSH, MAX_CONCURRENT_STREAMS, INITIAL_WINDOW_SIZE,
            MAX_FRAME_SIZE, MAX_HEADER_LIST_SIZE.

        :param h2_settings_order:
            A list specifying the order of the HTTP/2 settings.

        :param supported_signature_algorithms:
            A list of supported signature algorithms, such as PSSWithSHA256, ECDSAWithP256AndSHA256,
            PKCS1WithSHA256, etc.

        :param supported_delegated_credentials_algorithms:
            A list of supported delegated credentials algorithms, such as PSSWithSHA256,
            ECDSAWithP256AndSHA256, PKCS1WithSHA256, etc.

        :param supported_versions:
            A list of supported TLS versions, for example: GREASE, 1.3, 1.2.

        :param key_share_curves:
            A list of key share curves, for example: GREASE, P256, X25519.

        :param cert_compression_algo:
            Certificate compression algorithm, for example: "zlib", "brotli", or "zstd".

        :param additional_decode:
            Specifies an additional decoding algorithm for the response body, such as "gzip", "br", or "deflate".

        :param pseudo_header_order:
            A list specifying the pseudo-header order (e.g., :method, :authority, :scheme, :path).

        :param connection_flow:
            The connection flow control or window size increment for HTTP/2.

        :param priority_frames:
            A list specifying custom HTTP/2 priority frames.

        :param header_order:
            A list specifying the order of outgoing HTTP headers.

        :param header_priority:
            A list or dictionary specifying HTTP/2 header priority parameters.

        :param random_tls_extension_order:
            Whether to randomize the TLS extension order.

        :param force_http1:
            Whether to force HTTP/1 usage instead of HTTP/2 (or higher).

        :param catch_panics:
            Whether to catch and suppress Go-level panic traces.

        :param debug:
            Enables debug mode for additional logging output.

        :param certificate_pinning:
            A dictionary for certificate pinning. Useful for verifying certain hosts with pinned certificates.

        :param local_address:
            Local address to which the connection should bind.

        :param server_name_overwrite:
            Overwrites the Server Name Indication (SNI) used in the TLS handshake.

        :param request_host_override:
            Overrides the Host header.

        :param transport_options:
            Additional transport-related options (custom structure).

        :param stream_output_block_size:
            Block size in bytes for streaming output.

        :param stream_output_eof_symbol:
            Symbol or string marking the end-of-file when streaming output.

        :param stream_output_path:
            File path to which streamed output should be written.

        :param is_byte_response:
            If True, indicates that the response should be treated as raw bytes (no decoding).

        :param is_rotating_proxy:
            If True, signals that a rotating proxy setup is in use.

        :param disable_ipv6:
            If True, IPv6 traffic will be disabled.

        :param disable_ipv4:
            If True, IPv4 traffic will be disabled.

        :param with_default_cookie_jar:
            If True, uses the default cookie jar for session cookies.

        :param without_cookie_jar:
            If True, disables cookie handling entirely.

        :param default_headers:
            A dictionary of default headers, formatted as {"HeaderName": ["value1", "value2"]}.

        :param connect_headers:
            A dictionary of headers to be sent when establishing a CONNECT request.

        :param alpn_protocols:
            A list of ALPN protocols to advertise.

        :param alps_protocols:
            A list of ALPS protocols to advertise.

        :param ech_candidate_payloads:
            A list of ECH (Encrypted Client Hello) candidate payloads (uint16).

        :param ech_candidate_cipher_suites:
            A custom structure defining ECH candidate cipher suites.
            https://github.com/bogdanfinn/utls/blob/7cda087fe2c011df9697840209a6ef890169d0fe/cipher_suites.go#L678

        :return:
            None
        """
        self._session_id = str(uuid.uuid4())
        # Standard Settings
        self.headers = CaseInsensitiveDict(
            {
                "User-Agent": f"tls-client/{__version__}",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
        )
        self.proxies = {}
        self.params = {}
        self.cookies = cookiejar_from_dict({})
        self.timeout_seconds = 30
        self.certificate_pinning = certificate_pinning

        # Advanced Settings
        self.client_identifier = client_identifier
        self.ja3_string = ja3_string
        self.h2_settings = h2_settings
        self.h2_settings_order = h2_settings_order
        self.supported_signature_algorithms = supported_signature_algorithms
        self.supported_delegated_credentials_algorithms = supported_delegated_credentials_algorithms
        self.supported_versions = supported_versions
        self.key_share_curves = key_share_curves
        self.cert_compression_algo = cert_compression_algo
        self.additional_decode = additional_decode
        self.pseudo_header_order = pseudo_header_order
        self.connection_flow = connection_flow
        self.priority_frames = priority_frames
        self.header_order = header_order
        self.header_priority = header_priority
        self.random_tls_extension_order = random_tls_extension_order
        self.force_http1 = force_http1
        self.catch_panics = catch_panics
        self.debug = debug

        self.local_address = local_address
        self.server_name_overwrite = server_name_overwrite
        self.request_host_override = request_host_override
        self.transport_options = transport_options
        self.stream_output_block_size = stream_output_block_size
        self.stream_output_eof_symbol = stream_output_eof_symbol
        self.stream_output_path = stream_output_path
        self.is_byte_response = is_byte_response
        self.is_rotating_proxy = is_rotating_proxy
        self.disable_ipv6 = disable_ipv6
        self.disable_ipv4 = disable_ipv4
        self.with_default_cookie_jar = with_default_cookie_jar
        self.without_cookie_jar = without_cookie_jar
        self.default_headers = default_headers or {}
        self.connect_headers = connect_headers or {}
        self.alpn_protocols = alpn_protocols or []
        self.alps_protocols = alps_protocols or []
        self.ech_candidate_payloads = ech_candidate_payloads or []
        self.ech_candidate_cipher_suites = ech_candidate_cipher_suites

    async def __aenter__(self):
        """
        Enters the session in an asynchronous context manager.

        :returns:
            The current session instance.
        """
        return self

    async def __aexit__(self, *args):
        """
        Exits the session in an asynchronous context manager.

        Frees resources by calling the `close()` method asynchronously.
        """
        await self.close()

    async def close(self) -> str:
        """
        Closes the session and frees allocated Go memory resources.

        :returns:
            The JSON response string from the destroy session call.
        """
        destroy_session_payload = {
            "sessionId": self._session_id
        }

        destroy_session_response = await asyncio.to_thread(
            destroySession, dumps(destroy_session_payload).encode('utf-8')
        )
        destroy_session_response_bytes = ctypes.string_at(destroy_session_response)
        destroy_session_response_string = destroy_session_response_bytes.decode('utf-8')
        destroy_session_response_object = loads(destroy_session_response_string)

        await asyncio.to_thread(
            freeMemory, destroy_session_response_object['id'].encode('utf-8')
        )

        return destroy_session_response_string

    async def execute_request(
            self,
            method: str,
            url: str,
            params: Optional[dict] = None,
            data: Optional[Union[str, dict]] = None,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            json: Optional[dict] = None,
            allow_redirects: Optional[bool] = False,
            insecure_skip_verify: Optional[bool] = False,
            timeout_seconds: Optional[int] = None,
            proxy: Optional[dict] = None
    ) -> Response:
        """
        Executes an HTTP request using the Go-based TLS client in a separate thread.

        :param method:
            The HTTP method (GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD).
        :param url:
            The request URL.
        :param params:
            Querystring parameters to be appended to the URL.
            If values are lists, they represent multiple values for the same key.
        :param data:
            The request body for form data or raw string/bytes. Priority is given to `data` over `json`.
        :param headers:
            Additional headers to merge with the session's default headers.
        :param cookies:
            Cookies to merge with the session's cookies.
        :param json:
            JSON body if `data` is not provided. If it is a structured object, it will be JSON-encoded automatically.
        :param allow_redirects:
            Whether to follow redirects. Defaults to False.
        :param insecure_skip_verify:
            Whether to skip TLS certificate verification. Defaults to False.
        :param timeout_seconds:
            Request timeout in seconds. Defaults to session's `timeout_seconds`.
        :param proxy:
            Proxy settings as a dictionary or string.
            For example: {"http": "http://user:pass@ip:port", "https": "http://user:pass@ip:port"}.

        :returns:
            The response object.

        :raises TLSClientExeption:
            If the underlying Go client returns a status code of 0 (error).
        """

        def build_payload():
            final_url = url
            if params is not None:
                # Append query parameters to the URL
                final_url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"

            # Determine the request body
            if data is None and json is not None:
                # Use JSON as the body if data is not provided
                if isinstance(json, (dict, list)):
                    json_data = dumps(json)
                else:
                    json_data = json
                request_body = json_data
                content_type = "application/json"
            elif data is not None and not isinstance(data, (str, bytes)):
                # Use URL-encoded data
                request_body = urllib.parse.urlencode(data, doseq=True)
                content_type = "application/x-www-form-urlencoded"
            else:
                # Use raw data or bytes
                request_body = data
                content_type = None

            # Set Content-Type header if applicable
            if content_type is not None and "content-type" not in self.headers:
                self.headers["Content-Type"] = content_type

            # Merge headers from the session and the request
            if self.headers is None:
                merged_headers = CaseInsensitiveDict(headers)
            elif headers is None:
                merged_headers = self.headers
            else:
                merged_headers = CaseInsensitiveDict(self.headers)
                merged_headers.update(headers)
                # Remove keys with None values
                none_keys = [k for (k, v) in merged_headers.items() if v is None or k is None]
                for key in none_keys:
                    del merged_headers[key]

            # Merge cookies from the session and the request
            merged_cookies = merge_cookies(self.cookies, cookies or {})
            request_cookies = [
                {
                    "domain": c.domain,
                    "expires": c.expires,
                    "name": c.name,
                    "path": c.path,
                    "value": c.value.replace('"', "")
                }
                for c in merged_cookies
            ]

            # Determine the proxy configuration
            final_proxy = ""
            if isinstance(proxy, dict) and "http" in proxy:
                final_proxy = proxy["http"]
            elif isinstance(proxy, str):
                final_proxy = proxy

            # Use session timeout if not overridden
            final_timeout_seconds = timeout_seconds or self.timeout_seconds

            # Retrieve certificate pinning configuration if available
            final_certificate_pinning = self.certificate_pinning

            # Check if the request body is binary
            is_byte_request = isinstance(request_body, (bytes, bytearray))

            # Build the payload dictionary
            payload = {
                "sessionId": self._session_id,
                "followRedirects": allow_redirects,
                "forceHttp1": self.force_http1,
                "withDebug": self.debug,
                "catchPanics": self.catch_panics,

                # Headers and header order
                "headers": dict(merged_headers),
                "headerOrder": self.header_order,

                # TLS/HTTP settings
                "insecureSkipVerify": insecure_skip_verify,
                "isByteRequest": is_byte_request,
                "isByteResponse": self.is_byte_response,
                "isRotatingProxy": self.is_rotating_proxy,
                "disableIPV6": self.disable_ipv6,
                "disableIPV4": self.disable_ipv4,
                "withDefaultCookieJar": self.with_default_cookie_jar,
                "withoutCookieJar": self.without_cookie_jar,

                # Additional headers
                "defaultHeaders": self.default_headers,
                "connectHeaders": self.connect_headers,

                # Network settings
                "localAddress": self.local_address,
                "serverNameOverwrite": self.server_name_overwrite,
                "requestHostOverride": self.request_host_override,
                "transportOptions": self.transport_options,

                # Stream output settings
                "streamOutputBlockSize": self.stream_output_block_size,
                "streamOutputEOFSymbol": self.stream_output_eof_symbol,
                "streamOutputPath": self.stream_output_path,

                # Timeout settings (use only one)
                "timeoutMilliseconds": final_timeout_seconds * 1000,

                # Additional decoding settings
                "additionalDecode": self.additional_decode,

                # Proxy configuration
                "proxyUrl": final_proxy if final_proxy else None,

                # Request URL/method/body
                "requestUrl": final_url,
                "requestMethod": method,
                "requestBody": (
                    base64.b64encode(request_body).decode()
                    if is_byte_request else request_body
                ),
                "requestCookies": request_cookies,
            }

            # Add certificate pinning hosts if specified
            if final_certificate_pinning:
                payload["certificatePinningHosts"] = final_certificate_pinning

            # Use custom TLS settings if client_identifier is not specified
            if self.client_identifier is None:
                payload["customTlsClient"] = {
                    "ja3String": self.ja3_string or "",
                    "h2Settings": self.h2_settings or {},
                    "h2SettingsOrder": self.h2_settings_order or [],
                    "pseudoHeaderOrder": self.pseudo_header_order or [],
                    "connectionFlow": self.connection_flow or 0,
                    "priorityFrames": self.priority_frames or [],
                    "headerPriority": self.header_priority or {},
                    "certCompressionAlgo": self.cert_compression_algo or "",
                    "supportedVersions": self.supported_versions or [],
                    "supportedSignatureAlgorithms": self.supported_signature_algorithms or [],
                    "supportedDelegatedCredentialsAlgorithms": (
                            self.supported_delegated_credentials_algorithms or []
                    ),
                    "keyShareCurves": self.key_share_curves or [],
                    # New fields for customTlsClient
                    "alpnProtocols": self.alpn_protocols or [],
                    "alpsProtocols": self.alps_protocols or [],
                    "ECHCandidatePayloads": self.ech_candidate_payloads or [],
                    "ECHCandidateCipherSuites": self.ech_candidate_cipher_suites or [],
                }
            else:
                # Use predefined client_identifier
                payload["tlsClientIdentifier"] = self.client_identifier
                payload["withRandomTLSExtensionOrder"] = self.random_tls_extension_order

            return payload

        payload = build_payload()

        def make_request():
            return request(dumps(payload).encode('utf-8'))

        response = await asyncio.to_thread(make_request)

        response_bytes = ctypes.string_at(response)
        response_string = response_bytes.decode('utf-8')
        response_object = loads(response_string)
        await asyncio.to_thread(freeMemory, response_object['id'].encode('utf-8'))

        if response_object["status"] == 0:
            raise TLSClientExeption(response_object["body"])

        response_cookie_jar = extract_cookies_to_jar(
            request_url=url,
            request_headers=payload["headers"],
            cookie_jar=self.cookies,
            response_headers=response_object["headers"]
        )
        return build_response(response_object, response_cookie_jar)

    async def get(self, url: str, **kwargs: Any) -> Response:
        """
        Sends an asynchronous GET request.

        :param url:
            The request URL.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="GET", url=url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> Response:
        """
        Sends an asynchronous OPTIONS request.

        :param url:
            The request URL.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="OPTIONS", url=url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> Response:
        """
        Sends an asynchronous HEAD request.

        :param url:
            The request URL.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="HEAD", url=url, **kwargs)

    async def post(
            self,
            url: str,
            data: Optional[Union[str, dict]] = None,
            json: Optional[dict] = None,
            **kwargs: Any
    ) -> Response:
        """
        Sends an asynchronous POST request.

        :param url:
            The request URL.
        :param data:
            The request body for form data or raw string/bytes. Priority is given to `data` over `json`.
        :param json:
            JSON body if `data` is not provided. If it is a structured object, it will be JSON-encoded automatically.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="POST", url=url, data=data, json=json, **kwargs)

    async def put(
            self,
            url: str,
            data: Optional[Union[str, dict]] = None,
            json: Optional[dict] = None,
            **kwargs: Any
    ) -> Response:
        """
        Sends an asynchronous PUT request.

        :param url:
            The request URL.
        :param data:
            The request body for form data or raw string/bytes. Priority is given to `data` over `json`.
        :param json:
            JSON body if `data` is not provided. If it is a structured object, it will be JSON-encoded automatically.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="PUT", url=url, data=data, json=json, **kwargs)

    async def patch(
            self,
            url: str,
            data: Optional[Union[str, dict]] = None,
            json: Optional[dict] = None,
            **kwargs: Any
    ) -> Response:
        """
        Sends an asynchronous PATCH request.

        :param url:
            The request URL.
        :param data:
            The request body for form data or raw string/bytes. Priority is given to `data` over `json`.
        :param json:
            JSON body if `data` is not provided. If it is a structured object, it will be JSON-encoded automatically.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="PATCH", url=url, data=data, json=json, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Response:
        """
        Sends an asynchronous DELETE request.

        :param url:
            The request URL.
        :param kwargs:
            Additional arguments to be passed to `execute_request`.

        :returns:
            The response object.
        """
        return await self.execute_request(method="DELETE", url=url, **kwargs)
