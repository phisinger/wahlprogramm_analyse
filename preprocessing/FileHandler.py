import codecs
import fitz
import os
from os import path
from typing import Optional
import re


class FileHandler(object):
    def __init__(self) -> None:
        self.data_dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))), "data")
        self.directories = {"raw": os.path.join(self.data_dir, "raw"),
                            "txt": os.path.join(self.data_dir, "txt"),
                            "chapters": os.path.join(self.data_dir, "chapters"),
                            "clean": os.path.join(self.data_dir, "clean"),
                            "clean chapters": os.path.join(self.data_dir, "chapters", "clean")}

        # Check if the directories are present, if not create them
        for _, dir in self.directories.items():
            if not os.path.exists(dir):
                os.makedirs(dir)

    def open_pdf_files(self, source_dir: str,
                       years: Optional[list[str]] = None,
                       parties: Optional[list[str]] = None,
                       debug: Optional[bool] = None) -> dict[str, dict[str, str]]:
        if years is None:
            years = ["1949", "1953", "1957", "1961", "1965", "1969", "1972", "1976", "1980",
                     "1983", "1987", "1990", "1994", "1998", "2002", "2005", "2009", "2013", "2017", "2021"]
        if parties is None:
            parties = ["afd", "cdu", "fdp", "gruene", "linke", "spd"]
        if debug is None:
            debug = True

        print(f"Read files from: {self.directories[source_dir]}", )

        output_dict = {}

        for year in years:
            output_dict[year] = {}
            for party in parties:
                filename = party + "_" + year + ".pdf"
                in_file_path = os.path.join(
                    self.directories[source_dir], filename)
                try:
                    doc = fitz.open(in_file_path)  # type: ignore
                    output_dict[year][party] = doc
                except Exception:
                    if debug:
                        print(
                            f"Cannot find file: {filename}. Continue with next one.")
                    continue

        return output_dict

    def open_txt_files(self, source_dir: str,
                       years: Optional[list[str]] = None,
                       parties: Optional[list[str]] = None,
                       debug: Optional[bool] = None) -> dict[str, dict[str, list]]:
        if years is None:
            years = ["1949", "1953", "1957", "1961", "1965", "1969", "1972", "1976", "1980",
                     "1983", "1987", "1990", "1994", "1998", "2002", "2005", "2009", "2013", "2017", "2021"]
        if parties is None:
            parties = ["afd", "cdu", "fdp", "gruene", "linke", "spd"]
        if debug is None:
            debug = True

        print("Read files from: ", self.directories[source_dir])

        # Initialize empty two dimensional dict
        output_dict = {}

        file_list = os.listdir(self.directories[source_dir])
        file_list.sort()
        for file_name in file_list:
            party = file_name.split("_")[0]
            year = file_name.split("_")[1].split(".")[0]
            if party in parties and year in years:
                in_file_path = os.path.join(
                    self.directories[source_dir], file_name)
                try:
                    # define further dict structure when needed
                    if not (year in output_dict.keys()):
                        output_dict[year] = {}
                    if not (party in output_dict[year].keys()):
                        output_dict[year][party] = []

                    with codecs.open(in_file_path, mode="r", encoding="utf-8") as in_file:
                        content = in_file.read()
                        output_dict[year][party].append(
                            content)
                except Exception:
                    if debug:
                        print(
                            f"Cannot find file: {file_name}. Continue with next one.")
                    continue

        return output_dict

    def store_file(self, target_dir: str,
                   file_name: str,
                   content: str) -> None:
        out_file_path = os.path.join(self.directories[target_dir], file_name)
        with open(out_file_path, "w+") as out_file:
            out_file.write(content)
        print("Write files to: ", out_file_path)
        return

    def extract_complete(self, source_dir: str,
                         target_dir: str,
                         years: list[str] = ["2013", "2017", "2021"],
                         parties: Optional[list[str]] = None,
                         debug: bool = False) -> None:
        """
        Transform the complete pdf document into one text file.
        """

        # open pdf
        doc_dict = self.open_pdf_files(source_dir, years, parties, True)

        # Apply custom text boxes
        for year in doc_dict.keys():
            for party in doc_dict[year].keys():
                if party == "afd" and year == "2021":
                    text_box = (34, 89, 398, 556)
                elif party == "afd" and year == "2017":
                    text_box = (119, 90, 668, 551)
                elif party == "afd" and year == "2013":
                    text_box = (113, 85, 521, 669)
                elif party == "cdu":
                    if year == "2013":
                        text_box = (60, 174, 541, 805)
                    else:
                        text_box = (65, 70, 527, 770)
                elif party == "fdp" and year == "2021":
                    text_box = (42, 115, 555, 799)
                elif party == "fdp" and year == "2017":
                    text_box = (43, 43, 379, 525)
                elif party == "fdp" and year == "2013":
                    text_box = (35, 35, 386, 552)
                elif party == "gruene":
                    if year == "2013":
                        text_box = (42, 66, 315, 465)
                    else:
                        text_box = (107, 103, 492, 744)
                elif party == "linke":
                    text_box = (42, 41, 439, 639)
                    pass
                elif party == "spd" and year == "2021":
                    text_box = (70, 96, 536, 756)
                elif party == "spd" and year == "2017":
                    text_box = (42, 63, 400, 566)
                elif party == "spd" and year == "2013":
                    text_box = (70, 70, 524, 761)
                else:
                    print("Document type not found. No textbox is applied.")
                    text_box = None

                # Extract core text
                core_text = ""
                for page in doc_dict[year][party]:
                    core_text += page.get_textbox(text_box)  # type: ignore
                # Store core text as txt
                output_file_name = f"{party}_{year}.txt"
                self.store_file(target_dir, output_file_name, core_text)
        return

    def extract_chapters():
        """
        Transform the pdf document into multiple text files containing a chapter each."""

        return

    def extract_to_markdown(self, source_dir: str,
                            target_dir: str,
                            years: list[str] = ["2013", "2017", "2021"],
                            parties: Optional[list[str]] = None,
                            debug: bool = False) -> None:
        """
        Transform the complete pdf document into one text file conserving headlines as markdown headlines.
        """

        # open pdf
        doc_dict = self.open_pdf_files(source_dir, years, parties, True)

        # Apply custom text boxes
        for year in doc_dict.keys():
            for party in doc_dict[year].keys():
                if party == "afd" and year == "2021":
                    text_box = (34, 89, 398, 556)
                elif party == "afd" and year == "2017":
                    text_box = (119, 90, 668, 551)
                elif party == "afd" and year == "2013":
                    text_box = (113, 85, 521, 669)
                elif party == "cdu":
                    if year == "2013":
                        text_box = (60, 174, 541, 805)
                    else:
                        text_box = (65, 70, 527, 770)
                elif party == "fdp" and year == "2021":
                    text_box = (42, 115, 555, 799)
                elif party == "fdp" and year == "2017":
                    text_box = (43, 43, 379, 525)
                elif party == "fdp" and year == "2013":
                    text_box = (35, 35, 386, 552)
                elif party == "gruene":
                    if year == "2013":
                        text_box = (42, 66, 315, 465)
                    else:
                        text_box = (107, 103, 492, 744)
                elif party == "linke":
                    text_box = (42, 41, 439, 639)
                    pass
                elif party == "spd" and year == "2021":
                    text_box = (70, 96, 536, 756)
                elif party == "spd" and year == "2017":
                    text_box = (42, 63, 400, 566)
                elif party == "spd" and year == "2013":
                    text_box = (70, 70, 524, 761)
                else:
                    print("Document type not found. No textbox is applied.")
                    text_box = None

                # get table of content
                toc = doc_dict[year][party].get_toc()  # type: ignore

                # Extract core text
                core_text = ""
                for page in doc_dict[year][party]:
                    page_text = page.get_textbox(text_box)  # type: ignore
                    for entry in toc:
                        level = "#"*entry[0]
                        title = entry[1]
                        if len(title) >= 6:
                            page_text = page_text.replace(
                                title, f"{level} {title}")

                    core_text += page_text
                # Store core text as txt
                output_file_name = f"{party}_{year}.md"
                self.store_file(target_dir, output_file_name, core_text)

        return


if __name__ == "__main__":
    fh = FileHandler()
    fh.extract_complete("raw", "txt", debug=True)
    fh.extract_to_markdown("raw", "clean chapters", debug=True)
