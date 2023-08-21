from flask import Flask, request, jsonify
import os
import json
from functools import lru_cache

app = Flask(__name__)
port = 3001

auth_key = ""


class DataHandler:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def authorize(self):
        token = request.headers.get("Authorization")
        return token == f"Bearer {auth_key}"

    @lru_cache(maxsize=None)
    def read_data(self):
        try:
            with open(f"data/{self.data_file_path}.json", "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print("Error reading data:", e)
            return {}

    def write_data(self, data):
        try:
            with open(f"data/{self.data_file_path}.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Error writing data:", e)

    def get_data(self):
        if self.authorize():
            directory = request.headers.get("Directory", "")
            data = self.read_data()
            return jsonify(
                data.get(directory, {"success": False, "error": "Data not found"})
            )
        else:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

    def modify_data(self, modify_func):
        if self.authorize():
            try:
                data = self.read_data()
                request_data = request.get_json()
                print(request_data)
                directory = request.headers.get("Directory", "")
                if directory is None:
                    return (
                        jsonify({"success": False, "error": "Invalid request data"}),
                        400,
                    )

                modified_data = modify_func(data, directory, request_data)
                self.write_data(modified_data)
                self.read_data.cache_clear()
                return jsonify({"success": True})
            except Exception as e:
                print("Error modifying data:", e)
                return (
                    jsonify({"success": False, "error": "Internal server error"}),
                    500,
                )
        else:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

    def set_data(self):
        return self.modify_data(self._set_data)

    @staticmethod
    def _set_data(data, directory, request_data):
        value = request_data.get("value")
        if value is not None:
            data[directory] = value
        return data

    def delete_data(self):
        if self.authorize():
            try:
                data = self.read_data()
                directory = request.headers.get("Directory", "")

                if not directory:
                    return (
                        jsonify({"success": False, "error": "Invalid request data"}),
                        400,
                    )

                modified_data = self._delete_data(data, directory)
                self.write_data(modified_data)
                self.read_data.cache_clear()
                return jsonify({"success": True})
            except Exception as e:
                print("Error deleting data:", e)
                return (
                    jsonify({"success": False, "error": "Internal server error"}),
                    500,
                )
        else:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

    @staticmethod
    def _delete_data(data, directory):
        if directory in data:
            del data[directory]
        return data


@app.route("/<data_file_path>", methods=["GET"])
def get_data(data_file_path):
    data_handler = DataHandler(data_file_path)
    return data_handler.get_data()


@app.route("/<data_file_path>", methods=["POST"])
def set_data(data_file_path):
    data_handler = DataHandler(data_file_path)
    return data_handler.set_data()


@app.route("/<data_file_path>", methods=["DELETE"])
def delete_data(data_file_path):
    data_handler = DataHandler(data_file_path)
    return data_handler.delete_data()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
