from statemachine import StateMachine, State
import time
import threading
import os

# * A state machine to manage the movement of the RTS arm in correspondence with input from the robot

# * Transitions:
# * cycle: Will transition the state machine to the next normal (non error) state. Ground to starting, starting to started, etc.
# * curtain_tripped: Will transition the state machine from any state to the curtainTripped state.
# * curtain_reset: Will transition the state machine from curtainTripped to the stopped state. 

# * Methods:
# * on_enter_NAMEOFSTATE: Automatically called when NAMEOFSTATE is entered
# * checkInput: Checks the last line of a file every second and responds based on what that line is. The file is written 
# * from within the RTS software. Provides a connection between the RTS and the state machine.
class RTSMachine(StateMachine):
     # The states the system can be in
     ground = State(initial=True)
     starting = State()
     started = State()
     stopping = State() 
     stopped = State()
     curtainTripped = State()
     
     # Transitions the robot between non error states
     cycle = (
         ground.to(starting)
         | starting.to(started)
         | started.to(stopping)
         | stopping.to(stopped)
         | stopped.to(starting)
     )

     # Sends the robot right to the curtain tripped state
     curtain_tripped = (
         ground.to(curtainTripped)
         | starting.to(curtainTripped)
         | started.to(curtainTripped)
         | stopping.to(curtainTripped)
         | stopped.to(curtainTripped)
     )

     # Sends the robot to the stopped state from the curtain tripped state
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
         super().__init__()

     def before_cycle(self, event: str, source: State, target: State, message: str = ""):
         message = ". " + message if message else ""
         return f"Running {event} from {source.id} to {target.id}{message}"
     

     # * Methods called automatically when the robot enters the state they specify
     # * Everytime the robot enters a state it prints that state to the terminal
     # * If that state needs to get input from the robot a thread is created
     def on_enter_ground(self):
         time.sleep(.5)
         print("In ground state")
         threading.Thread(target=self.check_input, args=["ground"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_starting(self):
         print("Robot is starting.")
         threading.Thread(target=self.check_input, args=["starting"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")
     
     def on_enter_started(self):
         print("Robot is started.")
         threading.Thread(target=self.check_input, args=["started"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopping(self):
         print("Robot is stopping.")
         threading.Thread(target=self.check_input, args=["stopping"]).start()
         # // USED FOR DEBUGGING print("Thread checking input")

     def on_enter_stopped(self):
         print("Robot is stopped.")

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
                    if (last_line == "Stopped") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.stop() 
                    elif (last_line == "Starting") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.beginStarting()
                    elif (last_line == "Started") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.start()
                    elif (last_line == "Stopping") & (self.GUIidle) & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.startStopping()
                    elif (last_line == "CurtainTripped") & (not self.runningMethodCI):
                        self.runningMethodCI = True
                        self.tripCurtain()
                    elif (last_line == "CurtainReset") & (not self.runningMethodCI):
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