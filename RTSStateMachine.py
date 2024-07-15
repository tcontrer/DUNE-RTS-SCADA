from statemachine import StateMachine, State
import time
import threading
import os

# * A state machine to manage the movement of the RTS arm in correspondence with input from the robot

# * Transitions:
# cycle: Will transition the state machine to the next normal (non error) state. Ground to starting, starting to started, etc.
# begin_chip_moving: Will transition the state machine to the chip moving states.
# chip_cycle: Will transition the state machine between chip moving states.
# begin_testing: Will transition the state machine to the testing states.
# test_cycle: Will transition the state machine between testing states.
# begin_cleanup: Will transition the state machine to the cleanup states.
# cleanup_cycle: Will transition the state machine between the cleanup states.
# curtain_tripped: Will transition the state machine from any state to the curtainTripped state.
# reset_cycle: Will transition the state machine from the curtainTripped state through the resetting states. Run if there 
# could be chips on the RTS's arm.
# straight_reset: Will transition the state machine from curtainTripped to the ground state. Run if there is no possiblity 
# of chips being on the arm.

# * Methods:
# on_enter_NAMEOFSTATE: Automatically called when NAMEOFSTATE is entered. Print the state to the terminal and update lastNFS
# checkInput: Checks the last line of a file every second and responds based on what that line is. The file is written 
# from within the RTS software. Provides a connection between the RTS and the state machine.
# methods under checkInput: They are called from within check input and cycle the state machine based on its current state

# * Variables:
# exists: boolean that is true until the GUI is closed. Used to properly shut down the state machine
# GUIidle: boolean that is false when a button is pressed on the GUI and then becomes true again when the corrosponding action 
# is complete
# runningMethodCI: booolean that is true when a method within checkInput is called and then becomes false again when that 
# the corrosponding action is complete
# lastNFT: string that tracks the last non fault state the state machine was in. Used to help restart after light curtain trip
# chipsInArm: boolean that is true when there are chips on the RTS's arm and false when there aren't.

