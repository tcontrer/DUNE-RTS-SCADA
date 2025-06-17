from statemachine import StateMachine, State

class RTSStateMachine(StateMachine):
    "RTS State Machine"

    # States
    
    ground = State("Ground", initial=True)
    surveying_sockets = State("Surveying Sockets")
    moving_chip_to_socket = State("Moving Chip to Socket")
    testing = State("Testing")
    writing_to_hwdb = State("Writing to HWDB")
    moving_chip_to_tray = State("Moving Chip to Tray")

    # Fault States

    # State entered when system encounters an error or manual pause is triggered
    pause = State("Pause")

    # Transitions between states during normal operation and recovery from pause
    # Defines the allowed state transitions in the system:
    #   Normal operation flow:
    #   - From ground state to socket surveying
    #   - From surveying to moving chip to test socket
    #   - From moving to socket to testing
    #   - From testing to writing results
    #   - From writing results to moving chip to output tray
    #   - From output tray back to ground to start next cycle
    #
    #   Recovery from pause state:
    #   - Resume testing from pause
    #   - Resume moving to output tray from pause
    #   - Resume moving to test socket from pause
    cycle = (
        ground.to(surveying_sockets)
        | surveying_sockets.to(moving_chip_to_socket)
        | moving_chip_to_socket.to(testing)
        | testing.to(writing_to_hwdb)
        | writing_to_hwdb.to(moving_chip_to_tray)
        | moving_chip_to_tray.to(ground)
        | pause.to(testing)
        | pause.to(moving_chip_to_tray)
        | pause.to(moving_chip_to_socket)
    )

    # Pause Transitions
    # Defines transitions from any operational state to the pause state
    # This allows the system to be paused at any point during operation:
    #   - From initial ground state
    #   - During socket surveying
    #   - While moving chip to test socket
    #   - During chip testing
    #   - While writing results to database
    #   - During movement to output tray
    pause_cycle = (
        ground.to(pause)
        | surveying_sockets.to(pause)
        | moving_chip_to_socket.to(pause)
        | testing.to(pause)
        | writing_to_hwdb.to(pause)
        | moving_chip_to_tray.to(pause)
    )

    # Transition Methods - State Entry/Exit Callbacks
    
    def on_enter_ground(self):
        """Called when entering the ground state - system ready for next operation"""
        print("Entering ground state - system ready")
        # TODO: Initialize system for next chip cycle
        pass
    
    def on_exit_ground(self):
        """Called when leaving ground state"""
        print("Leaving ground state")
        pass
    
    def on_enter_surveying_sockets(self):
        """Called when entering socket surveying state"""
        print("Starting socket survey")
        # TODO: Begin socket identification and availability check
        pass
    
    def on_exit_surveying_sockets(self):
        """Called when leaving socket surveying state"""
        print("Socket survey complete")
        pass
    
    def on_enter_moving_chip_to_socket(self):
        """Called when entering chip movement to socket state"""
        print("Moving chip to test socket")
        # TODO: Command robot arm to place chip in identified socket
        pass
    
    def on_exit_moving_chip_to_socket(self):
        """Called when chip movement to socket is complete"""
        print("Chip placement complete")
        pass
    
    def on_enter_testing(self):
        """Called when entering testing state"""
        print("Starting WIB testing")
        # TODO: Initialize and run WIB test procedures
        pass
    
    def on_exit_testing(self):
        """Called when testing is complete"""
        print("Testing complete")
        # TODO: Process test results and determine pass/fail
        pass
    
    def on_enter_writing_to_hwdb(self):
        """Called when entering database writing state"""
        print("Writing test results to hardware database")
        # TODO: Store test results and chip data to database
        pass
    
    def on_exit_writing_to_hwdb(self):
        """Called when database writing is complete"""
        print("Database write complete")
        pass
    
    def on_enter_moving_chip_to_tray(self):
        """Called when entering chip movement to output tray state"""
        print("Moving chip to output tray")
        # TODO: Command robot arm to place chip in output tray
        pass
    
    def on_exit_moving_chip_to_tray(self):
        """Called when chip movement to tray is complete"""
        print("Chip moved to tray successfully")
        pass
    
    def on_enter_pause(self):
        """Called when entering pause state"""
        print("System paused - awaiting resume command")
        # TODO: Stop all active operations safely
        pass
    
    def on_exit_pause(self):
        """Called when leaving pause state"""
        print("Resuming system operation")
        # TODO: Resume operations from paused state
        pass