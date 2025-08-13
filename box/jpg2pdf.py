import os
import re
import sys
import subprocess
from pathlib import Path
import shutil

def jpg2pdf(jpj_dir, sav_dir):

    if os.path.basename(sav_dir) == "out":
        sys.exit(f"禁止文件夹名为：out")

    jpg_files = [f for f in os.listdir(jpj_dir) if f.lower().endswith('.jpg')]
    jpg_files = sorted(jpg_files, key=lambda x: int(re.search(r'(\d+)(?=\.jpg)', x).group()))

    current_path = os.getcwd()

    dir_name = os.path.basename(jpj_dir)
    with open(f'{dir_name}.tex', 'w', encoding='utf-8') as file:
        file.write(r"\documentclass{article}" + "\n")
        file.write(r"\usepackage{graphicx}" + "\n")
        file.write(r"\usepackage[a4paper, top=0mm, bottom=0mm, left=0mm, right=0mm]{geometry} " + "\n")

        file.write(r"\begin{document}" + "\n\n")

        for k in jpg_files:
            file.write(r"\begin{figure}[h!]" + "\n")
            file.write("\t" + r"\centering" + "\n")

            path_full = os.path.join(jpj_dir, k)
            path_full = path_full.replace('\\', '/')

            file.write(
                "\t" + r"\includegraphics[width=\paperwidth, height=\paperheight, keepaspectratio]" + f"{{{path_full}}}" + "\n")
            file.write(r"\end{figure}" + "\n\n")
            pass

        file.write(r"\end{document}" + "\n")

    result = subprocess.run(['pdflatex', f'{dir_name}.tex'], capture_output=True, text=True)

    [log.unlink() for log in Path(current_path).rglob('*.log')]
    [log.unlink() for log in Path(current_path).rglob('*.aux')]

    tmp_1 = os.path.join(sav_dir, f'{dir_name}.tex')
    if os.path.exists(tmp_1):
        os.remove(tmp_1)
    tmp_2 = os.path.join(sav_dir, f'{dir_name}.pdf')
    if os.path.exists(tmp_2):
        os.remove(tmp_2)

    shutil.move(f'{dir_name}.tex', sav_dir)
    shutil.move(f'{dir_name}.pdf', sav_dir)

    print(f"文件创建成功 - {tmp_1}")
    print(f"文件创建成功 - {tmp_2}")


    pass
