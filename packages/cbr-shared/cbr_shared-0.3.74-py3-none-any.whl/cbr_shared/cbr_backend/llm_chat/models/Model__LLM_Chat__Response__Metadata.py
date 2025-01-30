from osbot_utils.type_safe.Type_Safe       import Type_Safe


class Model__LLM_Chat__Response__Metadata(Type_Safe):
    finish_reason : str      # Reason for completion
    tokens_used   : int      # Number of tokens consumed