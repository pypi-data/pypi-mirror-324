import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel


class Batch(BaseModel):
    id: int
    uid: str
    name: str
    status: str
    project_id: int
    created_at: str
    updated_at: str


class Document(BaseModel):
    id: int
    uid: str
    display_name: str
    value: Dict[str, Any]
    file_hash: Optional[str]
    gcs_path: Optional[str]
    user_id: Optional[int] = None
    status: str
    created_at: str
    updated_at: str
    doc_type: str


class GenerateSignedUrlResponse(BaseModel):
    document: Document
    signed_url: str


class UploadDocumentsResponse(BaseModel):
    batch: Batch
    documents: List[Document]


class AddUrlsResponse(BaseModel):
    documents: List[Document]


def guess_mime_type(filename: str) -> str:
    """Guess content type from filename."""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or "application/octet-stream"


def is_valid_file_upload_file(file_obj):
    """
    Check if a file upload object satisfies the requirements of both FileStorage and UploadFile.

    Args:
        file_obj (Union[werkzeug.datastructures.FileStorage, starlette.datastructures.UploadFile]): The file upload object to be checked.

    Returns:
        bool: True if the object has the necessary attributes, False otherwise.
    """
    return all(
        [
            hasattr(file_obj, "filename"),
            hasattr(file_obj, "file"),
        ]
    )


def is_valid_file_object(file_obj):
    """
    Check if a file object is a valid Python file-like object (e.g. SpooledTemporaryFile, BufferedReader, etc.).

    Args:
        file_obj (object): The file object to be checked.

    Returns:
        bool: True if the object is a valid file-like object, False otherwise.
    """
    return all(
        [
            hasattr(file_obj, "read"),
            hasattr(file_obj, "seek"),
            hasattr(file_obj, "tell"),
        ]
    )


class Documents:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def _generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = self.client.post(
            f"{self.base_url}/public/v1/documents/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())

    def _process(self, document_uids: List[str]):
        """Process the uploaded files."""
        response = self.client.post(
            f"{self.base_url}/public/v1/documents/process",
            json={"document_uids": document_uids},
        )
        response.raise_for_status()
        return UploadDocumentsResponse(**response.json())

    def process_url(self, url: str):
        response = self.client.post(
            f"{self.base_url}/public/v1/documents/urls",
            params={"urls": [url]},
        )
        response.raise_for_status()
        add_urls_response = AddUrlsResponse(**response.json())
        if not add_urls_response.documents:
            raise ValueError("No documents were created from the provided URL")

        new_document_uid = add_urls_response.documents[0].uid
        response = self._process([new_document_uid])
        return response

    def upload_documents(self, files: List[Any]):
        document_uids = []
        for file in files:
            if is_valid_file_upload_file(file):
                filename = file.filename or f"temp-{uuid4()}"
                filestream = file.file
            elif is_valid_file_object(file):
                filename = Path(getattr(file, "name", f"temp-{uuid4()}")).name
                filestream = file

            # Get signed URL for upload
            response = self._generate_signed_url(filename)
            document_uids.append(response.document.uid)

            # Upload file using signed URL
            upload_response = self.client.put(
                response.signed_url,
                data=filestream,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()

        # Process all uploaded files
        response = self._process(document_uids)
        return response


class DocumentsAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def _generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = await self.client.post(
            f"{self.base_url}/public/v1/documents/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())

    async def _process(self, document_uids: List[str]):
        """Process the uploaded files."""
        response = await self.client.post(
            f"{self.base_url}/public/v1/documents/process",
            json={"document_uids": document_uids},
        )
        response.raise_for_status()
        return UploadDocumentsResponse(**response.json())

    async def process_url(self, url: str):
        response = await self.client.post(
            f"{self.base_url}/public/v1/documents/urls",
            params={"urls": [url]},
        )
        response.raise_for_status()
        add_urls_response = AddUrlsResponse(**response.json())
        if not add_urls_response.documents:
            raise ValueError("No documents were created from the provided URL")

        new_document_uid = add_urls_response.documents[0].uid
        response = await self._process([new_document_uid])
        return response

    async def upload_documents(self, files: List[Any]):
        document_uids = []
        for file in files:
            if is_valid_file_upload_file(file):
                filename = file.filename or f"temp-{uuid4()}"
                filestream = file.file
            elif is_valid_file_object(file):
                filename = Path(getattr(file, "name", f"temp-{uuid4()}")).name
                filestream = file

            # Get signed URL for upload
            response = await self._generate_signed_url(filename)
            document_uids.append(response.document.uid)

            # Upload file using signed URL
            upload_response = await self.client.put(
                response.signed_url,
                data=filestream,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()

        # Process all uploaded files
        response = await self._process(document_uids)
        return response
