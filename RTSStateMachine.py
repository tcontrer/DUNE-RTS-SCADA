from statemachine import StateMachine, State
from FNAL_RTS_integration import MoveChipsToSockets
from RTS_CFG import RTS_CFG
import sys
import os
from datetime import datetime
import time

class RTSStateMachine(StateMachine):

    def __init__(self):
        super().__init__()

        self.BypassRTS = True  # Set to False to use real hardware functions
        self.last_normal_state = None

        # Replace individual position tracking with dictionary-based approach
        self.chip_positions = {
            'tray': [],
            'col': [],
            'row': [],
            'dat': [],
            'dat_socket': [],
            'label': []
        }
        
        # Initialize with 40 chip positions (10 columns × 4 rows)
        self.max_col = 10
        self.max_row = 4
        self.current_chip_index = 0
        
        # Populate the chip_positions dictionary for a full tray
        self.populate_full_tray()
        
        # Initialize RTS connection
        # self.rts = RTS_CFG()
        # self.rts.rts_init(port=201, host_ip='192.168.121.1')

    def populate_full_tray(self):
        """Populate chip_positions for a full tray (10 columns × 4 rows)."""
        # Clear existing lists
        for key in self.chip_positions:
            self.chip_positions[key] = []
        chip_counter = 0
        for col in range(1, self.max_col + 1):
            for row in range(1, self.max_row + 1):
                self.chip_positions['col'].append(col)
                self.chip_positions['row'].append(row)
                self.chip_positions['tray'].append(2)
                self.chip_positions['dat'].append(2)
                if chip_counter % 2 == 0:
                    self.chip_positions['dat_socket'].append(21)
                    self.chip_positions['label'].append('CD0')
                else:
                    self.chip_positions['dat_socket'].append(22)
                    self.chip_positions['label'].append('CD1')
                chip_counter += 1

    def populate_from_dicts(self, chip_list):
        """
        Populate chip_positions from a list of chip dictionaries.

        Args:
            chip_list (list of dict): Each dict should have keys matching chip_positions fields
                (e.g., 'tray', 'col', 'row', 'dat', 'dat_socket', 'label').
                Missing keys default to None.

        Example:
            chip_list = [
                {'tray': 2, 'col': 1, 'row': 1, 'dat': 2, 'dat_socket': 21, 'label': 'CD0'},
                {'tray': 2, 'col': 1, 'row': 2, 'dat': 2, 'dat_socket': 22, 'label': 'CD1'}
            ]
        """
        # Clear existing
        for key in self.chip_positions:
            self.chip_positions[key] = []
        for chip in chip_list:
            for key in self.chip_positions:
                self.chip_positions[key].append(chip.get(key, None))

    # Normal states

    ground = State("Ground", initial=True)
    surveying_sockets = State("Surveying Sockets")
    moving_chip_to_socket = State("Moving Chip to Socket")
    testing = State("Testing")
    writing_to_hwdb = State("Writing to HWDB")
    moving_chip_to_tray = State("Moving Chip to Tray")

    # Fix states
    reseat = State("Reseat")
    moving_chip_to_bad_tray = State("Moving Chip to Bad Tray")

    # Pause state
    pause = State("Pause")

    # Error states
    no_server_connection = State("No Server Connection")
    chip_in_socket = State("Chip in Socket")
    vision_sequence_failed = State("Vision Sequence Failed")
    no_pressure = State("No Pressure")
    lost_vacuum = State("Lost Vacuum")
    bad_contact = State("Bad Contact")
    no_chip = State("No Chip")
    safe_guard = State("Safe Guard")
    bad_pins = State("Bad Pins")
    no_serial_number = State("No Serial Number")
    failed_init = State("Failed Initialization")
    no_wib_connection = State("No WIB Connection")
    failed_upload = State("Failed Upload")

    cycle = (
        ground.to(surveying_sockets)
        | surveying_sockets.to(moving_chip_to_socket)
        | moving_chip_to_socket.to(testing)
        | testing.to(writing_to_hwdb)
        | writing_to_hwdb.to(moving_chip_to_tray)
        | moving_chip_to_tray.to(ground)
    )

    test_cycle = (
        ground.to(pause)
        | pause.to(surveying_sockets)
        | surveying_sockets.to(pause)
        | pause.to(moving_chip_to_socket)
        | moving_chip_to_socket.to(pause)
        | pause.to(testing)
        | testing.to(pause)
        | pause.to(writing_to_hwdb)
        | writing_to_hwdb.to(pause)
        | pause.to(moving_chip_to_tray)
        | moving_chip_to_tray.to(pause)
        | pause.to(moving_chip_to_socket)
        | moving_chip_to_bad_tray.to(pause)
        | pause.to(moving_chip_to_socket)
    )

    pause_cycle = (
        ground.to(pause)
        | surveying_sockets.to(pause)
        | moving_chip_to_socket.to(pause)
        | testing.to(pause)
        | writing_to_hwdb.to(pause)
        | moving_chip_to_tray.to(pause)
        | moving_chip_to_bad_tray.to(pause)
        | reseat.to(pause)
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

    error_cycle = (
        ground.to(no_server_connection)
        | surveying_sockets.to(chip_in_socket)
        | surveying_sockets.to(vision_sequence_failed)
        | moving_chip_to_socket.to(no_pressure)
        | moving_chip_to_socket.to(lost_vacuum)
        | moving_chip_to_socket.to(bad_contact)
        | moving_chip_to_socket.to(no_chip)
        | moving_chip_to_socket.to(vision_sequence_failed)
        | moving_chip_to_socket.to(safe_guard)
        | moving_chip_to_socket.to(bad_pins)
        | moving_chip_to_socket.to(no_serial_number)
        | testing.to(failed_init)
        | testing.to(no_wib_connection)
        | failed_init.to(reseat)
        | writing_to_hwdb.to(failed_upload)
        | moving_chip_to_tray.to(no_pressure)
        | moving_chip_to_tray.to(lost_vacuum)
        | moving_chip_to_tray.to(bad_contact)
        | moving_chip_to_tray.to(no_chip)
        | moving_chip_to_tray.to(vision_sequence_failed)
        | moving_chip_to_tray.to(safe_guard)
        | moving_chip_to_bad_tray.to(moving_chip_to_socket)
        | bad_pins.to(moving_chip_to_bad_tray)
        | no_serial_number.to(moving_chip_to_bad_tray)
        | failed_upload.to(moving_chip_to_tray)
        | chip_in_socket.to(surveying_sockets)
        | vision_sequence_failed.to(surveying_sockets)
        | bad_contact.to(moving_chip_to_socket)
        | no_chip.to(surveying_sockets)
        | no_wib_connection.to(testing)
    )

    reset_cycle = (
        pause.to(ground)
        | reseat.to(ground)
        | moving_chip_to_bad_tray.to(ground)
        | no_pressure.to(ground)
        | lost_vacuum.to(ground)
        | safe_guard.to(ground)
        | no_server_connection.to(ground)
    )

    def on_enter_ground(self):
        self.create_session_folder()
        print("Entering ground state - system ready")
        self.last_normal_state = self.current_state

    def on_enter_surveying_sockets(self):
        print("Starting to survey sockets")
        self.last_normal_state = self.current_state

    def on_enter_moving_chip_to_socket(self):
        print("Moving chip to test socket")
        self.last_normal_state = self.current_state

        # Call MoveChipsToSockets with current chip position
        if self.BypassRTS:
            print("[SIMULATION] Moving chip to socket")
        else:
            try:
                MoveChipsToSockets(self.rts, self.chip_positions)
            except Exception as e:
                print(f"Error calling MoveChipsToSockets: {e}")

    def on_enter_testing(self):
        print("Starting chip testing")
        self.last_normal_state = self.current_state

    def on_enter_writing_to_hwdb(self):
        print("Writing test results to HWDB")
        self.last_normal_state = self.current_state

    def on_enter_moving_chip_to_tray(self):
        print("Moving chip to tray")
        self.last_normal_state = self.current_state

    def on_enter_pause(self):
        print("System paused - awaiting resume command")
        self.pause_with_user_input()

    def on_enter_reseat(self):
        print("System reseat initiated - repositioning components")

    def on_enter_moving_chip_to_bad_tray(self):
        print("Moved defective chip to bad tray")

    def on_enter_no_server_connection(self):
        print("Error: No server connection detected")

    def on_enter_chip_in_socket(self):
        print("Error: Chip already in socket")

    def on_enter_vision_sequence_failed(self):
        print("Error: Vision sequence failed")

    def on_enter_no_pressure(self):
        print("Error: No pressure detected")

    def on_enter_lost_vacuum(self):
        print("Error: Vacuum system failure")

    def on_enter_bad_contact(self):
        print("Error: Bad socket contact")

    def on_enter_no_chip(self): 
        print("Error: No chip detected")

    def on_enter_safe_guard(self):
        print("Error: Safety guard triggered")

    def on_enter_bad_pins(self):
        print("Error: Bad pins detected")

    def on_enter_no_serial_number(self):
        print("Error: No serial number")

    def on_enter_failed_init(self):
        print("Error: Test initialization failed")

    def on_enter_no_wib_connection(self):
        print("Error: No WIB connection")

    def on_enter_failed_upload(self):
        print("Error: Failed to upload to HWDB")

    # Pause methods
    def resume_to_previous(self):
        if self.last_normal_state:
            self.current_state = self.last_normal_state
        else:
            print("Last normal state not found")

    def advance_to_next_in_cycle(self):
        self.resume_to_previous()
        self.cycle()

    def pause_with_user_input(self):
        print(f"\nSYSTEM PAUSED")
        
        print("\nWhat would you like to do?")
        print("┌─────────────────────────────────────────┐")
        print("│ 1. Go back to Ground state              │")
        print("│ 2. Resume to previous state             │")
        print("│ 3. Continue to next state in cycle      │")
        print("│ 4. Quit                                 │")
        print("└─────────────────────────────────────────┘")
        
        print("Please enter your choice (1-4): ", end="")

        while True:
            try:
                user_input = input("").strip().lower()
                if user_input == "1":
                    self.current_state = self.ground
                    print(f"Resumed to Ground state")
                    print(f"Current state: {self.current_state}")
                    break
                elif user_input == "2":
                    self.resume_to_previous()
                    print(f"\nResumed to previous state")
                    print(f"Current state: {self.current_state}")
                    break
                elif user_input == "3":
                    self.advance_to_next_in_cycle()
                    break
                elif user_input == "4":
                    print("Exiting system...")
                    sys.exit()
            except (EOFError, KeyboardInterrupt):
                print("\n\nReceived interrupt signal. System remains paused.")
                print("Type 1, 2, 3, or 4 to continue.")


    def advance(self):
        """Advance to the next chip position on the tray."""
        if self.current_chip_index < len(self.chip_positions['col']) - 1:
            self.current_chip_index += 1
        else:
            raise StopIteration("Reached the end of the tray.")

    def get_position(self):
        """Get the current chip position on the tray."""
        return (self.chip_positions['col'][self.current_chip_index], self.chip_positions['row'][self.current_chip_index])

    def advance_chip_position(self):
        """Advance to the next chip position on the tray."""
        try:
            self.advance()
            print(f"Advanced to chip position: {self.get_position()}")
        except StopIteration:
            print("Reached the end of the tray. Starting over.")
            self.current_chip_index = 0

    def reset_tray_position(self):
        """Reset the chip position to the beginning of the tray."""
        self.current_chip_index = 0
        print("Reset chip position to (1, 1)")

    def is_tray_complete(self):
        """Check if we've processed all positions on the tray."""
        return self.current_chip_index == len(self.chip_positions['col']) - 1

    def run_full_cycle(self):
        """Run a full test cycle for one chip and then advance to the next chip position."""
        print(f"Starting full cycle at position {self.get_position()}")
        for i in range(6):
            self.cycle()
        print("Full cycle complete, advancing chip position")
        self.advance_chip_position()
    
    def handle_tray(self):
        """Run a full test cycle for all 40 chips on the tray."""
        for i in range(40):
            print(f"\n--- Processing chip {i+1}/40 ---")
            self.run_full_cycle()
        print(f"\nTray processing complete! Processed 40 chips.")

    def get_current_chip_data(self):
        """Get all data for the current chip."""
        return {
            'col': self.chip_positions['col'][self.current_chip_index],
            'row': self.chip_positions['row'][self.current_chip_index],
            'index': self.current_chip_index
        }
    
    def set_chip_data(self, index, col=None, row=None):
        """Set data for a specific chip at the given index."""
        if col is not None:
            self.chip_positions['col'][index] = col
        if row is not None:
            self.chip_positions['row'][index] = row

    def create_session_folder(self):
        """Create a new folder in 'images/' named with the current date and time."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f'session_{timestamp}'
        folder_path = os.path.join(folder_name)
        os.makedirs(folder_path, exist_ok=True)
        self.current_session_folder = folder_path

    def read_log_and_transition(self, log_path):
        """
        Periodically read a log file and transition the state machine to the state specified in each new line.
        Args:
            log_path (str): Path to the log file.
        """
        # Map log strings to state attributes
        state_map = {
            "ground": self.ground,
            "surveying_sockets": self.surveying_sockets,
            "moving_chip_to_socket": self.moving_chip_to_socket,
            "MoveChipFromTrayToSocket": self.moving_chip_to_socket,
            "Jumped to DAT": self.testing,
            "testing": self.testing,
            "writing_to_hwdb": self.writing_to_hwdb,
            "moving_chip_to_tray": self.moving_chip_to_tray,
            "Picked up chip from tray": self.moving_chip_to_socket,
            "reseat": self.reseat,
            "moving_chip_to_bad_tray": self.moving_chip_to_bad_tray,
            "pause": self.pause,
            "no_server_connection": self.no_server_connection,
            "chip_in_socket": self.chip_in_socket,
            "vision_sequence_failed": self.vision_sequence_failed,
            "no_pressure": self.no_pressure,
            "lost_vacuum": self.lost_vacuum,
            "bad_contact": self.bad_contact,
            "no_chip": self.no_chip,
            "safe_guard": self.safe_guard,
            "bad_pins": self.bad_pins,
            "no_serial_number": self.no_serial_number,
            "failed_init": self.failed_init,
            "no_wib_connection": self.no_wib_connection,
            "failed_upload": self.failed_upload,
        }
        last_line = 0
        print(f"Monitoring log file: {log_path}")
        while True:
            try:
                if not os.path.exists(log_path):
                    print(f"Log file does not exist: {log_path}")
                    break
                with open(log_path, 'r') as f:
                    lines = f.readlines()   # Store all lines from the log file in a list
                # Process only new lines
                new_lines = lines[last_line:]
                for line in new_lines:
                    state_str = line.strip().lower()
                    # Find first matching state
                    for key, state in state_map.items():
                        if key.lower() in state_str:
                            if self.current_state != state:
                                self.current_state = state
                                print(f"'{state_str}' -> {self.current_state}")
                            break
                last_line = len(lines)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopped log monitoring.")
                break
            except Exception as e:
                print(f"Error reading log file: {e}")
                time.sleep(1)