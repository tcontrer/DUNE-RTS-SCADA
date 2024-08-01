import time

# * Changes the state to stopped (run by stop button)
def stop_robot(GUI):
     GUI.sm.GUIidle = False
     # // USED FOR DEBUGGING print("GUI active")
     print("Stop button clicked")
     GUI.sm.log.append("to_stopping")
     GUI.sm.to_stopping()
     time.sleep(.5)
     GUI.sm.cycle()
      # // USED FOR DEBUGGING print("Cycled twice from stop button")
     GUI.sm.GUIidle = True
     print("GUI idle")

# Changes all the labels of the chip tray window and the corrosponding tracking lists back to their inital values
def resetChipTrayWindow(GUI):
       GUI.chipStatuses = []
       for i in range (40):
              GUI.chipStatusesLog[i] = None
              GUI.chipTrayLabels[i].config(text=f"Chip {i + 1}", bg="lightgray")



# * toBlank button methods
# Changes state from ground to starting
def starting(GUI):
     GUI.sm.GUIidle = False
     if(GUI.sm.current_state.id == "ground") | (GUI.sm.current_state.id == "stopped"):
          GUI.cycle()
     GUI.sm.GUIidle = True

# Changes state from starting to started
def started(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "starting"):
               GUI.cycle()
          GUI.sm.GUIidle = True
     
# Changes state from either started or chipsPlaced to pickingChips
def pickingChips(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "started"):
               GUI.sm.log.append("begin_chip_moving")
               GUI.sm.begin_chip_moving()
          elif(GUI.sm.current_state.id == "chipsPlaced"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from pickingChips to chipsPicked
def chipsPicked(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "pickingChips"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from chipsPicked to movingChipsToBoard
def movingChipsToBoard(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsPicked"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from movingChipsToBoard to chipsMovedToBoard
def chipsMovedToBoard(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "movingChipsToBoard"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from chipsMovedToBoard to placingChips
def placingChips(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsMovedToBoard"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from placingChips to chipsPlaced
def chipsPlaced(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "placingChips"):
               GUI.sm.log.append("chip_cycle")
               GUI.sm.chip_cycle()
          GUI.sm.GUIidle = True

# Changes state from chipsPlaced to poweringOnWIB
def poweringOnWIB(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsPlaced"):
               GUI.sm.log.append("begin_testing")
               GUI.sm.begin_testing()
          GUI.sm.GUIidle = True

# Changes state from poweringOnWIB to WIBOn
def WIBOn(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "poweringOnWIB"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from either WIBOn or resultsReviewed to testingChips
def testingChips(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "WIBOn"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          elif(GUI.sm.current_state.id == "resultsReviewed"):
               GUI.sm.log.append("retest")
               GUI.sm.retest()
          GUI.sm.GUIidle = True

# Changes state from testingChips to chipsTested
def chipsTested(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "testingChips"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from chipsTested to reviewingResults
def reviewingResults(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsTested"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True
     
# Changes state from reviewingResults to resultsReviewed
def resultsReviewed(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "reviewingResults"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from resultsReviewed to sendingData
def sendingData(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "resultsReviewed"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from sendingData to dataSent
def dataSent(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "sendingData"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from dataSent to poweringOffWIB
def poweringOffWIB(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "dataSent"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from poweringOffWIB to WIBOff
def WIBOff(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "poweringOffWIB"):
               GUI.sm.log.append("test_cycle")
               GUI.sm.test_cycle()
          GUI.sm.GUIidle = True

# Changes state from WIBOff to removingChips
def removingChips(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "WIBOff"):
               GUI.sm.log.append("begin_cleanup")
               GUI.sm.begin_cleanup()
          GUI.sm.GUIidle = True

# Changes state from removingChips to chipsRemoved
def chipsRemoved(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "removingChips"):
               GUI.sm.log.append("cleanup_cycle")
               GUI.sm.cleanup_cycle()
          GUI.sm.GUIidle = True

# Changes state from either chipsRemoved or chipsPlacedOnTray(completes reset after curtain trip) to ground
def ground(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsRemoved"):
               GUI.sm.log.append("done")
               GUI.sm.done()
          elif(GUI.sm.current_state.id == "chipsPlacedOnTray"):
               GUI.sm.log.append("reset_cycle")
               GUI.sm.reset_cycle()
          GUI.sm.GUIidle = True

# Changes state from waitingToMoveToTray to movingChipsToTray
def movingChipsToTray(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "waitingToMoveToTray"):
               GUI.sm.log.append("reset_cycle")
               GUI.sm.reset_cycle()
          GUI.sm.GUIidle = True

# Changes state from movingChipsToTray to chipsMovedToTray
def chipsMovedToTray(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "movingChipsToTray"):
               GUI.sm.log.append("reset_cycle")
               GUI.sm.reset_cycle()
          GUI.sm.GUIidle = True

# Changes state from chipsMovedToTray to placingChipsOnTray
def placingChipsOnTray(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "chipsMovedToTray"):
               GUI.sm.log.append("reset_cycle")
               GUI.sm.reset_cycle()
          GUI.sm.GUIidle = True

# Changes state from placingChipsOnTray to chipsPlacedOnTray
def chipsPlacedOnTray(GUI):
          GUI.sm.GUIidle = False
          if(GUI.sm.current_state.id == "placingChipsOnTray"):
               GUI.sm.log.append("reset_cycle")
               GUI.sm.reset_cycle()
          GUI.sm.GUIidle = True

# Will exit a curtain trip by continuing to the last non fault state
def ctn(GUI):
          GUI.sm.GUIidle = False
          GUI.sm.curtainContinue()
          GUI.sm.GUIidle = True

# Will exit a curtain trip by resetting and going back to the ground states
def reset(GUI):
          GUI.sm.GUIidle = False
          GUI.sm.resetCurtain()
          GUI.sm.GUIidle = True