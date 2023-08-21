import requests

base_url = "http://localhost:3001"
auth_key = ""

headers = {
    "Authorization": f"Bearer {auth_key}",
    "Content-Type": "application/json",
}


def test_get(data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    response = requests.get(url, headers=headers)
    print(response.json())


def test_set(data_file_path, directory, value):
    url = f"{base_url}/{data_file_path}"
    data = {"value": value}
    headers["Directory"] = directory
    response = requests.post(url, headers=headers, json=data)
    print(response.json())


def test_delete(data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    response = requests.delete(url, headers=headers)
    print(response.json())


def test_all_cases(data_file_path):
    directory = "isac"
    value = "0[1]XE/e+82hdDBAgEAAAAAAAAgAvzR5hnPHCAAAAAAAAAAAAAAAgAAAAAAAAAAABAAAAAAAAAAAAAAAAACAABIAB-AAAAEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAw-NAAAAAAAAAAAAAAAAQ--;F4HChYEAc3+iaGeMSBOAQNoCgPgqAdAGAswVAPeEkRxAP6tJvCAA;BC-CQEEgAOA;PYF8OomUE4wpckJFaqcBAAAAAAgxor7etMIA"

    print("Testing GET:")
    test_get(data_file_path, directory)

    print("\nTesting SET:")
    test_set(data_file_path, directory, value)

    print("\nTesting GET after SET:")
    test_get(data_file_path, directory)

    print("\nTesting DELETE:")
    test_delete(data_file_path, directory)

    print("\nTesting GET after DELETE:")
    test_get(data_file_path, directory)


if __name__ == "__main__":
    dirs = [
        "Banned",
        # "Codes"
    ]
    for dir in dirs:
        test_all_cases(dir)
