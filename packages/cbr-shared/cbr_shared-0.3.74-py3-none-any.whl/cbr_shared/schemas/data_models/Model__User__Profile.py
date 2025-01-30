from dataclasses                        import dataclass
from osbot_utils.type_safe.Type_Safe       import Type_Safe


@dataclass
class Model__User__Profile(Type_Safe):
    first_name              : str = ''
    last_name               : str = ''
    role                    : str = ''
    organisation            : str = ''
    sector                  : str = ''
    size_of_organisation    : str = ''
    country                 : str = ''
    linkedin                : str = ''
    additional_system_prompt: str = ''