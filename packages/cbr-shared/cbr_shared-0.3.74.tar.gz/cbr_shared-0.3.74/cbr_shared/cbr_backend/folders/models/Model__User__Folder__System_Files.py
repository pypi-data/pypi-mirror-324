from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid

class Model__User__Folder__System_Files(Type_Safe):
    folder_summary         : Random_Guid = None     # for now we only have this, but
    # folder_config        : Random_Guid = None   #   here are some other system files that we could add
    # folder_state         : Random_Guid = None
    # folder_system_prompt : Random_Guid = None