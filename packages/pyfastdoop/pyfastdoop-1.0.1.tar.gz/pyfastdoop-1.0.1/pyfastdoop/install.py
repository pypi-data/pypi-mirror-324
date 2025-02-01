import os
import subprocess

# Configuration
JAR_URL = "https://github.com/umbfer/fastdoop/releases/download/v1.0/fastdoop-1.0.0.jar"
JAR_NAME = "fastdoop-1.0.0.jar"
SPARK_HOME = subprocess.getoutput("python -c 'import pyspark; print(pyspark.__path__[0])'")  # Default location if not set
CONF_FILE = os.path.join(SPARK_HOME, "conf", "spark-defaults.conf")
JAR_PATH = os.path.join(SPARK_HOME, "jars", JAR_NAME)  # Store JAR in Spark's jars directory

# Step 1: Download JAR if it doesn't exist
if not os.path.isfile(JAR_PATH):
    print(f"Downloading {JAR_NAME} to {JAR_PATH}...")
    os.makedirs(os.path.dirname(JAR_PATH), exist_ok=True)
    subprocess.run(["curl", "-L", "-o", JAR_PATH, JAR_URL])
    print("Download completed.")
else:
    print(f"{JAR_NAME} already exists at {JAR_PATH}.")

# Step 2: Check if JAR is in spark-defaults.conf
if os.path.isfile(CONF_FILE):
    with open(CONF_FILE, 'r') as f:
        lines = f.readlines()
else:
    print(f"{CONF_FILE} not found. Creating a new one...")
    os.makedirs(os.path.dirname(CONF_FILE), exist_ok=True)
    lines = []

JAR_CONFIG_LINE = f"spark.jars {JAR_PATH}"

if any(line.strip() == JAR_CONFIG_LINE for line in lines):
    print(f"{JAR_NAME} is already configured in {CONF_FILE}.")
else:
    print(f"Adding {JAR_NAME} to {CONF_FILE}...")
    with open(CONF_FILE, 'a') as f:
        f.write(f"{JAR_CONFIG_LINE}\n")
    print("Configuration updated.")

# Expand the `~` to the full path of the home directory
bashrc_path = os.path.expanduser("~/.bashrc")
try:
    # Check if the SPARK_CONF_DIR is already in the file
    if not any(f"SPARK_CONF_DIR={SPARK_HOME}/conf/" in line for line in open(bashrc_path, 'r').readlines()):
        with open(bashrc_path, 'a') as f:
            f.write(f"export SPARK_CONF_DIR={SPARK_HOME}/conf/\n")

    # Source the file by running it in a shell
    subprocess.run(f"source {bashrc_path}", shell=True, executable='/bin/bash')
except Exception as e:
    print(f"Error with .bashrc: {e}")

# For Zsh users (Mac users)
zshrc_path = os.path.expanduser("~/.zshrc")
try:
    # Check if Zsh configuration file exists and modify it
    if os.path.isfile(zshrc_path):
        if not any(f"SPARK_CONF_DIR={SPARK_HOME}/conf/" in line for line in open(zshrc_path, 'r').readlines()):
            with open(zshrc_path, 'a') as f:
                f.write(f"export SPARK_CONF_DIR={SPARK_HOME}/conf/\n")

    # Source the Zsh configuration file
    subprocess.run(f"source {zshrc_path}", shell=True, executable='/bin/zsh')
except Exception as e:
    print(f"Error with .zshrc: {e}")

print("✅ Setup completed successfully.")
