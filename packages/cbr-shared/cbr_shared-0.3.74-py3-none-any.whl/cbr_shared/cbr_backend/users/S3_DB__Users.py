from cbr_shared.aws.s3.S3_DB_Base             import S3_DB_Base
from cbr_shared.cbr_backend.users.S3_DB__User import S3_DB__User, S3_DB_User__BUCKET_NAME__SUFFIX, S3_DB_User__BUCKET_NAME__PREFIX
from osbot_utils.helpers.Random_Guid          import Random_Guid


class S3_DB__Users(S3_DB_Base):
    bucket_name__suffix: str = S3_DB_User__BUCKET_NAME__SUFFIX
    bucket_name__prefix: str = S3_DB_User__BUCKET_NAME__PREFIX

    def db_user(self, user_id : Random_Guid = None):
        if type(user_id) is str:
            user_id = Random_Guid(user_id)
        return S3_DB__User(user_id=user_id)

    def db_users(self):
        db_users = []
        for user_id in self.db_users_ids():
            db_users.append(self.db_user(user_id))
        return db_users

    def db_users_ids(self):
        return self.s3_folder_list()

        # todo: refactor all these .s3() calls to helper methods
        # todo: refactor this method to use self.s3().folder_list(s3_bucket=self.s3_bucket(), parent_folder=parent_folder, return_full_path=return_full_path)
        # todo: refactor to new data structure
        # s3_keys = self.s3().find_files(self.s3_bucket(), self.s3_folder_users_metadata())  # Fetch S3 keys for user metadata files
        # usernames = []                                                                           # Initialize an empty list to store usernames
        # for s3_key in s3_keys:
        #     filename = s3_key.split('/')[-1]                                                     # Extract the filename from the S3 key
        #     username = filename.replace('.json', '')                                             # Remove the '.json' extension to get the username
        #     usernames.append(username)                                                           # Append the username to the list
        #
        # return usernames

    def random_db_user(self):
        user_id = Random_Guid()
        return self.db_user(user_id)
