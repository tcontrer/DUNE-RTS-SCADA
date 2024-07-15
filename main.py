import RTSStateMachine as RTSSM
import GUI as gui

if __name__ == "__main__":
     sm: RTSSM.RTSMachine = RTSSM.RTSMachine()
     g = gui.GUI(sm)
     print(sm.log)