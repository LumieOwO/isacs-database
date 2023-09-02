import requests
import timeit

base_url = "https://achingtraumaticoffices.idkdev2.repl.co"

headers = {
    "Content-Type": "application/json",
}


def test_get(data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    response = requests.get(url, headers=headers)
    print(url, headers)
    print(response.text)


def test_set(data_file_path, directory, value):
    url = f"{base_url}/{data_file_path}"
    data = {"value": value}
    headers["Directory"] = directory
    response = requests.post(url, headers=headers, json=data)
    print(response.text)


def test_delete(data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    response = requests.delete(url, headers=headers)
    print(response.text)


def test_all_cases():
    directory = "isac"
    value = "1"
    dirs = ["Banned"]
    for data_file_path in dirs:
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
    print(f"Tests took: {timeit.timeit(test_all_cases, number=1)}")
