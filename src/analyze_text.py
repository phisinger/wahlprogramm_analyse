import os
from pathlib import Path
import pandas as pd
import spacy
import re
import codecs
import plotly.express as px

class quant

def read_text(dir_path:str) -> dict:

    text_data = {}

    for year in ["2013", "2017", "2021"]:
        text_data[year] = {}
        for party in ["spd", "fdp", "cdu", "afd", "gruene", "linke"]:
            filename = party + "_" + year + ".txt"
            file_path = os.path.join(dir_path, filename)

            # read txt
            # with open(file_path, 'rb') as in_file:
            in_file = codecs.open(file_path, "r", encoding="utf-8")
            text_data[year][party] = in_file.read()
            in_file.close()
    return text_data




if __name__ == "__main__":        
    txt_data_path = os.path.join(Path().resolve().parent, "data", "text_cleaned")
    read_text(txt_data_path)