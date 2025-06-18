# RTS (Robotic Test System) State Machine

## Overview

The Robotic Test Stand (RTS) State Machine is a Python-based control system that manages and tracks the operational states of an automated testing platform. It provides a robust state management framework to coordinate robotic movements, testing procedures, and data handling while ensuring safe and predictable system behavior.

## What It Does

The system keeps track of states with the following key operations:

1. **Socket Surveying**: Identifies available test sockets
2. **Chip Movement**: Controls robotic arm to place chips in test sockets
3. **Testing**: Executes WIB (Warm Interface Board) testing procedures
4. **Data Management**: Writes test results to hardware database (HWDB)
5. **Output Handling**: Moves tested chips to output trays

### Key Features

- **State-based Control**: Uses a finite state machine to ensure predictable operation
- **Safety Integration**: Includes pause functionality for emergency stops
- **Modular Design**: Clean separation between states and transition logic
- **Extensible**: Easy to add new states and transitions as needed

## System States

### Normal Operation States
- `ground`: Initial/idle state, ready for next operation
- `surveying_sockets`: Scanning for available test sockets
- `moving_chip_to_socket`: Placing chip in identified socket
- `testing`: Running WIB test procedures
- `writing_to_hwdb`: Storing results in hardware database
- `moving_chip_to_tray`: Moving tested chip to output location

### Control States
- `pause`: System paused (can resume to any operational state)

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
```

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

### Testing

The `main.py` file provides a basic test of state transitions. For more comprehensive testing:

1. Run the main script: `python main.py`
2. Observe console output for state changes
3. Verify state machine behavior matches expected flow

## Dependencies

- `python-statemachine==2.5.0`: Provides the state machine framework

## Future Enhancements

- Error states
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