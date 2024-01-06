WH = 900
HEIGHT, WIDTH = (WH, WH)

N_PREY = 10
N_PREDATORS = 1


# 1 meter = 0.038 pixels
# 7.2 m/s = 7.2 / 0.038 = 189.5 pixels/s
# FPS=60; speed = 189.5 / 60 = 3.78947368421 pixels/frame

# BL = 5.26315789474


# Boid parameters
PREY_CRUISE_VELOCITY = 400.0  # Effectively mininmum velocity
PREY_MAX_VELOCITY = 600.0
PREY_BASE_ACCELERATION = 1200.0
PREY_MAX_ACCELERATION = 1500.0
PREY_MAX_ROTATION_ANGLE = 60  # NOTE: This parameter depends on the acceleration...
PREY_PERCEPTION_RADIUS = 500
PREY_SEPARATION_DISTANCE = 25
# NOTE: FOV has to be halved, because we have FOV/2 on each of the 2 sides
PREY_FOV = 300 // 2

# Behaviour parameters
PREY_SEPARATION_COEFFICIENT = 1
PREY_COHESION_COEFFICIENT = 0.01
PREY_ALIGNMENT_COEFFICIENT = 0.12
PREY_ESCAPE_COEFFICIENT = 10


PREDATOR_CRUISE_VELOCITY = 500.0  # Effectively minimum velocity
PREDATOR_MAX_VELOCITY = 650.0
PREDATOR_BASE_ACCELERATION = 1600.0
PREDATOR_MAX_ACCELERATION = 2500.0
PREDATOR_MAX_ROTATION_ANGLE = 30  # NOTE: This parameter depends on the acceleration...
PREDATOR_PERCEPTION_RADIUS = 1200
PREDATOR_SEPARATION_DISTANCE = 50
# NOTE: Has to be halved, because we have FOV/2 on each of the 2 sides
PREDATOR_FOV = 300 // 2


### Case where predator loops around prey...

# HEIGHT, WIDTH = (900, 1200)

# N_PREY = 50
# N_PREDATORS = 1

# # Boid parameters
# PREY_CRUISE_VELOCITY = 200.0  # Effectively mininmum velocity
# PREY_MAX_VELOCITY = 300.0
# PREY_BASE_ACCELERATION = 1200.0
# PREY_MAX_ACCELERATION = 1400.0
# PREY_MAX_ROTATION_ANGLE = 120  # NOTE: This parameter depends on the acceleration...
# PREY_PERCEPTION_RADIUS = 300
# PREY_SEPARATION_DISTANCE = 25
# # NOTE: FOV has to be halved, because we have FOV/2 on each of the 2 sides
# PREY_FOV = 300 // 2

# # Behaviour parameters
# PREY_SEPARATION_COEFFICIENT = 1
# PREY_COHESION_COEFFICIENT = 0.01
# PREY_ALIGNMENT_COEFFICIENT = 0.12
# PREY_ESCAPE_COEFFICIENT = 3


# PREDATOR_CRUISE_VELOCITY = 500.0  # Effectively minimum velocity
# PREDATOR_MAX_VELOCITY = 700.0
# PREDATOR_BASE_ACCELERATION = 1600.0
# PREDATOR_MAX_ACCELERATION = 2500.0
# PREDATOR_MAX_ROTATION_ANGLE = 240  # NOTE: This parameter depends on the acceleration...
# PREDATOR_PERCEPTION_RADIUS = 1200
# PREDATOR_SEPARATION_DISTANCE = 50
# # NOTE: Has to be halved, because we have FOV/2 on each of the 2 sides
# PREDATOR_FOV = 300 // 2
