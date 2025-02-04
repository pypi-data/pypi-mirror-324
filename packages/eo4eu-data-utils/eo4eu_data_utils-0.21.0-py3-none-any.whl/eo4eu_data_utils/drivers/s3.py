from pathlib import Path
from eo4eu_base_utils.result import Result
from eo4eu_base_utils import OptionalModule
from eo4eu_base_utils.typing import Any, Callable, Self

from .interface import Driver


_s3_module = OptionalModule(
    package = "eo4eu_data_utils",
    enabled_by = ["s3", "full"],
    depends_on = ["boto3"]
)

_cpl_module = OptionalModule(
    package = "eo4eu_data_utils",
    enabled_by = ["cloudpath", "full"],
    depends_on = ["cloudpathlib"]
)

if _s3_module.is_enabled():
    import boto3
    _cpl_is_enabled = _cpl_module.is_enabled()
    if _cpl_is_enabled:
        from cloudpathlib import CloudPath, S3Client
    else:
        CloudPath = _cpl_module.broken_class("CloudPath")
        S3Client = _cpl_module.broken_class("S3Client")


    class S3Driver(Driver):
        def __init__(
            self,
            config: dict[str,str],
            bucket: str,
        ):
            self.resource = boto3.resource("s3", **config)
            self.bucket = self.resource.Bucket(bucket)
            self.bucket_name = bucket

            if _cpl_is_enabled:
                self.bucket_path = CloudPath(
                    f"s3://{bucket}",
                    client = S3Client(
                        aws_access_key_id = config["aws_access_key_id"],
                        aws_secret_access_key = config["aws_secret_access_key"],
                        endpoint_url = config["endpoint_url"],
                    )
                )

        def source(self, input_path: Path) -> list[Path]:
            input_path_str = str(input_path)
            if input_path_str == ".":
                input_path_str = ""
            elif input_path_str.startswith("./"):
                input_path_str = input_path_str[2:]

            return [
                Path(path.key).relative_to(input_path)
                for path in self.bucket.objects.filter(Prefix = input_path_str)
            ]

        def upload(self, src: Path, dst: Path) -> Result:
            try:
                self.bucket.upload_file(str(src), str(dst))
                return Result.ok([dst])
            except Exception as e:
                return Result.err(f"Failed to upload file: {e}")

        def download(self, src: Path, dst: Path) -> Result:
            try:
                dst.parent.mkdir(parents = True, exist_ok = True)
                self.bucket.download_fileobj(str(src), dst.open("wb"))
                return Result.ok([dst])
            except Exception as e:
                return Result.err(f"Failed to download file: {e}")

        def get(self, path: Path) -> bytes:
            return self.resource.Object(self.bucket_name, str(path)).get()["Body"].read()

        def put(self, path: Path, data: bytes) -> Path:
            self.bucket.put_object(Key = str(path), Body = data)
            return path

        def path(self, *paths) -> CloudPath:
            if not _cpl_is_enabled:
                _cpl_module.raise_error("S3Driver.path")

            return self.bucket_path.joinpath(*paths)

        def list_paths(self, *paths) -> list[str]:
            return [
                str(path) for path in self.source(Path("").joinpath(paths))
            ]

        def upload_file(self, src: str|Path, dst: str|Path) -> bool:
            return self.upload(Path(src), Path(dst)).is_ok()

        def download_file(self, src: str|Path, dst: str|Path) -> bool:
            return self.download(Path(src), Path(dst)).is_ok()

        def upload_bytes(self, key: str|Path, data: bytes) -> bool:
            key_str = str(key)
            try:
                self.bucket.put_object(Key = key_str, Body = data)
                return True
            except Exception as e:
                return False

        def download_bytes(self, key: str|Path) -> bytes|None:
            key_str = str(key)
            try:
                result = self.resource.Object(self.bucket_name, key_str).get()["Body"].read()
                return result
            except Exception as e:
                return None
else:
    S3Driver = _s3_module.broken_class("S3Driver")
