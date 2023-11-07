import pygame as pg
import random
import constants


class Boid:
    boid_width, boid_height = 10, 6
    boid_shape = pg.Surface((boid_width, boid_height), pg.SRCALPHA)
    # Draw a triangle onto the boid_shape surface
    pg.draw.polygon(
        boid_shape,
        (0, 0, 255),
        [(boid_width, boid_height / 2), (0, 0), (0, boid_height)],
    )

    debug = False
    can_wrap = False
    min_speed = 100
    max_speed = 500
    max_force = 1
    max_turn = 5
    perception_radius = 50
    separation_distance = 25

    def __init__(self):
        start_position = pg.Vector2(
            random.uniform(0, constants.WIDTH), random.uniform(0, constants.HEIGHT)
        )

        random_velocity = pg.Vector2(
            random.uniform(-10, 10),
            random.uniform(-10, 10),
        )
        start_velocity = (
            (Boid.max_speed + Boid.min_speed)
            / 2
            * random_velocity
            / random_velocity.length()
        )

        self.position = start_position
        self.velocity = start_velocity
        self.debug = Boid.debug

    def update(self, boids, dt):
        neighbors = self.get_neighbors(boids)
        s = self.separation(neighbors)
        c = self.cohesion(neighbors)
        a = self.alignment(neighbors)
        b = self.bound_position()
        direction = s + c + a + b

        self.velocity += direction

        # Speed limit
        speed = self.velocity.length()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt

    def draw(self, screen):
        if Boid.debug:
            pg.draw.line(
                screen,
                (255, 0, 0),
                self.position,
                self.position + self.velocity.normalize() * 50,
            )
            pg.draw.circle(
                screen, (100, 100, 100), self.position, self.perception_radius, width=1
            )
            pg.draw.circle(
                screen,
                (255, 100, 100),
                self.position,
                self.separation_distance,
                width=1,
            )

        _, heading = self.velocity.as_polar()

        shape_rotated = pg.transform.rotate(Boid.boid_shape, -heading)
        screen.blit(
            shape_rotated, self.position - (Boid.boid_width / 2, Boid.boid_height / 2)
        )

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid is not self:
                dist_sq = self.position.distance_squared_to(boid.position)
                if dist_sq < self.perception_radius**2:
                    neighbors.append(boid)

        return neighbors

    def separation(self, neighbors):
        direction = pg.Vector2(0, 0)
        for boid in neighbors:
            if (
                boid.position - self.position
            ).length_squared() < Boid.separation_distance**2:
                direction -= boid.position - self.position

        return direction

    def cohesion(self, neighbors):
        if len(neighbors) == 0:
            return pg.Vector2(0, 0)
        direction = pg.Vector2()
        for boid in neighbors:
            direction += boid.position - self.position
        direction /= len(neighbors)
        return direction / 100  # Move 1% to the center

    def alignment(self, neighbors):
        if len(neighbors) == 0:
            return pg.Vector2(0, 0)
        direction = pg.Vector2(0, 0)
        for boid in neighbors:
            direction += boid.velocity

        direction /= len(neighbors)
        direction -= self.velocity
        return direction / 8

    def bound_position(self):
        direction = pg.Vector2(0, 0)
        if self.position.x <= constants.DISTANCE_TO_BOUNDS:
            direction.x = 1
        elif self.position.x >= constants.WIDTH - constants.DISTANCE_TO_BOUNDS:
            direction.x = -1

        if self.position.y <= constants.DISTANCE_TO_BOUNDS:
            direction.y = 1
        elif self.position.y >= constants.HEIGHT - constants.DISTANCE_TO_BOUNDS:
            direction.y = -1

        return direction * 10
