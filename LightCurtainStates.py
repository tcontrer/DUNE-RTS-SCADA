# Uses python-statemachine library
from statemachine import StateMachine, State

class RTSMachine(StateMachine):
    # A state machine to manage the movement of the RTS arm in correspondence with input from the light curtain
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

     def on_enter_stopped(self):
         print("Robot is stopped.")

     def on_enter_moving(self):
         print("Robot is moving.")

     def on_enter_stopping(self):
         print("Robot is stopping.")

sm = RTSMachine()
print("The state is currently " + sm.current_state.id)

flag = True

while flag:
    sto = input("To stop robot type 'stop' (type 'q' to break). ")

    if (sto == "stop"):
        sm.send("cycle")
        sm.send("cycle")
    elif (sto == "q"):
        flag = False
        break

    sta = input("Once the area is clear type 'start' to start the robot again (type 'q' to break). ")

    if (sta == "start"):
        sm.cycle()
    elif (sta == "q"):
        flag = False
        break