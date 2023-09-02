import os
import msgpack
from urllib.parse import unquote
from flask import Flask, jsonify, request

app = Flask(__name__)
port = 3001
ErrorMSG = "null"


class DataHandler:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def read_data(self):
        try:
            with open(f"data/{self.data_file_path}.msgpack", "rb") as f:
                data = msgpack.unpack(f, raw=False)
                return data
        except Exception as e:
            print("Error reading data:", e)
            return (
                ErrorMSG,
                404,
            )

    def write_data(self, data):
        try:
            with open(f"data/{self.data_file_path}.msgpack", "wb") as f:
                msgpack.pack(data, f, use_bin_type=True)
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
            return ErrorMSG, 404

        return response_data, 200

    def modify_data(self, modify_func):
        try:
            data = self.read_data()
            request_data = request.get_json()  # Parse JSON data from request
            directory = unquote(request.headers.get("Directory", ""))
            if directory is None or request_data is None:
                return (
                    ErrorMSG,
                    400,
                )

            modified_data = modify_func(data, directory, request_data)
            self.write_data(modified_data)
            return jsonify({"success": True})
        except Exception as e:
            print("Error modifying data:", e)
            return (
                ErrorMSG,
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
                    ErrorMSG,
                    400,
                )

            modified_data = self._delete_data(data, directory)
            self.write_data(modified_data)
            return jsonify({"success": True})
        except Exception as e:
            print("Error deleting data:", e)
            return (
                ErrorMSG,
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
    app.run(host="0.0.0.0")
