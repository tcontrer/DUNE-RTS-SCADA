# DUNE-RTS-SCADA

A simple state machine for automated chip testing using a robotic test stand.

## What it does

Manages the testing cycle for electronic chips:
1. Survey available test sockets
2. Move chip to socket
3. Run WIB testing
4. Write results to database
5. Move chip to output tray
6. Return to start for next chip

## States

- **Ground**: Ready to start
- **Surveying Sockets**: Finding available test positions
- **Moving Chip to Socket**: Robot placing chip
- **Testing**: Running WIB tests
- **Writing to HWDB**: Saving results
- **Moving Chip to Tray**: Robot moving tested chip
- **Pause**: System paused (can resume)

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
sm.cycle()  # Move to next state
sm.pause_cycle()  # Pause system
```

## Status

**Done**: Basic state machine, transitions, pause/resume
**Next**: Write a test that automates the state machine for an entire tray of chips (40)