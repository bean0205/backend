import requests
import json
import os
import base64
from typing import Optional, Dict, List, Any, Union, BinaryIO
from urllib.parse import quote

class MinioService:
    """
    Service class for interacting with MinIO File Management API
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the MinIO service with the API base URL

        Args:
            base_url: The base URL of the MinIO API
        """
        self.base_url = base_url.rstrip('/')

    def get_api_info(self) -> Dict[str, Any]:
        """
        Get general information about the API

        Returns:
            Dict containing API information
        """
        response = requests.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()

    def check_health(self) -> Dict[str, Any]:
        """
        Check if the API and MinIO connection are healthy

        Returns:
            Dict containing health status information
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def list_buckets(self) -> Dict[str, Any]:
        """
        Get a list of all buckets in MinIO

        Returns:
            Dict containing list of buckets and count
        """
        response = requests.get(f"{self.base_url}/buckets")
        response.raise_for_status()
        return response.json()

    def create_bucket(self, bucket_name: str) -> Dict[str, Any]:
        """
        Create a new bucket in MinIO

        Args:
            bucket_name: Name of the bucket to create

        Returns:
            Dict containing creation status message
        """
        response = requests.post(f"{self.base_url}/buckets/{bucket_name}")
        response.raise_for_status()
        return response.json()

    def upload_file(self, bucket_name: str, file_path: str) -> Dict[str, Any]:
        """
        Upload a file to MinIO

        Args:
            bucket_name: Name of the bucket to upload to
            file_path: Path to the local file to upload

        Returns:
            Dict containing upload information
        """
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            data = {'bucket_name': bucket_name}
            response = requests.post(f"{self.base_url}/upload", data=data, files=files)

        response.raise_for_status()
        return response.json()

    def upload_file_object(self, bucket_name: str, filename: str, file_object: BinaryIO, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file object to MinIO

        Args:
            bucket_name: Name of the bucket to upload to
            filename: Name for the file in MinIO
            file_object: File-like object to upload
            content_type: Content type of the file (optional)

        Returns:
            Dict containing upload information
        """
        files = {'file': (filename, file_object, content_type)}
        data = {'bucket_name': bucket_name}
        response = requests.post(f"{self.base_url}/upload", data=data, files=files)

        response.raise_for_status()
        return response.json()

    def upload_base64_image(self, bucket_name: str, file_name: str, base64_data: str, content_type: str = "image/jpeg") -> Dict[str, Any]:
        """
        Upload a base64-encoded image to MinIO

        Args:
            bucket_name: Name of the bucket to upload to
            file_name: Name for the file in MinIO
            base64_data: Base64-encoded image data
            content_type: Content type of the image (default: image/jpeg)

        Returns:
            Dict containing upload information
        """
        data = {
            "bucket_name": bucket_name,
            "file_name": file_name,
            "base64_data": base64_data,
            "content_type": content_type
        }

        response = requests.post(f"{self.base_url}/upload-base64", json=data)
        response.raise_for_status()
        return response.json()

    def download_file(self, bucket_name: str, object_name: str, output_path: str) -> str:
        """
        Download a file from MinIO and save to local path

        Args:
            bucket_name: Name of the bucket containing the file
            object_name: Name of the object to download
            output_path: Local path to save the downloaded file

        Returns:
            Path to the downloaded file
        """
        # URL encoding object name for safe usage in URL
        encoded_object_name = quote(object_name)
        response = requests.get(f"{self.base_url}/download/{bucket_name}/{encoded_object_name}", stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as output_file:
            for chunk in response.iter_content(chunk_size=8192):
                output_file.write(chunk)

        return output_path

    def get_file_content(self, bucket_name: str, object_name: str) -> bytes:
        """
        Get file content from MinIO without saving to disk

        Args:
            bucket_name: Name of the bucket containing the file
            object_name: Name of the object to download

        Returns:
            File content as bytes
        """
        encoded_object_name = quote(object_name)
        response = requests.get(f"{self.base_url}/download/{bucket_name}/{encoded_object_name}")
        response.raise_for_status()
        return response.content

    def list_files(self, bucket_name: str, prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        List files in a MinIO bucket

        Args:
            bucket_name: Name of the bucket
            prefix: Optional prefix to filter files (e.g., folder path)

        Returns:
            Dict containing list of objects in the bucket
        """
        url = f"{self.base_url}/files/{bucket_name}"
        if prefix:
            url += f"?prefix={quote(prefix)}"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def delete_file(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        """
        Delete a file from MinIO

        Args:
            bucket_name: Name of the bucket containing the file
            object_name: Name of the object to delete

        Returns:
            Dict containing deletion status message
        """
        encoded_object_name = quote(object_name)
        response = requests.delete(f"{self.base_url}/delete/{bucket_name}/{encoded_object_name}")
        response.raise_for_status()
        return response.json()

    def get_file_info(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        """
        Get information about a file in MinIO

        Args:
            bucket_name: Name of the bucket containing the file
            object_name: Name of the object to get info for

        Returns:
            Dict containing file information
        """
        encoded_object_name = quote(object_name)
        response = requests.get(f"{self.base_url}/info/{bucket_name}/{encoded_object_name}")
        response.raise_for_status()
        return response.json()

    def get_presigned_url(self, bucket_name: str, object_name: str, expires_hours: int = 1) -> Dict[str, Any]:
        """
        Get a presigned URL for accessing a file without authentication

        Args:
            bucket_name: Name of the bucket containing the file
            object_name: Name of the object to get a URL for
            expires_hours: Number of hours the URL will be valid for (default: 1)

        Returns:
            Dict containing the presigned URL and expiration information
        """
        encoded_object_name = quote(object_name)
        response = requests.get(
            f"{self.base_url}/presigned-url/{bucket_name}/{encoded_object_name}?expires_hours={expires_hours}"
        )
        response.raise_for_status()
        return response.json()
