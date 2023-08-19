from io import StringIO
import os
from pathlib import Path
import glob

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()

# get file paths
raw_data_path = os.path.join(Path().resolve().parent, "data", "raw")
txt_data_path = os.path.join(Path().resolve().parent, "data", "text")
print("Write files to:")

# I only take the last three elections
for year in ["2013", "2017", "2021"]:
    for filename in glob.glob(pathname=("*"+year+".pdf"), root_dir=raw_data_path): # type: ignore
        file_path = os.path.join(raw_data_path, filename)

        # read pdf and convert it to string
        with open(file_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        # contruct new file names
        dest_file_path = os.path.join(txt_data_path, filename.replace(".pdf", ".txt"))
        
        
        print(dest_file_path)
        
        with open(dest_file_path, "w") as out_file:
            out_file.write(output_string.getvalue())
            
print("Finished")