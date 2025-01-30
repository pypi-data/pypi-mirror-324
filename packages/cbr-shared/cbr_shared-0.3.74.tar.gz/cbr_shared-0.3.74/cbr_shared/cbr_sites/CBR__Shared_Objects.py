from osbot_utils.type_safe.Type_Safe                                   import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self

class CBR__Shared_Objects(Type_Safe):

    @cache_on_self
    def cbr_cache_llm_prompts(self):
        from cbr_shared.cbr_caches.CBR__Cache__LLM_Prompts import CBR__Cache__LLM_Prompts
        return CBR__Cache__LLM_Prompts()

    @cache_on_self
    def cbr_service_accounts(self):
        from cbr_shared.config.CBR__Service_Accounts import CBR__Service_Accounts
        return CBR__Service_Accounts()

    @cache_on_self
    def s3_db_cbr(self):
        from cbr_shared.cbr_backend.cbr.S3_DB__CBR import S3_DB__CBR

        # if server_config__cbr_website.s3_log_requests() is False:
        #     return S3_DB_Base__Disabled()
        with  S3_DB__CBR() as _:
            _.setup()
            return _

    @cache_on_self
    def s3_db_chat_threads(self):                                               # todo: refactor this code with the method s3_db_server_requests() since 95% is the same
        from cbr_shared.cbr_backend.chat_threads__legacy.S3_DB__Chat_Threads import S3_DB__Chat_Threads
        from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

        # if server_config__cbr_website.s3_log_requests() is False:
        #     return S3_DB__Chat_Threads__Disabled()

        server_name = server_config__cbr_website.server_name()
        kwargs      = dict(server_name =  server_name)
        with  S3_DB__Chat_Threads(**kwargs)  as _:
            _.setup()                                                           # set up tasks, including creating target bucket if it doesn't exist
            _.s3_key_generator.use_request_path = False
            _.s3_key_generator.use_when         = True
            _.s3_key_generator.use_hours        = True
            _.s3_key_generator.use_minutes      = False
            return _

    @cache_on_self
    def db_guests(self):
        from cbr_shared.cbr_backend.guests.S3_DB__Guests import S3_DB__Guests      # due to circular dependency on the S3_DB_Guest which needs access to this class for getting the db_users and db_sessions objects
        with S3_DB__Guests() as _:
            _.setup()
            return _

    @cache_on_self
    def s3_db_server_requests(self):                                                # todo: refactor this code to remove duplicated code
        from cbr_shared.cbr_backend.server_requests.S3_DB__Server_Requests import S3_DB__Server_Requests
        from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

        # if server_config__cbr_website.s3_log_requests() is False:
        #     return S3_DB__Server_Requests__Disabled()

        server_name = server_config__cbr_website.server_name()
        kwargs      = dict(server_name =  server_name)
        with  S3_DB__Server_Requests(**kwargs)  as _:
            _.setup()                                                               # set up tasks, including creating target bucket if it doesn't exist
            _.s3_key_generator.use_request_path = True
            _.s3_key_generator.use_when         = True
            _.s3_key_generator.use_minutes      = False
            _.s3_key_generator.use_hours        = True
            return _

    @cache_on_self
    def s3_db_servers(self):                                                        # todo: refactor this code to remove duplicated code
        from cbr_shared.cbr_backend.servers.S3_DB__Servers import S3_DB__Servers
        from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website
        # if server_config__cbr_website.s3_log_requests() is False:
        #     return S3_DB__Servers_Disabled()

        server_name = server_config__cbr_website.server_name()
        kwargs      = dict(server_name =  server_name)
        with  S3_DB__Servers(**kwargs)  as _:
            _.setup()                                                               # set up tasks, including creating target bucket if it doesn't exist
            _.s3_key_generator.use_request_path = False
            _.s3_key_generator.use_when         = True
            _.s3_key_generator.use_hours        = True
            _.s3_key_generator.use_minutes      = False
            return _

    @cache_on_self
    def db_sessions(self):
        from cbr_shared.cbr_backend.session.S3_DB__Sessions import S3_DB__Sessions

        with S3_DB__Sessions() as _:
            _.setup()
            return _

    @cache_on_self
    def db_users(self):

        from cbr_shared.cbr_backend.users.S3_DB__Users import S3_DB__Users
        with S3_DB__Users() as _:
            _.setup()
            return _

cbr_shared_objects = CBR__Shared_Objects()
