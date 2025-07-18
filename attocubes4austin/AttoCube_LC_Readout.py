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
                  '207Ch1 [pM]', 
                  '207Ch2 [pM]',
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
                  'SA LC [N]']
    
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
            'MAIN.rb_x'
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
        
        # Increment index number
        index = index + 1
        
        # Write a new row in the CSV based on the fieldnames defined above
        PLC_writer.writerow({
            'Index' : index,
            'Seconds': monotonic() - t0,
            'PLC Time' : symbols['MAIN.sTime'],
            '206Ch1 [pM]': Dev206Ch0,
            '206Ch2 [pM]': Dev206Ch1, 
            '207Ch1 [pM]': Dev207Ch0, 
            '207Ch2 [pM]': Dev207Ch1,
            'Atto Avg. [uM]' : ((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000, # Average all Attos and convert to uM
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
            'BWY [mm]' : (symbols['MAIN.engMirEnc'] - symbols['MAIN.engActEnc'])
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

df.plot(x=7, y=12, legend=False, xlabel="Attocube Avg. [um]", ylabel="Loadcell [N]", label="Attocube Results")
m, b = np.polyfit(df['Atto Avg. [uM]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.1f}x {b:+.1f}')
plt.xlim((min(df['Atto Avg. [uM]'])), (max(df['Atto Avg. [uM]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=9, y=12, legend=False, xlabel="Actuator [mm]", ylabel="Loadcell [N]", label="Actuator Results")
m, b = np.polyfit(df['engAct [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.1f}x {b:+.1f}')
plt.xlim((min(df['engAct [mm]'])), (max(df['engAct [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=11, y=12, legend=False, xlabel="Mirror [um]", ylabel="Loadcell [N]", label="Mirror Results")
m, b = np.polyfit(df['engMir [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.1f}x {b:+.1f}')
plt.xlim((min(df['engMir [mm]'])), (max(df['engMir [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

df.plot(x=22, y=12, legend=False, xlabel="BWY [mm]", ylabel="Loadcell [N]", label="BWY Results")
m, b = np.polyfit(df['BWY [mm]'], df['loadCell [N]'], deg=1)
plt.axline(xy1=(0, b), slope=m, color="red", label=f'y = {m:.1f}x {b:+.1f}')
plt.xlim((min(df['BWY [mm]'])), (max(df['BWY [mm]'])))
plt.ylim((min(df['loadCell [N]']) + 0.1*min(df['loadCell [N]'])), (max(df['loadCell [N]']) + 0.1*max(df['loadCell [N]'])))
plt.legend()
plt.Figure()

# Save to multi-page PDF
save_image(fullFileNamePDF)

exit("Done.")