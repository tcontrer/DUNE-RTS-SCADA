import tkinter as tk
from tkinter import messagebox
import RTSStateMachine as RTSSM
import time

class GUI:
    def __init__(self, sm: RTSSM.RTSMachine) -> None:
        self.sm: RTSSM.RTSMachine = sm
        
        # Creating window
        self.root: tk.Tk = tk.Tk()
        self.root.geometry("500x200")
        self.root.title("Robot State Machine")

        # Adding label to display state
        self.label: tk.Label = tk.Label(self.root, text="Current State: " + sm.current_state.id, font=('Arial', 20))
        self.label.pack(padx=10, pady=10)

        # Button to update the state to stopped (can only be pressed if moving)
        self.stopbtn: tk.Button = tk.Button(self.root, bg="#FF0000", text="Stop", font=('Arial', 18), command=self.stop_robot)
        self.stopbtn.pack(padx=10, pady=10)

        self.startbtn: tk.Button = tk.Button(self.root, text="Start", font=('Arial', 18))

        self.root.mainloop()

    def stop_robot(self):
         if(self.sm.current_state.id == "moving"):
              self.cycle()
              time.sleep(1)
              self.cycle()
         else:
              messagebox.showerror(message="The robot is already stopping or stopped.")
    
    def update_label(self):
            self.label.config(text="Current State: " + self.sm.current_state.id)

    def cycle(self):
         self.sm.cycle()
         self.update_label()

