from helper.package import load_config
from helper.package import read_query_file
from helper.package import execute_query_in_ksql
import os 


def main():
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, "config.yaml")

    config = load_config(config_path)

    container = config.get("ksqldb_cli_container")
    server_url = config.get("ksqldb_server_url")
    query_files = config.get("queries", [])

    for file in query_files:
        file_path = os.path.join(current_dir, file)
        if os.path.isfile(file_path):
            query = read_query_file(file_path)
            execute_query_in_ksql(container, server_url, query, file_path)
        else:
            print(f"File Not Found: {file_path}, Skipping....")
        


if __name__=="__main__":
    main()