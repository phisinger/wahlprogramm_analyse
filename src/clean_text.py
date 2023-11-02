import os


def remove_line_breaks_dash(text: str) -> str:
    ''' remove line breaks with dashes'''
    cleaned_text = text.replace("-\n", "")

    return cleaned_text


txt_data_path = os.path.join(os.getcwd(), "data", "text_truncated")
clean_data_path = os.path.join(os.getcwd(), "data", "text_cleaned")

for year in ["2013", "2017", "2021"]:
    for party in ["afd", "cdu", "fdp", "gruene", "linke", "spd"]:
        filename = party + "_" + year + ".txt"
        in_file_path = os.path.join(txt_data_path, filename)
        out_file_path = os.path.join(
            clean_data_path, filename)

        with open(in_file_path, "r") as in_file:
            in_text = in_file.read()
            text_without_dash = remove_line_breaks_dash(in_text)

        with open(out_file_path, "w") as out_file:
            out_file.write(text_without_dash)


# remove line breaks with that don't end with a whitespace
