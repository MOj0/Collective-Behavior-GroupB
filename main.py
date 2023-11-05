import pygame as pg
import boid

WIDTH, HEIGHT = 800, 600
fps = 60
dt = 1 / fps

pg.init()

# Set up the drawing window
screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

boids = [boid.Boid() for _ in range(10)]

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Fill (background)
    screen.fill((0, 0, 0))

    for boid in boids:
        boid.update(boids, dt)
    for boid in boids:
        boid.draw(screen)

    # Update the entire display
    pg.display.flip()

    clock.tick(fps)


pg.quit()
