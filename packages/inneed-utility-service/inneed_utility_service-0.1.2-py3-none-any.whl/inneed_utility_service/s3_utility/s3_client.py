import boto3
import os
from inneed_utility_service.error_utility.error_handler import ErrorHandler
from inneed_utility_service.error_utility.error_handler import S3ConnectionError, S3OperationError

class S3Client:
    @ErrorHandler.handle_error(S3ConnectionError, "Failed to initialize S3 client")
    def __init__(self, region: str):
        """
        Initialize a synchronous S3 client.
        Only the AWS region is required (credentials are assumed to be provided by the environment).
        """
        self.region = region
        try:
            self.s3 = boto3.client('s3', region_name=self.region)
        except Exception as e:
            # In case boto3.client fails, this will be caught by the decorator.
            raise S3ConnectionError(
                message=f"Failed to initialize S3 client for region {self.region}",
                original_exception=e
            )

    @ErrorHandler.handle_error(S3OperationError, "Error listing S3 buckets")
    def list_buckets(self):
        """List all S3 buckets."""
        response = self.s3.list_buckets()
        return response.get('Buckets', [])

    @ErrorHandler.handle_error(S3OperationError, "Error creating S3 bucket")
    def create_bucket(self, bucket_name: str):
        """Create a new S3 bucket."""
        params = {'Bucket': bucket_name}
        if self.region != 'us-east-1':
            params['CreateBucketConfiguration'] = {'LocationConstraint': self.region}
        return self.s3.create_bucket(**params)

    @ErrorHandler.handle_error(S3OperationError, "Error deleting S3 bucket")
    def delete_bucket(self, bucket_name: str):
        """Delete an S3 bucket."""
        return self.s3.delete_bucket(Bucket=bucket_name)

    @ErrorHandler.handle_error(S3OperationError, "Error listing objects in S3 bucket")
    def list_objects(self, bucket_name: str, prefix: str = '', max_keys: int = 1000):
        """
        List objects in the specified bucket.
        
        Args:
            bucket_name: Name of the bucket.
            prefix: Limits the response to keys that begin with the specified prefix.
            max_keys: Maximum number of keys to return.
        """
        response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys)
        return response.get('Contents', [])

    @ErrorHandler.handle_error(S3OperationError, "Error retrieving S3 object")
    def get_object(self, bucket_name: str, object_key: str):
        """
        Retrieve an object from S3.
        
        Returns the raw bytes of the object.
        """
        response = self.s3.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()

    @ErrorHandler.handle_error(S3OperationError, "Error putting S3 object")
    def put_object(self, bucket_name: str, object_key: str, body, content_type: str = None, metadata: dict = None):
        """
        Upload an object to S3.
        
        Args:
            bucket_name: Name of the target bucket.
            object_key: S3 object key.
            body: Data to upload (bytes, file-like object, or string).
            content_type: MIME type of the object.
            metadata: Additional metadata for the object.
        """
        params = {
            'Bucket': bucket_name,
            'Key': object_key,
            'Body': body
        }
        if content_type:
            params['ContentType'] = content_type
        if metadata:
            params['Metadata'] = metadata
        return self.s3.put_object(**params)

    @ErrorHandler.handle_error(S3OperationError, "Error copying S3 object")
    def copy_object(self, source_bucket: str, source_key: str, dest_bucket: str, dest_key: str):
        """
        Copy an object from one bucket to another (or within the same bucket).
        
        Args:
            source_bucket: Name of the source bucket.
            source_key: Key of the source object.
            dest_bucket: Name of the destination bucket.
            dest_key: Key for the copied object.
        """
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        return self.s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)

    @ErrorHandler.handle_error(S3OperationError, "Error uploading file to S3")
    def upload_file(self, file_path: str, bucket_name: str, object_name: str = None):
        """
        Upload a file to S3.
        
        Args:
            file_path: Local path of the file.
            bucket_name: Target S3 bucket.
            object_name: S3 object name (if not provided, the file basename is used).
        """
        if object_name is None:
            object_name = os.path.basename(file_path)
        self.s3.upload_file(file_path, bucket_name, object_name)
        return f"Uploaded {file_path} to {bucket_name}/{object_name}"

    @ErrorHandler.handle_error(S3OperationError, "Error downloading file from S3")
    def download_file(self, bucket_name: str, object_name: str, file_path: str):
        """
        Download an S3 object to a local file.
        
        Args:
            bucket_name: Source S3 bucket.
            object_name: S3 object key.
            file_path: Local file path to save the object.
        """
        self.s3.download_file(bucket_name, object_name, file_path)
        return f"Downloaded {bucket_name}/{object_name} to {file_path}"

    @ErrorHandler.handle_error(S3OperationError, "Error deleting S3 object")
    def delete_object(self, bucket_name: str, object_key: str):
        """
        Delete an object from an S3 bucket.
        
        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object to delete.
        """
        return self.s3.delete_object(Bucket=bucket_name, Key=object_key)

    @ErrorHandler.handle_error(S3OperationError, "Error retrieving S3 bucket metadata")
    def head_bucket(self, bucket_name: str):
        """
        Retrieve metadata from an S3 bucket without returning the bucket contents.
        """
        return self.s3.head_bucket(Bucket=bucket_name)

    @ErrorHandler.handle_error(S3OperationError, "Error retrieving S3 bucket ACL")
    def get_bucket_acl(self, bucket_name: str):
        """
        Retrieve the access control list (ACL) of an S3 bucket.
        """
        return self.s3.get_bucket_acl(Bucket=bucket_name)

    @ErrorHandler.handle_error(S3OperationError, "Error setting S3 bucket ACL")
    def put_bucket_acl(self, bucket_name: str, acl: str):
        """
        Set the access control list (ACL) for an S3 bucket.
        
        Args:
            acl: The ACL policy (e.g., 'private', 'public-read').
        """
        return self.s3.put_bucket_acl(Bucket=bucket_name, ACL=acl)

    @ErrorHandler.handle_error(S3OperationError, "Error retrieving S3 bucket policy")
    def get_bucket_policy(self, bucket_name: str):
        """
        Retrieve the bucket policy of an S3 bucket.
        """
        return self.s3.get_bucket_policy(Bucket=bucket_name)

    @ErrorHandler.handle_error(S3OperationError, "Error setting S3 bucket policy")
    def put_bucket_policy(self, bucket_name: str, policy: str):
        """
        Set the bucket policy for an S3 bucket.
        
        Args:
            policy: A JSON-formatted bucket policy.
        """
        return self.s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)

    @ErrorHandler.handle_error(S3OperationError, "Error deleting S3 bucket policy")
    def delete_bucket_policy(self, bucket_name: str):
        """
        Delete the bucket policy of an S3 bucket.
        """
        return self.s3.delete_bucket_policy(Bucket=bucket_name)

    @ErrorHandler.handle_error(S3OperationError, "Error retrieving S3 bucket location")
    def get_bucket_location(self, bucket_name: str):
        """
        Retrieve the geographic region where the bucket resides.
        """
        response = self.s3.get_bucket_location(Bucket=bucket_name)
        return response.get('LocationConstraint', None)
