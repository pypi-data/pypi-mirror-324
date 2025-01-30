from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now


class Model__User__Notification(Type_Safe):
    notification_id   : Random_Guid
    message           : str
    level             : int
    data              : dict
    timestamp         : Timestamp_Now
    user_delivered    : bool
    user_acknowledged : bool
