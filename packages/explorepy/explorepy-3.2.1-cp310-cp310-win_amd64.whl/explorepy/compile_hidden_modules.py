import shutil
from distutils.extension import Extension
import os
from setuptools import setup

# to use this compiler, ues the following command from the director:
# python compile_hidden_modules.py build_ext --inplace
# Specify the directory where the .py files are located
directory = os.getcwd()

# List of specific filenames to rename
files_to_rename = ["tools.py", "packet.py", "btcpp.py"]

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is one of the specific files to rename
    if filename in files_to_rename:
        # Define the old and new file paths
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, filename[:-3] + ".pyx")

        # Copy the file to a new file with the .pyx extension
        shutil.copyfile(old_path, new_path)
        print(f"Copied {old_path} to {new_path}")

# List of .pyx files to be compiled
pyx_files = ["tools.pyx", "packet.pyx", "btcpp.pyx"]

# Define extensions for each .pyx file
extensions = [Extension(file.split(".")[0], [file]) for file in pyx_files]

setup(
    name="my_project",
    ext_modules=cythonize(extensions),
)
