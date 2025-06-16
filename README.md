# DUNE-RTS-SCADA
Supervisory Control and Data Acquisition (SCADA) software for testing electronics for the DUNE far detector using a Robot Test Stand (RTS)

# RTS State Machine – Caleb's Branch

This branch is a restructured version of the Robotic Test Stand (RTS) state machine logic. The goal is to align the control flow more closely with the fault-tolerant state diagram preferred by Dr. Taylor Contreras, while selectively incorporating reusable components from Virginia's 2023 implementation.

## Objectives

- Design a clean, modular FSM architecture with clear transition logic.
- Integrate robust fault handling for conditions like:
  - Lost vacuum
  - Bad contact
  - No chip
  - Vision sequence failure
  - Bad pins
- Retain and adapt functional pieces from the previous codebase (e.g., chip cycling, basic transition mechanisms).
- Prepare the system for easier debugging, logging, and long-term maintainability.

## Key Differences from Previous Implementation

| Area                     | Virginia's FSM               | This Branch                        |
|--------------------------|------------------------------|-------------------------------------|
| Structure                | Linear, stage-based          | Modular, interrupt-aware            |
| Fault Handling           | Minimal                      | Explicit transitions and safeguards |
| Supervisor Alignment     | Partial                      | Full alignment with PDF FSM diagram |
| Reusability              | Monolithic                   | Refactored into smaller handlers    |

## Status

- [x] FSM skeleton defined
- [x] Transition logic mapped from supervisor diagram
- [ ] Implementing `PickChip` fault substates
- [ ] Modular logging for interrupts
- [ ] Integration with RTS hardware interfaces

## Notes

- This branch is experimental. Code is subject to change as logic gets refined.
- All additions are documented inline and in `docs/transition_map.md` (WIP).
- Contributions from Virginia's code are credited in code comments where used.