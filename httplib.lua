local HttpService = game:GetService("HttpService")

local baseUrl = "http://localhost:3001"
local authKey = "uwu"

local function testGet(dataFilePath, directory)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Authorization = "Bearer " .. authKey,
		Directory = directory,
	}

	local response = HttpService:GetAsync(url, false, headers)
	print(response)
end

local function testSet(dataFilePath, directory, value)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Authorization = "Bearer " .. authKey,
		Directory = directory,
	}
	local data = HttpService:JSONEncode({ value = value })

	local response = HttpService:PostAsync(url, data, Enum.HttpContentType.ApplicationJson,false ,headers)
	local responseData = HttpService:JSONDecode(response)
	print(responseData)
end

local function testDelete(dataFilePath, directory)
	local url = baseUrl .. "/" .. dataFilePath
	local headers = {
		Authorization = "Bearer " .. authKey,
		Directory = directory,
	}

	local response = HttpService:RequestAsync({
		Url = url,
		Method = "DELETE",
		Headers = headers,
	})

	print(response)
end

local function testAllCases()
	local directories = {"Banned", "Codes"}
	for _, dir in ipairs(directories) do
		local value = "your_value_here"

		print("Testing GET:")
		testGet(dir,'1')

		print("\nTesting SET:")
		testSet(dir,'1', 'value')

		print("\nTesting GET after SET:")
		testGet(dir,'1')

		print("\nTesting DELETE:")
		testDelete(dir,'1')

		print("\nTesting GET after DELETE:")
		testGet(dir,'1')
	end
end

testAllCases()
