# DUNE-RTS-SCADA

A simple state machine for automated chip testing using a robotic test stand.

## What it does

Manages the testing cycle for electronic chips on a 4×10 tray:
1. Survey available test sockets
2. Move chip to socket
3. Run WIB testing
4. Write results to database
5. Move chip to output tray
6. Return to start for next chip
7. Advance to next position on tray (column-wise: 1,1 → 1,2 → ... → 10,4)

## States

### Normal Operation States
- **Ground**: Ready to start
- **Surveying Sockets**: Finding available test positions
- **Moving Chip to Socket**: Robot placing chip
- **Testing**: Running WIB tests
- **Writing to HWDB**: Saving results
- **Moving Chip to Tray**: Robot moving tested chip

### Control States
- **Pause**: System paused with interactive menu

### Fix States
- **Reseat**: System reseat for component repositioning
- **Moving Chip to Bad Tray**: Routing defective chips

### Error States
- **No Server Connection**: Server communication failure
- **Chip in Socket**: Socket already occupied
- **Vision Sequence Failed**: Vision system failure
- **No Pressure**: Pressure system failure
- **Lost Vacuum**: Vacuum system failure
- **Bad Contact**: Poor electrical contact
- **No Chip**: Expected chip not found
- **Safe Guard**: Safety system triggered
- **Bad Pins**: Pin issues detected
- **No Serial Number**: Chip identification failure
- **Failed Initialization**: Test initialization failure
- **No WIB Connection**: WIB connection failure
- **Failed Upload**: Database upload failure

## Chip Tray System

The system tracks chip positions on a 4×10 tray in column-wise order:
- **40 total positions**: 10 columns × 4 rows
- **Position tracking**: (col, row) from (1,1) to (10,4)
- **Automatic advancement**: Moves to next position after each cycle
- **Tray completion**: Handles end-of-tray logic with automatic reset

## Pause/Resume System

Advanced pause functionality with interactive menu:
- **Option 1**: Return to Ground state
- **Option 2**: Resume to previous normal state
- **Option 3**: Continue to next state in cycle
- **Option 4**: Quit system

The system automatically tracks the last normal state for precise resume functionality.

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python main.py
```

## Usage

```python
import RTSStateMachine as RTSSM

sm = RTSSM.RTSStateMachine()

# Basic state transitions
sm.cycle()  # Move to next state in normal cycle
sm.pause_cycle()  # Pause system with interactive menu
sm.error_cycle()  # Trigger error handling transitions
sm.test_cycle()  # Run test cycle with pauses

# Chip positioning
print(sm.get_position())  # Get current (col, row) position
sm.advance_chip_position()  # Move to next position

# Automated testing
sm.run_full_cycle()  # Run 6 cycles for one chip, then advance position
sm.handle_tray()  # Process all 40 chips on the tray

# Pause/Resume control
sm.resume_to_previous()  # Resume to last normal state
sm.advance_to_next_in_cycle()  # Resume and advance one step
```

## State Management Methods

### Chip Management
- `get_position()`: Returns current (col, row) position
- `advance_chip_position()`: Move to next position, handles tray completion
- `reset_tray_position()`: Reset to position (1,1)
- `is_tray_complete()`: Check if at final position (10,4)
- `run_full_cycle()`: Run 6 cycles for one chip, then advance
- `handle_tray()`: Process all 40 chips on the tray

### Pause/Resume Control
- `resume_to_previous()`: Resume to last recorded normal state
- `advance_to_next_in_cycle()`: Resume to previous state then advance one step
- `pause_with_user_input()`: Interactive pause menu

## Transitions

- **cycle**: Normal operation flow (ground → surveying → moving → testing → writing → moving to tray → ground)
- **test_cycle**: Test mode with pauses between each step
- **pause_cycle**: Pause transitions from any state
- **error_cycle**: Error handling and recovery transitions

## Status

**Done**: Simplified state machine, advanced pause/resume with interactive menu, chip tray positioning, automated testing cycles, error handling
**Next**: Fix transition logic, Integration with actual hardware systems