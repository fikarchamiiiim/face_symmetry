import subprocess

subprocess.run(["pyuic5", "ui\\main_ui.ui", "-o", "ui\\main_ui.py"])