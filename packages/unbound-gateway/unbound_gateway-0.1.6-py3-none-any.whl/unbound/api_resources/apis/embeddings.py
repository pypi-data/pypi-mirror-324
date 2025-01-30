import json
from typing import Optional, Union
import typing
from unbound.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from unbound.api_resources.client import AsyncUnbound, Unbound
from unbound.api_resources.types.embeddings_type import CreateEmbeddingResponse
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Embeddings(APIResource):
    def __init__(self, client: Unbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create(
        self,
        *,
        input: str,
        model: Optional[str] = "unbound-default",
        dimensions: Union[int, NotGiven] = NOT_GIVEN,
        encoding_format: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> CreateEmbeddingResponse:
        response = self.openai_client.with_raw_response.embeddings.create(
            input=input,
            model=model,
            dimensions=dimensions,
            encoding_format=encoding_format,
            user=user,
            extra_body=kwargs,
        )

        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEmbeddings(AsyncAPIResource):
    def __init__(self, client: AsyncUnbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create(
        self,
        *,
        input: str,
        model: Optional[str] = "unbound-default",
        dimensions: Union[int, NotGiven] = NOT_GIVEN,
        encoding_format: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> CreateEmbeddingResponse:
        response = await self.openai_client.with_raw_response.embeddings.create(
            input=input,
            model=model,
            dimensions=dimensions,
            encoding_format=encoding_format,
            user=user,
            extra_body=kwargs,
        )
        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
