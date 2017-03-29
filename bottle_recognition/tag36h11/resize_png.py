import os

for i in range(0, 10):
    os.system("convert tag36_11_0000" + str(i) + ".png -scale 180x180 2_5in/tag36_11_0000" + str(i) + ".png")

for i in range(10, 100):
    os.system("convert tag36_11_000" + str(i) + ".png -scale 180x180 2_5in/tag36_11_000" + str(i) + ".png")

for i in range(100, 587):
    os.system("convert tag36_11_00" + str(i) + ".png -scale 180x180 2_5in/tag36_11_00" + str(i) + ".png")
