import os
import pathlib
import pyads
import csv
from sys import exit
import datetime
from datetime import datetime as dt
from time import monotonic
from IDS import Device
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

J = np.array([[-0.0931,    0.4916,   -0.8658,   -0.1226,   -0.0119,    0.0064],
             [-0.1192,    0.4903,   -0.8634,   -0.1223,    0.0193,    0.0278],
             [0.1827,    0.6106,   -0.7706,    0.0953,   -0.1074,   -0.0625],
             [0.1964,    0.5962,   -0.7784,    0.0719,   -0.1225,   -0.0757],
             [-0.1134,   -0.0576,   -0.9919,    0.0931,    0.1340,   -0.0184],
             [-0.1281,   -0.0835,   -0.9882,    0.0619,    0.1513,   -0.0208]])

optical_paths = np.array([0, 0, 0, 0, 0, 0])

matrix_result = np.array([[0], [0], [0], [0], [0], [0]])

#-----------------------------------------------------------------------------------------------#

def save_image(filename):
    
    # PdfPages is a wrapper around pdf 
    # file so there is no clash and create
    # files with no error.
    p = PdfPages(filename)
      
    # get_fignums Return list of existing 
    # figure numbers
    fig_nums = plt.get_fignums()  
    figs = [plt.figure(n) for n in fig_nums]
      
    # iterating over the numbers in list
    for fig in figs: 
        
        # and saving the files
        fig.savefig(p, format='pdf') 
      
    # close the object
    p.close()  
    
#-----------------------------------------------------------------------------------------------#

# Try establish connection to AttoCube 206 and get info from device; If unable, print error to console and exit
try:
    print("Connecting to AttoCubube 206...")
    dev206 = Device('192.168.88.206')
    dev206.connect()
    
    print(dev206.getFeatureName(1)) #OK
    print(dev206.getSerialNumber()) #OK
    print(dev206.getFpgaVersion()) #OK
    print(dev206.getMacAddress()) #OK
    print(dev206.getDeviceType()) #OK
    print(dev206.getDeviceName()) #OK
    print("#206 CONNECTED \n")


    print("Connecting to AttoCubube 207...")
    dev207 = Device('192.168.88.207')
    dev207.connect()
    
    print(dev207.getFeatureName(1)) #OK
    print(dev207.getSerialNumber()) #OK
    print(dev207.getFpgaVersion()) #OK
    print(dev207.getMacAddress()) #OK
    print(dev207.getDeviceType()) #OK
    print(dev207.getDeviceName()) #OK
    print("#207 CONNECTED \n")
    
except:
    print("Could not connect to AttoCubes.\n Please check connection and try again.\n Now exiting.")
    exit()

# Try to establish connection to HPT Teststand at known NetID; If unable, print error to console and exit
AMSAddr = "10.10.160.129.1.1"
Port = 851
try:
    print("Connecting to Hardpoint teststand...")
    #plc = pyads.Connection('10.10.160.129.1.1', 851)
    plc = pyads.Connection(AMSAddr, Port)
    plc.open()
    print("Local address: " + str(plc.get_local_address()) + "\n")
    print("CONNECTED TO HARDPOINT TESTSTAND")

except:
    print("Could not connect to hardpoint teststand.\n Check that the NetID of the local machine is entered correctly.\n Now exiting.")
    exit()

# Try to establsih ADS Symbol Transaction at server cycle frequency; If unable, print error to console and exit
try:
    pyads.constants.ADSTRANS_SERVERCYCLE = 3
except:
    print("ERROR SETTING SYMBOL READ TO SERVER CYCLE MODE")


# Try to open folder at PATH location; If it doesnt exisit, create it. If unable, print error to console, print current
# PATH locations for troubleshooting, and exit 
try:
    
    if not os.path.isdir("\AttoCube_Results"):
        os.mkdir("\AttoCube_Results") 

