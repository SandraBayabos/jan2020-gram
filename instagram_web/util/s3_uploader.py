import boto3
import botocore
from config import Config
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.S3_KEY,
    aws_secret_access_key=Config.S3_SECRET
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name):

    try:

        s3.upload_fileobj(
            file,
            Config.S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return f'{Config.S3_LOCATION}{file.filename}'
