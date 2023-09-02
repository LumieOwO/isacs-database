import os
import json
import msgpack

json_directory = "./data"


def process_json_file(file_path):
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        msgpack_data = msgpack.packb(json_data, use_bin_type=True)

        msgpack_filename = os.path.splitext(file_path)[0] + ".msgpack"

        with open(msgpack_filename, "wb") as msgpack_file:
            msgpack_file.write(msgpack_data)


for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)
        process_json_file(file_path)
