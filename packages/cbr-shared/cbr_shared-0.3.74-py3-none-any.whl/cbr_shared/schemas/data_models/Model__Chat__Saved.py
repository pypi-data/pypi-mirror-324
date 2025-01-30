from dataclasses                            import dataclass, field
from osbot_utils.helpers.Random_Guid_Short  import Random_Guid_Short
from osbot_utils.helpers.Timestamp_Now      import Timestamp_Now
from osbot_utils.type_safe.Type_Safe           import Type_Safe
from osbot_utils.utils.Misc                 import date_now, time_now


@dataclass
class Model__Chat__Saved(Type_Safe):
    chat_path       : str               = None
    user_id         : str               = None
    chat_id         : Random_Guid_Short = None
    data            : dict              = field(default_factory=list)
    date            : str               = None
    last_user_prompt: str               = ''
    history_size    : int               = 0
    prompts_size    : int               = 0
    responses_size  : int               = 0
    summary         : str               = ''
    time            : str               = None
    timestamp       : Timestamp_Now     = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_id   = Random_Guid_Short()
        self.timestamp = Timestamp_Now()
        self.date      = date_now()
        self.time      = time_now(milliseconds_numbers=0)
