MISSING_API_KEY_ERROR_MESSAGE = """Unbound API Key Not Found \

Resolution: \

1. Get your Unbound API key from https://gateway.unboundsecurity.ai/api-keys
2. Pass it while instantiating the Unbound client with api_key param,\
 or set it as an environment variable with export UNBOUND_API_KEY=YOUR_API_KEY
"""

MISSING_BASE_URL = """No Base url provided. Please provide a valid base url.
For example: https://gateway.unboundsecurity.ai
"""

MISSING_CONFIG_MESSAGE = (
    """The 'config' parameter is not set. Please provide a valid Config object."""
)
MISSING_MODE_MESSAGE = (
    """The 'mode' parameter is not set. Please provide a valid mode literal."""
)

INVALID_UNBOUND_MODE = """
Argument of type '{}' cannot be assigned to parameter "mode" of \
    type "ModesLiteral | Modes | None"
"""

LOCALHOST_CONNECTION_ERROR = """Could not instantiate the Unbound client. \
You can either add a valid `api_key` parameter (from https://gateway.unboundsecurity.ai/api-keys)\
or check the `base_url` parameter in the Unbound client, \
for your AI Gateway's instance's URL.
"""

CUSTOM_HOST_CONNECTION_ERROR = """We could not connect to the AI Gateway's instance. \
Please check the `base_url` parameter in the Unbound client.
"""

DEFAULT_MAX_RETRIES = 2
VERSION = "0.1.0"
DEFAULT_TIMEOUT = 60
UNBOUND_HEADER_PREFIX = "x-unbound-"
UNBOUND_BASE_URL = "https://gateway.unboundsecurity.ai/v1"
UNBOUND_GATEWAY_URL = UNBOUND_BASE_URL
LOCAL_BASE_URL = "http://localhost:8787/v1"
UNBOUND_API_KEY_ENV = "UNBOUND_API_KEY"
UNBOUND_PROXY_ENV = "UNBOUND_PROXY"
OPEN_AI_API_KEY = "OPENAI_API_KEY"
