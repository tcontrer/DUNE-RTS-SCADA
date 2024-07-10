from statemachine import StateMachine, State
import time
import threading
import os

# * A state machine to manage the movement of the RTS arm in correspondence with input from the robot
class RTSMachine(StateMachine):
     # The states the system can be in
     ground = State(initial=True)
     starting = State()
     started = State()
     stopping = State() 
     stopped = State()
     
     # Transitions the robot between states
     cycle = (
         ground.to(starting)
         | starting.to(started)
         | started.to(stopping)
         | stopping.to(stopped)
         | stopped.to(starting)
     )
     
     def __init__(self):
         # Tracks if the GUI has been closed
         self.exists: bool = True
         # Tracks if a button on the GUI has been pressed
         self.GUIidle: bool = True
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
     
     def on_enter_starting(self):
         print("Robot is starting.")
         threading.Thread(target=self.check_input, args=["starting"]).start()
     
     def on_enter_started(self):
         print("Robot is started.")
         threading.Thread(target=self.check_input, args=["started"]).start()

     def on_enter_stopping(self):
         print("Robot is stopping.")
         threading.Thread(target=self.check_input, args=["stopping"]).start()

     def on_enter_stopped(self):
         print("Robot is stopped.")


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
                    # * Won't run if currently cycling due to input from the GUI
                    if (last_line == "Stopped") & (self.GUIidle):
                        self.stop() 
                    elif (last_line == "Starting") & (self.GUIidle):
                        self.beginStarting()
                    elif (last_line == "Started") & (self.GUIidle):
                        self.start()
                    elif (last_line == "Stopping") & (self.GUIidle):
                        self.startStopping()
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

     # * Cycles to the starting state
     def beginStarting(self):
         if (self.current_state.id == "stopped") | (self.current_state.id == "ground"):
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
    
     # * Cycles to the started state
     def start(self):
         if (self.current_state.id == "starting"):
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled once from file")
         elif (self.current_state.id == "ground"):
             self.cycle()
             self.cycle()
             # // USED FOR DEBUGGING print("Cycled twice from file")