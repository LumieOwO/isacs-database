import aiohttp
import asyncio
import timeit

base_url = "http://achingtraumaticoffices.idkdev2.repl.co"

headers = {
    "Content-Type": "application/json",
}


async def test_get(session, data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    async with session.get(url, headers=headers) as response:
        response_text = await response.text()
        print(url, headers)
        print(response_text)


async def test_set(session, data_file_path, directory, value):
    url = f"{base_url}/{data_file_path}"
    data = {"value": value}
    headers["Directory"] = directory
    async with session.post(url, headers=headers, json=data) as response:
        response_text = await response.text()
        print(response_text)


async def test_delete(session, data_file_path, directory):
    url = f"{base_url}/{data_file_path}"
    headers["Directory"] = directory
    async with session.delete(url, headers=headers) as response:
        response_text = await response.text()
        print(response_text)


async def test_all_cases():
    directory = "24211592"
    value = "24211592"
    dirs = ["PlayerDataV1"]
    async with aiohttp.ClientSession() as session:
        for data_file_path in dirs:
            print("Testing GET:")
            await test_get(session, data_file_path, directory)

            print("\nTesting SET:")
            await test_set(session, data_file_path, directory, value)

            print("\nTesting GET after SET:")
            await test_get(session, data_file_path, directory)

            print("\nTesting DELETE:")
            await test_delete(session, data_file_path, directory)

            print("\nTesting GET after DELETE:")
            await test_get(session, data_file_path, directory)


if __name__ == "__main__":
    execution_time = timeit.timeit(lambda: asyncio.run(test_all_cases()), number=1)
    print(f"Tests took: {execution_time} seconds")
