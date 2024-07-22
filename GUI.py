import tkinter as tk
from tkinter import messagebox

import RTSStateMachine as RTSSM
import time
import threading


# * Creates a user interface that displays the current state and has buttons to start and stop the robot
# * Must be passed a RTS state machine

# * GUI Elements:
# label: Text that displays the state or type of state
# frame: Holds the buttons
# startbtn: Button that changes the state to started
# stopbtn: Button that changes the state to stopped
# ctnbtn: Button that is shown when the curtain is tripped. Sends the state machine back to the last non fault state
# resetbtn: Button that is shown when the curtain is tripped. Sends the state machine into the waitingToMoveToTray state.

# * Methods:
# __init__: Creates the GUI in its inital state with start and stop button and label to display current state.
# Runs check state in seperate thread to consitantly update the GUI
# checkState: Runs every second until the GUI is closed. Calls update_label, update_buttons, and update_background
# on_closing: Runs when the GUI is closed. Properly destroys the window.
# start_robot: Cycles through to the starting then the started state
# stop_robot: Cycles through to the stopping then the stopped state
# update_label: Changes the color and text of the label to match the current state
# update_buttons: Disables the buttons in states where they shouldn't be pressed and resets them when they can be pressed
# update_background: Changes the background to orange when in an fault state and resets it when not. Creates a popup
# when the curtain is tripped.
# cycle: Cycles the state machine and updates the label

# * Variables:
# sm: Assigned to the state machine passed into the class. Used to access and transition state.
# flag: Boolean that tracks if the GUI has been closed

