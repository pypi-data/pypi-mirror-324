from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Random_Guid import Random_Guid


class Model__LLM_Chat__Provider__Setup(Type_Safe):
    api_version : str           # API version
    description : str           # Human-readable description
    is_active   : bool          # Whether setup is currently active
    name        : str           # Provider name (e.g. "groq", "anthropic")
    model       : str           # Model identifier
    provider_id : Random_Guid   # Unique provider ID
    temperature : float         # Provider-specific temperature setting