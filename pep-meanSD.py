import os, re
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd

def mean_SD(setmit):
    for item in setmit:
        mean = np.mean(item[2:5])
        standDevi = np.std(item[2:5])
        item[5] = mean
        item[6] = standDevi
        
        
def mergeFile(file, setmit, temp, filecounter):
    with open(file, 'r') as infile:
        
        # Generate list of lines. Iterate.
        list_lines = infile.readlines()
        for line in list_lines:
        
            # Split line.
            line = re.split('\s+', line)
            # Check if our line is already in the master list by checking if the sequence is already in it.                   
            
            seq_found = 0
            
            for item in setmit:
                if item[0] == line[0]:
                    item[filecounter + 2] = int(line[1])
                    seq_found = 1

            # If not, add the line to the master list.
            if seq_found == 0:
                temp[0] = line[0]
                temp[1] = line[2].strip()
                temp[2] = 0
                temp[3] = 0
                temp[4] = 0
                temp[filecounter + 2] = int(line[1])
                
                setmit.append(temp.copy())
            # print(temp)
    

def splitCombiner(files):

    setmit = []
    temp = ["","",0,0,0,"",""] # If 0 is at cell 3 and 4, it works fine
    
    # Using enumerate over manual counting of files.
    for filecounter, file in enumerate(files):
        mergeFile(file, setmit, temp, filecounter) # Call for file merger seen above.
        
    mean_SD(setmit)
    
    # Get directory, start writing outfile.
    with open(os.path.dirname(files[0]) + '\\' + 'RF_MSD_' + (os.path.basename(files[0])), 'w') as outfile:
        
        setmit.sort(reverse=True) # Sort in descending order.
        for item in setmit:
            outfile.write(item[0] + "\t" + item[1] + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t" + str(item[4]) + "\t" + str(item[5]) + "\t" + str(item[6]) + "\n")


# Tkinter options and initial file request
root = tk.Tk()
root.withdraw()
files = fd.askopenfilenames(parent=root, title='Choose files to merge')
splitCombiner(files)