class GUI:
     def __init__(self, sm: RTSSM.RTSMachine) -> None:       
          self.sm: RTSSM.RTSMachine = sm
          self.flag = True
          self.count: int = 0

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

          # * Button to stop the robot (can only be pressed if started)
          # * Calls the stop_robot() method
          self.stopbtn: tk.Button = tk.Button(self.frame, bg="red", text="Stop", font=('Helvetica', 18), command=self.stop_robot)
          self.stopbtn.pack(pady=10)

          # * toBlank buttons
          # * Transition the state machine to the next non fault state
          self.toStarting: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Starting", font=('Helvetica', 18), command=self.starting)
          
          self.toStarted: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Started", font=('Helvetica', 18), command=self.started)
          
          self.toPickingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Picking Chips", font=('Helvetica', 18), command=self.pickingChips)

          self.toChipsPicked: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Picked", font=('Helvetica', 18), command=self.chipsPicked)

          self.toMovingChipsToBoard: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Moving Chips To Board", font=('Helvetica', 18), command=self.movingChipsToBoard)

          self.toChipsMovedToBoard: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Moved To Board", font=('Helvetica', 18), command=self.chipsMovedToBoard)

          self.toPlacingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Placing Chips", font=('Helvetica', 18), command=self.placingChips)

          self.toChipsPlaced: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Placed", font=('Helvetica', 18), command=self.chipsPlaced)

          self.toPoweringOnWIB: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Powering On WIB", font=('Helvetica', 18), command=self.poweringOnWIB)

          self.toWIBOn: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To WIB On", font=('Helvetica', 18), command=self.WIBOn)

          self.toTestingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Testing Chips", font=('Helvetica', 18), command=self.testingChips)

          self.toChipsTested: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Tested", font=('Helvetica', 18), command=self.chipsTested)

          self.toReviewingResults: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Reviewing Results", font=('Helvetica', 18), command=self.reviewingResults)

          self.toResultsReviewed: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Results Reviewed", font=('Helvetica', 18), command=self.resultsReviewed)

          self.toSendingData: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Sending Data", font=('Helvetica', 18), command=self.sendingData)

          self.toDataSent: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Data Sent", font=('Helvetica', 18), command=self.dataSent)

          self.toPoweringOffWIB: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Powering Off WIB", font=('Helvetica', 18), command=self.poweringOffWIB)
          
          self.toWIBOff: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To WIB Off", font=('Helvetica', 18), command=self.WIBOff)

          self.toRemovingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Removing Chips", font=('Helvetica', 18), command=self.removingChips)

          self.toChipsRemoved: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Removed", font=('Helvetica', 18), command=self.chipsRemoved)

          self.toGround: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Ground", font=('Helvetica', 18), command=self.ground)

          self.toMovingChipsToTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Moving Chips To Tray", font=('Helvetica', 18), command=self.resetCycle)

          self.toChipsMovedToTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Moved To Tray", font=('Helvetica', 18), command=self.resetCycle)

          self.toPlacingChipsOnTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Placing Chips On Tray", font=('Helvetica', 18), command=self.resetCycle)

          self.toChipsPlacedOnTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Placed On Tray", font=('Helvetica', 18), command=self.resetCycle)

          self.toBlankBtns: tuple = (self.toStarting, self.toStarted, self.toPickingChips, self.toChipsPicked, self.toMovingChipsToBoard, self.toChipsMovedToBoard, self.toPlacingChips, self.toChipsPlaced, self.toPoweringOnWIB, self.toWIBOn, self.toTestingChips, self.toChipsTested, self.toSendingData, self.toDataSent, self.toPoweringOffWIB, self.toWIBOff, self.toRemovingChips, self.toChipsRemoved, self.toGround)

          self.ctnbtn: tk.Button = tk.Button(self.root, bg="grey", text="Continue", font=('Helvetica', 18), command=self.ctn)
          self.ctnbtn.pack(pady=10)

          self.resetbtn: tk.Button = tk.Button(self.root, bg="grey", text="Reset", font=('Helvetica', 18), command=self.reset)
          self.resetbtn.pack(pady=10)

          self.ctnbtn.pack_forget()
          self.resetbtn.pack_forget()

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
    
    # * Changes label text and color to correspond to the current state
     def update_label(self):
          if (self.sm.current_state.id == "starting") | (self.sm.current_state.id == "started") | (self.sm.current_state.id == "ground"):
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
          elif (self.sm.current_state.id in self.sm.movingChipStates) | (self.sm.current_state.id in self.sm.testingChipStates) | (self.sm.current_state.id in self.sm.cleanupChipStates):
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#4C8C2B")
               self.root.update()
          elif self.sm.current_state.id in self.sm.resettingStates:
               self.label.config(text="Current State: " + self.sm.current_state.id, fg="#CB6015")
               self.root.update()

     # * Changes the state, color, and visibility of buttons based on the state of the state machine to prevent them from being pressed at the wrong times
     def update_buttons(self):
          if(self.sm.current_state.id == "curtainTripped"):
               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")

               for button in self.toBlankBtns:
                    button.pack_forget()
                    
               self.ctnbtn.pack()
               self.resetbtn.pack()

          elif(self.sm.current_state.id == "ground"):
               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")

               self.toGround.pack_forget()
               self.toStarting.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "starting"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toStarting.pack_forget()
               self.toStarted.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "started"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toStarted.pack_forget()
               self.toPickingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "pickingChips"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toPoweringOnWIB.pack_forget()
               self.toPickingChips.pack_forget()
               self.toChipsPicked.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsPicked"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsPicked.pack_forget()
               self.toMovingChipsToBoard.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "movingChipsToBoard"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toMovingChipsToBoard.pack_forget()
               self.toChipsMovedToBoard.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsMovedToBoard"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsMovedToBoard.pack_forget()
               self.toPlacingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "placingChips"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toPlacingChips.pack_forget()
               self.toChipsPlaced.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsPlaced"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsPlaced.pack_forget()
               self.toPoweringOnWIB.pack()
               self.toPickingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "poweringOnWIB"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toPoweringOnWIB.pack_forget()
               self.toPickingChips.pack_forget()
               self.toWIBOn.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "WIBOn"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toWIBOn.pack_forget()
               self.toTestingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "testingChips"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toTestingChips.pack_forget()
               self.toSendingData.pack_forget()
               self.toChipsTested.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsTested"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsTested.pack_forget()
               self.toReviewingResults.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "reviewingResults"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toReviewingResults.pack_forget()
               self.toResultsReviewed.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "resultsReviewed"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toResultsReviewed.pack_forget()
               self.toSendingData.pack()
               self.toTestingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "sendingData"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toSendingData.pack_forget()
               self.toTestingChips.pack_forget()
               self.toDataSent.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "dataSent"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toDataSent.pack_forget()
               self.toPoweringOffWIB.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "poweringOffWIB"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toPoweringOffWIB.pack_forget()
               self.toWIBOff.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "WIBOff"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toWIBOff.pack_forget()
               self.toRemovingChips.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "removingChips"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toRemovingChips.pack_forget()
               self.toChipsRemoved.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsRemoved"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsRemoved.pack_forget()
               self.toGround.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "waitingToMoveToTray"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()

               self.toMovingChipsToTray.pack()
          elif(self.sm.current_state.id == "movingChipsToTray"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toMovingChipsToTray.pack_forget()
               self.toChipsMovedToTray.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsMovedToTray"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsMovedToTray.pack_forget()
               self.toPlacingChipsOnTray.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "placingChipsOnTray"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toPlacingChipsOnTray.pack_forget()
               self.toChipsPlacedOnTray.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif(self.sm.current_state.id == "chipsPlacedOnTray"):
               self.stopbtn["state"] = "normal"
               self.stopbtn.config(bg="red")

               self.toChipsPlacedOnTray.pack_forget()
               self.toGround.pack()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif (self.sm.current_state.id == "stopped"):

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")
               
               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()
          elif (self.sm.current_state.id == "stopping"):

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")
               
               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()

     # * Sets the background to orange if in a fault state and resets it if not
     def update_background(self):
          if(self.sm.current_state.id == "curtainTripped"):
               self.root.config(bg="#CB6015")
               self.frame.config(bg="#FAF9F6")
               self.label.config(bg="#FAF9F6")
               self.root.update()
               if self.count < 1:
                    messagebox.showerror(message="Light Curtain Tripped", detail="The area around the robot must be cleared. Then you can reset it by pressing the small red square button on the control pannel. Then press OK.")
                    self.count += 1
          else:
               self.root.config(bg="#99D6EA")
               self.frame.config(bg="lightblue")
               self.label.config(bg="lightblue")
               self.count = 0

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

     def starting(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "ground"):
               self.cycle()
          self.sm.GUIidle = True

     def started(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "starting"):
               self.cycle()
          self.sm.GUIidle = True
     
     def pickingChips(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "started"):
               self.sm.begin_chip_moving()
          elif(self.sm.current_state.id == "chipsPlaced"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def chipsPicked(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "pickingChips"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def movingChipsToBoard(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "chipsPicked"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def chipsMovedToBoard(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "movingChipsToBoard"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def placingChips(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "chipsMovedToBoard"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def chipsPlaced(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "placingChips"):
               self.sm.chip_cycle()
          self.sm.GUIidle = True

     def poweringOnWIB(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "chipsPlaced"):
               self.sm.begin_testing()
          self.sm.GUIidle = True

     def WIBOn(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "poweringOnWIB"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def testingChips(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "WIBOn"):
               self.sm.test_cycle()
          elif(self.sm.current_state.id == "resultsReviewed"):
               self.sm.retest()
          self.sm.GUIidle = True

     def chipsTested(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "testingChips"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def reviewingResults(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "chipsTested"):
               self.sm.test_cycle()
          self.sm.GUIidle = True
     
     def resultsReviewed(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "reviewingResults"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def sendingData(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "resultsReviewed"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def dataSent(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "sendingData"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def poweringOffWIB(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "dataSent"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def WIBOff(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "poweringOffWIB"):
               self.sm.test_cycle()
          self.sm.GUIidle = True

     def removingChips(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "WIBOff"):
               self.sm.begin_cleanup()
          self.sm.GUIidle = True

     def chipsRemoved(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "removingChips"):
               self.sm.cleanup_cycle()
          self.sm.GUIidle = True

     def ground(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id == "chipsRemoved"):
               self.sm.done()
          elif(self.sm.current_state.id == "chipsPlacedOnTray"):
               self.sm.reset_cycle()
          self.sm.GUIidle = True

     def resetCycle(self):
          self.sm.GUIidle = False
          if(self.sm.current_state.id in self.sm.resettingStates):
               self.sm.reset_cycle()
          self.sm.GUIidle = True

     def ctn(self):
          self.sm.GUIidle = False
          self.sm.curtainContinue()
          self.sm.GUIidle = True

     def reset(self):
          self.sm.GUIidle = False
          self.sm.resetCurtain()
          self.sm.GUIidle = True

     # * Cyles the state machine and updates the label
     def cycle(self):
          self.sm.log.append("cycle") 
          self.sm.cycle()
          self.update_label()