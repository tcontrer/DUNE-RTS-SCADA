import os

# * Class with the methods called to update and reset the DAT Window. Methods are called from within GUI.py

# * Method that reads the input from a file and updates what chips have been tested by accessing variables
# * defined in the GUI class
def readDAT(GUI):
    # * Path name for file being read
         # ! Must be updated for different machines and file names
         path: str = '/Users/volson/Desktop/chipsTestDisplay.txt'
         
         if os.path.isfile(path):
            # Reads only the last line of the file and sets the state based on that line
            with open(path, 'rb') as f:
                try:  # Catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)

                last_line = f.readline().decode()
                if last_line != None:
                    last_line = last_line.rstrip()

                # Updates what chips have been placed
                if last_line == "ChipSlotOnePlaced":
                    GUI.chipSlotsPlaced[0] = True
                if last_line == "ChipSlotTwoPlaced":
                    GUI.chipSlotsPlaced[1] = True
                if last_line == "ChipSlotThreePlaced":
                      GUI.chipSlotsPlaced[2] = True
                if last_line == "ChipSlotFourPlaced":
                    GUI.chipSlotsPlaced[3] = True
                if last_line == "ChipSlotFivePlaced":
                    GUI.chipSlotsPlaced[4] = True
                if last_line == "ChipSlotSixPlaced":
                    GUI.chipSlotsPlaced[5] = True
                if last_line == "ChipSlotSevenPlaced":
                    GUI.chipSlotsPlaced[6] = True
                if last_line == "ChipSlotEightPlaced":
                    GUI.chipSlotsPlaced[7] = True
                if (last_line == "reset") & GUI.DATCreated:
                     resetChipTests(GUI)
         else:
            print("Check file path name")

# * Updates the display to reflect which chip slots have completed testing. Only run when DAT window is open
def updateDATDisplay(GUI):
    if GUI.chipSlotsPlaced[0]:
        GUI.chipOneLabel.config(bg="green")
    if GUI.chipSlotsPlaced[1]:
        GUI.chipTwoLabel.config(bg="green")
    if GUI.chipSlotsPlaced[2]:
        GUI.chipThreeLabel.config(bg="green")
    if GUI.chipSlotsPlaced[3]:
        GUI.chipFourLabel.config(bg="green")
    if GUI.chipSlotsPlaced[4]:
        GUI.chipFiveLabel.config(bg="green")
    if GUI.chipSlotsPlaced[5]:
        GUI.chipSixLabel.config(bg="green")
    if GUI.chipSlotsPlaced[6]:
        GUI.chipSevenLabel.config(bg="green")
    if GUI.chipSlotsPlaced[7]:
        GUI.chipEightLabel.config(bg="green")

    if GUI.sm.current_state.id == "chipsTested":
        GUI.testsCompleteLabel.grid(row=2, column=2)
    else:
        GUI.testsCompleteLabel.grid_remove()

# * Resets all chipLabels and tracking variables to their pre-test values
def resetChipTests(GUI):
    count: int = 0
    while count < 8:
        if GUI.flag:
            GUI.chipLabels[count].config(bg="lightgray")
            GUI.chipSlotsPlaced[count] = False
        
        count += 1
    
    GUI.sm.chipTestNeedsReset = False

# * Reads a file to recive input on how to update the chip tray display
def readChipTray(GUI):
    # * Path name for file being read
         # ! Must be updated for different machines and file names
         path: str = '/Users/volson/Desktop/chipTrayDisplay.txt'
         
         if os.path.isfile(path):
            # Reads only the last line of the file and sets the state based on that line
            with open(path, 'rb') as f:
                try:  # Catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)

                last_line = f.readline().decode()
                if last_line != None:
                    last_line = last_line.rstrip()

                if (last_line not in GUI.chipStatuses) & (last_line != ""):
                    GUI.chipStatuses.append(last_line)

                if (last_line != "") & (last_line != "reset"):
                    chipNum: int = int(last_line[5:7])
                    GUI.chipStatusesLog[chipNum - 1] = last_line
                elif last_line == "reset":
                    GUI.resetChipTrayWindowMethod()

# * Updates labels on the chip tray display based on the chopStatuses list
def updateChipTrayDisplay(GUI):
    for chipStatus in GUI.chipStatuses:
        chipNum: int = int(chipStatus[5:7].rstrip())
        
        if chipStatus[8:] == "passed":
            GUI.chipTrayLabels[chipNum - 1].config(text="Passed", bg="green")
            GUI.chipStatuses.remove(chipStatus)
        elif chipStatus[8:] == "failed":
            GUI.chipTrayLabels[chipNum - 1].config(text="Failed", bg="red")
            GUI.chipStatuses.remove(chipStatus)
        else:
            print("Unrecognized item in chipTrayLabels list")