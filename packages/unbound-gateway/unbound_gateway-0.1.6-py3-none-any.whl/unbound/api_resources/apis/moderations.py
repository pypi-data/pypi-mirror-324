import json
from typing import List, Union
from unbound.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from unbound.api_resources.client import AsyncUnbound, Unbound
from ..._vendor.openai._types import NotGiven, NOT_GIVEN
from unbound.api_resources.types.moderations_type import ModerationCreateResponse


class Moderations(APIResource):
    def __init__(self, client: Unbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        input: Union[str, List[str]],
        model: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ModerationCreateResponse:
        response = self.openai_client.with_raw_response.moderations.create(
            input=input, model=model, extra_body=kwargs
        )
        data = ModerationCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncModerations(AsyncAPIResource):
    def __init__(self, client: AsyncUnbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        input: Union[str, List[str]],
        model: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ModerationCreateResponse:
        response = await self.openai_client.with_raw_response.moderations.create(
            input=input, model=model, extra_body=kwargs
        )
        data = ModerationCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