except:
    print("ERROR IN FOLDER ACCESS")
    print("Current script directory: " + str(pathlib.Path(__file__).parent.resolve()))
    print("Current working directory: " + str(pathlib.Path().resolve()) )
    exit()

# Create new timestamped filename
HPT_NAME = plc.read_by_name("MAIN.sSelHPT", pyads.PLCTYPE_STRING)
startDate = datetime.date.today()
startTime = dt.now()
fileNameTS = HPT_NAME + "-" + startDate.strftime("%Y%m%d") + "_" + startTime.strftime("%Hh%Mm")
pathName = '\AttoCube_Results'
fullFileName = pathName + "\\" + fileNameTS + ".csv"

# Start collecting data
print("Starting data collection...")

# Use monotonic time so time never has a negative value
t0 = monotonic()
# Start CSV index at zero
index = 0

# Create new CSV file at previously created folder location with PLC_file name. Create all appropriate field names in for
# CSV dictionary sample collection.
with open(fullFileName, 'w', newline='') as PLC_file:
    
    # Define the field names to be used for the CSV. THIS MUST MATCH THE .writerow() CALL!!!
    fieldnames = ['Index',
                  'Seconds',
                  'PLC Time',
                  '206Ch1 [pM]', 
                  '206Ch2 [pM]',
                  '206Ch3 [pM]',
                  '207Ch1 [pM]', 
                  '207Ch2 [pM]',
                  '207Ch3 [pM]',
                  'Atto Avg. [uM]',
                  'ActCount [cts]', 
                  'engAct [mm]', 
                  'MirCount [cts]',
                  'engMir [mm]',
                  'loadCell [N]',
                  'mtrPos [cts]',
                  'mtrRPM',
                  'mtrCurnt [A]',
                  'encTemp [C]',
                  'mtrTemp [C]',
                  'bwyPSI',
                  'flowRate [slpm]',
                  'Setpoint [cts]',
                  'Interfer [mm]',
                  'BWY [mm]',
                  'AttoX [uM]',
                  'AttoY [uM]',
                  'AttoZ [uM]',
                  'AttoRotX [uRad]',
                  'AttoRotY [uRad]',
                  'AttoRotZ [uRad]',
                  'SA LC [N]',
                  'Setpoint [N]']
    
    # Create new instance of CSV writer, write dictionary defined above
    PLC_writer = csv.DictWriter(PLC_file, fieldnames=fieldnames)

    # Write header to CSV file
    PLC_writer.writeheader()

    # Create list of variable names to be block read from the PLC
    var_list = [
            'GVL_TS.ActEncCount',
            'MAIN.engActEnc',
            'GVL_TS.MirEncCount',
            'MAIN.engMirEnc',
            'GVL_TS.LC_InR',
            'GVL_TS.mtr_pos',
            'MAIN.mtrRPM',
            'MAIN.mtrCurrent',
            'MAIN.EncTemp',
            'MAIN.MtrTemp',
            'MAIN.BWYPressPSI',
            'MAIN.FlowRate',
            'MAIN.fbPLOOP.fSetpointValue',
            'MAIN.COARSE_VAL',
            'MAIN.sTime',
            'MAIN.PyLoadBusy',
            'MAIN.tglSine',
            'MAIN.tglROM',
            'MAIN.tglStiffness',
            'MAIN.tglBWY',
            'MAIN.tglPLoop',
            'MAIN.rb_x',
            'MAIN.sp_x'
            ]

    symbols = plc.read_list_by_name(var_list)

    # Loop for t seconds pulling data from both AttoCubes and all PLC symbols, writing a new line to CSV file on each loop
    while symbols['MAIN.PyLoadBusy'] == True:
        
        # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
        # PLC symbol name into var_list and call by name
        symbols = plc.read_list_by_name(var_list)
        
        # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
        # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
        Dev206Ch0 = dev206.getAxisDisplacement(0)
        Dev206Ch1 = dev206.getAxisDisplacement(1)
        Dev206Ch2 = dev206.getAxisDisplacement(2)
        Dev207Ch0 = dev207.getAxisDisplacement(0)
        Dev207Ch1 = dev207.getAxisDisplacement(1)
        Dev207Ch2 = dev207.getAxisDisplacement(2)
        
        plc.write_by_name('MAIN.atto1', Dev206Ch0)  # write to target
        plc.write_by_name('MAIN.atto2', Dev206Ch1)  # write to target
        plc.write_by_name('MAIN.atto3', Dev206Ch2)  # write to target
        plc.write_by_name('MAIN.atto4', Dev207Ch0)  # write to target
        plc.write_by_name('MAIN.atto5', Dev207Ch1)  # write to target
        plc.write_by_name('MAIN.atto6', Dev207Ch2)  # write to target
        
        optical_paths = ([Dev206Ch0, Dev206Ch1, Dev206Ch2, Dev207Ch0, Dev207Ch1, Dev207Ch2])
        
        matrix_result = np.dot(optical_paths, J)
        
        # Increment index number
        index = index + 1
        
        
        # Write a new row in the CSV based on the fieldnames defined above
        PLC_writer.writerow({
            'Index' : index,
            'Seconds': monotonic() - t0,
            'PLC Time' : symbols['MAIN.sTime'],
            '206Ch1 [pM]': Dev206Ch0,
            '206Ch2 [pM]': Dev206Ch1, 
            '206Ch3 [pM]': Dev206Ch2, 
            '207Ch1 [pM]': Dev207Ch0, 
            '207Ch2 [pM]': Dev207Ch1,
            '207Ch3 [pM]': Dev207Ch2,
            'Atto Avg. [uM]' : ((Dev206Ch0 + Dev206Ch1 + Dev206Ch2 + Dev207Ch0 + Dev207Ch1+ Dev207Ch2) / 6) / 1000000, # Average all Attos and convert to uM
            'ActCount [cts]' : symbols['GVL_TS.ActEncCount'],
            'engAct [mm]' : symbols['MAIN.engActEnc'],
            'MirCount [cts]' : symbols['GVL_TS.MirEncCount'], 
            'engMir [mm]' : symbols['MAIN.engMirEnc'],
            'loadCell [N]' : symbols['GVL_TS.LC_InR'],
            'mtrPos [cts]' : symbols['GVL_TS.mtr_pos'],
            'mtrRPM' : symbols['MAIN.mtrRPM'],
            'mtrCurnt [A]' : symbols['MAIN.mtrCurrent'],
            'encTemp [C]' : symbols['MAIN.EncTemp'],
            'mtrTemp [C]' : symbols['MAIN.MtrTemp'],
            'bwyPSI' :  symbols['MAIN.BWYPressPSI'],     
            'flowRate [slpm]' : symbols['MAIN.FlowRate'],
            'Setpoint [cts]' : symbols['MAIN.fbPLOOP.fSetpointValue'],
            'Interfer [mm]' : symbols['MAIN.COARSE_VAL'],
            'BWY [mm]' : (symbols['MAIN.engMirEnc'] - symbols['MAIN.engActEnc']),
            'AttoX [uM]' : matrix_result[0] / 1000000,
            'AttoY [uM]' : matrix_result[1] / 1000000,
            'AttoZ [uM]' : matrix_result[2] / 1000000,
            'AttoRotX [uRad]' : matrix_result[3] / 1000000,
            'AttoRotY [uRad]' : matrix_result[4] / 1000000,
            'AttoRotZ [uRad]' : matrix_result[5] / 1000000,
            'SA LC [N]' : symbols['MAIN.rb_x'],
            'Setpoint [N]' : symbols['MAIN.sp_x']                        
            })

