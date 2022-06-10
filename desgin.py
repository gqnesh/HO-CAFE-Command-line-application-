''''for i in range(6):
    for j in range(6):
        if j == 0 or j == 1:
            print("ↈ", end = "  ")
        elif j == 4 or j == 5:
            print("ↈ", end = "  ")
        elif (i==2 or i ==3) and (j >1 and j<4):
            print("ↈ", end = "  ")
        else:
            print("__", end = "  ")
    print()
'''
from datetime import datetime 
import pandas as pd
import time

data = time.strftime("%B %d %Y %I:%M:%S %p")
data1 = [data.split(" ")]

df = pd.DataFrame(data1, columns= ["Month", "Date", "Year", "time", "AM/PM"])
print(df)

'''
ch1 = time.time()

ch2 = time.ctime(ch1)

# Wed Feb 16 13:39:47 2022
ch3 = list(ch2.split(" "))

data = [(ch3)]

df = pd.DataFrame(data, columns= ["Day"," Month", "Date", "Time", "Year"])

print(df)
'''
