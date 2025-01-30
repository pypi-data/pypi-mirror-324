from __future__ import annotations

from typing import Optional
from unbound.api_resources import apis
from unbound.api_resources.base_client import APIClient, AsyncAPIClient

# from openai import AsyncOpenAI, OpenAI
from .._vendor.openai import OpenAI, AsyncOpenAI


class Unbound(APIClient):
    completions: apis.Completion
    chat: apis.ChatCompletion
    generations: apis.Generations
    prompts: apis.Prompts
    embeddings: apis.Embeddings
    feedback: apis.Feedback
    images: apis.Images
    files: apis.MainFiles
    models: apis.Models
    moderations: apis.Moderations
    audio: apis.Audio
    batches: apis.Batches
    fine_tuning: apis.FineTuning
    admin: apis.Admin
    uploads: apis.Uploads
    configs: apis.Configs
    api_keys: apis.ApiKeys
    virtual_keys: apis.VirtualKeys
    logs: apis.Logs

    class beta:
        assistants: apis.Assistants
        threads: apis.Threads
        vector_stores: apis.VectorStores
        chat: apis.BetaChat

        def __init__(self, client: Unbound) -> None:
            self.assistants = apis.Assistants(client)
            self.threads = apis.Threads(client)
            self.vector_stores = apis.VectorStores(client)
            self.chat = apis.BetaChat(client)

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )

        self.openai_client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            default_headers=self.allHeaders,
            max_retries=0,
        )

        self.completions = apis.Completion(self)
        self.chat = apis.ChatCompletion(self)
        self.generations = apis.Generations(self)
        self.prompts = apis.Prompts(self)
        self.embeddings = apis.Embeddings(self)
        self.feedback = apis.Feedback(self)
        self.images = apis.Images(self)
        self.files = apis.MainFiles(self)
        self.models = apis.Models(self)
        self.moderations = apis.Moderations(self)
        self.audio = apis.Audio(self)
        self.batches = apis.Batches(self)
        self.fine_tuning = apis.FineTuning(self)
        self.admin = apis.Admin(self)
        self.uploads = apis.Uploads(self)
        self.configs = apis.Configs(self)
        self.api_keys = apis.ApiKeys(self)
        self.virtual_keys = apis.VirtualKeys(self)
        self.logs = apis.Logs(self)
        self.beta = self.beta(self)  # type: ignore

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> Unbound:
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            **kwargs,
        )

    def post(self, url: str, **kwargs):
        return apis.Post(self).create(url=url, **kwargs)

    with_options = copy


class AsyncUnbound(AsyncAPIClient):
    completions: apis.AsyncCompletion
    chat: apis.AsyncChatCompletion
    generations: apis.AsyncGenerations
    prompts: apis.AsyncPrompts
    embeddings: apis.AsyncEmbeddings
    feedback: apis.AsyncFeedback
    images: apis.AsyncImages
    files: apis.AsyncMainFiles
    models: apis.AsyncModels
    moderations: apis.AsyncModerations
    audio: apis.AsyncAudio
    batches: apis.AsyncBatches
    fine_tuning: apis.AsyncFineTuning
    admin: apis.AsyncAdmin
    uploads: apis.AsyncUploads
    configs: apis.AsyncConfigs
    api_keys: apis.AsyncApiKeys
    virtual_keys: apis.AsyncVirtualKeys
    logs: apis.AsyncLogs

    class beta:
        assistants: apis.AsyncAssistants
        threads: apis.AsyncThreads
        vector_stores: apis.AsyncVectorStores
        chat: apis.AsyncBetaChat

        def __init__(self, client: AsyncUnbound) -> None:
            self.assistants = apis.AsyncAssistants(client)
            self.threads = apis.AsyncThreads(client)
            self.vector_stores = apis.AsyncVectorStores(client)
            self.chat = apis.AsyncBetaChat(client)

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )

        self.openai_client = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url,
            default_headers=self.allHeaders,
            max_retries=0,
        )

        self.completions = apis.AsyncCompletion(self)
        self.chat = apis.AsyncChatCompletion(self)
        self.generations = apis.AsyncGenerations(self)
        self.prompts = apis.AsyncPrompts(self)
        self.embeddings = apis.AsyncEmbeddings(self)
        self.feedback = apis.AsyncFeedback(self)
        self.images = apis.AsyncImages(self)
        self.files = apis.AsyncMainFiles(self)
        self.models = apis.AsyncModels(self)
        self.moderations = apis.AsyncModerations(self)
        self.audio = apis.AsyncAudio(self)
        self.batches = apis.AsyncBatches(self)
        self.fine_tuning = apis.AsyncFineTuning(self)
        self.admin = apis.AsyncAdmin(self)
        self.uploads = apis.AsyncUploads(self)
        self.configs = apis.AsyncConfigs(self)
        self.api_keys = apis.AsyncApiKeys(self)
        self.virtual_keys = apis.AsyncVirtualKeys(self)
        self.logs = apis.AsyncLogs(self)
        self.beta = self.beta(self)  # type: ignore

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> AsyncUnbound:
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            **kwargs,
        )

    async def post(self, url: str, **kwargs):
        return await apis.AsyncPost(self).create(url=url, **kwargs)

    with_options = copy
