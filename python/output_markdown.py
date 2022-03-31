#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

import pandas as pd
import re

from lib.dataframe_to_text import dataframe_to_text
from lib.utils import DATA_DIR,TABLES_DIR,OUTPUT_DIR

os.makedirs(OUTPUT_DIR,exist_ok=True)

r4=pd.read_csv(f"{DATA_DIR}/outcomes.csv")
r4_l1=pd.read_csv(f"{DATA_DIR}/outcomes_l1.csv")
r4_l2=pd.read_csv(f"{DATA_DIR}/outcomes_l2.csv")
r4=pd.merge(r4_l2,r4,how="right",on="第2層")
r4=pd.merge(r4_l1,r4,how="right",on="第1層")
r4=r4.dropna(subset=["第1層","第2層","第3層","第4層"]).fillna("")

r4_to_md=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md["第1層"]="\n"+"# "+r4["第1層"]+"\n\n"+r4["第1層説明"]+"\n"
r4_to_md["第2層"]="\n"+"## "+r4["第2層"]+"\n\n"+r4["第2層説明"]+"\n"
r4_to_md["第3層"]="\n"+"### "+r4["第3層"]+"\n"
r4_to_md["第4層"]="1. "+r4["第4層"]
r4_to_md=r4_to_md.dropna(subset=["第1層","第2層","第3層","第4層"])

r4_md = dataframe_to_text(r4_to_md)

with open(f"{OUTPUT_DIR}/outcomes.md","w") as f:
    f.write(r4_md)
print("output... ./dist/outcomes.md")

r4


# In[ ]:


r4_md=re.sub(r"(\n# )",r"\n\\newpage\n\1",r4_md)

r4_md=r"""---
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
"""+r4_md

r4_md += f"\n\\newpage\n\n# 別表\n\n"

tables = ""

with open(f"{OUTPUT_DIR}/tables.tex","r") as f:
    latex_tables = f.read()
print("output... ./dist/r4_draft_tables.tex")

r4_md += latex_tables


with open("./dist/r4_draft_tex.md","w") as f:
    f.write(r4_md)

print("output... ./dist/r4_draft_tex.md")

r4_to_md_draft

