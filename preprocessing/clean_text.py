import os
import re
from FileHandler import FileHandler
from cleantext import clean


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
    text = re.sub(r"\u00AD\n", "", text)
    text = re.sub(r"\u2022", "", text)
    text = text.replace("|", " ")
    return text


def remove_mass_points(text: str) -> str:
    """Removes all groups of points with more than 3 points"""
    text = re.sub(r"\.{4,}", " ", text)
    return text


def clean_gruene_2017(text: str) -> str:
    """remove line breaks that don't end with a whitespace. Should only be used for gruene_2017"""
    text = re.sub(r"(\w)\n(\w)", r"\1\2", text)
    # text = re.sub(r"(\w)[ \n]{2,}(\w)", r"\1\2", text)
    return text


def replace_truncated_and(text: str) -> str:
    text = text.replace(" nd ", " and ")
    # text = text.replace(" ND ", " and ")
    # text = text.replace(" Nd ", " and ")
    return text


def clean_afd_2017(text: str) -> str:
    text = text.replace("K A P I T E L", "")
    return text


def clean_complete():
    fh = FileHandler()
    txt_dict = fh.open_txt_files("txt", debug=True)

    for year in txt_dict.keys():
        for party in txt_dict[year].keys():

            txt_dict[year][party][0] = remove_non_ascii(remove_line_breaks_dash(
                remove_mass_points(replace_truncated_and(txt_dict[year][party][0]))))

            if year == "2017" and party == "gruene":
                txt_dict[year][party][0] = clean_gruene_2017(
                    txt_dict[year][party][0])

            if year == "2017" and party == "spd":
                txt_dict[year][party][0] = remove_dash_wo_line_break(
                    txt_dict[year][party][0])

            if year == "2017" and party == "afd":
                txt_dict[year][party][0] = clean_afd_2017(
                    txt_dict[year][party][0])

            # using clean-text library
            txt_dict[year][party][0] = clean(
                txt_dict[year][party][0], no_line_breaks=True, lang="de")

            fh.store_file("clean", f"{party}_{year}.txt",
                          txt_dict[year][party][0])


if __name__ == "__main__":
    clean_complete()
