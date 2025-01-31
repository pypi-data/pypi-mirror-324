import os
import glob
import shutil
import subprocess

def calculate_swhid(directory_path, file_path):
    os.makedirs(directory_path, exist_ok=True)
    try:
        command = f"tar -xf {file_path} -C {directory_path}"
        subprocess.run(command, shell=True, check=True)
        command = ["swh.identify", directory_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.startswith("swh:1:dir:"):
                    swhid = line.split("\t")[0]
                    cleanup_extracted_files(directory_path)
                    return swhid
        else:
            print(f"Failed to compute folder SWHID: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to process tarball {file_path}: {e}")
    finally:
        cleanup_extracted_files(directory_path)
    return None

def cleanup_extracted_files(directory_path):
    try:
        for file_path in glob.glob(f"{directory_path}/*"):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
    except Exception as e:
        print(f"Failed to clean up {directory_path}: {e}")