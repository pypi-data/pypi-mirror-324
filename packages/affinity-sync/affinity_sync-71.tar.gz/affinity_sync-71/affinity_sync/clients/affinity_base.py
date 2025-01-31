import logging
from typing import Type, get_origin, TypeVar, Any, Union

import backoff
import requests

from ..module_types import base, affinity_v2_api as affinity_types

T = TypeVar('T', base.Base, list[base.Base])


class TryAgainError(Exception):
    pass


class AffinityBase:
    __URL = 'https://api.affinity.co/v2/'

    def __init__(self, api_key: str):
        self.__session = requests.Session()
        self.__session.headers.update({'Authorization': f'Bearer {api_key}'})
        self.__logger = logging.getLogger('affinity_sync.AffinityBaseClient')
        self.__api_key = api_key
        self.api_call_entitlement: affinity_types.ApiCallEntitlement | None = None

    def __extract_rate_limit(self, response: requests.Response):
        if not all(
                key in response.headers
                for key in [
                    'X-Ratelimit-Limit-User',
                    'X-Ratelimit-Limit-User-Remaining',
                    'X-Ratelimit-Limit-User-Reset',
                    'X-Ratelimit-Limit-Org',
                    'X-Ratelimit-Limit-Org-Remaining',
                    'X-Ratelimit-Limit-Org-Reset',
                ]
        ):
            raise ValueError('Rate limit headers not found in response')

        self.api_call_entitlement = affinity_types.ApiCallEntitlement.model_validate(response.headers)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.ConnectionError, TryAgainError),
        max_tries=3
    )
    def _send_request(
            self,
            method: str,
            url: str,
            result_type: Type[T],
            params: dict | None = None,
            json: dict | None = None,
            files: Any | None = None
    ) -> T:

        if files and json:
            raise ValueError('Cannot send both data and json in a request')

        self.__logger.debug(f'Sending {method.upper()} request to {url}')
        response = self.__session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            files=files,
            **({'auth': ('username', self.__api_key)} if 'v2' not in url else {})
        )

        if response.status_code == 422:
            raise TryAgainError()

        response.raise_for_status()
        self.__extract_rate_limit(response)

        if get_origin(result_type) is list:
            inner_type = result_type.__args__[0]

            return [inner_type.model_validate(item) for item in response.json()]

        if get_origin(result_type) is Union:
            inner_types = result_type.__args__
            errors = []

            for inner_type in inner_types:
                try:
                    return inner_type.model_validate(response.json())
                except Exception as e:
                    errors.append(e)
                    continue

            for error in errors:
                self.__logger.error(error)

            raise errors[0]

        return result_type.model_validate(response.json())
