from io import StringIO
import os
import glob
import pdftotext


def pdf2txt():

    # get file paths
    raw_data_path = os.path.join(os.getcwd(), "data", "raw")
    txt_data_path = os.path.join(os.getcwd(), "data", "text")
    print("Read files from: ", raw_data_path)
    print("Write files to: ", txt_data_path)

    # I only take the last three elections
    for year in ["2013", "2017", "2021"]:
        pathname = "*"+year+".pdf"
        for filename in glob.glob(pathname=pathname, root_dir=raw_data_path):
            file_path = os.path.join(raw_data_path, filename)

            output_string = StringIO()

            # read pdf and convert it to string
            with open(file_path, 'rb') as in_file:
                pdf = pdftotext.PDF(in_file)
            in_file.close()

            # contruct new file names
            dest_file_path = os.path.join(
                txt_data_path, filename.replace(".pdf", ".txt"))

            print(dest_file_path)

            with open(dest_file_path, "w+") as out_file:
                out_file.write("".join(pdf))
            out_file.close()

    print("Finished")
    return


if __name__ == "__main__":
    pdf2txt()
