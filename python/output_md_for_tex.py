#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re

from lib.utils import DATA_DIR,TABLES_DIR,OUTPUT_DIR

with open(f"{DATA_DIR}/outcomes.md","r") as f:
    outcomes_md = f.read()


outcomes_md=re.sub(r"(\n# )",r"\n\\newpage\n\1",outcomes_md)

outcomes_md=r"""---
title: "医学教育モデル・コア・カリキュラム"
header-includes: 
- \usepackage{multirow}
- \usepackage{xltabular}
- \usepackage{longtable}
- \usepackage{ltablex}
- \usepackage {booktabs}
figureTitle: "図 "
tableTitle: "表 "
listingTitle: "コード "
figPrefix: "図."
eqnPrefix: "式."
tblPrefix: "表."
lstPrefix: "コード."
---
"""+outcomes_md

outcomes_md += f"\n\\newpage\n\n# 別表\n\n"

tables = ""

with open(f"{OUTPUT_DIR}/tables.tex","r") as f:
    latex_tables = f.read()

outcomes_md += latex_tables


with open(f"{OUTPUT_DIR}/outcomes_for_tex.md","w") as f:
    f.write(outcomes_md)

print("output... outcomes_for_tex.md")

outcomes_md

