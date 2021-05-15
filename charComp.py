import json

print(__name__);

with open('sample.json') as f:
    print(json.load(f))