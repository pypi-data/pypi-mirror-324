from eo4eu_data_utils.drivers import S3Driver
from eo4eu_data_utils.config import ConfigBuilder, Try
from eo4eu_data_utils.pipeline import Pipeline, then
from pprint import pprint
from pathlib import Path
try:
    from typing import Self
except Exception:
    from typing_extensions import Self
from enum import Enum
import logging
import re

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config_builder = ConfigBuilder(
    boto = {
        "region_name": "us-east-1",
        "endpoint_url": Try.cfgmap("s3-access", "endpoint_url"),
        "aws_access_key_id": Try.secret("s3-access-scr", "aws_access_key_id"),
        "aws_secret_access_key": Try.secret("s3-access-scr", "aws_secret_access_key")
    },
    bucket = "apollo-test"
)

if __name__ == "__main__":
    config = config_builder.use_env().build()
    s3_driver = S3Driver(
        config = config.boto.to_dict(),
        bucket = config.bucket
    )

    pipeline = Pipeline(
        logger = logger,
        summary = logger,
    )

    result = (pipeline
        .source(s3_driver)
        .download("download")
        .exec()
    )

    pprint(result)
