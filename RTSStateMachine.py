from statemachine import StateMachine, State


class RTSStateMachine(StateMachine):
    """RTS State Machine for managing robotic test system operations."""
    
    def __init__(self):
        super().__init__()
        self._previous_state = None

    # ==================== STATES ====================
    
    # Normal Operation States
    ground = State("Ground", initial=True)
    surveying_sockets = State("Surveying Sockets")
    moving_chip_to_socket = State("Moving Chip to Socket")
    testing = State("Testing")
    writing_to_hwdb = State("Writing to HWDB")
    moving_chip_to_tray = State("Moving Chip to Tray")
    reseat = State("Reseat")
    moving_chip_to_bad_tray = State("Moving Chip to Bad Tray")

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
        | moving_chip_to_bad_tray.to(ground)
        | pause.to(ground)
        | pause.to(surveying_sockets)
        | pause.to(moving_chip_to_socket)
        | pause.to(testing)
        | pause.to(writing_to_hwdb)
        | pause.to(moving_chip_to_tray)
        | pause.to(moving_chip_to_bad_tray)
        | pause.to(surveying_sockets)  # Resume from pause to re-survey
        | reseat.to(ground)
    )

    # Pause Transitions
    # Allows pausing from any operational state and error states
    pause_cycle = (
        ground.to(pause)
        | surveying_sockets.to(pause)
        | moving_chip_to_socket.to(pause)
        | testing.to(pause)
        | writing_to_hwdb.to(pause)
        | moving_chip_to_tray.to(pause)
        | moving_chip_to_bad_tray.to(pause)
        | reseat.to(pause)
        # Error states can pause for manual intervention
        | no_server_connection.to(pause)
        | chip_in_socket.to(pause)
        | vision_sequence_failed.to(pause)
        | no_pressure.to(pause)
        | lost_vacuum.to(pause)
        | bad_contact.to(pause)
        | no_chip.to(pause)
        | safe_guard.to(pause)
        | bad_pins.to(pause)
        | no_serial_number.to(pause)
        | failed_init.to(pause)
        | no_wib_connection.to(pause)
        | failed_upload.to(pause)
    )

    # Error Transitions
    # Handles fault conditions from operational states to appropriate error states
    error_cycle = (
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
        | failed_init.to(reseat)
        | reseat.to(ground)
        # Database errors
        | writing_to_hwdb.to(failed_upload)
        # Chip movement to tray errors
        | moving_chip_to_tray.to(no_pressure)
        | moving_chip_to_tray.to(lost_vacuum)
        | moving_chip_to_tray.to(bad_contact)
        | moving_chip_to_tray.to(no_chip)
        | moving_chip_to_tray.to(vision_sequence_failed)
        | moving_chip_to_tray.to(safe_guard)
        | moving_chip_to_bad_tray.to(moving_chip_to_socket)
        # Smart error recovery paths
        | bad_pins.to(moving_chip_to_bad_tray)
        | no_serial_number.to(moving_chip_to_bad_tray)
        | failed_upload.to(moving_chip_to_tray)
        # Contextual error recovery paths
        | chip_in_socket.to(surveying_sockets)  # Re-survey to find empty socket
        | vision_sequence_failed.to(surveying_sockets)  # Vision failed, start over
        | no_pressure.to(ground)  # Pressure issue, return to ground
        | lost_vacuum.to(ground)  # Vacuum issue, return to ground  
        | bad_contact.to(moving_chip_to_socket)  # Bad contact, retry chip movement
        | no_chip.to(surveying_sockets)  # No chip found, re-survey
        | safe_guard.to(ground)  # Safety triggered, return to safe ground state
        | no_wib_connection.to(testing)  # WIB connection issue, retry testing
        | no_server_connection.to(ground)  # Server issue, stay at ground
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

    def on_enter_reseat(self):
        """Called when entering reseat state."""
        print("System reseat initiated - repositioning components")
    
    def on_exit_reseat(self):
        """Called when leaving reseat state."""
        print("Reseat complete - system ready for operation")

    def on_enter_moving_chip_to_bad_tray(self):
        """Called when entering bad tray movement state."""
        print("Moving defective chip to bad tray")
    
    def on_exit_moving_chip_to_bad_tray(self):
        """Called when bad tray movement is complete."""
        print("Chip moved to bad tray - ready for next operation")

    # ==================== ERROR STATE CALLBACKS ====================
    
    def on_enter_no_server_connection(self):
        """Called when server connection is lost."""
        print("❌ ERROR: No server connection detected")
    
    def on_enter_chip_in_socket(self):
        """Called when socket is already occupied."""
        print("❌ ERROR: Chip already in socket")
    
    def on_enter_vision_sequence_failed(self):
        """Called when vision system fails."""
        print("❌ ERROR: Vision sequence failed")
    
    def on_enter_no_pressure(self):
        """Called when pressure is lost."""
        print("❌ ERROR: No pressure detected")
    
    def on_enter_lost_vacuum(self):
        """Called when vacuum is lost."""
        print("❌ ERROR: Vacuum system failure")
    
    def on_enter_bad_contact(self):
        """Called when electrical contact is poor."""
        print("❌ ERROR: Bad electrical contact")
    
    def on_enter_no_chip(self):
        """Called when expected chip is not found."""
        print("❌ ERROR: No chip detected")
    
    def on_enter_safe_guard(self):
        """Called when safety system is triggered."""
        print("❌ ERROR: Safety guard triggered")
    
    def on_enter_bad_pins(self):
        """Called when pin issues are detected."""
        print("❌ ERROR: Bad pins detected - routing to bad tray")
    
    def on_enter_no_serial_number(self):
        """Called when chip identification fails."""
        print("❌ ERROR: No serial number - routing to bad tray")
    
    def on_enter_failed_init(self):
        """Called when test initialization fails."""
        print("❌ ERROR: Test initialization failed - system reseat required")
    
    def on_enter_no_wib_connection(self):
        """Called when WIB connection fails."""
        print("❌ ERROR: No WIB connection")
    
    def on_enter_failed_upload(self):
        """Called when database upload fails."""
        print("❌ ERROR: Failed to upload to database - retrying")

    # ==================== ADVANCED PAUSE/RESUME METHODS ====================
    
    def before_pause_cycle(self):
        """Store the current state before pausing for precise resume."""
        self._previous_state = self.current_state
        print(f"Storing current state: {self.current_state}")
    
    def resume_to_previous(self):
        """Resume to the exact state we were in before the pause."""
        if self._previous_state and self.current_state == self.pause:
            # Manually set state back to previous (bypasses transition validation)
            self.current_state = self._previous_state
            print(f"Resumed to previous state: {self.current_state}")
            self._previous_state = None  # Clear stored state
        else:
            print("No previous state to resume to or not currently paused")
