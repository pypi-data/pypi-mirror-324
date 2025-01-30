from labrador.document_loaders.directory import DirectoryLoader
from labrador.document_loaders.docx import DocxLoader
from labrador.document_loaders.html import HTMLLoader
from labrador.document_loaders.json import JSONLoader
from labrador.document_loaders.pdf import PDFLoader
from labrador.document_loaders.s3 import S3Loader
from labrador.document_loaders.watson_discovery import WatsonDiscoveryLoader

__all__ = [
    "DirectoryLoader",
    "DocxLoader",
    "HTMLLoader",
    "JSONLoader",
    "PDFLoader",
    "S3Loader",
    "WatsonDiscoveryLoader",
]
