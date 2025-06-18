from helper.lib import get_date_range,  fetch_timeseries, save_timeseries_to_csv, get_and_save_data, load_minute_data, generate_second_level_data,save_to_csv,convert_minute_to_second_csv
from helper.config import TWELVE_API_KEY
import os

symbol = "CAD/USD"
hours = 10
output_dir = "data"
update_data_dir =  os.path.join(output_dir, "update")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(update_data_dir, exist_ok=True)
get_and_save_data(symbol=symbol,TWELVE_API_KEY=TWELVE_API_KEY, output_dir=output_dir, interval="1min", hours=hours, days_back=1)
convert_minute_to_second_csv(symbol=symbol, input_dir=output_dir, output_dir=update_data_dir)




