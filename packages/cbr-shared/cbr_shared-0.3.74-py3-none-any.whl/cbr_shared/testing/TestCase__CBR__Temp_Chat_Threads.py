from unittest                                                           import TestCase
from cbr_shared.cbr_sites.CBR__Shared_Objects                           import cbr_shared_objects
from cbr_shared.config.Server_Config__CBR_Website                       import server_config__cbr_website
from cbr_shared.schemas.base_models.chat_threads.LLMs__Chat_Completion  import LLMs__Chat_Completion
from osbot_utils.helpers.Random_Guid                                    import Random_Guid
from tests.integration.cbr_shared__for_integration_tests                import cbr_shared__assert_local_stack


class TestCase__CBR__Temp_Chat_Threads(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_shared__assert_local_stack()
        assert server_config__cbr_website.cbr_config_active().config_file_name == 'cbr-website.community.toml'      # confirm the config file that we are using

        cls.s3_db_server_requests = cbr_shared_objects.s3_db_server_requests()
        cls.s3_db_chat_threads    = cbr_shared_objects.s3_db_chat_threads   (reload_cache=True)
        cls.server_name           = server_config__cbr_website.server_name   ()

        with cls.s3_db_chat_threads as _:
            assert _.using_local_stack() is True                # confirm we are using Local Stack
            assert _.bucket_exists    () is True                # confirm the bucket exists

        with cls.s3_db_server_requests as _:
            assert _.bucket_exists() is True                    # confirm the bucket exists

    # @classmethod
    # def tearDownClass(cls):
    #     with cls.s3_db_chat_threads as _:                       # delete temp bucket for chat_threads
    #         assert _.using_minio() is True
    #         assert _.bucket_delete_all_files()
    #         assert _.bucket_delete() is True
    #
    #     with cls.s3_db_server_requests as _:                    # delete temp bucket for server_requests
    #         assert _.using_minio() is True
    #         assert _.bucket_delete_all_files()
    #         assert _.bucket_delete() is True
    #
    #     cls.random_aws_creds.restore_vars()
    #
    #     server_config__cbr_website.cbr_config().cbr_website.s3_log_requests = False  # restore value of s3_log_requests

    def s3_key__new_chat(self, **kwargs):
        request_id = Random_Guid()
        llm_chat_completion = LLMs__Chat_Completion(**kwargs)
        response = self.s3_db_chat_threads.save_chat_completion__user_response(llm_chat_completion, request_id)
        return response.get('data').get('s3_key')

    def s3_key__new_chats(self, count=5, **kwargs):
        s3_keys = []
        for i in range(count):
            s3_keys.append(self.s3_key__new_chat(**kwargs))
        return s3_keys