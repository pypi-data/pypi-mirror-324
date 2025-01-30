from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now

class Model__LLM_Chat__Feedback__Summary(Type_Safe):
    block        : int
    bookmark     : int
    negative     : int
    neutral      : int
    positive     : int
    total        : int
    last_feedback: Timestamp_Now   # Timestamp of last feedback