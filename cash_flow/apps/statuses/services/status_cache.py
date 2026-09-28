import hashlib
import uuid
from urllib.parse import urlencode

from django.core.cache import cache
from django.http.request import QueryDict


def _build_version_key(user_id: int) -> str:
    return f"statuses:{user_id}"


def _build_status_page_key(
    user_id: int,
    cache_version: str,
    page: int,
    hashed_params: str,
) -> str:
    return f"statuses:{user_id}:{cache_version}:{page}:{hashed_params}"


def _get_query_params_string(query_params: QueryDict) -> str:
    request_params = sorted((k, v) for k, vals in query_params.lists() for v in vals)
    hash_params_str = hashlib.sha256()
    hash_params_str.update(urlencode(request_params).encode())

    return hash_params_str.hexdigest()


def _get_page_from_params(query_params: QueryDict) -> int:
    page_value = int(query_params.get("page", 1))
    query_params.pop("page", None)
    return page_value


class StatusCache:
    def _get_version(self, user_id: int) -> str:
        version_key = _build_version_key(user_id)
        version_value = cache.get(key=version_key)
        if version_value is None:
            version_value = uuid.uuid4().hex
            cache.set(key=version_key, value=version_value, timeout=None)

        return version_value

    def set_status_cache(
        self,
        response_data: list | dict,
        user_id: int,
        query_params: QueryDict,
    ) -> None:
        mutable_params = query_params.copy()
        cache_version = self._get_version(user_id)
        page = _get_page_from_params(mutable_params)
        hashed_params = _get_query_params_string(mutable_params)
        page_key = _build_status_page_key(
            user_id=user_id,
            cache_version=cache_version,
            page=page,
            hashed_params=hashed_params,
        )

        cache.set(key=page_key, value=response_data, timeout=300)

    def read_status_cache(
        self, user_id: int, query_params: QueryDict
    ) -> dict | None:
        mutable_params = query_params.copy()
        cache_version = self._get_version(user_id)
        page = _get_page_from_params(mutable_params)
        hashed_params = _get_query_params_string(mutable_params)
        page_key = _build_status_page_key(
            user_id=user_id,
            cache_version=cache_version,
            page=page,
            hashed_params=hashed_params,
        )

        statuses = cache.get(
            key=page_key,
            default=None,
        )

        return statuses

    def invalidate_status_cache(self, user_id: int):
        version_key = _build_version_key(user_id)
        version_value = uuid.uuid4().hex
        cache.set(key=version_key, value=version_value, timeout=None)
