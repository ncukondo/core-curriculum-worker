#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from lib.utils import OUTPUT_DIR,DATA_DIR


from dateutil.parser import parse as parse_date

from lib.google_drive import from_service_account

folder_id="1L4fQFNd42HEN5mPEgicRxZe3rY5_ZliB"

drive = from_service_account()
file_list= [
    f"{OUTPUT_DIR}/outcomes.pdf",
    f"{OUTPUT_DIR}/statistics_new_items.csv",
    f"{OUTPUT_DIR}/statistics_removed_ids.csv",
    f"{OUTPUT_DIR}/statistics_item_counts.csv",
    f"{OUTPUT_DIR}/statistics_h28_to_r4.csv",
    f"{DATA_DIR}/2016/goals.csv",
]
for file_path in file_list:
    root, ext = os.path.splitext(file_path)
    mimeType= ""
    exclude_ext=False
    if ext==".csv":
        mimeType= 'application/vnd.google-apps.spreadsheet'
        exclude_ext=True
    id=drive.update_by_name(file_path,folder_id,target_mime_type=mimeType,exclude_ext=exclude_ext)
    print(f"deploy {os.path.basename(file_path)} as {id}")

