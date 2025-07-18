import os
import pathlib
import pyads
import csv
from sys import exit
import datetime
from datetime import datetime as dt
from time import monotonic
import time
from IDS import Device

# Number of steps to move hardpoint in each direction
stepSize = 2000
# Number of seconds to hold PID aat each setpoint
testTime = 10

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
#AMSAddr = "10.10.16.17.1.1"
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

# Get current current actuator encoder position for setpoint, check to ensure it is within sensible limits
#print('Enter PID Setpoint: ')
sp = plc.read_by_name('GVL_TS.ActEncCount', pyads.PLCTYPE_ULINT)
#sp = int(sp)
if (sp > 31400000) or (sp < 22400000):
    print("Setpoint outside of actuator limits, exiting..." + "\n")
    exit()

try:
    plc.write_by_name("MAIN.sSetpoint", str(sp), pyads.PLCTYPE_STRING)
except:
    print("Error writing to variable")
    exit()

#try:
    #print("tglPLoop = " + str(plc.read_by_name('MAIN.tglPLoop', pyads.PLCTYPE_BOOL)))
    #plc.write_by_name('MAIN.tglPLoop', True, pyads.PLCTYPE_BOOL)
#except:
   # print("Cannot start position loop test! Exiting...")
    #exit()
        
# Create new timestamped filename
HPT_NAME = plc.read_by_name("MAIN.sSelHPT", pyads.PLCTYPE_STRING)
startDate = datetime.date.today()
startTime = dt.now()
fileNameTS = HPT_NAME + "-PosRep-Kp" + str(round(plc.read_by_name('MAIN.fbPLOOP.stCTRL_PID_PARAMS.fKp'))) +'Ki' + str(round(plc.read_by_name('MAIN.fbPLOOP.stCTRL_PID_PARAMS.tTn'))) + "_" + startDate.strftime("%Y%m%d") + "_" + startTime.strftime("%Hh%Mm")
pathName = '\AttoCube_Results'
fullFileName = pathName + "\\" + fileNameTS + ".csv"

# Start collecting data
print("Starting automatic position repeatibility test and collecting data...")
print("Setpoint: " + str(sp))

#print("PAUSING FOR DEBUG")
#time.sleep(60)

# Use monotonic time so time never has a negative value
t0 = monotonic()
# Start CSV index at zero
index = 0

