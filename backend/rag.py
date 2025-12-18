import file_loader as loader

pdf_path = loader.pdf_path

text_blocks = loader.extract_text(pdf_path)
table_blocks = loader.extract_tables(pdf_path)
image_blocks = loader.extract_images(pdf_path)

chunks = text_blocks + table_blocks + image_blocks

print(chunks)

