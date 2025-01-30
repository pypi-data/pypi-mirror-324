from typing                                                              import List
from cbr_shared.cbr_backend.user_notifications.Model__User__Notification import Model__User__Notification
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from osbot_utils.helpers.Timestamp_Now                                   import Timestamp_Now


class Model__User__Notifications(Type_Safe):
    notifications_id        : Random_Guid
    notifications           : List[Model__User__Notification]
    timestamp__created      : Timestamp_Now
    timestamp__last_updated : Timestamp_Now         = None
    timestamp__last_read    : Timestamp_Now         = None
