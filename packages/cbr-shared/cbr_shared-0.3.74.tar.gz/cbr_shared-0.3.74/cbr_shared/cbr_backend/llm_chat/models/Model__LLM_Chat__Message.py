from typing                                                                     import List
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__Response__Metadata import Model__LLM_Chat__Response__Metadata
from cbr_shared.cbr_backend.llm_chat.models.Model__LLM_Chat__User__Feedback     import Model__LLM_Chat__User__Feedback
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.helpers.Random_Guid                                            import Random_Guid
from osbot_utils.helpers.Timestamp_Now                                          import Timestamp_Now

class Model__LLM_Chat__Message(Type_Safe):
    message_id       : Random_Guid                         # Unique message identifier
    role             : str                                  # system, user, or assistant
    content          : str                                  # Message content
    timestamp        : Timestamp_Now                        # Creation time
    parent_ids       : List[Random_Guid]                    # Links to parent messages
    child_ids        : List[Random_Guid]                    # Links to child messages
    provider_id      : Random_Guid                          # References provider setup
    response_metadata: Model__LLM_Chat__Response__Metadata  # Provider response data
    user_feedback    : Model__LLM_Chat__User__Feedback      # User feedback for message