from flask import Flask, request, jsonify
import json
from functools import lru_cache
from urllib.parse import unquote

app = Flask(__name__)
port = 3001


class DataHandler:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    @lru_cache(maxsize=None)
    def read_data(self):
        try:
            with open(f"data/{self.data_file_path}.json", "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print("Error reading data:", e)
            return (
                jsonify(
                    {
                        "Success": False,
                        "StatusCode": 404,
                        "StatusMessage": "Data Not Found!",
                    }
                ),
                404,
            )

    def write_data(self, data):
        try:
            with open(f"data/{self.data_file_path}.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Error writing data:", e)

    def get_data(self):
        directory = unquote(request.headers.get("Directory", ""))
        data = self.read_data()
        response_data = data.get(
            directory,
            {
                "Success": False,
                "StatusCode": 404,
                "StatusMessage": "Data Not Found!",
            },
        )

        if response_data == {
            "Success": False,
            "StatusCode": 404,
            "StatusMessage": "Data Not Found!",
        }:
            response_body = jsonify(response_data)
            return response_body, 404

        success_response_data = {
            "Success": True,
            "StatusCode": 200,
            "StatusMessage": "Data Successfully Found!",
            "Body": response_data,
        }
        success_response_body = jsonify(success_response_data)

        return success_response_body, 200

    def modify_data(self, modify_func):
        try:
            data = self.read_data()
            request_data = request.get_json()
            print(request_data)
            directory = unquote(request.headers.get("Directory", ""))
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

    def set_data(self):
        return self.modify_data(self._set_data)

    @staticmethod
    def _set_data(data, directory, request_data):
        value = request_data.get("value")
        if value is not None:
            data[directory] = value
        return data

    def delete_data(self):
        try:
            data = self.read_data()
            directory = unquote(request.headers.get("Directory", ""))

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

    @staticmethod
    def _delete_data(data, directory):
        if directory in data:
            del data[directory]
        return data


@app.route("/<data_file_path>", methods=["GET"])
def get_data(data_file_path):
    data_handler = DataHandler(unquote(data_file_path))
    return data_handler.get_data()


@app.route("/<data_file_path>", methods=["POST"])
def set_data(data_file_path):
    data_handler = DataHandler(unquote(data_file_path))
    return data_handler.set_data()


@app.route("/<data_file_path>", methods=["DELETE"])
def delete_data(data_file_path):
    data_handler = DataHandler(unquote(data_file_path))
    return data_handler.delete_data()


if __name__ == "__main__":
    app.run(host="", port=port)
