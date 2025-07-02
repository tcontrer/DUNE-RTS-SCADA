import RTSStateMachine as RTSSM

if __name__ == "__main__":
    sm = RTSSM.RTSStateMachine() # ground
    # sm.cycle()                   # surveying socket
    # sm.cycle()                   # moving to socket
    # sm.cycle()                   # testing
    # sm.pause_cycle()             # pause
    # sm.cycle()                   # (1) ground (2) testing (3) writing to HWDB (4) quit
    # sm.pause_cycle()
    # sm.cycle()

    # sm.handle_tray()

    sm.cycle()