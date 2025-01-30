from osbot_aws.aws.s3.S3__DB_Base   import S3__DB_Base

ENV_NAME__USE_MINIO_AS_S3 = 'USE_MINIO_AS_S3'
S3_FOLDER__ODIN_DATA = 'odin_data'

class S3_DB_Base(S3__DB_Base):                                      # todo: once we know there are no side effects , remove this class

    def s3_folder_odin_data(self):                                  # Return the standard folder name for Odin data
        return S3_FOLDER__ODIN_DATA

    def s3_temp_folder__download_string(self, pre_signed_url):      # Download string content from a pre-signed URL
        import requests
        response = requests.get(pre_signed_url)
        if response.status_code == 200:
            return response.text

    def s3_temp_folder__upload_string(self, pre_signed_url, file_contents):    # Upload string content using a pre-signed URL
        import requests
        response = requests.put(pre_signed_url, data=file_contents)
        if response.status_code == 200:
            return True
        else:
            return False