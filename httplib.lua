local baseUrl = ""
local HttpService = game:GetService("HttpService")

local function testGet(dataFilePath, directory)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Directory = directory,
	}

	local success, response = pcall(HttpService.GetAsync, HttpService, url, false, headers)
	if success then
		print(response)
	else
		print("GET Error:", response)
	end
end

local function testSet(dataFilePath, directory, value)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Directory = directory,
	}
	local data = HttpService:JSONEncode({ value = value })

	local success, response = pcall(HttpService.PostAsync, HttpService, url, data, Enum.HttpContentType.ApplicationJson,
		false, headers)
	if success then
		local responseData = HttpService:JSONDecode(response)
		print(responseData)
	else
		print("SET Error:", response)
	end
end

local function testDelete(dataFilePath, directory)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Directory = directory,
	}

	local success, response = pcall(HttpService.RequestAsync, HttpService, {
		Url = url,
		Method = "DELETE",
		Headers = headers,
	})

	if success then
		print(response)
	else
		print("DELETE Error:", response)
	end
end

local function testAllCases()
	local directories = { "Banned", "Codes" }
	for _, dir in ipairs(directories) do
		local value = "your_value_here"

		print("Testing GET:")
		testGet(dir, '1')

		print("\nTesting SET:")
		testSet(dir, '1', 'value')

		print("\nTesting GET after SET:")
		testGet(dir, '1')

		print("\nTesting DELETE:")
		testDelete(dir, '1')

		print("\nTesting GET after DELETE:")
		testGet(dir, '1')
	end
end

testAllCases()
