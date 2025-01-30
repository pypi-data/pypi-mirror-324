
from osbot_utils.type_safe.Type_Safe           import Type_Safe

DEFAULT__CONFIG__ASSETS_DIST        = '/dist'
DEFAULT__CONFIG__ASSETS_ROOT        = '/assets'
DEFAULT__CONFIG__ATHENA_URL         = "/api"
DEFAULT__CONFIG__AWS_ENABLED        = False
DEFAULT__CONFIG__CAPTURE_EXCEPTIONS = True
DEFAULT__CONFIG__CBR_LOGO           = 'cbr/cbr-logo-community.png'
DEFAULT__CONFIG__ENV                = 'LOCAL'
DEFAULT__CONFIG__LOGIN_ENABLED      = False
DEFAULT__CONFIG__GTA_ENABLED        = False
DEFAULT__CONFIG__S3_LOAD_SECRETS    = False
DEFAULT__CONFIG__S3_LOG_REQUESTS    = False
DEFAULT__CONFIG__REQ_TRACES_ENABLED = False
DEFAULT__CONFIG__S3_USE_MINIO       = False
DEFAULT__CONFIG__SERVER_NAME        = 'cbr-server'
DEFAULT__CONFIG__USE_LOCAL_STACK    = False

class CBR__Config__Dev(Type_Safe):
    capture_exceptions : bool = DEFAULT__CONFIG__CAPTURE_EXCEPTIONS

class CBR__Config__Website(Type_Safe):
    athena_path         : str  = DEFAULT__CONFIG__ATHENA_URL
    assets_root         : str  = DEFAULT__CONFIG__ASSETS_ROOT
    assets_dist         : str  = DEFAULT__CONFIG__ASSETS_DIST
    aws_enabled         : bool = DEFAULT__CONFIG__AWS_ENABLED
    cbr_logo            : str  = DEFAULT__CONFIG__CBR_LOGO
    env                 : str  = DEFAULT__CONFIG__ENV
    login_enabled       : bool = DEFAULT__CONFIG__LOGIN_ENABLED
    gta_enabled         : bool = DEFAULT__CONFIG__GTA_ENABLED
    s3_load_secrets     : bool = DEFAULT__CONFIG__S3_LOAD_SECRETS
    s3_log_requests     : bool = DEFAULT__CONFIG__S3_LOG_REQUESTS
    s3_use_minio        : bool = DEFAULT__CONFIG__S3_USE_MINIO
    server_name         : str  = DEFAULT__CONFIG__SERVER_NAME
    req_traces_enabled  : bool = DEFAULT__CONFIG__REQ_TRACES_ENABLED
    use_local_stack     : bool = DEFAULT__CONFIG__USE_LOCAL_STACK

class CBR__Config(Type_Safe):
    cbr_dev     : CBR__Config__Dev
    cbr_website : CBR__Config__Website

    def env(self):
        return self.cbr_website.env

    # def env(self):                                # todo: refactor this where this value is set via the config files
    #     return get_env('EXECUTION_ENV', 'LOCAL')


    def athena_path(self):
        return self.cbr_website.athena_path

    def assets_dist(self):
        return self.cbr_website.assets_dist

    def assets_root(self):
        return self.cbr_website.assets_root

    def aws_enabled(self):
        return self.cbr_website.aws_enabled

    def aws_disabled(self):
        return self.aws_enabled() is False

    def gta_enabled(self):
        return self.cbr_website.gta_enabled

    def cbr_logo(self):
        return self.cbr_website.cbr_logo


    def dev__capture_exceptions(self):
        return self.cbr_dev.capture_exceptions

    def login_enabled(self):
        return self.cbr_website.login_enabled

    def login_disabled(self):
        return self.login_enabled() is False

    def s3_load_secrets(self):
        return self.cbr_website.s3_load_secrets

    def s3_log_requests(self):
        return self.cbr_website.s3_log_requests

    def s3_use_minio(self):
        return self.cbr_website.s3_use_minio

    def server_name(self):
        return self.cbr_website.server_name

    def req_traces_enabled(self):
        return self.cbr_website.req_traces_enabled

    def use_local_stack(self):
        return self.cbr_website.use_local_stack

    # extra values
    def version(self):                      # todo: see if there is the best place to put this (since this value is not loaded from config file and it is already on the CBR__Site__Info object
        from cbr_shared.utils.Version import version__cbr_shared
        return version__cbr_shared

    # static values                         # todo: figure out best place to store these, since they really shouldn't change
    def session_cookie_httponly(self):
        return True

    def remember_cookie_httponly(self):
        return True

    def remember_cookie_duration(self):
        return 3600                         # todo: look at increasing this value, since I think this is reason why the user session expires quite often
