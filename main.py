import pygame as pg
import boid as boid_class
import constants


def init_boids(n):
    return [boid_class.Boid() for _ in range(n)]


pg.init()
screen = pg.display.set_mode([constants.WIDTH, constants.HEIGHT])
clock = pg.time.Clock()

fps = 60
dt = 1 / fps
boids = init_boids(constants.N_BOIDS)
running = True


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                boids = init_boids(constants.N_BOIDS)
            elif event.key == pg.K_ESCAPE:
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