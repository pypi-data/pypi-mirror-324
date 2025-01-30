from typing                                                                 import List, Optional
from cbr_shared.cbr_backend.user_notifications.Model__User__Notification    import Model__User__Notification
from cbr_shared.cbr_backend.user_notifications.Model__User__Notifications   import Model__User__Notifications
from cbr_shared.cbr_backend.users.User__Section_Data                        import User__Section_Data
from osbot_utils.helpers.Random_Guid                                        import Random_Guid
from osbot_utils.helpers.Timestamp_Now                                      import Timestamp_Now


FILE_NAME__NOTIFICATIONS = 'notifications.json'

class User__Notifications(User__Section_Data):
    section_name: str = 'notifications'

    def add(self, notification: Model__User__Notification) -> bool:
        user_notifications = self.current()
        user_notifications.notifications.append(notification)
        return self.save(user_notifications)

    def all(self) -> List[Model__User__Notification]:
        return self.current().notifications

    def current(self) -> Model__User__Notifications:
        if self.exists():
            data = self.file_data(self.file_user_notifications())
            return Model__User__Notifications.from_json(data, raise_on_not_found=True)
        return Model__User__Notifications(notifications_id   = Random_Guid()  ,
                                          notifications      = []             ,
                                          timestamp__created = Timestamp_Now())

    def delete(self, notification_id: Random_Guid) -> bool:
        from osbot_utils.utils.Misc import is_guid

        if is_guid(notification_id) is False:
            return False
        user_notifications                         = self.current()
        user_notifications.notifications           = [n for n in user_notifications.notifications
                                                        if n.notification_id != notification_id]
        return self.save(user_notifications)

    def delete_all(self) -> bool:
        return self.file_delete(self.file_user_notifications())

    def exists(self) -> bool:
        return self.file_exists(self.file_user_notifications())

    def file_user_notifications(self) -> str:
        return FILE_NAME__NOTIFICATIONS

    def mark_delivered(self, notification_ids: List[str]) -> bool:
        user_notifications = self.current()
        updated            = False
        for notification in user_notifications.notifications:
            if notification.notification_id in notification_ids:
                notification.user_delivered = True
                updated = True
        if updated:
            return self.save(user_notifications)
        return False

    def new(self, last_notification_timestamp: Optional[float] = None) -> List[Model__User__Notification]:
        notifications = self.current().notifications
        if last_notification_timestamp:
            return [n for n in notifications
                   if n.timestamp > last_notification_timestamp and not n.user_delivered]
        return [n for n in notifications if not n.user_delivered]

    def save(self, user_notifications: Model__User__Notifications) -> bool:
        user_notifications.timestamp__last_updated = Timestamp_Now()
        return self.file_save(self.file_user_notifications(), user_notifications.json())