## Features

The Unbound SDK is built on top of the OpenAI SDK, allowing you to seamlessly integrate Unbound's advanced features while retaining full compatibility with OpenAI methods. With Unbound, you can enhance your interactions with OpenAI or any other OpenAI-like provider by leveraging robust monitoring, reliability, prompt management, and more features - without modifying much of your existing code.


## Usage

#### Prerequisites
1. [Sign up on Unbound](https://gateway.unboundsec.dev/) and grab your Unbound API Key
2. Add your API Keys to Unbound's API Keys page and keep it handy

```bash
# Installing the SDK

$ pip install unbound-gateway
```

#### Making a Request to OpenAI
* Unbound fully adheres to the OpenAI SDK signature. You can instantly switch to Unbound and start using our production features right out of the box. <br />
* Just replace `from openai import OpenAI` with `from unbound import Unbound`:
```py
from unbound import Unbound

unbound = Unbound(
    base_url="UNBOUND_BASE_URL",
    api_key="UNBOUND_API_KEY",
)

chat_completion = unbound.chat.completions.create(
    messages = [{ "role": 'user', "content": 'Say this is a test' }],
    model = 'gpt-4'
)

print(chat_completion)
```

#### Async Usage
* Use `AsyncUnbound` instead of `Unbound` with `await`:
```py
import asyncio
from unbound import AsyncUnbound

unbound = AsyncUnbound(
    base_url="UNBOUND_BASE_URL",
    api_key="UNBOUND_API_KEY"
)

async def main():
    chat_completion = await unbound.chat.completions.create(
        messages=[{'role': 'user', 'content': 'Say this is a test'}],
        model='gpt-4'
    )

    print(chat_completion)

asyncio.run(main())
```
