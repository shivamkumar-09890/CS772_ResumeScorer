import os
from docling.document_converter import DocumentConverter

# Folders
input_folder = "doc_parser/Data"
output_folder = "results"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize DocLing converter
converter = DocumentConverter()

# Iterate over all PDF files in input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        print(f"Processing {pdf_path} ...")
        
        # Convert PDF to DocLing document
        result = converter.convert(pdf_path)
        
        # Export to markdown
        markdown_content = result.document.export_to_markdown()
        
        # Create output markdown file name
        base_name = os.path.splitext(filename)[0]  # Remove .pdf
        output_file = os.path.join(output_folder, f"{base_name}.md")
        
        # Save markdown
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Saved markdown to {output_file}")

print("All PDFs processed!")
