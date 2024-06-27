import RTSStateMachine as RTSSM
import GUI as gui

if __name__ == "__main__":
    sm: RTSSM.RTSMachine = RTSSM.RTSMachine()
    gui.GUI(sm)