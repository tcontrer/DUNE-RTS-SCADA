import tkinter as tk
from tkinter import messagebox

import RTSStateMachine as RTSSM
import time
import threading

import buttonMethods
import UpdateTestDisplay


# * Creates a user interface that displays the current state and has buttons to start and stop the robot
# * Must be passed a RTS state machine

# * GUI Elements:
# label: Text that displays the state or type of state
# frame: Holds the buttons on the main window
     # * Buttons (Methods run are in the buttonMethods.py file):
     # stopbtn: Button that changes the state to stopped
     # ctnbtn: Button that is shown when the curtain is tripped. Sends the state machine back to the last non fault state
     # resetbtn: Button that is shown when the curtain is tripped. Sends the state machine into the waitingToMoveToTray state.
     # The toBlank buttons: Buttons that step the state machine to the state in the name. Only present when in a state that directly transitions
     # to the state in the button name.
# * DAT Toplevel: Seperate window to display the state of the chips on the DAT board
     # chipSlot_NUMBER_: Frames that create boarders around chip_NUMBER_labels. Represent a chip slot on the actual DAT board.
     # chip_NUMBER_label: Labels that describe what chip slot the frame represents.
     # testsCompleteLabel: Label that is visible when in the chipsTested state to indicate that the tests have been completed
# * ChipTrayWindow Toplevel: Seperate window to display the results of testing for each chip (pass vs fail)
     # chipTrayLabels: List that tracks each of the fourty labels on the chip tray window.

# * Methods:
# __init__: Creates the GUI in its inital state with start and stop button and label to display current state.
# Runs check state in seperate thread to consitantly update the GUI
# checkState: Runs every second until the GUI is closed. Calls update_label, update_buttons, and update_background
# createDATWindow: Creates a new window that contains representatons of eight chip slots.
# createChipTrayWindow: Creates a new window that contains representations of fourty chips.
# on_closing: Runs when the GUI is closed. Properly destroys the window.
# closeDATWindow: Runs when DAT window is closed. Properly destroys the window.
# closeChipTrayWindow: Runs when chip tray window is closed. Properly destroys the window.
# update_label: Changes the color and text of the label to match the current state
# update_buttons: Disables the buttons in states where they shouldn't be pressed and resets them when they can be pressed
# update_background: Changes the background to orange when in an fault state and resets it when not. Creates a popup
# when the curtain is tripped.
# cycle: Cycles the state machine and updates the label

# * Variables:
# sm: Assigned to the state machine passed into the GUI. Used to access and transition state.
# flag: Boolean that tracks if the GUI has been closed.
# DATCreated: Boolean that tracks if the DAT window has been created. Used to know if widgets on the DAT can be updated.
# chipTrayCreated: Boolean that tracks if the chip tray display window is open.
# count: Keeps track of the number of messageboxes pulled up. Prevents a new messagebox being created every second that the 
# curtain is tripped.
# chipLabels: List to hold all the labels on the DAT Display Window. Represent chip slots on the actual DAT board.
# chipTrayLabels: List to hold all the labels on the chip tray display window. Represent the fourty chips that fit on the chip tray.
# chipSlotsPlaced: List that tracks which of the chips in the eight chip slots have been tested. Used to track which slots on
# chipStatuses: List that tracks which of the chip labels on the chip tray display window need to be updated.
# chipStatusesLog: List that logs the state of all the labels on the chip tray display window.
# the DAT display should be green.
# toBlankBtns: Tuple of all the toBlank buttons.

