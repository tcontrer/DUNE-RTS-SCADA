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
# curtain_reset: Will transition the state machine from curtainTripped to the stopped state. 

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

class RTSMachine(StateMachine):
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
     movingChipsToTray = State()
     chipsMovedToTray = State()
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
         | chipsPicked.to(movingChipsToTray)
         | movingChipsToTray.to(chipsMovedToTray)
         | chipsMovedToTray.to(placingChips)
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
         | movingChipsToTray.to(curtainTripped)
         | chipsMovedToTray.to(curtainTripped)
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

     # Sends the state machine to the stopped state from the curtain tripped state
     curtain_reset = (
         curtainTripped.to(stopped)
     )
     
     def __init__(self):
         # Tracks if the GUI has been closed
         self.exists: bool = True
         # Tracks if a button on the GUI has been pressed
         self.GUIidle: bool = True
         # Tracks if a method is in progress from check input
         self.runningMethodCI = False
         # Tracks the last non fault state the robot has been in
         self.lastNFS: str
         
         # * Tuples that group states together. Used to have more general checks of state.
         self.basicStates: tuple = ("ground", "starting", "started", "stopping", "stopped")
         self.movingChipStates: tuple = ("pickingChips", "chipsPicked", "movingChipsToTray", "chipsMovedToTray", "placingChips", "chipsPlaced")
         self.testingChipStates: tuple = ("poweringOnWIB", "WIBOn", "testingChips", "chipsTested", "sendingData", "dataSent", "poweringOffWIB", "WIBOff")
         self.cleanupChipStates: tuple = ("removingChips", "chipsRemoved")

         super().__init__()

     def before_cycle(self, event: str, source: State, target: State, message: str = ""):
         message = ". " + message if message else ""
         return f"Running {event} from {source.id} to {target.id}{message}"
     

     # * Methods called automatically when the state machine enters the state they specify
     # * Everytime the state machine enters a state it prints that state to the terminal
     # * If that state needs to get input from the robot a thread is created
     def on_enter_ground(self):
         print("In ground state")
         self.lastNFS = "ground"
         threading.Thread(target=self.check_input, args=["ground"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_starting(self):
         print("Robot is starting.")
         self.lastNFS = "starting"
         threading.Thread(target=self.check_input, args=["starting"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_started(self):
         print("Robot is started.")
         self.lastNFS = "started"
         threading.Thread(target=self.check_input, args=["started"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopping(self):
         print("Robot is stopping.")
         self.lastNFS = "stopping"
         threading.Thread(target=self.check_input, args=["stopping"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopped(self):
         print("Robot is stopped.")
         self.lastNFS = self.current_state.id

     def on_enter_pickingChips(self):
         print("Robot is picking chips")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["pickingChips"]).start()

     def on_enter_chipsPicked(self):
         print("Robot has picked the chips")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["chipsPicked"]).start()

     def on_enter_movingChipsToTray(self):
         print("Robot is moving the chips to the tray")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["movingChipsToTray"]).start()

     def on_enter_chipsMovedToTray(self):
         print("Robot has moved the chips to the tray")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["chipsMovedToTray"]).start()

     def on_enter_placingChips(self):
         print("Robot is placing chips on the tray")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["placingChips"]).start()

     def on_enter_chipsPlaced(self):
         print("Robot has placed the chips on the tray")
         self.lastNFS = self.current_state.id
         threading.Thread(target=self.check_input, args=["chipsPlaced"]).start()

     def on_enter_poweringOnWIB(self):
         print("The WIB is being powered on")
         self.lastNFS = self.current_state.id

     def on_enter_WIBOn(self):
         print("The WIB has been powered on")
         self.lastNFS = self.current_state.id

     def on_enter_testingChips(self):
         print("The chips are being tested")
         self.lastNFS = self.current_state.id

     def on_enter_chipsTested(self):
         print("The chips have been tested")
         self.lastNFS = self.current_state.id

     def on_enter_sendingData(self):
         print("The test data is being sent")
         self.lastNFS = self.current_state.id

     def on_enter_dataSent(self):
         print("The testing data has been sent")
         self.lastNFS = self.current_state.id

     def on_enter_poweringOffWIB(self):
         print("The WIB is being powered off")
         self.lastNFS = self.current_state.id
         
     def on_enter_WIBOff(self):
         print("The WIB has been powered off")
         self.lastNFS = self.current_state.id

     def on_enter_removingChips(self):
         print("The chips are being removed")
         self.lastNFS = self.current_state.id

     def on_enter_chipsRemoved(self):
         print("The chips have been removed")
         self.lastNFS = self.current_state.id

     def on_enter_curtainTripped(self):
         print("LIGHT CURTAIN HAS BEEN TRIPPED")
         threading.Thread(target=self.check_input, args=["curtainTripped"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

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
                    # // USED FOR DEBUGGING print(f"Last line is {last_line}")

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
                    elif (last_line.rstrip() in self.basicStates) & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.basicCycle()
                    elif (last_line.rstrip() == "pickingChips") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginChipMoving()
                    elif (last_line.rstrip() != self.lastNFS) & (last_line.rstrip() in self.movingChipStates) & (self.current_state.id in self.movingChipStates) & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.cycleChipMoving()
                    elif (last_line.rstrip() == "poweringOnWIB") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginChipTesting()
                    elif (last_line.rstrip() == "curtainTripped") & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.tripCurtain()
                    elif (last_line.rstrip() == "curtainReset") & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.resetCurtain()
                    time.sleep(1)
                    f.close()
         else:
             print("File does not exist")

     # * Next methods are called from within checkInput()
     # * Cycles to the stopping state
     def startStopping(self):
         if self.current_state.id == "started":
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif self.current_state.id == "starting":
             self.cycle()
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Cycles to the stopped state
     def stop(self):
         if self.current_state.id == "started":
             self.cycle()
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")
         elif self.current_state.id == "stopping":
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif self.current_state.id == "starting":
             self.cycle()
             self.cycle()
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled three times from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Cycles to the starting state
     def beginStarting(self):
         if (self.current_state.id == "stopped") | (self.current_state.id == "ground"):
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False
    
     # * Cycles to the started state
     def start(self):
         if (self.current_state.id == "starting"):
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif (self.current_state.id == "ground"):
             self.cycle()
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")

         # * Allows check input methods to be run again
         self.runningMethodCI = False

     def beginChipMoving(self):
         if self.current_state.id == "started":
            self.begin_chip_moving()
         
         self.runningMethodCI = False

     def cycleChipMoving(self):
         self.chip_cycle()
         self.runningMethodCI = False

     def beginChipTesting(self):
         if self.current_state.id == "chipsPlaced":
             self.begin_testing()

     # * Transitions from any state to curtainTripped
     def tripCurtain(self):
         if(self.current_state.id != "curtainTripped"):
             self.curtain_tripped()
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False

     # * Transitions from curtainTripped to curtainReset
     def resetCurtain(self):
         if(self.current_state.id == "curtainTripped"):
             self.curtain_reset()
         
         # * Allows check input methods to be run again
         self.runningMethodCI = False