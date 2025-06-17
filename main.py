import RTSStateMachine as RTSSM

if __name__ == "__main__":
    # Create an instance of the RTSStateMachine
    sm: RTSSM.RTSStateMachine = RTSSM.RTSStateMachine()

    # Test basic transitions
    print(f"Current state: {sm.current_state}")
    sm.cycle()  # Should move to surveying_sockets
    print(f"After cycle: {sm.current_state}")