# ESP32-DM860H-NEMA-23-Stepper-Motor-Test
An ESP32-based stepper motor control project using a DM860H driver and NEMA 23 stepper motor. The project demonstrates basic STEP/DIR control, forward and reverse rotation, and motor-driver interfacing for robotics and motion-control applications.

**Objective**
The main objective of this project was to:
- Test a NEMA 23 stepper motor.
- Interface an ESP32 with a DM860H driver.
- Understand STEP/DIR motor control.
- Test forward and reverse rotation.

**Working**
- ESP32 enables the DM860H driver.
- Direction is initially set to HIGH.
- ESP32 generates 200 step pulses.
- The motor rotates for 200 steps.
- The system waits for 1 second.
- The direction is changed to LOW.
- Another 200 step pulses are generated.
- The motor rotates in the reverse direction.
- The sequence repeats continuously.

**Key Concepts**
- STEP: Each valid pulse commands the driver to move the motor by one configured microstep.
- DIR: Determines the direction of motor rotation.
- ENABLE: Enables or disables the driver output, depending on the driver's enable logic/configuration.
- Microstepping: The DM860H can be configured for different microstepping resolutions. Therefore, the number of pulses required for one complete motor revolution depends on the driver's DIP-switch settings.
