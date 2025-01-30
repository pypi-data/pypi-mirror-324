from cbr_shared.cbr_backend.files.User__File                                import User__File
from cbr_shared.cbr_backend.folders.User__Folders__Structure                import User__Folders__Structure
from cbr_shared.cbr_backend.users.S3_DB__User                               import S3_DB__User
from osbot_utils.type_safe.Type_Safe                                           import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self
from osbot_utils.helpers.Random_Guid                                        import Random_Guid

FILE_NAME__FOLDER__SUMMARY = 'folder-summary.md'

class User__Folders(Type_Safe):
    db_user: S3_DB__User

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.save()                                         # only save if no exception occurred
        else:
            return False                                        # will re-raise the exception

    def add_folder(self, parent_folder_id=None, folder_name=None ):
        return self.user_folders_operations().folder__add__to_folder_id(parent_folder_id=parent_folder_id, folder_name=folder_name)

    def add_file(self, folder_id, file_id=None, file_name=None):
        return self.user_folders_operations().file__add__to_folder_id(folder_id=folder_id, file_id=file_id, file_name=file_name)

    def folder_system_file__folder_summary(self, folder_id: Random_Guid, file_bytes:bytes):
        folder      = self.user_folder(folder_id)
        if folder:
            if folder.system_files.folder_summary is None:
                new_file    = User__File(db_user=self.db_user)
                new_file_id = new_file.file_id
                new_file.create(file_bytes=file_bytes, file_name=FILE_NAME__FOLDER__SUMMARY, user_folder_id=folder_id)
                self.user_folders_operations().folder__set_system_file__folder_summary(folder=folder, file_id=new_file_id)
                return new_file_id


    def delete(self):
        return self.user_folders_structure().delete()

    def delete_file(self, file_id):
        return self.user_folders_operations().file__delete(file_id)

    def delete_folder(self, folder_id):
        return self.user_folders_operations().folder__delete(folder_id)

    @cache_on_self
    def folders_structure(self):
        return self.user_folders_structure().folders_structure

    def user_file(self, file_id):
        return User__File(db_user=self.db_user, file_id=file_id)

    def user_folder_file(self, file_id):
        return self.user_folders_structure().file(file_id)

    def user_folder(self, user_folder_id: Random_Guid):
        return self.user_folders_structure().user_folder(user_folder_id)

    @cache_on_self
    def user_folders_structure(self):
        return User__Folders__Structure(db_user=self.db_user).load()

    @cache_on_self
    def user_folders_operations(self):
        return self.user_folders_structure().folders_operations()

    def root_folder(self):
        return self.user_folders_operations().folder__root()

    def root_folder__id(self):
        return self.folders_structure().root_id

    def save(self):
        return self.user_folders_structure().save()

    def setup(self):
        if self.db_user.has__file_system() is False:
            self.user_folders_structure().create()
            if self.root_folder__id() is None:
                self.user_folders_structure().folders_operations().create_root()
                self.user_folders_structure().save()
                self.db_user.user_config__update_value('file_system', True)  # update the user_config object to set the file_system to True      # todo: see if this is the best place to make this check
        return self

    def tree_view(self):
        return self.user_folders_operations().tree_view()
