import os
import re
from FileHandler import FileHandler


def remove_line_breaks_dash(text: str) -> str:
    ''' remove line breaks with dashes'''
    cleaned_text = text.replace("-\n", "")
    return cleaned_text


def remove_dash_wo_line_break(text: str) -> str:
    return re.sub(r"(\w)-(\w)", r"\1\2", text)


def remove_non_ascii(text: str) -> str:
    """remove all non-ASCII characters """
    text = re.sub(r"[\uFFF0-\uFFFD]+", "", text)
    text = re.sub(r"\uf0b7", "", text)
    return text


def clean_gruene_2017(text: str) -> str:
    """remove line breaks that don't end with a whitespace. Should only be used for gruene_2017"""
    text = re.sub(r"(\w)\n(\w)", r"\1\2", text)
    # text = re.sub(r"(\w)[ \n]{2,}(\w)", r"\1\2", text)
    return text


def clean_complete():
    fh = FileHandler()
    txt_dict = fh.open_txt_files("txt", debug=True)

    for year in txt_dict.keys():
        for party in txt_dict[year].keys():
            txt_dict[year][party][0] = remove_non_ascii(remove_line_breaks_dash(
                txt_dict[year][party][0]))

            if year == "2017" and party == "gruene":
                txt_dict[year][party][0] = clean_gruene_2017(
                    txt_dict[year][party][0])

            if year == "2017" and party == "spd":
                txt_dict[year][party][0] = remove_dash_wo_line_break(
                    txt_dict[year][party][0])

            fh.store_file("clean", f"{party}_{year}.txt",
                          txt_dict[year][party][0])


if __name__ == "__main__":
    clean_complete()
