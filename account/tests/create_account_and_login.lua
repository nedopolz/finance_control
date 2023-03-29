create_account = function()
    headers = {}
    headers["Content-Type"] = "application/json"
    s = ""
    for i=1,10 do
        s = s .. string.char(math.random(97, 97 + 25))
    end
    existed = math.random(1, 100)
    if existed < 0 then
        s = "qwer"
    end
    body = string.format("{\"username\": \"%s\",\"password\": \"%s\",\"email\": \"%s\"}", s, s, s)
    return wrk.format("POST", "/v1/signup", headers, body)
end

requests = {}
table.insert(requests, create_account)

request = function()
    return requests[1]()
end

response = function(status, headers, body)
end