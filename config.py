import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    # AWS IMPORTS
    S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_KEY = os.environ.get("AWS_ACCESS_KEY")
    S3_SECRET = os.environ.get("AWS_SECRET_KEY")
    AWS_LINK = f'https://s3.amazonaws.com/{S3_BUCKET}'
    S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'
    BT_PUBLIC_KEY = os.environ.get('BT_PUBLIC_KEY')
    BT_PRIVATE_KEY = os.environ.get('BT_PRIVATE_KEY')
    BT_MERCHANT_KEY = os.environ.get('BT_MERCHANT_KEY')


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    # GOOGLE OAUTH CONFIGURATION
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False
    # GOOGLE OAUTH CONFIGURATION
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
