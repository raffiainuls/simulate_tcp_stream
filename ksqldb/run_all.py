import os
import subprocess
import yaml
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_main_py(module_path):
    try:
        subprocess.run(["python", "-m", module_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {module_path}: {e}")

def main():
    base_dir = os.path.dirname(__file__)  # sql/
    config_path = os.path.join(base_dir, "config.yaml")

    config = load_config(config_path)
    folders = config.get("folders", [])

    for folder in folders:
        full_folder_path = os.path.join(base_dir, folder)
        main_file = os.path.join(full_folder_path, "main.py")
        if os.path.isfile(main_file):
            module_name = f"ksqldb.{folder}.main"
            print(f"▶️  Running: {module_name}")
            run_main_py(module_name)
        else:
            print(f"⚠️  Skipping {folder}: main.py not found.")

if __name__ == "__main__":
    main()
