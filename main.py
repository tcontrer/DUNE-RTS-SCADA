import RTSStateMachine as RTSSM

if __name__ == "__main__":
    sm = RTSSM.RTSStateMachine()
    print(f"Initial state: {sm.current_state}")

    # Test with BypassRTS True (simulation)
    sm.BypassRTS = True
    print("\n[TEST] BypassRTS = True (Simulation Mode)")
    sm.cycle()  # Surveying Sockets
    sm.cycle()  # Moving Chip to Socket
    sm.cycle()  # Testing
    sm.cycle()  # Writing to HWDB
    sm.cycle()  # Moving Chip to Tray (should print simulation message)
    sm.cycle()  # Back to Ground

    # Test with BypassRTS False (real hardware call)
    sm.BypassRTS = False
    print("\n[TEST] BypassRTS = False (Real Hardware Mode)")
    sm.cycle()  # Surveying Sockets
    sm.cycle()  # Moving Chip to Socket
    sm.cycle()  # Testing
    sm.cycle()  # Writing to HWDB
    sm.cycle()  # Moving Chip to Tray (should attempt real function)
    sm.cycle()  # Back to Ground