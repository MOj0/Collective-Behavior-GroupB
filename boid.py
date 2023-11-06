import pygame as pg
import random
import constants


class Boid:
    debug = False
    can_wrap = False
    min_speed = 100
    max_speed = 500
    max_force = 1
    max_turn = 5
    perception_radius = 50
    separation_distance = 25

    def __init__(self):
        max_x, max_y = 800, 600

        start_position = pg.Vector2(random.uniform(0, max_x), random.uniform(0, max_y))

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
        self.acceleration = pg.Vector2(0, 0)
        self.steer_direction = pg.Vector2(0, 0)
        self.debug = Boid.debug

    def update(self, boids, dt):
        neighbors = self.get_neighbors(boids)
        s = self.separation(neighbors)
        c = self.cohesion(neighbors)
        a = self.alignment(neighbors)
        b = self.bound_position()
        direction = s + c + a + b

        self.velocity += direction

        # if direction.length_squared() > 0:
        #     self.acceleration = direction
        # # TODO: Enforce turn limits

        # self.velocity += self.acceleration

        # Speed limit
        speed = self.velocity.length()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt
        # self.position += self.velocity

    def draw(self, screen):
        pg.draw.circle(screen, (0, 0, 255), self.position, 5)

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
            direction.x = 10
        elif self.position.x >= constants.WIDTH - constants.DISTANCE_TO_BOUNDS:
            direction.x = -10

        if self.position.y <= constants.DISTANCE_TO_BOUNDS:
            direction.y = 10
        elif self.position.y >= constants.HEIGHT - constants.DISTANCE_TO_BOUNDS:
            direction.y = -10

        return direction
