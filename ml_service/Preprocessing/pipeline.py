import os
from ml_service.Preprocessing.embd import BulletEmbeddingProcessorPCA
from ml_service.Preprocessing.parsing import PdfToStructuredResumeParser
from ml_service.Preprocessing.extracting import ResumeContentExtractor

class ResumePipeline:
    """
    End-to-end pipeline:
    1. Read PDF → Bytes
    2. Parse to structured JSON
    3. Extract relevant sections (Experience, Projects, Education...)
    4. Generate 32D embeddings for bullets
    5. Write extracted content to a physical output directory
    """

    def __init__(self, output_dir="parsed_output"):
        self.parser = PdfToStructuredResumeParser()
        self.output_dir = output_dir
        self.bullet_processor = BulletEmbeddingProcessorPCA(n_components=32)

        os.makedirs(self.output_dir, exist_ok=True)

    def pdf_to_bytes(self, pdf_path: str) -> bytes:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        with open(pdf_path, "rb") as f:
            return f.read()

    def run(self, pdf_path: str) -> dict:
        # Step 1: Load PDF
        pdf_bytes = self.pdf_to_bytes(pdf_path)
        filename = os.path.basename(pdf_path)

        # Step 2: Parse PDF → structured doc JSON
        parsed_resume = self.parser.parse(pdf_bytes, filename)

        # Step 3: Extract relevant content (cleaned bullets/text)
        extractor = ResumeContentExtractor(parsed_resume)
        extracted_content = extractor.extract()

        # Step 4: Generate 32D embeddings for bullets
        bullet_embeddings = self.bullet_processor.process(extracted_content)

        # Optionally merge embeddings back into extracted_content
        extracted_content.update(bullet_embeddings)

        # Step 5: Write into physical output file
        self._write_to_output_file(filename, extracted_content)

        return extracted_content

    def _write_to_output_file(self, pdf_filename: str, extracted_content: dict) -> str:
        base_name = os.path.splitext(pdf_filename)[0]
        out_path = os.path.join(self.output_dir, f"{base_name}_extracted.txt")

        with open(out_path, "w", encoding="utf-8") as f:
            for section, content in extracted_content.items():
                f.write(f"{section.upper()}\n")
                # If content is a dict (has embedding), write only the text
                if isinstance(content, dict) and "content" in content:
                    f.write(content["content"])
                else:
                    f.write(str(content))
                f.write("\n\n")
        print(f"Extracted content and embeddings written to {out_path}")

