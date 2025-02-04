from json_js import FrozenJSON, MutableJSON

print(FrozenJSON({"a":10}))

test = FrozenJSON({"a": 10, "b": [10, {"c": 20}]})

print(test.a)
print(test.b)
print(test.b[1])
print(test.b[1].c)
