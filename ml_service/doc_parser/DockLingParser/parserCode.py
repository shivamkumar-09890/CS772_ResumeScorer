import os
from docling.document_converter import DocumentConverter

input_folder = "doc_parser/Data"
output_folder = "results_2"
os.makedirs(output_folder, exist_ok=True)
converter = DocumentConverter()

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        print(f"Processing {pdf_path} ...")
        
        result = converter.convert(pdf_path)
        markdown_content = result.document.export_to_markdown()
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(output_folder, f"{base_name}.md")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Saved markdown to {output_file}")

print("All PDFs processed!")
