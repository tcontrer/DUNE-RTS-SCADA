from statemachine import StateMachine, State
#from GUI import update_label

'''A state machine to manage the movement of the RTS arm in correspondence with input from the light curtain'''
class RTSMachine(StateMachine):
     moving = State(initial=True)
     stopping = State() 
     stopped = State()

     cycle = (
         moving.to(stopping)
         | stopping.to(stopped)
         | stopped.to(moving)
     )

     async def before_cycle(self, event: str, source: State, target: State, message: str = ""):
         message = ". " + message if message else ""
         return f"Running {event} from {source.id} to {target.id}{message}"

     def on_enter_moving(self):
         print("Robot is moving.")

     def on_enter_stopping(self):
         print("Robot is stopping.")

     def on_enter_stopped(self):
         print("Robot is stopped.")

#if __name__ == "__main__":
     #sm: RTSMachine = RTSMachine()
     #gui.GUI(sm)