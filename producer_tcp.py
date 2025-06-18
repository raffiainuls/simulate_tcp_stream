import socket
import pandas as pd
import time
from datetime import datetime
import os
from helper.lib import load_data, send_to_client, handle_new_connections,broadcast_data, start_server

HOST = "localhost"
PORT = 9999
client_sockets = []
CSV_FILE = "./data/update/data/data.csv"  # Ganti jika lokasi file berbeda
start_server(csv_path=CSV_FILE, host=HOST, port=PORT, load_data=load_data, handle_new_connections=handle_new_connections, send_to_client=send_to_client, broadcast_data=broadcast_data, client_sockets=client_sockets)
