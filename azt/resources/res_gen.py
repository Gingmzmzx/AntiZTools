import os

current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)
res_list: list = {}
data_py = os.path.join(current_script_dir, "res_data.py")

if os.path.exists(data_py):
    os.remove(data_py)

for root, dirs, files in os.walk(os.path.join(current_script_dir, "files")):
    for file in files:
        with open(os.path.join(root, file), "rb") as f:
            file_content = f.read()

        filename = ".".join(file.split(".")[:-1])
        print("Generating", filename)
        with open(data_py, "a+") as f:
            f.write(f"\n\n{filename} = "+repr(file_content))

        res_list[filename] = file


with open(os.path.join(current_script_dir, "res_list.py"), "w+") as f:
    f.write("res_list = "+repr(res_list))

