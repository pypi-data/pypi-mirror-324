from _typeshed import Incomplete
from pydantic_settings import BaseSettings
from rlogging.settings import AppBaseSettings as AppBaseSettings, ENV_FILE as ENV_FILE
from storages.backends.s3boto3 import S3Boto3Storage

APP_SETTINGS: Incomplete

class StaticDjangoStorageSettings(BaseSettings):
    model_config: Incomplete
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    LOCATION: str | None
    ENDPOINT_URL: str
    DEFAULT_ACL: str
    QUERYSTRING_AUTH: bool
    OBJECT_PARAMETERS: dict[str, str]
    def get_location(self): ...

class MediaDjangoStorageSettings(StaticDjangoStorageSettings):
    model_config: Incomplete

STATIC_DJANGO_STORAGE_SETTINGS: Incomplete
MEDIA_DJANGO_STORAGE_SETTINGS: Incomplete

class StaticS3Storage(S3Boto3Storage):
    access_key: Incomplete
    secret_key: Incomplete
    location: Incomplete
    bucket_name: Incomplete
    endpoint_url: Incomplete
    object_parameters: Incomplete
    default_acl: Incomplete
    querystring_auth: Incomplete

class MediaS3Storage(S3Boto3Storage):
    access_key: Incomplete
    secret_key: Incomplete
    location: Incomplete
    bucket_name: Incomplete
    endpoint_url: Incomplete
    object_parameters: Incomplete
    default_acl: Incomplete
    querystring_auth: Incomplete
