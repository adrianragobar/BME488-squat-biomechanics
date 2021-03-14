# Squatting Project
This project is a course requirement for BME 488 Computational Biomechanics.The project aims to investigate parameters that are crucial for performing a safe deep squat using an individual's anthropoemetry.

## Anthropometry
- Body weight
- Leg length: Patella to ankle
- Thigh length: Greater trochanter to patella
- Torso length: Nose to greater trochanter
- Upper extremity (arm) length: Shoulder to tip of middle finger

## Joint angles
- Arm angle: Angle between vetical and arm at shoulder
- Torso angle: Angle between vertical and spine at hip
- Thigh angle: Angle between vertical and thigh at knee
- Leg angle: Angle between vertical and leg at ankle

#### torso_angle.py
- Given an individual's body dimensions, does the length of the femur allow the individual to obtain stability when attempting a deep squat?
  - Torso angle was incremented. For each torso angle, femur length was varied and the x coordinate for the centre of mass was calculated and plotted.
