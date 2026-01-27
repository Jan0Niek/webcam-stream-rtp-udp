import json
import matplotlib.pyplot as plt

with open("webp.json", "r") as wf, open("jpg.json", "r") as jf:
    webp = json.load(wf)
    jpeg = json.load(jf)

webpavgt = [sum(z[0] for z in x)/10 for x in webp]
webpavgs = [sum(z[1] for z in x)/10 for x in webp]
jpegavgt = [sum(z[0] for z in x)/10 for x in jpeg]
jpegavgs = [sum(z[1] for z in x)/10 for x in jpeg]

plt.plot(range(95), webpavgt)
plt.plot(range(95), jpegavgt)
plt.ylabel("tijd in seconden")
plt.xlabel("kwaliteit")
plt.show()
plt.plot(range(95), webpavgs)
plt.plot(range(95), jpegavgs)
plt.ylabel("grootte in bytes")
plt.xlabel("kwaliteit")
plt.show()
