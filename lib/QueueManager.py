import json
import boto3
import traceback
from io import BytesIO
from gzip import GzipFile

def start(imageslist):
    try:
        client = boto3.resource(
            's3',
            aws_access_key_id='AWS_ACCESS_KEY_ID',
            aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
        )

        bucket = client.Bucket('AWS_S3_BUCKET_NAME')
        for imgs in imageslist:
            index = imageslist.index(imgs) + 1
            images = json.dumps(imgs)
            gz_body = BytesIO()
            gz = GzipFile(None, 'wb', 9, gz_body)
            gz.write(images.encode('utf-8'))
            gz.close()

            bucket.put_object(
                Key=str("{0:0=4d}".format(index)),
                Body=gz_body.getvalue(),
                ContentEncoding='gzip',
                ContentType='text/json'
            )
        return

    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    start()
