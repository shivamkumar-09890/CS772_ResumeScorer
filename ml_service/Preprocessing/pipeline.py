import os
import tempfile

from ml_service.Preprocessing.parsing import PdfToStructuredResumeParser
from ml_service.Preprocessing.extracting import ResumeContentExtractor


class ResumePipeline:
    """
    End-to-end pipeline:
    1. Read PDF → Bytes
    2. Parse to structured JSON using Docling wrapper
    3. Extract relevant sections (Experience, Projects, Education...)
    4. Write extracted content to a temp file
    """

    def __init__(self):
        self.parser = PdfToStructuredResumeParser()

    def pdf_to_bytes(self, pdf_path: str) -> bytes:
        """Read PDF file from disk and return its byte stream."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        with open(pdf_path, "rb") as f:
            return f.read()

    def run(self, pdf_path: str) -> str:
        """
        Execute complete pipeline and return path to temporary output file.
        """
        # Step 1: Load PDF into memory
        pdf_bytes = self.pdf_to_bytes(pdf_path)
        filename = os.path.basename(pdf_path)

        # Step 2: Parse PDF → structured doc JSON
        parsed_resume = self.parser.parse(pdf_bytes, filename)

        # Step 3: Extract relevant content (your bullets/text logic)
        self.extractor = ResumeContentExtractor(parsed_resume)
        extracted_content = self.extractor.extract()

        # Step 4: Write final extracted content into a temp file
        output_path = self._write_to_tempfile(extracted_content)

        return output_path

    def _write_to_tempfile(self, extracted_content: dict) -> str:
        """Write extracted resume content into a temporary .txt file."""
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")

        for section, text in extracted_content.items():
            tmp_file.write(f"=== {section.upper()} ===\n")
            tmp_file.write(text)
            tmp_file.write("\n\n")

        tmp_file.close()
        return tmp_file.name


if __name__ == "__main__":
    # Example usage:
    pipeline = ResumePipeline()
    pdf_path = "downloaded_resumes/25133_Surabhi_Sharma.pdf"

    output_file = pipeline.run(pdf_path)
    print("Processed resume written to:", output_file)
