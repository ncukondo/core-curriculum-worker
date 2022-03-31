#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from lib.dataframe_to_table import make_latex_table
from lib.dataframe_to_table import make_html_table
from textwrap import dedent
import glob

from lib.utils import DATA_DIR,TABLES_DIR,OUTPUT_DIR,TABLES_INDEX


def output_tables():
    table_index = pd.read_csv(f'{TABLES_INDEX}',encoding="utf_8_sig")

    latex_output=""
    html_output=""
    for row in table_index.itertuples():
        table = pd.read_csv(f"{TABLES_DIR}/{row.id}.csv")
        table = table.drop("id",axis=1)

        latex_output+=make_latex_table(table,label=row.id,group_rows=True,caption=row.表名)+"\n\n"
        html_output+=make_html_table(table,group_rows=True)+"\n\n"

    with open(f"{OUTPUT_DIR}/tables.tex","w") as f:
        f.write(latex_output)
    with open(f"{OUTPUT_DIR}/tables.html","w") as f:
        f.write(html_output)

    print("output... tables.tex")
    print("output... tables.html")

output_tables()

