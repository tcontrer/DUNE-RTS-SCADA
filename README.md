# RTS (Robotic Test System) State Machine

## Overview

The Robotic Test Stand (RTS) State Machine is a Python-based control system that manages and tracks the operational states of an automated testing platform. It provides a robust state management framework to coordinate robotic movements, testing procedures, and data handling while ensuring safe and predictable system behavior with comprehensive error handling and recovery capabilities.

## What It Does

The system keeps track of states with the following key operations:

1. **Socket Surveying**: Identifies available test sockets
2. **Chip Movement**: Controls robotic arm to place chips in test sockets
3. **Testing**: Executes WIB (Warm Interface Board) testing procedures
4. **Data Management**: Writes test results to hardware database (HWDB)
5. **Output Handling**: Moves tested chips to output trays
6. **Error Management**: Handles various fault conditions with appropriate error states
7. **System Recovery**: Provides mechanisms to recover from errors and pause states

### Key Features

- **State-based Control**: Uses a finite state machine to ensure predictable operation
- **Comprehensive Error Handling**: Dedicated error states for different fault conditions
- **Safety Integration**: Includes pause functionality for emergency stops and error recovery
- **Modular Design**: Clean separation between states, transitions, and error handling
- **Extensible**: Easy to add new states, transitions, and error conditions as needed
- **Robust Recovery**: Well-defined recovery paths from error and pause states

## System States

### Normal Operation States
- `ground`: Initial/idle state, ready for next operation
- `surveying_sockets`: Scanning for available test sockets
- `moving_chip_to_socket`: Placing chip in identified socket
- `testing`: Running WIB test procedures
- `writing_to_hwdb`: Storing results in hardware database
- `moving_chip_to_tray`: Moving tested chip to output location
- `reset`: System reset state for recovery operations

### Control States
- `pause`: System paused (can resume to any operational state)

### Error States

#### Ground State Errors
- `no_server_connection`: Server communication failure

#### Socket Surveying Errors
- `chip_in_socket`: Socket already occupied by chip
- `vision_sequence_failed`: Camera/vision system malfunction

#### Chip Movement Errors (Socket & Tray)
- `no_pressure`: Pressure loss
- `lost_vacuum`: Vacuum system failure
- `bad_contact`: Poor electrical contact detected
- `no_chip`: Expected chip not found
- `safe_guard`: Safety system triggered
- `bad_pins`: Pin alignment or damage detected
- `no_serial_number`: Chip identification failure

#### Testing Errors
- `failed_init`: Test initialization failure
- `no_wib_connection`: WIB communication error

#### Database Errors
- `failed_upload`: Database write operation failed

## Project Structure

```
DUNE-RTS-SCADA/
├── RTSStateMachine.py    # Main state machine implementation
├── main.py               # Example usage and testing script
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd DUNE-RTS-SCADA
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Basic Usage

1. **Run the example script**:
   ```bash
   python main.py
   ```

   This will:
   - Create an instance of the RTS State Machine
   - Show the current state (initially "Ground")
   - Execute a state transition to "Surveying Sockets"
   - Display the new state

### Using the State Machine in Your Code

```python
import RTSStateMachine as RTSSM

# Create state machine instance
sm = RTSSM.RTSStateMachine()

# Check current state
print(f"Current state: {sm.current_state}")

# Trigger state transitions
sm.cycle()  # Move to next state in normal flow

# Pause the system
sm.pause_cycle()  # Transition to pause state

# Resume operations (from pause state)
sm.cycle()  # Resume to appropriate operational state

# Handle error transitions (when fault conditions are detected)
# These would typically be triggered by external monitoring systems
sm.error_transitions()  # Transition to appropriate error state
```

### State Transition Examples

```python
# Normal operation flow
sm = RTSStateMachine()
sm.cycle()  # ground → surveying_sockets
sm.cycle()  # surveying_sockets → moving_chip_to_socket
sm.cycle()  # moving_chip_to_socket → testing
sm.cycle()  # testing → writing_to_hwdb
sm.cycle()  # writing_to_hwdb → moving_chip_to_tray
sm.cycle()  # moving_chip_to_tray → ground (cycle complete)

# Emergency pause from any state
sm.pause_cycle()  # current_state → pause

# Resume from pause
sm.cycle()  # pause → appropriate_operational_state

# Error handling (triggered by fault detection)
# Example: Vision system failure during socket surveying
if vision_system_error_detected:
    sm.error_transitions()  # surveying_sockets → vision_sequence_failed
```

## State Transition Architecture

The state machine implements three main transition groups:

### 1. Normal Operation Transitions (`cycle`)
- Defines the standard operational flow
- Includes recovery paths from pause state
- Ensures predictable progression through testing workflow

### 2. Pause Transitions (`pause_cycle`)
- Allows pausing from any operational state
- Enables safe system shutdown for maintenance or emergencies
- Maintains state context for proper resume operation

### 3. Error Transitions (`error_transitions`)
- Handles fault conditions from each operational state
- Provides specific error states for different failure modes
- Enables targeted error recovery and debugging

## Development

### Adding New States

1. Define the new state in the `RTSStateMachine` class:
   ```python
   new_state = State("New State Name")
   ```

2. Add transition rules to appropriate transition groups:
   ```python
   cycle = (
       # ... existing transitions ...
       | new_state.to(target_state)
   )
   ```

3. Implement entry/exit callbacks:
   ```python
   def on_enter_new_state(self):
       print("Entering new state")
       # Implementation here
   
   def on_exit_new_state(self):
       print("Leaving new state")
       # Cleanup here
   ```

### Adding Error States

1. Define the error state:
   ```python
   new_error_state = State("New Error Condition")
   ```

2. Add error transitions from relevant operational states:
   ```python
   error_transitions = (
       # ... existing error transitions ...
       | operational_state.to(new_error_state)
   )
   ```

3. Implement error handling callbacks:
   ```python
   def on_enter_new_error_state(self):
       print("Error detected: specific condition")
       # Error handling and logging
   ```

### Testing

The `main.py` file provides a basic test of state transitions. For more comprehensive testing:

1. Run the main script: `python main.py`
2. Observe console output for state changes
3. Verify state machine behavior matches expected flow
4. Test error conditions and recovery paths
5. Validate pause/resume functionality

## Dependencies

- `python-statemachine==2.5.0`: Provides the state machine framework

## Future Enhancements

- Integration with robot software
- GUI interface for system monitoring
- Logging and error handling improvements
- Configuration file support
- Real-time status monitoring

## Contributing

1. Follow the existing code style and structure
2. Add appropriate state entry/exit callbacks for new states
3. Update this README when adding significant features
4. Test state transitions thoroughly before committing