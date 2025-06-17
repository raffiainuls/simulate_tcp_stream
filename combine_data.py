import os
import pandas as pd
from helper.lib import combine_and_sort_csv

input_dir = "data/update"
update_data_dir =  os.path.join(input_dir, "data")
os.makedirs(update_data_dir, exist_ok=True)
# Misal folder kamu bernama "data"
df_result = combine_and_sort_csv(input_dir)

# Menyimpan hasil gabungan dan terurut ke file baru
df_result.to_csv( os.path.join(update_data_dir, "data.csv"), index=False)

# Atau menampilkan 5 baris pertama
print(df_result.head())
