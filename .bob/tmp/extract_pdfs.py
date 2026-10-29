import fitz, os, sys

base = r"C:\Users\KishorMarri\Desktop\Rapid Move - Competency\Rapid Move - Competency\14. Training Material\Transformation Cockpit\Transformation Cockpit"
jobs = [
    ("tc2019_adv", os.path.join(base, "Transformation Cockpit Advanced SNP3", "Transformation_Cockpit_2019_03_SP00_EN_20191130.pdf")),
    ("tc2019_snp2", os.path.join(base, "Transformation Cockpit SNP2", "Transformaton Cockpit_2019_03_SP00_EN_20191205.pdf")),
]
for name, path in jobs:
    if not os.path.exists(path):
        print(name, "NOT FOUND:", path)
        continue
    d = fitz.open(path)
    print(name, "pages:", len(d), "title:", d.metadata.get("title"), "toc:", len(d.get_toc()))
    with open(f".bob/tmp/{name}.txt", "w", encoding="utf-8") as out:
        for i, pg in enumerate(d):
            out.write(f"=====PAGE {i+1}=====\n" + pg.get_text() + "\n")
    with open(f".bob/tmp/{name}_toc.txt", "w", encoding="utf-8") as t:
        for lvl, ti, pn in d.get_toc():
            t.write("  " * (lvl - 1) + f"{ti} .... {pn}\n")
