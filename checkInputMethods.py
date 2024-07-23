import os
import time

# * Creates the methods run from within check_input() in RTSStateMachine.py

# Method that reads the last line of the file described by the path name
def readFile():
    # * Path name for file being read
         # ! Must be updated for different machines and file names
         path: str = '/Users/volson/Desktop/robotState.txt'
         
         if os.path.isfile(path):
            # Reads only the last line of the file and sets the state based on that line
            with open(path, 'rb') as f:
                try:  # Catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)

                return f.readline().decode()
         else:
            print("Check file path name")

# Method that updates the state of the state machine based on a last line which is passed into the method
def updateStateMachine(sm, last_line: str):
    # * Will change the state according to the last line of the file
    # * Won't run anything that calls cycle if currently cycling due to input from the GUI. Achieved by GUIidle check.
    # * Won't run if one of these methods is already being run to prevent accidently cycling. Achieved by runningMethodCI check.
    if (last_line.rstrip() == "stopped") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        stop(sm) 
    elif (last_line.rstrip() == "starting") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        beginStarting(sm)
    elif (last_line.rstrip() == "started") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        start(sm)
    elif (last_line.rstrip() == "stopping") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        startStopping(sm)
    elif (last_line.rstrip() == "ground") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        goToGround(sm)
    elif (last_line.rstrip() == "pickingChips") & (sm.GUIidle) & (not sm.runningMethodCI):
        sm.runningMethodCI = True
        beginChipMoving(sm)
    elif (sm.current_state.id in sm.movingChipStates) & (last_line.rstrip() in sm.movingChipStates):
        if ((sm.movingChipStates.index(sm.current_state.id) + 1) == sm.movingChipStates.index(last_line)) & (sm.GUIidle) & (not sm.runningMethodCI):
            sm.runningMethodCI = True
            cycleChipMoving(sm)
    elif (last_line.rstrip() == "poweringOnWIB") & (sm.GUIidle) & (not sm.runningMethodCI):
            sm.runningMethodCI = True
            beginChipTesting(sm)
    elif (sm.current_state.id in sm.resettingStates) & (last_line.rstrip() in sm.resettingStates):
            if ((sm.resettingStates.index(sm.current_state.id) + 1) == sm.resettingStates.index(last_line)) & (sm.GUIidle) & (not sm.runningMethodCI):
                sm.runningMethodCI = True
                print("Running Reset Cycle from file reading")
                cycleResetting(sm)
    elif (last_line.rstrip() == "curtainTripped") & (sm.GUIidle) & (not sm.runningMethodCI):
                sm.runningMethodCI = True
                tripCurtain(sm)


# * Next methods are called from within updateStateMachine()
# * Cycles to the stopping state
def startStopping(sm):
    if sm.current_state.id == "started":
        sm.log.append("cycle")
        sm.cycle()
        # // USED FOR DEBUGGING print("Cycled once from file")
    elif sm.current_state.id == "starting":
        sm.log.append("cycle")
        sm.cycle()
        sm.log.append("cycle")
        sm.cycle()
        # // USED FOR DEBUGGING print("Cycled twice from file")
         
    # * Allows check input methods to be run again
    sm.runningMethodCI = False

# * Cycles to the stopped state
def stop(sm):
    sm.to_stopping()
    time.sleep(.1)
    sm.cycle()

    # * Allows check input methods to be run again
    sm.runningMethodCI = False

# * Cycles to the starting state
def beginStarting(sm):
    if (sm.current_state.id == "stopped") | (sm.current_state.id == "ground"):
        sm.log.append("cycle")
        sm.cycle()
        # // USED FOR DEBUGGING print("Cycled once from file")

    # * Allows check input methods to be run again
    sm.runningMethodCI = False
    
# * Cycles to the started state
def start(sm):
    if (sm.current_state.id == "starting"):
        sm.log.append("cycle")
        sm.cycle()
        # // USED FOR DEBUGGING print("Cycled once from file")
    elif (sm.current_state.id == "ground"):
        sm.log.append("cycle")
        sm.cycle()
        sm.log.append("cycle")
        sm.cycle()
        # // USED FOR DEBUGGING print("Cycled twice from file")

    # * Allows check input methods to be run again
    sm.runningMethodCI = False

# * Goes from chipsPlacedOnTray, the last resetting state, to ground, the first basic state
def goToGround(sm):
    if (sm.current_state.id == "chipsPlacedOnTray"):
        sm.log.append("reset_cycle")
        sm.reset_cycle()

    sm.runningMethodCI = False

# * Switches from started to pickingChips, the first chip moving state
def beginChipMoving(sm):
    if sm.current_state.id == "started":
        sm.log.append("begin_chip_moving")
        sm.begin_chip_moving()
         
    sm.runningMethodCI = False

# * Moves between the chips moving states
def cycleChipMoving(sm):
    sm.log.append("chip_cycle")
    sm.chip_cycle()
    sm.runningMethodCI = False

# * Switches from chipsPlaced to the poweringOnWIB, the first testing state
def beginChipTesting(sm):
    if sm.current_state.id == "chipsPlaced":
        sm.log.append("begin_testing")
        sm.begin_testing()

# * Cycles between the reset states
def cycleResetting(sm):
    sm.log.append("reset_cycle")
    sm.reset_cycle()
    sm.runningMethodCI = False

# * Transitions from any state to curtainTripped
def tripCurtain(sm):
    if(sm.current_state.id != "curtainTripped") & (sm.current_state.id != "ground"):
        sm.log.append("curtain_tripped")
        sm.curtain_tripped()
         
    # * Allows check input methods to be run again
    sm.runningMethodCI = False