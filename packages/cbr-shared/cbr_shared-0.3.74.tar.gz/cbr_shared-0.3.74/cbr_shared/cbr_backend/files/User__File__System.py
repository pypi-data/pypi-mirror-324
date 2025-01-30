from cbr_shared.cbr_backend.files.User__File                 import User__File
from cbr_shared.cbr_backend.folders.User__Folders            import User__Folders
from cbr_shared.cbr_backend.folders.User__Folders__JSON_View import User__Folders__JSON_View
from cbr_shared.cbr_backend.users.S3_DB__User                import S3_DB__User
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.decorators.methods.cache_on_self            import cache_on_self
from osbot_utils.helpers.Random_Guid                         import Random_Guid
from osbot_utils.utils.Misc                                  import bytes_to_base64, str_to_bytes


class User__File__System(Type_Safe):
    db_user : S3_DB__User

    def add_file(self, file_name: str, file_bytes: bytes, user_folder_id: Random_Guid = None):
        with self.user_folders() as user_folders:
            user_folder = user_folders.user_folder(user_folder_id=user_folder_id)
            if user_folder:
                if not user_folder_id:
                    user_folder_id = user_folder.folder_id                                              #

                user_file = User__File(db_user=self.db_user)
                user_file   .create  (file_bytes=file_bytes, file_name=file_name, user_folder_id=user_folder_id)
                user_folders.add_file(folder_id=user_folder_id, file_id=user_file.file_id, file_name=file_name)
                return user_file

    def add_folder(self, parent_folder_id=None, folder_name=None):
        with self.user_folders() as user_folders:
            return user_folders.add_folder(folder_name=folder_name, parent_folder_id=parent_folder_id)

    def delete(self):
        self.user_folders().user_folders_structure().delete()
        self.db_user.user_config__update_value('file_system', False)                # todo: review this user_config.file_system set to False, since at the moment it is not consistent with way that True value is set
        return True

    def delete_file(self, file_id):
        file = User__File(file_id=file_id, db_user=self.db_user)
        if file.exists():
            with self.user_folders() as user_folders:
                user_folders.delete_file(file_id=file_id)
            file.delete()
            return True

    def delete_folder(self, folder_id):
        with self.user_folders() as user_folders:
            return user_folders.delete_folder(folder_id=folder_id)

    def file(self, file_id: Random_Guid):
        return self.user_folders().user_file(file_id)

    def file__bytes(self, file_id: Random_Guid, version_id=None):
        file = self.file(file_id)
        if file.exists():
            file_bytes          = file.contents(version_id=version_id)
            file_bytes__base64  = bytes_to_base64(file_bytes)
            return dict(file_bytes__base64 = file_bytes__base64,
                        version_id         = version_id        )
        return {}

    def file__contents(self, file_id: Random_Guid):
        file = self.file(file_id)
        if file.exists():
            file_data           = self.file__data(file_id).json()
            file_bytes          = file.contents()
            file_bytes__base64  = bytes_to_base64(file_bytes)
            file_summary        = file.summary()
            return dict(file_data          = file_data         ,
                        file_bytes__base64 = file_bytes__base64,
                        file_summary       = file_summary      )
        return {}

    def file__data(self, file_id: Random_Guid):
        return self.file(file_id).data()


    def file__temp_signed_url(self, file_id: Random_Guid, expiration=60):
        user_file = self.file(file_id)
        if user_file.exists():
            s3_key        = user_file.s3_key__for_file_content()
            s3_bucket     = user_file.db_user.s3_bucket()
            operation     = 'get_object'
            expiration    = expiration                                  # default is 60 seconds expiration
            create_kwargs = dict(bucket_name = s3_bucket  ,
                                 object_name = s3_key     ,
                                 operation   = operation  ,
                                 expiration  = expiration )
            pre_signed_url = user_file.db_user.s3().create_pre_signed_url(**create_kwargs)
            return pre_signed_url

    def file_versions(self, file_id):
        user_file = self.file(file_id)
        if user_file.exists():
            return user_file.versions()
        return []

    def folder(self, user_folder_id: Random_Guid):
        return self.user_folders().user_folder(user_folder_id)

    def folder_structure(self):
        return self.user_folders().folders_structure()

    def folder_structure__files(self):
        return self.folder_structure().files

    def folder_summary(self, folder_id: str):
        folder_summary_file = self.folder_summary__user_file(folder_id)
        if folder_summary_file:
            return folder_summary_file.contents()

    def folder_summary__update(self, folder_id, folder_summary):
        folder_summary_file = self.folder_summary__user_file(folder_id)
        if folder_summary_file:
            file_bytes = str_to_bytes(folder_summary)
            folder_summary_file.contents__update(file_bytes)
            return True
        return False

    def folder_summary__user_file(self, folder_id):
        folder = self.folder(folder_id)
        if folder:
            folder_summary_file_id = folder.system_files.folder_summary
            if folder_summary_file_id is None:
                file_bytes = b''
                with self.user_folders() as _:                                              # context saves folder_structure
                    folder_summary_file_id = _.folder_system_file__folder_summary(folder_id, file_bytes)
            system_file = User__File(file_id=folder_summary_file_id, db_user=self.db_user)
            return system_file

    def root_folder(self):
        return self.user_folders().root_folder()

    def json_view(self):
        return User__Folders__JSON_View(folders_structure=self.folder_structure()).to_json()

    def tree_view(self):
        return self.user_folders().tree_view()


    @cache_on_self
    def user_folders(self):
        return User__Folders(db_user=self.db_user)

    def setup(self):
        if self.db_user is None:
            raise ValueError("in User__File__System.setup db_user cannot be None")
        self.user_folders().setup()
        return self

    def rename_file(self, file_id, new_file_name):
        file = self.file(file_id=file_id)
        if file:
            file.data__update_file_name(new_file_name)
            with self.user_folders() as user_folders:
                return user_folders.user_folders_operations().file__rename(file_id, new_file_name)

    def rename_folder(self, folder_id, new_folder_name):
        with self.user_folders() as user_folders:
            return user_folders.user_folders_operations().folder__rename(folder_id, new_folder_name)