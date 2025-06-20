from statemachine import StateMachine, State


class RTSStateMachine(StateMachine):
    """RTS State Machine for managing robotic test system operations."""

    # ==================== STATES ====================
    
    # Normal Operation States
    ground = State("Ground", initial=True)
    surveying_sockets = State("Surveying Sockets")
    moving_chip_to_socket = State("Moving Chip to Socket")
    testing = State("Testing")
    writing_to_hwdb = State("Writing to HWDB")
    moving_chip_to_tray = State("Moving Chip to Tray")
    reset = State("Reset")

    # Control States
    pause = State("Pause")  # State entered when system encounters an error or manual pause is triggered

    # ==================== ERROR STATES ====================

    # Ground State Errors
    no_server_connection = State("No Server Connection")

    # Socket Surveying Errors
    chip_in_socket = State("Chip in Socket")
    vision_sequence_failed = State("Vision Sequence Failed")  # Also applies to chip movement operations

    # Chip Movement Errors (applies to both socket and tray operations)
    no_pressure = State("No Pressure")
    lost_vacuum = State("Lost Vacuum")
    bad_contact = State("Bad Contact")
    no_chip = State("No Chip")
    safe_guard = State("Safe Guard")
    bad_pins = State("Bad Pins")
    no_serial_number = State("No Serial Number")

    # Testing Errors
    failed_init = State("Failed Initialization")
    no_wib_connection = State("No WIB Connection")
    
    # Database Errors
    failed_upload = State("Failed Upload")

    # ==================== TRANSITIONS ====================

    # Normal Operation Transitions
    # Defines the allowed state transitions during normal operation and recovery from pause
    cycle = (
        ground.to(surveying_sockets)
        | surveying_sockets.to(moving_chip_to_socket)
        | moving_chip_to_socket.to(testing)
        | testing.to(writing_to_hwdb)
        | writing_to_hwdb.to(moving_chip_to_tray)
        | moving_chip_to_tray.to(ground)
        | pause.to(ground)
        | pause.to(testing)
        | pause.to(moving_chip_to_tray)
        | pause.to(moving_chip_to_socket)
    )

    # Pause Transitions
    # Allows pausing from any operational state
    pause_cycle = (
        ground.to(pause)
        | surveying_sockets.to(pause)
        | moving_chip_to_socket.to(pause)
        | testing.to(pause)
        | writing_to_hwdb.to(pause)
        | moving_chip_to_tray.to(pause)
    )

    # Error Transitions
    # Handles fault conditions from operational states to appropriate error states
    error_transitions = (
        # Ground state errors
        ground.to(no_server_connection)
        # Socket surveying errors
        | surveying_sockets.to(chip_in_socket)
        | surveying_sockets.to(vision_sequence_failed)
        # Chip movement to socket errors
        | moving_chip_to_socket.to(no_pressure)
        | moving_chip_to_socket.to(lost_vacuum)
        | moving_chip_to_socket.to(bad_contact)
        | moving_chip_to_socket.to(no_chip)
        | moving_chip_to_socket.to(vision_sequence_failed)
        | moving_chip_to_socket.to(safe_guard)
        | moving_chip_to_socket.to(bad_pins)
        | moving_chip_to_socket.to(no_serial_number)
        # Testing errors
        | testing.to(failed_init)
        | testing.to(no_wib_connection)
        # Database errors
        | writing_to_hwdb.to(failed_upload)
        # Chip movement to tray errors
        | moving_chip_to_tray.to(no_pressure)
        | moving_chip_to_tray.to(lost_vacuum)
        | moving_chip_to_tray.to(bad_contact)
        | moving_chip_to_tray.to(no_chip)
        | moving_chip_to_tray.to(vision_sequence_failed)
        | moving_chip_to_tray.to(safe_guard)
    )

    # ==================== STATE CALLBACKS ====================
    
    def on_enter_ground(self):
        """Called when entering the ground state - system ready for next operation."""
        print("Entering ground state - system ready")
    
    def on_exit_ground(self):
        """Called when leaving ground state."""
        print("Leaving ground state")
    
    def on_enter_surveying_sockets(self):
        """Called when entering socket surveying state."""
        print("Starting socket survey")
    
    def on_exit_surveying_sockets(self):
        """Called when leaving socket surveying state."""
        print("Socket survey complete")
    
    def on_enter_moving_chip_to_socket(self):
        """Called when entering chip movement to socket state."""
        print("Moving chip to test socket")
    
    def on_exit_moving_chip_to_socket(self):
        """Called when chip movement to socket is complete."""
        print("Chip placement complete")
    
    def on_enter_testing(self):
        """Called when entering testing state."""
        print("Starting WIB testing")
    
    def on_exit_testing(self):
        """Called when testing is complete."""
        print("Testing complete")
    
    def on_enter_writing_to_hwdb(self):
        """Called when entering database writing state."""
        print("Writing test results to hardware database")
    
    def on_exit_writing_to_hwdb(self):
        """Called when database writing is complete."""
        print("Database write complete")
    
    def on_enter_moving_chip_to_tray(self):
        """Called when entering chip movement to output tray state."""
        print("Moving chip to output tray")
    
    def on_exit_moving_chip_to_tray(self):
        """Called when chip movement to tray is complete."""
        print("Chip moved to tray successfully")
    
    def on_enter_pause(self):
        """Called when entering pause state."""
        print("System paused - awaiting resume command")
    
    def on_exit_pause(self):
        """Called when leaving pause state."""
        print("Resuming system operation")