# Create new CSV file at previously created folder location with PLC_file name. Create all appropriate field names in for
# CSV dictionary sample collection.
with open(fullFileName, 'w', newline='') as PLC_file:
    
    PLC_file.write(HPT_NAME + "\n")
    PLC_file.write("Date: " + startDate.strftime("%B %d %Y") + "\n")
    PLC_file.write("Start time: " + startTime.strftime("%Hh%Mm%Ss") + "\n")
    PLC_file.write("Kp = " + str(plc.read_by_name('MAIN.fbPLOOP.stCTRL_PID_PARAMS.fKp')) + '  Ki= ' + str(plc.read_by_name('MAIN.fbPLOOP.stCTRL_PID_PARAMS.tTn')))
    PLC_file.write("\n")
    
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
                  'AttoAdj [um]',
                  'SetpointAdj [um]']
    
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
            'MAIN.tglPLoop'
            ]

    Dev206Ch0 = dev206.getAxisDisplacement(0)
    Dev206Ch1 = dev206.getAxisDisplacement(1)
    Dev207Ch0 = dev207.getAxisDisplacement(0)
    Dev207Ch1 = dev207.getAxisDisplacement(1)

    symbols = plc.read_list_by_name(var_list)
    attoAdj = ((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000
    spAdj = plc.read_by_name('MAIN.fbPLOOP.fSetpointValue', pyads.PLCTYPE_REAL)
    

    # Loop for t seconds pulling data from both AttoCubes and all PLC symbols, writing a new line to CSV file on each loop
    #while symbols['MAIN.PyLoadBusy'] == True
        
    while (monotonic() - t0) < testTime:
            
            # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
            # PLC symbol name into var_list and call by name
            symbols = plc.read_list_by_name(var_list)
        
            # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
            # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
            Dev206Ch0 = dev206.getAxisDisplacement(0)
            Dev206Ch1 = dev206.getAxisDisplacement(1)
            Dev207Ch0 = dev207.getAxisDisplacement(0)
            Dev207Ch1 = dev207.getAxisDisplacement(1)
        
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
                'BWY [mm]' : symbols['MAIN.engMirEnc'] - symbols['MAIN.engActEnc'],
                'AttoAdj [um]' : (((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000) - attoAdj,
                'SetpointAdj [um]' : (symbols['MAIN.fbPLOOP.fSetpointValue'] - spAdj) * 5E-3                          
                })
            
    sp = sp + stepSize
    print("Setpoint: " + str(sp))
    plc.write_by_name("MAIN.sSetpoint", str(sp), pyads.PLCTYPE_STRING)
    while ((monotonic() - t0) >= (testTime * 1)) and ((monotonic() - t0) < (testTime * 2)):
                
        # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
        # PLC symbol name into var_list and call by name
        symbols = plc.read_list_by_name(var_list)
            
        # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
        # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
        Dev206Ch0 = dev206.getAxisDisplacement(0)
        Dev206Ch1 = dev206.getAxisDisplacement(1)
        Dev207Ch0 = dev207.getAxisDisplacement(0)
        Dev207Ch1 = dev207.getAxisDisplacement(1)
            
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
            'AttoAdj [um]' : (((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000) - attoAdj,
            'SetpointAdj [um]' : (symbols['MAIN.fbPLOOP.fSetpointValue'] - spAdj) * 5E-3                                     
            })
                
    sp = sp - stepSize
    print("Setpoint: " + str(sp))
    plc.write_by_name("MAIN.sSetpoint", str(sp), pyads.PLCTYPE_STRING)
    while ((monotonic() - t0) >= (testTime * 2)) and ((monotonic() - t0) < (testTime * 3)):
                    
        # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
        # PLC symbol name into var_list and call by name
        symbols = plc.read_list_by_name(var_list)
                
        # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
        # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
        Dev206Ch0 = dev206.getAxisDisplacement(0)
        Dev206Ch1 = dev206.getAxisDisplacement(1)
        Dev207Ch0 = dev207.getAxisDisplacement(0)
        Dev207Ch1 = dev207.getAxisDisplacement(1)
        
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
            'AttoAdj [um]' : (((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000) - attoAdj,
            'SetpointAdj [um]' : (symbols['MAIN.fbPLOOP.fSetpointValue'] - spAdj) * 5E-3                                    
            })
                    
    sp = sp - stepSize
    print("Setpoint: " + str(sp))
    plc.write_by_name("MAIN.sSetpoint", str(sp), pyads.PLCTYPE_STRING)
    while ((monotonic() - t0) >= (testTime * 3)) and ((monotonic() - t0) < (testTime * 4)):
                        
        # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
        # PLC symbol name into var_list and call by name
        symbols = plc.read_list_by_name(var_list)
                    
        # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
        # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
        Dev206Ch0 = dev206.getAxisDisplacement(0)
        Dev206Ch1 = dev206.getAxisDisplacement(1)
        Dev207Ch0 = dev207.getAxisDisplacement(0)
        Dev207Ch1 = dev207.getAxisDisplacement(1)
            
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
            'AttoAdj [um]' : (((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000) - attoAdj,
            'SetpointAdj [um]' : (symbols['MAIN.fbPLOOP.fSetpointValue'] - spAdj) * 5E-3                                    
            })
                        
    sp = sp + stepSize
    print("Setpoint: " + str(sp))
    plc.write_by_name("MAIN.sSetpoint", str(sp), pyads.PLCTYPE_STRING)
    while ((monotonic() - t0) >= (testTime * 4)) and ((monotonic() - t0) < (testTime * 5)):
                            
        # Grab all symbols defined in var_list; if more are desired to be recorded, all that is recquired is to add the
        # PLC symbol name into var_list and call by name
        symbols = plc.read_list_by_name(var_list)
                        
        # Grab each axis from both AttoCubes and store to individual variables in order to average them later.
        # This is done to avoid having to make a second call to the AttoCubes and slowing down the overall sample rate
        Dev206Ch0 = dev206.getAxisDisplacement(0)
        Dev206Ch1 = dev206.getAxisDisplacement(1)
        Dev207Ch0 = dev207.getAxisDisplacement(0)
        Dev207Ch1 = dev207.getAxisDisplacement(1)
                        
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
            'AttoAdj [um]' : (((Dev206Ch0 + Dev206Ch1 + Dev207Ch0 + Dev207Ch1) / 4) / 1000000) - attoAdj,
            'SetpointAdj [um]' : (symbols['MAIN.fbPLOOP.fSetpointValue'] - spAdj) * 5E-3                                
            })
        
# Disable the test variable on the TwinCAT side to reenable the HMI button
plc.write_by_name('MAIN.btnPyPosRep', False, pyads.PLCTYPE_BOOL)


# Close all connections to both AttoCubes and HPTTS and exit
plc.close()
dev206.close()
dev207.close()

exit("Done.")