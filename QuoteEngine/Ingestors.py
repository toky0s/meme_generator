from typing import override

from QuoteEngine.IngestorInterface import IngestorInterface
from models.QuoteModel import QuoteModel
from docx import Document
import pathlib
import csv
import subprocess


class CsvIngestor(IngestorInterface):

    @override
    @classmethod
    def can_ingest(cls, path) -> bool:
        try:
            suffix = pathlib.Path(path).suffix
            if str.upper(suffix) != '.CSV':
                return False
            with open(path, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                return "body" in header and "author" in header
        except Exception:
            return False

    @override
    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        quotes = []
        with open(path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                quote = row["body"]
                author = row["author"]
                quote_obj = QuoteModel(quote, author)
                quotes.append(quote_obj)
        return quotes


class DocxIngestor(IngestorInterface):

    @override
    @classmethod
    def can_ingest(cls, path) -> bool:
        try:
            suffix = pathlib.Path(path).suffix
            if str.upper(suffix) != '.DOCX':
                return False
            return True
        except Exception:
            return False

    @override
    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        quote_models = []
        doc = Document(path)
        for paragraph in doc.paragraphs:
            line: str = paragraph.text
            if (line == ""):
                break
            split_text = line.split('-')
            quote_models.append(QuoteModel(split_text[0], split_text[1]))
        return quote_models


class PdfIngestor(IngestorInterface):
    """
    A PDF Ingestor
    """

    @override
    @classmethod
    def can_ingest(cls, path) -> bool:
        try:
            suffix = pathlib.Path(path).suffix
            if str.upper(suffix) != '.PDF':
                return False
            return True
        except Exception:
            return False

    @override
    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """
        @param cls: PdfIngestor
        @param path: Pdf path

        @return List of QuoteModel
        """
        fOutput = 'pdftotext.txt'
        _ = subprocess.run(f"pdftotext -layout {path} {fOutput}")

        quote_models: list[QuoteModel] = []
        with open(fOutput, 'r') as fText:
            for text in fText.readlines():
                arr_text = str.split(text, ' - ')
                if (len(arr_text) == 1):
                    break
                quote_models.append(QuoteModel(arr_text[0], arr_text[1]))
        return quote_models


class TextIngestor(IngestorInterface):

    @override
    @classmethod
    def can_ingest(cls, path) -> bool:
        try:
            suffix = pathlib.Path(path).suffix
            if str.upper(suffix) != '.TXT':
                return False
            return True
        except Exception:
            return False

    @override
    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        quote_models: list[QuoteModel] = []
        with open(path, 'r') as fText:
            for text in fText.readlines():
                arr_text = str.split(text, ' - ')
                quote_models.append(QuoteModel(arr_text[0], arr_text[1]))
        return quote_models


class Ingestor:

    @classmethod
    def create(cls, type: str) -> IngestorInterface:
        if type == '.txt':
            return TextIngestor()
        elif type == '.pdf':
            return PdfIngestor()
        elif type == '.csv':
            return CsvIngestor()
        else:
            return DocxIngestor()
