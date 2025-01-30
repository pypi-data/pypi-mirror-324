from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now

class Model__LLM_Chat__User__Feedback(Type_Safe):
    rating        : int             # 1 (positive) or -1 (negative)
    is_bookmarked : bool            # Bookmark status
    is_flagged    : bool            # Flag for review
    timestamp     : Timestamp_Now   # When feedback was given
    comment       : str             # Optional user comment  # todo: create a helper class like Safe_Id, but for text (Safe_Text would be a good option)