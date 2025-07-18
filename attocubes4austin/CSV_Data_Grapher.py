"""
-Stand alone automatic graphing/PDF creator utility for combined TC and RTD data
-Uses the PySimpleGUI library for easy selection of files and filename creation
-Current version of tool only works for combination TC/RTD files, files must NOT have anything other
than data column names in header for tool to work
    -Other Python programs written for thermometry work may need some code changes to conform to standard
    data structure so all tools can function together (to-do)

Created on Fri Jul 30 11:08:27 2023

@author: aeverman
"""

import pandas as pd
from matplotlib import pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

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

sg.theme("DarkTeal2")
layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],[sg.Button("Submit")]]

# Building Window
window = sg.Window('My File Browser', layout, size=(600,150))
    
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        fullFileName = values["-IN-"]

fullFileNamePDF = fullFileName[:-4] + ".pdf"

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