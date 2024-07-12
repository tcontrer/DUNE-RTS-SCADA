import tkinter as tk
from tkinter import messagebox

import RTSStateMachine as RTSSM
import time
import threading


# * Creates a user interface that displays the current state and has buttons to start and stop the robot
# * Must be passed a RTS state machine

# * Methods:
# __init__: Creates the GUI in its inital state with start and stop button and label to display current state.
# Runs check state in seperate thread to consitantly update the GUI
# checkState: Runs every second until the GUI is closed. Calls update_label, update_buttons, and update_background
# on_closing: Runs when the GUI is closed. Properly destroys the window.
# start_robot: Cycles through to the starting then the started state
# stop_robot: Cycles through to the stopping then the stopped state
# update_label: Changes the color and text of the label to match the current state
# update_buttons: Disables the buttons in states where they shouldn't be pressed and resets them when they can be pressed
# update_background: Changes the background to orange when in an fault state and resets it when not
# curtain_tripped_message: Called within update_background. Creates a pop up explaing that the curtain has been tripped.
# cycle: Cycles the state machine and updates the label

# * Variables:
# sm: Assigned to the state machine passed into the class. Used to access and transition state.
# flag: Boolean that tracks if the GUI has been closed

class GUI:
     def __init__(self, sm: RTSSM.RTSMachine) -> None:       
          self.sm: RTSSM.RTSMachine = sm
          self.flag = True

          # Creating window
          self.root: tk.Tk = tk.Tk()
          self.root.geometry("500x200")
          self.root.title("Robot State Machine")
          self.root.config(bg="#99D6EA") 

          # Adding label to display state
          if (self.sm.current_state.id == "starting") | (self.sm.current_state.id == "started") | (self.sm.current_state.id == "ground"):
               self.label: tk.Label = tk.Label(self.root, text="Current State: " + self.sm.current_state.id, font=('Helvetica', 24), fg="#4C8C2B", bg="lightblue")
               self.label.pack()
          else: 
               self.label: tk.Label = tk.Label(self.root, text="Current State: " + self.sm.current_state.id, font=('Helvetica', 24), fg="#000000", bg="lightblue")
               self.label.pack(padx=10, pady=10)

          # A frame to hold the buttons
          self.frame = tk.Frame(self.root, bg="lightblue")
          self.frame.pack()

          # * A button to start the robot (can't be pressed if stopping)
          # * Calls the start_robot() method
          self.startbtn: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="Start", font=('Helvetica', 18), command=self.start_robot)
          self.startbtn.grid(row=0, column=0, padx=10, pady=10)

          # * Button to stop the robot (can only be pressed if started)
          # * Calls the stop_robot() method
          self.stopbtn: tk.Button = tk.Button(self.frame, bg="#8A2A2B", text="Stop", font=('Helvetica', 18), command=self.stop_robot)
          self.stopbtn.grid(row=0, column=1, padx=10, pady=10)

          # Create a new thread where the gui will constantly check the state
          t1 = threading.Thread(target=self.check_state)
          t1.start()

          # When the window is closed the method on closing will run
          self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

          # Creating the window
          self.root.mainloop()

     # * Checks the state and updates the label accordingly every second
     def check_state(self):
          while self.flag:
               time.sleep(1)
               if self.flag == False:
                    break
               else:
                    print(self.sm.current_state.id)
                    self.update_label()
                    self.update_buttons()
                    self.update_background()
                    

     # * When window is closed destroies the GUI
     def on_closing(self):
          print("Closing")
          self.flag = False
          self.root.destroy()
          self.sm.exists = False

     # * Changes the state to started unless the robot is stopping (run by start button)
     def start_robot(self):
          self.sm.GUIidle = False
          # // USED FOR DEBUGGING print("GUI active")
          print("Start button clicked")
          if(self.sm.current_state.id == "stopped") | (self.sm.current_state.id == "ground"):
              self.cycle()
              time.sleep(1)
              self.cycle()
              # // USED FOR DEBUGGING print("Cycled twice from start button")
          elif(self.sm.current_state.id == "starting"):
               self.cycle()
               # // USED FOR DEBUGGING print("Cycled once from start button")
          elif(self.sm.current_state.id == "stopping"):
              messagebox.showerror(message="The robot can't be started because it is stopping.")

          self.sm.GUIidle = True
          # // USED FOR DEBUGGING print("GUI idle")

     # * Changes the state to stopped when currently started (run by stop button)
     def stop_robot(self):
          self.sm.GUIidle = False
          # // USED FOR DEBUGGING print("GUI active")
          print("Stop button clicked")
          if(self.sm.current_state.id == "started"):
              self.cycle()
              time.sleep(1)
              self.cycle()
              # // USED FOR DEBUGGING print("Cycled twice from stop button")
          else:
              messagebox.showerror(message="The can't be stopped because it isn't in the started state.")
          self.sm.GUIidle = True
          print("GUI idle")
    
    # * Changes label text and color to correspond to the current state
     def update_label(self):
          if (self.sm.current_state.id == "starting") | (self.sm.current_state.id == "started"):
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#4C8C2B")
               self.root.update()
          elif self.sm.current_state.id == "stopping":
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#CB6015")
               self.root.update()
          elif self.sm.current_state.id == "stopped":
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#8A2A2B")
               self.root.update()
          elif self.sm.current_state.id == "curtainTripped":
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#8A2A2B")
               self.root.update()
          elif self.sm.current_state.id in self.sm.movingChipStates:
               self.label.config(text="Moving Chips", fg="#4C8C2B")
               self.root.update()
          elif self.sm.current_state.id in self.sm.testingChipStates:
               self.label.config(text="Testing Chips", fg="#4C8C2B")
               self.root.update()
          else:
               self.stopbtn: tk.Button = tk.Button(self.frame, bg="#FF0000", text="Stop", font=('Arial', 18), command=self.stop_robot)
               self.stopbtn.grid(row=0, column=1, padx=10, pady=10)

     # * Changes the state and color of the buttons based on the state of the state machine to prevent them from being pressed at the wrong times
     def update_buttons(self):
          if(self.sm.current_state.id == "ground"):
               self.startbtn["state"] = "normal"
               self.startbtn.config(bg="#4C8C2B")

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")

          if(self.sm.current_state.id == "starting") | (self.sm.current_state.id == "started")  | (self.sm.current_state.id in self.sm.movingChipStates) | (self.sm.current_state.id in self.sm.testingChipStates):
               self.startbtn["state"] = "disabled"
               self.startbtn.config(bg="#FAF9F6")

               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="#8A2A2B")

          if (self.sm.current_state.id == "stopped"):
               self.startbtn["state"] = "normal"
               self.startbtn.config(bg="#4C8C2B")

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")

          if (self.sm.current_state.id == "stopping") | (self.sm.current_state.id == "curtainTripped"):
               self.startbtn["state"] = "disabled"
               self.startbtn.config(bg="#FAF9F6")

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")

     # * Sets the background to orange if in a fault state and resets it if not
     def update_background(self):
          if(self.sm.current_state.id == "curtainTripped"):
               self.root.config(bg="#CB6015")
               self.frame.config(bg="#FAF9F6")
               self.label.config(bg="#FAF9F6")
               threading.Thread(target=self.curtain_tripped_message).start()
          if(self.sm.current_state.id == "stopped"):
               self.root.config(bg="#99D6EA")
               self.frame.config(bg="lightblue")
               self.label.config(bg="lightblue")

     # * Creates a pop up with an error message when the light curtain is tripped
     def curtain_tripped_message(self):
          messagebox.showerror(message="Light Curtain Tripped", detail="The area around the robot must be cleared. Then you can reset it by pressing the small red square button on the control pannel.")

     # * Cyles the state machine and updates the label
     def cycle(self):
          self.sm.cycle()
          self.update_label()