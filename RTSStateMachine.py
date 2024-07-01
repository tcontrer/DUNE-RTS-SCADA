from statemachine import StateMachine, State
import time
import threading

'''A state machine to manage the movement of the RTS arm in correspondence with input from the robot'''
class RTSMachine(StateMachine):
     moving = State(initial=True)
     stopping = State() 
     stopped = State()

     cycle = (
         moving.to(stopping)
         | stopping.to(stopped)
         | stopped.to(moving)
     )

     def __init__(self):
         super().__init__()
         
         # Creates thread to update the state from the state machine side
         threading.Thread(target=self.test_input).start()
         

     async def before_cycle(self, event: str, source: State, target: State, message: str = ""):
         message = ". " + message if message else ""
         return f"Running {event} from {source.id} to {target.id}{message}"

     def on_enter_moving(self):
         print("Robot is moving.")

     def on_enter_stopping(self):
         print("Robot is stopping.")

     def on_enter_stopped(self):
         print("Robot is stopped.")

     # Cycles the robot from the state machine side
     def test_input(self):
         time.sleep(10)
         self.cycle()
         time.sleep(1)
         self.cycle()
         print("Test input cycled")