class GUI:
     def __init__(self, sm: RTSSM.RTSMachine) -> None:       
          # GUI's link to the state machine
          self.sm: RTSSM.RTSMachine = sm
          # Tracks if the GUI has been closed
          self.flag = True
          # Tracks if the DAT window has been created
          self.DATCreated = False
          # Tracks if the Chip Tray display window has been created
          self.chipTrayCreated = False
          # Tracks the number of messageboxes
          self.count: int = 0

          # Placeholder for chipLabels lists that will be created with DAT window
          self.chipLabels: list = []

          # Placeholder for the labels on the chip tray display window
          self.chipTrayLabels: list = []

          self.chipSlotsPlaced: list = [False, False, False, False, False, False, False, False]

          # Variable used to track what labels on the chip tray window currently need to be updated
          self.chipStatuses: list = []
          # Variable used to save the values of chip tray labels
          self.chipStatusesLog: list = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

          self.testsCompleteLabel: tk.Label

          # Creating window
          self.root: tk.Tk = tk.Tk()
          self.root.geometry("500x400")
          self.root.title("Robot State Machine")
          self.root.config(bg="#99D6EA") 

          self.showDAT: tk.Button = tk.Button(self.root, text="Show DAT Status", font=('Helvetica', 18), command=self.createDATWindow)
          self.showDAT.pack(padx=10, pady=10)

          self.showChipTray: tk.Button = tk.Button(self.root, text="Show Chip Tray Status", font=('Helvetica', 18), command=self.createChipTrayWindow)
          self.showChipTray.pack(padx=10, pady=10)

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

          # * Button to stop the robot
          # * Calls the stop_robot() method
          self.stopbtn: tk.Button = tk.Button(self.frame, bg="red", text="Stop", font=('Helvetica', 18), command=lambda: buttonMethods.stop_robot(self))
          self.stopbtn.pack(pady=10)

          self.ctnbtn: tk.Button = tk.Button(self.root, bg="grey", text="Continue", font=('Helvetica', 18), command=lambda: buttonMethods.ctn(self))
          self.ctnbtn.pack(pady=10)

          self.resetbtn: tk.Button = tk.Button(self.root, bg="grey", text="Reset", font=('Helvetica', 18), command=lambda: buttonMethods.reset(self))
          self.resetbtn.pack(pady=10)

          self.ctnbtn.pack_forget()
          self.resetbtn.pack_forget()

          # * toBlank buttons
          # * Transition the state machine to the next non fault state
          self.toStarting: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Starting", font=('Helvetica', 18), command=lambda: buttonMethods.starting(self))
          
          self.toStarted: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Started", font=('Helvetica', 18), command=lambda: buttonMethods.started(self))
          
          self.toPickingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Picking Chips", font=('Helvetica', 18), command=lambda: buttonMethods.pickingChips(self))

          self.toChipsPicked: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Picked", font=('Helvetica', 18), command=lambda: buttonMethods.chipsPicked(self))

          self.toMovingChipsToBoard: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Moving Chips To Board", font=('Helvetica', 18), command=lambda: buttonMethods.movingChipsToBoard(self))

          self.toChipsMovedToBoard: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Moved To Board", font=('Helvetica', 18), command=lambda: buttonMethods.chipsMovedToBoard(self))

          self.toPlacingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Placing Chips", font=('Helvetica', 18), command=lambda: buttonMethods.placingChips(self))

          self.toChipsPlaced: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Placed", font=('Helvetica', 18), command=lambda: buttonMethods.chipsPlaced(self))

          self.toPoweringOnWIB: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Powering On WIB", font=('Helvetica', 18), command=lambda: buttonMethods.poweringOnWIB(self))

          self.toWIBOn: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To WIB On", font=('Helvetica', 18), command=lambda: buttonMethods.WIBOn(self))

          self.toTestingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Testing Chips", font=('Helvetica', 18), command=lambda: buttonMethods.testingChips(self))

          self.toChipsTested: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Tested", font=('Helvetica', 18), command=lambda: buttonMethods.chipsTested(self))

          self.toReviewingResults: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Reviewing Results", font=('Helvetica', 18), command=lambda: buttonMethods.reviewingResults(self))

          self.toResultsReviewed: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Results Reviewed", font=('Helvetica', 18), command=lambda: buttonMethods.resultsReviewed(self))

          self.toSendingData: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Sending Data", font=('Helvetica', 18), command=lambda: buttonMethods.sendingData(self))

          self.toDataSent: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Data Sent", font=('Helvetica', 18), command=lambda: buttonMethods.dataSent(self))

          self.toPoweringOffWIB: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Powering Off WIB", font=('Helvetica', 18), command=lambda: buttonMethods.poweringOffWIB(self))
          
          self.toWIBOff: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To WIB Off", font=('Helvetica', 18), command=lambda: buttonMethods.WIBOff(self))

          self.toRemovingChips: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Removing Chips", font=('Helvetica', 18), command=lambda: buttonMethods.removingChips(self))

          self.toChipsRemoved: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Removed", font=('Helvetica', 18), command=lambda: buttonMethods.chipsRemoved(self))

          self.toGround: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Ground", font=('Helvetica', 18), command=lambda: buttonMethods.ground(self))

          self.toMovingChipsToTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Moving Chips To Tray", font=('Helvetica', 18), command=lambda: buttonMethods.movingChipsToTray(self))

          self.toChipsMovedToTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Moved To Tray", font=('Helvetica', 18), command=lambda: buttonMethods.chipsMovedToTray(self))

          self.toPlacingChipsOnTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Placing Chips On Tray", font=('Helvetica', 18), command=lambda: buttonMethods.placingChipsOnTray(self))

          self.toChipsPlacedOnTray: tk.Button = tk.Button(self.frame, bg="#4C8C2B", text="To Chips Placed On Tray", font=('Helvetica', 18), command=lambda: buttonMethods.chipsPlacedOnTray(self))

          self.toBlankBtns: tuple = (self.toStarting, self.toStarted, self.toPickingChips, self.toChipsPicked, self.toMovingChipsToBoard, self.toChipsMovedToBoard, self.toPlacingChips, self.toChipsPlaced, self.toPoweringOnWIB, self.toWIBOn, self.toTestingChips, self.toChipsTested, self.toSendingData, self.toDataSent, self.toPoweringOffWIB, self.toWIBOff, self.toRemovingChips, self.toChipsRemoved, self.toGround, self.toMovingChipsToTray, self.toChipsMovedToTray, self.toPlacingChipsOnTray, self.toChipsPlacedOnTray)

          # Uncomment the below line of code to have a DAT Window created on startup
          # // self.createDATWindow()

          # Uncomment the below line of code to have a Chip Tray Window created on startup
          # // self.createChipTrayWindow()

          # Create a new thread where the gui will constantly check the state
          t1 = threading.Thread(target=self.check_state)
          t1.start()

          # When the window is closed the method on closing will run
          self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

          # Creating the window
          self.root.mainloop()

     # * Checks the state and updates the label, buttons, background, and DAT window accordingly every second
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
                    UpdateTestDisplay.readDAT(self)
                    if self.DATCreated:
                         UpdateTestDisplay.updateDATDisplay(self)
                         if self.sm.chipTestNeedsReset:
                              UpdateTestDisplay.resetChipTests(self)
                    UpdateTestDisplay.readChipTray(self)
                    if self.chipTrayCreated:
                         # // USED FOR DEBUGGING print(self.chipStatuses)
                         UpdateTestDisplay.updateChipTrayDisplay(self)


     # * Creates a second window to display DAT test states
     def createDATWindow(self):
          self.DAT = tk.Toplevel()
          self.DATCreated: bool = True
          self.DAT.title("DAT Status Display")

          self.showDAT["state"] = "disabled"
          
          self.chipOneLabel = tk.Label(self.DAT, text="Chip Slot One", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipOneLabel.grid(row=0, column=0, padx=10, pady=10)

          self.chipTwoLabel = tk.Label(self.DAT, text="Chip Slot Two", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipTwoLabel.grid(row=0, column=1, padx=10, pady=10)

          self.chipThreeLabel = tk.Label(self.DAT, text="Chip Slot Three", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipThreeLabel.grid(row=0, column=2, padx=10, pady=10)

          self.chipFourLabel = tk.Label(self.DAT, text="Chip Slot Four", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipFourLabel.grid(row=0, column=3, padx=10, pady=10)

          self.chipFiveLabel = tk.Label(self.DAT, text="Chip Slot Five", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipFiveLabel.grid(row=1, column=0, padx=10, pady=10)

          self.chipSixLabel = tk.Label(self.DAT, text="Chip Slot Six", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipSixLabel.grid(row=1, column=1, padx=10, pady=10)

          self.chipSevenLabel = tk.Label(self.DAT, text="Chip Slot Seven", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipSevenLabel.grid(row=1, column=2, padx=10, pady=10)

          self.chipEightLabel = tk.Label(self.DAT, text="Chip Slot Eight", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
          self.chipEightLabel.grid(row=1, column=3, padx=10, pady=10)

          self.chipLabels = [self.chipOneLabel, self.chipTwoLabel, self.chipThreeLabel, self.chipFourLabel, self.chipFiveLabel, self.chipSixLabel, self.chipSevenLabel, self.chipEightLabel]

          self.testsCompleteLabel = tk.Label(self.DAT, text="Tests Complete", font=('Helvetica', 18))

          self.DAT.protocol("WM_DELETE_WINDOW", self.closeDATWindow)

     # * Creates window with 40 labels that each represent a chip and updates the labels to match the chipStatusesLog
     def createChipTrayWindow(self):
          # Creating window
          self.ChipTrayWindow: tk.Toplevel = tk.Toplevel()
          self.chipTrayCreated = True

          self.showChipTray["state"] = "disabled"

          self.ChipTrayWindow.title("Chip Tray Display")

          for r in range(5):
               for c in range(8):
                    chipTrayLabel: tk.Label = tk.Label(self.ChipTrayWindow, text=f"Chip {((r + 1) * 8) - (8 - c)  + 1}", font=('Helvetica', 18), bg="lightgray", borderwidth=2, relief="solid")
                    chipTrayLabel.grid(row=r, column=c, padx=10, pady=10)

                    self.chipTrayLabels.append(chipTrayLabel)

          # Updating labels
          count = 0
          for chipStatus in self.chipStatusesLog:
               if chipStatus != None:
                    if chipStatus[8:] == "passed":
                         self.chipTrayLabels[count].config(text="Passed", bg="green")
                         # // USED FOR DEBUGGING print(f"Changing label from log: Chip {count} passed")
                    if chipStatus[8:] == "failed":
                         self.chipTrayLabels[count].config(text="Failed", bg="red")
                         # // USED FOR DEBUGGING print(f"Changing label from log: Chip {count} failed")
                    
               count += 1

          # Creating reset button
          self.resetChipTrayWindow: tk.Button = tk.Button(self.ChipTrayWindow, text="Reset", font=('Helvetica', 18), command=lambda: buttonMethods.resetChipTrayWindow(self))
          self.resetChipTrayWindow.grid(row=5, column=4)
            

          self.ChipTrayWindow.protocol("WM_DELETE_WINDOW", self.closeChipTrayWindow)
     
     # Run from both reset button and when reset is the last line of the file
     def resetChipTrayWindowMethod(self):
       self.chipStatuses = []
       for i in range (40):
           self.chipStatusesLog[i] = None
           if self.chipTrayCreated:
               self.chipTrayLabels[i].config(text=f"Chip {i + 1}", bg="lightgray")
                    

     # * When window is closed destroies the GUI
     def on_closing(self):
          print("Closing")
          self.flag = False
          self.root.destroy()
          self.sm.exists = False

     # * When DAT window is closed it is properly destroyed
     def closeDATWindow(self):
          self.DATCreated = False
          self.DAT.destroy()
          
          self.showDAT["state"] = "normal"

     # * When chip tray window is closed it is properly destroyed
     def closeChipTrayWindow(self):
          self.chipTrayCreated = False
          self.ChipTrayWindow.destroy()
          self.chipTrayLabels = []

          self.showChipTray["state"] = "normal"

     # * Cyles the state machine and updates the label
     def cycle(self):
          self.sm.log.append("cycle") 
          self.sm.cycle()
          self.update_label()

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

     def update_background(self):
          # * Sets the background to orange if in a fault state and resets it if not
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

          # * Updates the background of the DAT window to be yellow when testing and gray when not testing.
          if(self.sm.testing) & (self.DATCreated):
               self.DAT.config(bg="#fff2cc")
          elif (self.DATCreated):
               self.DAT.config(bg="lightgray")

     # * Changes the state, color, and visibility of buttons based on the state of the state machine
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
               self.toPickingChips.pack(pady=10)

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
               self.toTestingChips.pack(pady=10)

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

               for button in self.toBlankBtns:
                    button.pack_forget()

               self.toStarting.pack()
          elif (self.sm.current_state.id == "stopping"):

               self.stopbtn["state"] = "disabled"
               self.stopbtn.config(bg="#FAF9F6")
               
               for button in self.toBlankBtns:
                    button.pack_forget()

               self.ctnbtn.pack_forget()
               self.resetbtn.pack_forget()