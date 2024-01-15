# Collective-Behavior-GroupB

![demoGIF](/demo.gif)


## Team

- Matija Ojo - [MOj0](https://github.com/MOj0)
- Miha Krajnc - [mihoci10](https://github.com/mihoci10)
- Marko Adžaga - [markoAdza](https://github.com/markoAdza)
- Janez Kuhar  - [Glusk](https://github.com/Glusk)


## Theme

Theme of our project is simulation of predator-prey flocks and will be based on the following research paper: [Emergence of splits and collective turns in pigeon flocks under predation](https://royalsocietypublishing.org/doi/10.1098/rsos.211898).
The goal of the project is to have a realistic simulation with results being as close as possible to the ones in nature.
This way, we will be able to accurately simulate different types of models (the ones that only percieve its surrounding area (most realistic), prey always has up to date positional information about the entire flock, prey always has up to date positional information about the entire flock and the predator (least realistic)), and different types of escape maneuvers (split, hourglass, herd, vacuole, ...).
The expansion on the paper would be different parameters for configuring the flock (speed of prey, predator, turning angle speed/sharpness, flock coordination (information transfer speed, decision for prey to obey/work with neighbors or to perform on its own...)).
We would also like to simulate a large amount of prey and predators.
We do not plan to use machine learning.

## Plan

- 20.11: Basic boid simulation
- 18.12: Accurate boid simulation with predator(s), different types of models, escape maneuvers
- 8.1: Generalized to a simulation with tweakable parameters, large amounts of boids

## How to run

``pip install pygame``

``python src/main.py``

## Screenshots

![ScreenShot](/report/fig/boids_step_233.jpg)

![ScreenShot](/report/fig/boids_step_261.jpg)

