import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR= os.path.join(BASE_DIR,"data_in_github")
TABLES_DIR= os.path.join(DATA_DIR,"tables_formatted")
TABLES_INDEX= os.path.join(DATA_DIR,"table_index.csv")
OUTPUT_DIR= os.path.join(BASE_DIR,"output")
