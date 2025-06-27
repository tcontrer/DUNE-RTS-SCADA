import RTSStateMachine as RTSSM

if __name__ == "__main__":
    sm = RTSSM.RTSStateMachine()
    sm.cycle()
    sm.pause_cycle()