import yaml 
import subprocess
import os

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    

def read_query_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def execute_query_in_ksql(container_name, server_url, query, file_name):
    try:
        print(f"\n Running Query: {file_name}")


        # Tambahkan offset reset
        full_query =  query

        # Format full query jadi satu baris (escape newline)
        full_query = full_query.replace("\n", " ")

        # Gunakan --execute agar langsung dieksekusi
        cmd = [
            "docker", "exec", container_name,
            "ksql",
            server_url,
            "--execute", full_query
        ]
        process = subprocess.run(cmd, input=query.encode('utf-8'), capture_output=True)

        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')

        print(f"✅ Return code: {process.returncode}")
        print(f"📤 STDOUT:\n{stdout}")
        print(f"📥 STDERR:\n{stderr}")

        if process.returncode !=0 or "ERROR" in stdout.upper() or "ERROR" in stderr.upper():
            print(f"❌ Error when execute {file_name}:\n{stderr or stdout}")
        
        else:
            print(f"Finished execute {file_name}:\n{stdout}")

    except Exception as e:
        print(f" Exception When Excute query {file_name}: {e}")

