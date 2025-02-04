import os
import time
import logging
from pathlib import Path
from pprint import pprint
from eo4eu_data_utils.drivers import S3Driver

logger = logging.getLogger("test")
logging.basicConfig()
logger.setLevel(logging.DEBUG)


boto_config = {
    "region_name": "us-east-1",
    "endpoint_url": os.environ["S3_ENDPOINT_URL"],
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
}


if __name__ == "__main__":
    s3_driver = S3Driver(
        config = boto_config,
        bucket = "test_pre_pro-base"
    )
    s3_driver_insitu = S3Driver(
        config = boto_config,
        bucket = "eo4eu-insitu"
    )

    # for item in s3_driver.bucket.objects.filter():
    #     print(item.key)
    # for item in s3_driver.bucket.objects.filter(Prefix = "logs"):
    #     print(item.key)
    for item in s3_driver.bucket.objects.filter(Prefix = ""):
        print(item.key)

    print(s3_driver.source("logs"))

    # s3_driver.download(Path("logs/pre_pro.log"), Path("pre_pro.log")).log(logger)
    # # s3_driver.upload(Path("test_actions.py"), Path("logs/test_actions.py")).log(logger)
    # s3_driver.put(
    #     Path("logs/test_s3.py"),
    #     Path("test_s3.py").read_bytes(),
    # )

    # s3_driver_insitu.get(Path("250858e4-9e03-402b-995b-fafe14801a80/insitu.zip"))
    # uploaded = s3_driver.upload_file("local_file.csv", "s3_key.csv")
    # if not uploaded:
    #     print("marmaga")
