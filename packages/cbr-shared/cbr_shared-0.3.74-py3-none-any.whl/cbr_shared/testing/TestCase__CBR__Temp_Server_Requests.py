from unittest                                                       import TestCase
from cbr_shared.cbr_backend.server_requests.S3__Server_Request      import S3__Server_Request
from cbr_shared.cbr_sites.CBR__Shared_Objects                       import cbr_shared_objects
from cbr_shared.config.Server_Config__CBR_Website                   import server_config__cbr_website
from osbot_fast_api.utils.testing.Mock_Obj__Fast_API__Request_Data  import Mock_Obj__Fast_API__Request_Data

class TestCase__CBR__Temp_Server_Requests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s3_db_server_requests = cbr_shared_objects.s3_db_server_requests()
        cls.server_name           = server_config__cbr_website.server_name()
        with cls.s3_db_server_requests as _:
            assert _.using_local_stack() is True                      # confirm we are using Localstack
            assert _.bucket_exists() is True
            cls.request_data          = Mock_Obj__Fast_API__Request_Data().create()
            cls.s3_server_request     = S3__Server_Request(request_data = cls.request_data  ,
                                                           s3_db        = _                 )
        assert cls.s3_server_request.create() is True
        assert cls.s3_server_request.exists() is True


    # @classmethod
    # def tearDownClass(cls):
    #     with cls.s3_server_request as _:
    #         assert _.delete() is True
    #         assert _.exists() is False
    #
    #     with cls.s3_db_server_requests as _:
    #         assert _.using_minio() is True
    #         assert _.bucket_delete_all_files()
    #         assert _.bucket_delete() is True
    #
    #     cls.random_aws_creds.restore_vars()
