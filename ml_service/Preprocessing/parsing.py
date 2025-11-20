import json
import time
from io import BytesIO
from collections import defaultdict

from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions, TesseractCliOcrOptions
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.document import DocumentStream

class PdfToStructuredResumeParser:

    def __init__(self):
        """Initialize OCR + PDF parsing pipeline."""
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.ocr_options = TesseractCliOcrOptions()

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=PyPdfiumDocumentBackend
                )
            }
        )

    def convert_pdf_bytes_to_json(self, pdf_bytes: bytes, filename="resume.pdf") -> dict:
        pdf_stream = BytesIO(pdf_bytes)
        doc_stream = DocumentStream(
            stream=pdf_stream,
            name=filename
        )

        start = time.time()
        result = self.converter.convert(doc_stream)
        print(f"PDF parsed in {time.time() - start:.2f} seconds.")

        return result.document.export_to_dict()

    def parse_docling_json(self, data: dict) -> dict:
        self.data = data

        self.texts_by_ref = {x["self_ref"]: x for x in data.get("texts", [])}
        self.groups_by_ref = {x["self_ref"]: x for x in data.get("groups", [])}
        self.tables_by_ref = {x["self_ref"]: x for x in data.get("tables", [])}
        self.pictures_by_ref = {x["self_ref"]: x for x in data.get("pictures", [])}

        self.resume = defaultdict(lambda: {
            "text": [],
            "bullets": [],
            "tables": [],
            "pictures": []
        })

        self.current_section = "UNASSIGNED"
        body_children = [self.resolve(ref) for ref in data["body"]["children"]]

        for child in body_children:
            ref = child["self_ref"]

            if ref.startswith("#/texts"):
                self._add_text(self.texts_by_ref[ref])

            elif ref.startswith("#/groups"):
                for item_ref in self.groups_by_ref[ref].get("children", []):
                    self._add_text(self.resolve(item_ref))

            elif ref.startswith("#/tables"):
                self._add_table(self.tables_by_ref[ref])

            elif ref.startswith("#/pictures"):
                self._add_picture(child)

        return self.resume


    def resolve(self, ref):
        if ref is None:
            return None
        if isinstance(ref, dict) and "$ref" in ref:
            ref = ref["$ref"]

        node = self.data
        for p in ref.lstrip("#/").split("/"):
            if isinstance(node, list):
                p = int(p)
            node = node[p]
        return node

    def _clean_text(self, text):
        return text.replace("\uf0b7", "•").strip()

    def _add_text(self, elem):
        text = self._clean_text(elem.get("text", ""))
        if not text:
            return

        label = elem.get("label", "")
        if label == "section_header":
            self.current_section = text.upper()
            return

        if label == "list_item":
            self.resume[self.current_section]["bullets"].append(text)
        else:
            self.resume[self.current_section]["text"].append(text)

    def _add_table(self, table):
        rows_raw = defaultdict(dict)
        for cell in table["data"]["table_cells"]:
            r = cell["start_row_offset_idx"]
            c = cell["start_col_offset_idx"]
            rows_raw[r][c] = cell.get("text", "")

        rows = [
            [rows_raw[r].get(c, "") for c in sorted(rows_raw[r].keys())]
            for r in sorted(rows_raw)
        ]
        self.resume[self.current_section]["tables"].append(rows)

    def _add_picture(self, _):
        self.resume[self.current_section]["pictures"].append("IMAGE/LOGO")

    def parse(self, pdf_bytes: bytes, filename="resume.pdf"):
        docling_json = self.convert_pdf_bytes_to_json(pdf_bytes, filename)
        return self.parse_docling_json(docling_json)

# if __name__ == "__main__":

#     parser = PdfToStructuredResumeParser()

#     with open("downloaded_resumes/25133_Surabhi_Sharma.pdf", "rb") as f:
#         pdf_bytes = f.read()

#     result = parser.parse(pdf_bytes, "25133_Surabhi_Sharma.pdf")

#     # save output
#     with open("parsed_output/25133_Surabhi_Sharma_parsed.json", "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=4)