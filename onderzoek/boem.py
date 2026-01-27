import json

r = [[0]*5] * 10
for i in range(10):
    for j in range(5):
        r[i][j] = j

with open("boem.json", "w") as f:
    json.dump(r, f)