# Close all connections to both AttoCubes and HPTTS and exit
plc.close()
dev206.close()
dev207.close()

#-----------------------------------------------------------------------------------------------#

df = pd.read_csv(fullFileName, usecols=fieldnames)

# Set the figure size
plt.rcParams["figure.figsize"] = [14.00, 7.00]
plt.rcParams["figure.autolayout"] = True
fullFileNamePDF = fullFileName[:-4] + ".pdf"

print(min(df['Atto Avg. [uM]']))
print(max(df['Atto Avg. [uM]']))

df.plot(x=9, y=14, legend=False, xlabel="Attocube Avg. [um]", ylabel="Loadcell [N]", label="Attocube Results")
m, b = np.polyfit(df['Atto Avg. [uM]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.1f}x {b:+.1f}')
plt.xlim((min(df['Atto Avg. [uM]'])), (max(df['Atto Avg. [uM]'])))
#plt.xlim((min(df['Atto Avg. [uM]']) + 0.1*(min(df['Atto Avg. [uM]'])), (max(df['Atto Avg. [uM]'])) + 0.1*(max(df['Atto Avg. [uM]']))))
plt.ylim((min(df['loadCell [N]']) + 0.3*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.3*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=11, y=14, legend=False, xlabel="Actuator [mm]", ylabel="Loadcell [N]", label="Actuator Results")
m, b = np.polyfit(df['engAct [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['engAct [mm]'])), (max(df['engAct [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=13, y=14, legend=False, xlabel="Mirror [um]", ylabel="Loadcell [N]", label="Mirror Results")
m, b = np.polyfit(df['engMir [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['engMir [mm]'])), (max(df['engMir [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=24, y=14, legend=False, xlabel="BWY [mm]", ylabel="Loadcell [N]", label="BWY Results")
m, b = np.polyfit(df['BWY [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['BWY [mm]'])), (max(df['BWY [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=25, y=14, legend=False, xlabel="Atto X Displacement [uM]", ylabel="Loadcell [N]", label="Atto X")
m, b = np.polyfit(df['AttoX [uM]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoX [uM]'])), (max(df['AttoX [uM]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=26, y=14, legend=False, xlabel="Atto Y Displacement [uM]", ylabel="Loadcell [N]", label="Atto Y")
m, b = np.polyfit(df['AttoY [uM]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoY [uM]'])), (max(df['AttoY [uM]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=27, y=14, legend=False, xlabel="Atto Z Displacement [uM]", ylabel="Loadcell [N]", label="Atto Z")
m, b = np.polyfit(df['AttoZ [uM]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoZ [uM]'])), (max(df['AttoZ [uM]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=28, y=14, legend=False, xlabel="Atto X Rotation [uRad]", ylabel="Loadcell [N]", label="Atto RotX")
m, b = np.polyfit(df['AttoRotX [uRad]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoRotX [uRad]'])), (max(df['AttoRotX [uRad]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=29, y=14, legend=False, xlabel="Atto Y Rotation [uRad]", ylabel="Loadcell [N]", label="Atto RotY")
m, b = np.polyfit(df['AttoRotY [uRad]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoRotY [uRad]'])), (max(df['AttoRotY [uRad]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=30, y=14, legend=False, xlabel="Atto Z Rotation [uRad]", ylabel="Loadcell [N]", label="Atto RotZ")
m, b = np.polyfit(df['AttoRotZ [uRad]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['AttoRotZ [uRad]'])), (max(df['AttoRotZ [uRad]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=32, y=31, legend=False, xlabel="SA Setpoint [N]", ylabel="SA LC [N]", label="SA LC")
m, b = np.polyfit(df['Setpoint [N]'], df['SA LC [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.4f}x {b:+.4f}')
plt.xlim((min(df['Setpoint [N]'])), (max(df['Setpoint [N]'])))
plt.ylim((min(df['SA LC [N]']) + 0.1*min(df['SA LC [N]'])), (max(df['SA LC [N]']) + 0.1*max(df['SA LC [N]'])))
plt.legend()
plt.Figure()

# Save to multi-page PDF
save_image(fullFileNamePDF)

exit("Done.")