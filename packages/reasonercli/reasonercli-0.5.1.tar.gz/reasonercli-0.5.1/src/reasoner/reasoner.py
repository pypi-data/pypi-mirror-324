import asyncio
import importlib.metadata
import time
from enum import Enum
from typing import Optional, Union

import httpx

from .config import read_config_file

BASE_URL = "https://api.reasoner.com"
REASONER_SDK = "reasoner-1-pro"
REASONER_SDK_VERSION = importlib.metadata.version("reasonercli")


MAX_QUERY_TIMEOUT_SECS = 600  # 10 mins


class TraceStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


def try_get_api_key_from_config_file():
    try:
        config = read_config_file()
        api_key = config.get("API_KEY")
        return api_key
    except Exception:
        pass


class Reasoner:
    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into Reasoner(api_key)"
            )

        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
                "X-REASONER-SDK-VERSION": REASONER_SDK_VERSION,
            },
            timeout=300.0,
        )

    @property
    def auth(self):
        from .auth import Auth

        return Auth(self.client, self.base_url)

    @property
    def documents(self):
        from .documents import Documents

        return Documents(self.client, self.base_url)

    @property
    def indexes(self):
        from .indexes import Indexes

        return Indexes(self.client, self.base_url)

    def trace(self, query: str, index_uid: str, options: Union[dict, None] = None, wait=True):
        data = {"index_uid": index_uid, "query": query}
        if options:
            data["options"] = options

        response = self.client.post(
            f"{self.base_url}/public/v1/trace",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid query response")

        if wait:
            return self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    def get_trace_response(self, response_uid: str):
        response = self.client.get(
            f"{self.base_url}/public/v1/trace/status/{response_uid}",
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return response_json

    def _poll_for_trace_response(self, response_uid: str):
        # Poll for response until it's complete
        start_time = time.time()
        while True:
            response_json = self.get_trace_response(response_uid)
            status = response_json.get("status")

            if status == TraceStatus.SUCCESS.value:
                return response_json.get("response")
            elif status == TraceStatus.ERROR.value:
                raise ValueError("Query processing failed")

            if time.time() - start_time > MAX_QUERY_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Query processing timed out after {MAX_QUERY_TIMEOUT_SECS}s"
                )

            time.sleep(5)


class ReasonerAsync:
    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.api_key = api_key
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into ReasonerAsync(api_key)"
            )

        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
                "X-REASONER-SDK-VERSION": REASONER_SDK_VERSION,
            },
            timeout=300.0,
        )

    @property
    def auth(self):
        from .auth import AuthAsync

        return AuthAsync(self.client, self.base_url)

    @property
    def documents(self):
        from .documents import DocumentsAsync

        return DocumentsAsync(self.client, self.base_url)

    @property
    def indexes(self):
        from .indexes import IndexesAsync

        return IndexesAsync(self.client, self.base_url)

    async def trace(
        self, query: str, index_uid: str, options: Union[dict,  None] = None, wait=True
    ):
        data = {"index_uid": index_uid, "query": query}
        if options:
            data["options"] = options

        response = await self.client.post(
            f"{self.base_url}/public/v1/trace",
            json=data,
        )
        response.raise_for_status()
        response_json = response.json() or {}
        response_uid = response_json.get("response_uid")
        if not response_uid:
            raise ValueError("Invalid query response")

        if wait:
            return await self._poll_for_trace_response(response_uid)
        else:
            return response_uid

    async def get_trace_response(self, response_uid: str):
        response = await self.client.get(
            f"{self.base_url}/public/v1/trace/status/{response_uid}",
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return response_json

    async def _poll_for_trace_response(self, response_uid: str):
        # Poll for response until it's complete
        start_time = time.time()
        while True:
            response_json = await self.get_trace_response(response_uid)
            status = response_json.get("status")

            if status == TraceStatus.SUCCESS.value:
                return response_json.get("response")
            elif status == TraceStatus.ERROR.value:
                raise ValueError("Query processing failed")

            if time.time() - start_time > MAX_QUERY_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Query processing timed out after {MAX_QUERY_TIMEOUT_SECS}s"
                )

            await asyncio.sleep(5)
