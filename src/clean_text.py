import os
from FileHandler import FileHandler


def remove_line_breaks_dash(text: str) -> str:
    ''' remove line breaks with dashes'''
    cleaned_text = text.replace("-\n", "")
    return cleaned_text

#


def remove_line_breaks_(text: str) -> str:
    """remove line breaks that don't end with a whitespace. Should only be used for some files"""
    return text.replace("\w\n", "")
