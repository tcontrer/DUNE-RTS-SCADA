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
    
    # Test advanced pause/resume (precise state restoration)
    sm.before_pause_cycle()  # Store current state
    sm.pause_cycle()  # Pause
    print(f"After pause: {sm.current_state}")
    
    # Resume to exact previous state
    sm.resume_to_previous()
    print(f"After precise resume: {sm.current_state}")
    
    # Test error handling with contextual recovery
    print("\n--- Testing Contextual Error Recovery ---")
    sm.error_cycle()
    print(f"After error: {sm.current_state}")
    
    # Test recovery from error
    sm.error_cycle()
    print(f"After recovery: {sm.current_state}")
    
    print("Basic test complete")