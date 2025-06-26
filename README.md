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

- **Ground**: Ready to start
- **Surveying Sockets**: Finding available test positions
- **Moving Chip to Socket**: Robot placing chip
- **Testing**: Running WIB tests
- **Writing to HWDB**: Saving results
- **Moving Chip to Tray**: Robot moving tested chip
- **Pause**: System paused (can resume)

## Chip Tray System

The system tracks chip positions on a 4×10 tray in column-wise order:
- **40 total positions**: 10 columns × 4 rows
- **Position tracking**: (col, row) from (1,1) to (10,4)
- **Automatic advancement**: Moves to next position after each cycle
- **Tray completion**: Handles end-of-tray logic with automatic reset

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
sm.cycle()  # Move to next state
sm.pause_cycle()  # Pause system

# Chip positioning
print(sm.get_position())  # Get current (col, row) position
sm.advance_chip_position()  # Move to next position

# Automated testing
sm.run_full_cycle()  # Run 6 cycles for one chip, then advance position
sm.handle_tray()  # Process all 40 chips on the tray
```

## Chip Management Methods

- `get_position()`: Returns current (col, row) position
- `advance_chip_position()`: Move to next position, handles tray completion
- `reset_tray_position()`: Reset to position (1,1)
- `is_tray_complete()`: Check if at final position (10,4)
- `run_full_cycle()`: Run 6 cycles for one chip, then advance
- `handle_tray()`: Process all 40 chips on the tray

## Status

**Done**: Basic state machine, transitions, pause/resume, chip tray positioning, automated testing cycles
**Next**: Integration with actual hardware systems