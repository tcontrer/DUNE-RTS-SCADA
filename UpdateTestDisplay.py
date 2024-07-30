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

                # Updates what chips have been tested
                if GUI.sm.testing: 
                    if last_line == "ChipSlotOneTested":
                        GUI.chipSlotsTested[0] = True
                    if last_line == "ChipSlotTwoTested":
                        GUI.chipSlotsTested[1] = True
                    if last_line == "ChipSlotThreeTested":
                        GUI.chipSlotsTested[2] = True
                    if last_line == "ChipSlotFourTested":
                        GUI.chipSlotsTested[3] = True
                    if last_line == "ChipSlotFiveTested":
                        GUI.chipSlotsTested[4] = True
                    if last_line == "ChipSlotSixTested":
                        GUI.chipSlotsTested[5] = True
                    if last_line == "ChipSlotSevenTested":
                        GUI.chipSlotsTested[6] = True
                    if last_line == "ChipSlotEightTested":
                        GUI.chipSlotsTested[7] = True
         else:
            print("Check file path name")

# * Updates the display to reflect which chip slots have completed testing. Only run when DAT window is open
def updateDATDisplay(GUI):
    if GUI.chipSlotsTested[0]:
        GUI.chipSlotOne.config(bg="green")
        GUI.chipOneLabel.config(bg="green")
    if GUI.chipSlotsTested[1]:
        GUI.chipSlotTwo.config(bg="green")
        GUI.chipTwoLabel.config(bg="green")
    if GUI.chipSlotsTested[2]:
        GUI.chipSlotThree.config(bg="green")
        GUI.chipThreeLabel.config(bg="green")
    if GUI.chipSlotsTested[3]:
        GUI.chipSlotFour.config(bg="green")
        GUI.chipFourLabel.config(bg="green")
    if GUI.chipSlotsTested[4]:
        GUI.chipSlotFive.config(bg="green")
        GUI.chipFiveLabel.config(bg="green")
    if GUI.chipSlotsTested[5]:
        GUI.chipSlotSix.config(bg="green")
        GUI.chipSixLabel.config(bg="green")
    if GUI.chipSlotsTested[6]:
        GUI.chipSlotSeven.config(bg="green")
        GUI.chipSevenLabel.config(bg="green")
    if GUI.chipSlotsTested[7]:
        GUI.chipSlotEight.config(bg="green")
        GUI.chipEightLabel.config(bg="green")

# * Resets all chipSlots, chipLabels, and tracking variables to their no test values
def resetChipTests(GUI):
    count: int = 0
    while count < 8:
        GUI.chipSlots[count].config(bg="black")
        GUI.chipLabels[count].config(bg="lightgray")
        GUI.chipSlotsTested[count] = False
        
        count += 1
    
    GUI.sm.chipTestNeedsReset = False