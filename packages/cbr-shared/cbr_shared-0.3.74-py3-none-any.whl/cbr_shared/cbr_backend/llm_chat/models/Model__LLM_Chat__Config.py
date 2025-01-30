from osbot_utils.type_safe.Type_Safe       import Type_Safe

class Model__LLM_Chat__Config(Type_Safe):
    max_tokens : int       # Maximum response length
    stream     : bool      # Enable streaming responses
    seed       : int       # Optional deterministic seed