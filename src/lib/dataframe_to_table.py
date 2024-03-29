'''
make html or text table output from dataframe
'''
import json
from textwrap import dedent
from string import Template
import pandas as pd

def escape_tex(data:str):
    """escape special characters in latex"""
    dic={
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "~": r"\verb|~|",
        "_": r"\_",
        "^": r"\verb|^|",
        "∖": r"\verb|\|",
        "{": r"\{",
        "}": r"\}",
        ">": r"\verb|>|",
        "<": r"\verb|<|",
        "|": r"\verb+|+",
    }
    return data.translate(str.maketrans(dic))

def do_group_rows(table:pd.DataFrame):
    """ group samerows in dataframe"""
    def process_cell_info(text:str,row_span:int):
        cell_info = json.dumps({
            "text": text,
            "row_span":row_span
        })
        return [cell_info,*([None]*(row_span-1))]

    columns=list(table.columns.values)
    output_table=table.copy().fillna("")
    template_table=output_table.copy()
    for i in range(0,len(columns)-1):
        to_indexed = columns[0:i+1]
        indexed =template_table.groupby(to_indexed,as_index=False,sort=False)\
            .count()\
            .apply(lambda x:process_cell_info(x[i],x[i+1]),axis=1)
        indexed = sum(indexed,[])
        indexed = list(map(lambda x:json.loads(x) if x is not None else None,indexed))
        output_table.iloc[:,i]=indexed
    return output_table

def make_html_table(table:pd.DataFrame,
    group_rows:bool=False,
    legend:str="",
    id=""):
    """ make html table from dataframe """
    def to_table_cell(x):
        if x is None:
            return ""
        elif isinstance(x,dict):
            return f'<td rowspan="{x["row_span"]}">{x["text"]}</td>'
        else:
            return f"<td>{x}</td>"

    output_table= do_group_rows(table) if group_rows else table.copy().fillna("")
    columns=list(table.columns.values)

    output_table=output_table.applymap(to_table_cell)

    theader=f"<thead><tr><th>{'</th><th>'.join(columns)}</th></tr></thead>"
    tbody="<tbody>\n"
    for items in output_table.fillna("").itertuples():
        row=f"<tr>{''.join(items[1:])}</tr>\n"
        tbody += row
    tbody+="</tbody>\n"
    id_part= f' id={id}' if len(id)>0 else "" 
    legend_part= f"<p>{legend}</p>" if len(legend)>0 else ""
    table_html=f"{legend_part}<table border=1{id_part}>{theader}\n{tbody}</table>"
    return table_html

def repeat(char:str,count:int):
    """ repeat same char for count time """
    return "".join([char for x in range(count)])

def make_latex_table(
    table:pd.DataFrame,
    label:str="",
    layout:str="",
    caption:str="",
    legend:str="",
    group_rows:bool=False):
    """ make latex table from dataframe """
    def to_table_cell(x):
        if x is None:
            return ""
        elif isinstance(x,dict):
            return x["text"]
        else:
            return x

    columns=list(table.columns.values)
    layout = layout if layout!="" else repeat("X",len(columns))
    output_table= do_group_rows(table) if group_rows else table.copy().fillna("")

    output_table=output_table.applymap(to_table_cell)
    output_table=output_table.applymap(escape_tex)
    #label = escape_tex(label)
    caption = escape_tex(caption)

    theader=Template(r"""
        \begin{xltabular}{\linewidth}{$layout}
        \caption{\label{tbl:$label}$caption} \\
    """).safe_substitute({"layout":layout,"label":label,"caption":caption})
    if legend!="":
        theader+=Template("    \\caption*{$legend} \\\\\n").safe_substitute({"legend":legend})
    theader=dedent(theader)+"\\toprule\n"
    theader+=' & '.join(columns)+r" \\"
    tbody="\\midrule\n\\endhead\n"
    for items in output_table.itertuples():
        row=' & '.join(items[1:])+r" \\"+"\n"
        tbody += row
    tbody+=r"\bottomrule"
    table_latex=f"{theader}\n{tbody}"+dedent(r"""
        \end{xltabular}
    """)
    return table_latex

def make_markdown_table(
    table:pd.DataFrame,
    group_rows:bool=False,
    id="",
    legend:str="",
    caption:str=""):
    """ make markdown table from dataframe """
    def to_table_cell(x):
        if x is None:
            return ""
        elif isinstance(x,dict):
            return f'{x["text"]}'
        else:
            return f"{x}"

    output_table= do_group_rows(table) if group_rows else table.copy().fillna("")
    columns=list(table.columns.values)

    output_table=output_table.applymap(to_table_cell)

    theader=f"| {' | '.join(columns)} |\n"
    theader+=f"| "+' | '.join(list(map(lambda _: "----",columns)))+" |\n"
    tbody=""
    for items in output_table.fillna("").itertuples():
        row=f"| {' | '.join(items[1:])} |\n"
        tbody += row
    id_part= f"\n## {caption} "+'{#'+id+'}\n\n' if len(id)>0 else "" 
    legend_part= f"\n\n{legend}\n\n" if len(legend)>0 else ""
    output_table=f"{id_part}{legend_part}{theader}{tbody}"
    return output_table
