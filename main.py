import RTSStateMachine as RTSSM

if __name__ == "__main__":
    # Create state machine instance
    sm = RTSSM.RTSStateMachine()
    
    # Show initial state
    print(f"Initial state: {sm.current_state}")
    
    # Test a few basic transitions
    sm.cycle()
    print(f"After 1st cycle: {sm.current_state}")
    
    sm.cycle()
    print(f"After 2nd cycle: {sm.current_state}")
    
    sm.cycle()
    print(f"After 3rd cycle: {sm.current_state}")
    
    # Test pause
    sm.pause_cycle()
    print(f"After pause: {sm.current_state}")
    
    # Resume
    sm.cycle()
    print(f"After resume: {sm.current_state}")
    
    # Test error handling
    sm.error_cycle()
    print(f"After error: {sm.current_state}")
    
    # Test recovery (if available)
    # sm.cycle()
    # print(f"After recovery: {sm.current_state}")