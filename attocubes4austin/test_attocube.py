import pickle
import time
import pandas as pd

from IDS import Device

dev = Device('192.168.88.207')
dev.connect()

print(dev.getFeatureName(1)) #OK
print(dev.getSerialNumber()) #OK
print(dev.getFpgaVersion()) #OK
print(dev.getMacAddress()) #OK
print(dev.getDeviceType()) #OK
print(dev.getDeviceName()) #OK

print("Starting: ", dev.startMeasurement()) #OK

t0 = time.monotonic()

data = []
while time.monotonic() - t0 < 60:
    data.append([time.monotonic() - t0, dev.getAxisDisplacement(0), dev.getAxisDisplacement(1)])

with open ("test.bin", "wb") as f:
    pickle.dump(data, f)
    
with open("test.bin", "rb") as g:
    object = pickle.load(g)
    
f = pd.DataFrame(object)
f.to_csv('r_file.csv')
print("Stopping...")
dev.close()
