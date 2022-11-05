import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR= os.path.join(BASE_DIR,"data_in_github")
TABLES_DIR= os.path.join(DATA_DIR,"tables")
TABLES_INDEX= os.path.join(DATA_DIR,"table_index.csv")
OUTPUT_DIR= os.path.join(BASE_DIR,"output")
GDRIVE_OUTPUT_FOLDER= os.environ.get("GDRIVE_OUTPUT_FOLDER")

def get_full_outcomes():
    r4_l1=pd.read_csv(f"{DATA_DIR}/outcomes_l1.csv").rename(columns={"UID":"l1_UID","index":"l1_index"})
    r4_l2=pd.read_csv(f"{DATA_DIR}/outcomes_l2.csv").rename(columns={"UID":"l2_UID","index":"l2_index"})
    r4_l3=pd.read_csv(f"{DATA_DIR}/outcomes_l3.csv").rename(columns={"UID":"l3_UID","index":"l3_index"})
    r4_l4=pd.read_csv(f"{DATA_DIR}/outcomes_l4.csv").rename(columns={"index":"l4_index"})
    r4_l12 = pd.merge(r4_l1,r4_l2,on="l1_index")
    r4_l123 = pd.merge(r4_l12,r4_l3,on="l2_index")
    r4 = pd.merge(r4_l123,r4_l4,on="l3_index")
    r4_full=r4.dropna(subset=["l1","l2","l3","l4"]).fillna("")
    return r4_full


