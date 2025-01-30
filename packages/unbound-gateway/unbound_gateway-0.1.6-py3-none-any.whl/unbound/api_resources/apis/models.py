import json
from typing import Union
from unbound.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from unbound.api_resources.client import AsyncUnbound, Unbound
from unbound.api_resources.types.models_type import Model, ModelDeleted, ModelList
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Models(APIResource):
    def __init__(self, client: Unbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, **kwargs) -> ModelList:
        response = self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def retrieve(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Model:
        response = self.openai_client.with_raw_response.models.retrieve(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        response = self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncModels(AsyncAPIResource):
    def __init__(self, client: AsyncUnbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, **kwargs) -> ModelList:
        response = await self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def retrieve(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Model:
        response = await self.openai_client.with_raw_response.models.retrieve(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        response = await self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data
