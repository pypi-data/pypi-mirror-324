from davidkhala.gcp.auth import OptionsInterface
from davidkhala.gcp.auth.service_account import Info, from_service_account, ServiceAccount
from pyarrow.fs import GcsFileSystem, FileInfo

from davidkhala.data.format.arrow.fs import FS


class GCS(FS):
    """
    https://arrow.apache.org/docs/python/generated/pyarrow.fs.GcsFileSystem.html
    - GcsFileSystem.open_append_stream(...) is not implemented.
        - > pyarrow.lib.ArrowNotImplementedError: Append is not supported in GCS
    """

    def __init__(self, public_bucket: bool = False, *, location='ASIA-EAST2', auth_options: OptionsInterface = None):
        options = {
            'anonymous': public_bucket,
            'default_bucket_location': location,
        }
        if auth_options:
            options['access_token'] = auth_options.token
            options['credential_token_expiration'] = auth_options.expiry
        self.fs = GcsFileSystem(**options)

    @staticmethod
    def from_service_account(info: Info):
        service_account = from_service_account(info)
        ServiceAccount.token.fget(service_account)  # credential validation included
        return GCS(auth_options=service_account)

    def ls(self, bucket: str) -> FileInfo | list[FileInfo]:
        return super().ls(bucket)

    def open_output_stream(self, path, **kwargs):
        if path.startswith('gs://'):
            path = path[5:]
        return super().open_output_stream(path)
