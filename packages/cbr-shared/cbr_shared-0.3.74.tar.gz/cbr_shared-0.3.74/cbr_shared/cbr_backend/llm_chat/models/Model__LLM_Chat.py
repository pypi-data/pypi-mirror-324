from typing                                                                    import Dict, List
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Config            import Model__LLM_Chat__Config
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Feedback__Summary import Model__LLM_Chat__Feedback__Summary
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Message           import Model__LLM_Chat__Message
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Provider__Setup   import Model__LLM_Chat__Provider__Setup
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.helpers.Random_Guid                                           import Random_Guid
from osbot_utils.helpers.Safe_Id                                               import Safe_Id
from osbot_utils.helpers.Timestamp_Now                                         import Timestamp_Now

class Model__LLM_Chat(Type_Safe):
    chat_id          : Random_Guid                                          # Unique chat ID
    config           : Model__LLM_Chat__Config                              # Global configuration
    providers        : Dict[Random_Guid, Model__LLM_Chat__Provider__Setup]  # Provider configurations
    messages         : Dict[Random_Guid, Model__LLM_Chat__Message]          # Conversation history
    created_at       : Timestamp_Now                                        # Session start time
    updated_at       : Timestamp_Now                                        # Last update time
    version          : Safe_Id                                              # Schema version
    active_branch    : List[Random_Guid]                                    # Current conversation path
    token_usage      : Dict[Random_Guid, int]                               # Token usage by provider
    feedback_summary : Model__LLM_Chat__Feedback__Summary                   # Aggregated feedback