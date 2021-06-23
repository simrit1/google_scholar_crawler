import os
import pandas as pd
import numpy as np
import subprocess
from pdflatex import PDFLaTeX
from pathlib import Path



def init(config):
    path = config["storage"]["path"]
    assert os.path.isfile(path + "/combined_authors.csv"),\
        "Looks like the combined_authors.csv is not found in the data output location"
    data = pd.read_csv(path + "/combined_authors.csv", delimiter=",")
    return data


def show_values_on_bars(axs, h_v="v", space=0.4):
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = int(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height()
                value = int(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)




def generate_pdf(config):
    try:
        save_path = config["storage"]["path"]
        path = os.path.dirname(os.path.abspath(__file__))
        save_location = os.path.join(path, "report/")
        pdfl = PDFLaTeX.from_texfile(save_location + 'output.tex')
        # Dangerously set
        os.chdir(save_location)
        pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
        # Dangerously set
        os.chdir("../../" + save_path)
        f = open("output.pdf", "wb")
        f.write(pdf)
        f.close()
    except OSError as e:
        print("Execution failed:", e)
    except IOError as e:
        print("Execution failed:", e)


def generate_pdf_old():
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        save_location = os.path.join(path, "report/")
        os.chdir(save_location)
        subprocess.run(["pdflatex", save_location + "output.tex", "/dev/null"], capture_output=False)
    except OSError as e:
        print("Execution failed:", e)