class RTSMachine(StateMachine):
     def __init__(self):
         # Tracks if the GUI has been closed
         self.exists: bool = True
         # Tracks if a button on the GUI has been pressed
         self.GUIidle: bool = True
         # Tracks if a method is in progress from check input
         self.runningMethodCI = False
         # Tracks the last non fault state the robot has been in
         self.lastNFS: State
         # Tracks if the arm has chips in it
         self.chipsInArm: bool = False

         # * Tuples that group states together. Used to have more general checks of state.
         self.basicStates: tuple = ("ground", "starting", "started", "stopping", "stopped")
         self.movingChipStates: tuple = ("pickingChips", "chipsPicked", "movingChipsToBoard", "chipsMovedToBoard", "placingChips", "chipsPlaced")
         self.testingChipStates: tuple = ("poweringOnWIB", "WIBOn", "testingChips", "chipsTested", "sendingData", "dataSent", "poweringOffWIB", "WIBOff")
         self.cleanupChipStates: tuple = ("removingChips", "chipsRemoved")
         self.resettingStates: tuple = ("waitingToMoveToTray", "movingChipsToTray", "chipsMovedToTray", "placingChipsOnTray", "chipsPlacedOnTray")

         # * List to track the transitions and states the state machine has gone through
         self.log: list = []

         super().__init__()
     
     # * The states the system can be in
     # Simple states
     ground = State(initial=True)
     starting = State()
     started = State()
     stopping = State() 
     stopped = State()

     # Chip moving states
     pickingChips = State()
     chipsPicked = State()
     movingChipsToBoard = State()
     chipsMovedToBoard = State()
     placingChips = State()
     chipsPlaced = State()

     # Testing states
     poweringOnWIB = State()
     WIBOn = State()
     testingChips = State()
     chipsTested = State()
     sendingData = State()
     dataSent = State()
     poweringOffWIB = State()
     WIBOff = State()

     # Cleanup States
     removingChips = State()
     chipsRemoved = State()

     # Reset States
     waitingToMoveToTray = State()
     movingChipsToTray = State()
     chipsMovedToTray = State()
     placingChipsOnTray = State()
     chipsPlacedOnTray = State()

     # * Fault states
     curtainTripped = State()

     # Transitions the state machine between basic(?) states
     cycle = (
         ground.to(starting)
         | starting.to(started)
         | started.to(stopping)
         | stopping.to(stopped)
         | stopped.to(starting)
     )

     # Transtions the state machine to chip moving states
     begin_chip_moving = (
         started.to(pickingChips)
     )

     # Transtions the state machine between chip moving states
     chip_cycle = (
         pickingChips.to(chipsPicked)
         | chipsPicked.to(movingChipsToBoard)
         | movingChipsToBoard.to(chipsMovedToBoard)
         | chipsMovedToBoard.to(placingChips)
         | placingChips.to(chipsPlaced)
         | chipsPlaced.to(pickingChips)
     )

     # Transitions the state machine to testing states
     begin_testing = (
         chipsPlaced.to(poweringOnWIB)
     )

     # Transitions the state machine between testing states
     test_cycle = (
         poweringOnWIB.to(WIBOn)
         | WIBOn.to(testingChips)
         | testingChips.to(chipsTested)
         | chipsTested.to(sendingData)
         | sendingData.to(dataSent)
         | dataSent.to(poweringOffWIB)
         | poweringOffWIB.to(WIBOff)
     )

     # Transitions the state machine to cleanup states
     begin_cleanup = (
         WIBOff.to(removingChips)
     )

     # Transitions the state machine between cleanup states
     cleanup_cycle = (
         removingChips.to(chipsRemoved)
     )

     # Sends the state machine right to the curtain tripped state
     curtain_tripped = (
         ground.to(curtainTripped)
         | starting.to(curtainTripped)
         | started.to(curtainTripped)
         | stopping.to(curtainTripped)
         | stopped.to(curtainTripped)
         | pickingChips.to(curtainTripped)
         | chipsPicked.to(curtainTripped)
         | movingChipsToBoard.to(curtainTripped)
         | chipsMovedToBoard.to(curtainTripped)
         | placingChips.to(curtainTripped)
         | chipsPlaced.to(curtainTripped)
         | poweringOnWIB.to(curtainTripped)
         | WIBOn.to(curtainTripped)
         | testingChips.to(curtainTripped)
         | chipsTested.to(curtainTripped)
         | sendingData.to(curtainTripped)
         | dataSent.to(curtainTripped)
         | poweringOffWIB.to(curtainTripped)
         | WIBOff.to(curtainTripped)
         | removingChips.to(curtainTripped)
         | chipsRemoved.to(curtainTripped)
     )

     # Sends the state machine from curtain tripped through the resetting states
     reset_cycle = (
         curtainTripped.to(waitingToMoveToTray)
         | waitingToMoveToTray.to(movingChipsToTray)
         | movingChipsToTray.to(chipsMovedToTray)
         | chipsMovedToTray.to(placingChipsOnTray)
         | placingChipsOnTray.to(chipsPlacedOnTray)
         | chipsPlacedOnTray.to(ground)
     )

     # Sends the state machine from curtain tripped straight to the ground state
     straight_reset = (
         curtainTripped.to(ground)
     )
     

     def before_cycle(self, event: str, source: State, target: State, message: str = ""):
         message = ". " + message if message else ""
         return f"Running {event} from {source.id} to {target.id}{message}"
     

     # * Methods called automatically when the state machine enters the state they specify
     # * Everytime the state machine enters a state it prints that state to the terminal
     # * If that state needs to get input from the robot a thread is created
     def on_enter_ground(self):
         print("In ground state")
         self.log.append("ground")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["ground"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_starting(self):
         print("Robot is starting.")
         self.log.append("starting")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["starting"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_started(self):
         print("Robot is started.")
         self.log.append("started")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["started"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopping(self):
         print("Robot is stopping.")
         self.log.append("stopping")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["stopping"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopped(self):
         print("Robot is stopped.")
         self.log.append("stopped")
         self.lastNFS = self.current_state
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_pickingChips(self):
         print("Robot is picking chips")
         self.log.append("pickingChips")
         self.lastNFS = self.current_state
         self.chipsInArm = True
         threading.Thread(target=self.check_input, args=["pickingChips"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_chipsPicked(self):
         print("Robot has picked the chips")
         self.log.append("chipsPicked")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["chipsPicked"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_movingChipsToBoard(self):
         print("Robot is moving the chips to the board")
         self.log.append("movingChipsToBoard")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["movingChipsToBoard"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_chipsMovedToBoard(self):
         print("Robot has moved the chips to the board")
         self.log.append("chipsMovedToBoard")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["chipsMovedToBoard"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_placingChips(self):
         print("Robot is placing chips on the tray")
         self.log.append("placingChips")
         self.lastNFS = self.current_state
         threading.Thread(target=self.check_input, args=["placingChips"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_chipsPlaced(self):
         print("Robot has placed the chips on the tray")
         self.log.append("chipsPlaced")
         self.lastNFS = self.current_state
         self.chipsInArm = False
         threading.Thread(target=self.check_input, args=["chipsPlaced"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_poweringOnWIB(self):
         print("The WIB is being powered on")
         self.log.append("poweringOnWIB")
         self.lastNFS = self.current_state

     def on_enter_WIBOn(self):
         print("The WIB has been powered on")
         self.log.append("WIBOn")
         self.lastNFS = self.current_state

     def on_enter_testingChips(self):
         print("The chips are being tested")
         self.log.append("testingChips")
         self.lastNFS = self.current_state

     def on_enter_chipsTested(self):
         print("The chips have been tested")
         self.log.append("chipsTested")
         self.lastNFS = self.current_state

     def on_enter_sendingData(self):
         print("The test data is being sent")
         self.log.append("sendingData")
         self.lastNFS = self.current_state

     def on_enter_dataSent(self):
         print("The testing data has been sent")
         self.log.append("dataSent")
         self.lastNFS = self.current_state

     def on_enter_poweringOffWIB(self):
         print("The WIB is being powered off")
         self.log.append("poweringOffWIB")
         self.lastNFS = self.current_state
         
     def on_enter_WIBOff(self):
         print("The WIB has been powered off")
         self.log.append("WIBOff")
         self.lastNFS = self.current_state

     def on_enter_removingChips(self):
         print("The chips are being removed")
         self.log.append("removingChips")
         self.lastNFS = self.current_state

     def on_enter_chipsRemoved(self):
         print("The chips have been removed")
         self.log.append("chipsRemoved")
         self.lastNFS = self.current_state

     def on_enter_waitingToMoveToTray(self):
         print("Waiting to move chips back to tray")
         self.lastNFS = self.current_state
         self.log.append("waitingToMoveToTray")
         threading.Thread(target=self.check_input, args=["waitingToMoveToTray"]).start()

     def on_enter_movingChipsToTray(self):
         print("Moving chips back to tray")
         self.lastNFS = self.current_state
         self.log.append("movingChipsToTray")
         threading.Thread(target=self.check_input, args=["movingChipsToTray"]).start()

     def on_enter_chipsMovedToTray(self):
         print("Chips have been moved back to tray")
         self.lastNFS = self.current_state
         self.log.append("chipsMovedToTray")
         threading.Thread(target=self.check_input, args=["chipsMovedToTray"]).start()

     def on_enter_placingChipsOnTray(self):
         print("Placing chips back on tray")
         self.lastNFS = self.current_state
         self.log.append("placingChipsOnTray")
         threading.Thread(target=self.check_input, args=["placingChipsOnTray"]).start()

     def on_enter_chipsPlacedOnTray(self):
         print("Chips have been placed back on tray")
         self.lastNFS = self.current_state
         self.log.append("chipsPlacedOnTray")
         threading.Thread(target=self.check_input, args=["chipsPlacedOnTray"]).start()
         self.chipsInArm = False

     def on_enter_curtainTripped(self):
         print("LIGHT CURTAIN HAS BEEN TRIPPED")
         self.log.append("curtainTripped")

     # * Method called automatically when the state machine exits the state it specifies
     def on_exit_curtainTripped(self):
         print("Light curtain has been reset")


     # * Method that reads a file written by the robot and updates the state if needed
     # * Must be passed the state at the time of method call so it can stop once the state is changed
     def check_input(self, state: str):
         
         # * Path name for file being read
         # ! Must be updated for different machines and file names
         path: str = '/Users/volson/Desktop/robotState.txt'
         
         if os.path.isfile(path):
            # Once GUI is closed or state transitions loop stops
            while (self.exists) & (self.current_state.id == state):
                # Reads only the last line of the file and sets the state based on that line
                with open(path, 'rb') as f:
                    try:  # Catch OSError in case of a one line file 
                        f.seek(-2, os.SEEK_END)
                        while f.read(1) != b'\n':
                            f.seek(-2, os.SEEK_CUR)
                    except OSError:
                        f.seek(0)
                    
                    last_line = f.readline().decode()

                    # * Will change the state according to the last line of the file
                    # * Won't run anything that calls cycle if currently cycling due to input from the GUI. Achieved by GUIidle check.
                    # * Won't run if one of these methods is already being run to prevent accidently cycling. Achieved by runningMethodCI check.
                    if (last_line.rstrip() == "stopped") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.stop() 
                    elif (last_line.rstrip() == "starting") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginStarting()
                    elif (last_line.rstrip() == "started") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.start()
                    elif (last_line.rstrip() == "stopping") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.startStopping()
                    elif (last_line.rstrip() == "ground") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.goToGround()
                    elif (last_line.rstrip() == "pickingChips") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginChipMoving()
                    elif (last_line.rstrip() != self.lastNFS.id) & (last_line.rstrip() in self.movingChipStates) & (self.current_state.id in self.movingChipStates) & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.cycleChipMoving()
                    elif (last_line.rstrip() == "poweringOnWIB") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginChipTesting()
                    elif (last_line.rstrip() != self.lastNFS.id) & (last_line.rstrip() in self.resettingStates) & (self.current_state.id in self.resettingStates) & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.cycleResetting()
                    elif (last_line.rstrip() == "curtainTripped") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.tripCurtain()
                    elif (last_line.rstrip() == "curtainReset") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.resetCurtain()
                    elif (last_line.rstrip() == "curtainContinue") & (self.GUIidle) & (not self.runningMethodCI):
                        self.curtainContinue()

                    time.sleep(1)
                    f.close()
         else:
             print("File does not exist")

     # * Next methods are called from within checkInput()
     # * Cycles to the stopping state
     def startStopping(self):
         if self.current_state.id == "started":
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif self.current_state.id == "starting":
             self.log.append("cycle")
             self.cycle()
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Cycles to the stopped state
     def stop(self):
         if self.current_state.id == "started":
             self.log.append("cycle")
             self.cycle()
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")
         elif self.current_state.id == "stopping":
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif self.current_state.id == "starting":
             self.log.append("cycle")
             self.cycle()
             self.log.append("cycle")
             self.cycle()
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled three times from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Cycles to the starting state
     def beginStarting(self):
         if (self.current_state.id == "stopped") | (self.current_state.id == "ground"):
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False
    
     # * Cycles to the started state
     def start(self):
         if (self.current_state.id == "starting"):
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif (self.current_state.id == "ground"):
             self.log.append("cycle")
             self.cycle()
             self.log.append("cycle")
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Goes from chipsPlacedOnTray, the last resetting state, to ground, the first basic state
     def goToGround(self):
         if (self.current_state.id == "chipsPlacedOnTray"):
            self.log.append("reset_cycle")
            self.reset_cycle()

         self.runningMethodCI = False

     # * Switches from started to pickingChips, the first chip moving state
     def beginChipMoving(self):
         if self.current_state.id == "started":
            self.log.append("begin_chip_moving")
            self.begin_chip_moving()
         
         self.runningMethodCI = False

     # * Moves between the chips moving states
     def cycleChipMoving(self):
         self.log.append("chip_cycle")
         self.chip_cycle()
         self.runningMethodCI = False

     # * Switches from chipsPlaced to the poweringOnWIB, the first testing state
     def beginChipTesting(self):
         if self.current_state.id == "chipsPlaced":
             self.log.append("begin_testing")
             self.begin_testing()

     # * Cycles between the reset states
     def cycleResetting(self):
         self.log.append("reset_cycle")
         self.reset_cycle()
         self.runningMethodCI = False

     # * Transitions from any state to curtainTripped
     def tripCurtain(self):
         if(self.current_state.id != "curtainTripped") & (self.current_state.id != "ground"):
             self.log.append("curtain_tripped")
             self.curtain_tripped()
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Transitions from curtainTripped to stopped
     def resetCurtain(self):
         if(self.current_state.id == "curtainTripped"):
             if self.chipsInArm:
                 self.log.append("reset_cycle")
                 self.reset_cycle()
             else:
                 self.log.append("straight_reset")
                 self.straight_reset()
         
         self.runningMethodCI = False

     # * Transtions from curtainTripped to the last non fault state
     def curtainContinue(self):
         if self.current_state.id == "curtainTripped":
            self.current_state = self.lastNFS
            self.on_exit_curtainTripped()
            self.log.append("curtain_continue")
            self.log.append(self.lastNFS.id)
            threading.Thread(target=self.check_input, args=[self.lastNFS.id]).start()
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False