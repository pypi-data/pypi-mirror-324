from dataclasses                        import dataclass
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.utils.Misc             import random_text
from osbot_utils.utils.Str              import safe_str


@dataclass
class Model__User__Config(Type_Safe):
    user_id    : Random_Guid
    user_name  : str
    file_system: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.user_name:
            self.user_name = random_text('user', lowercase=True)
        self.user_name = safe_str(self.user_name)


def random__model_user_config():
    user_id   = Random_Guid()
    user_name = random_text("an-random-user", lowercase=True)
    return Model__User__Config(user_id=user_id, user_name=user_name)