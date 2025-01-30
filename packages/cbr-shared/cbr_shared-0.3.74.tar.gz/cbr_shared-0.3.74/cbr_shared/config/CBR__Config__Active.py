from cbr_shared.config.CBR__Config      import CBR__Config
from osbot_utils.type_safe.Type_Safe       import Type_Safe


class CBR__Config__Active(Type_Safe):
    cbr_config       : CBR__Config
    config_file_name : str
    file_loaded_at   : str
    status           : str