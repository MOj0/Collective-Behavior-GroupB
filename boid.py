import pygame as pg
import random


class Boid:
    debug = False
    can_wrap = False
    min_speed = 0.01
    max_speed = 0.2
    max_force = 1
    max_turn = 5
    perception = 1000
    separation_distance = 15
    edge_distance_pct = 5

    def __init__(self):
        max_x, max_y = 800, 600

        start_position = pg.Vector2(random.uniform(0, max_x), random.uniform(0, max_y))

        random_velocity = pg.Vector2(
            random.uniform(-10, 10),
            random.uniform(-10, 10),
        )
        start_velocity = Boid.max_speed * random_velocity / random_velocity.length()

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
        direction = s + c + a

        if direction.length_squared() > 0:
            self.acceleration = direction
        # TODO: Enforce turn limits

        self.velocity += self.acceleration
        speed = self.velocity.length()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # lol...
        if not (0 <= self.position.x <= 800):
            self.velocity.x *= -1
        if not (0 <= self.position.y <= 600):
            self.velocity.y *= -1

        # self.position += self.velocity * dt
        self.position += self.velocity

    def draw(self, screen):
        pg.draw.circle(screen, (0, 0, 255), self.position, 5)

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid is not self:
                dist_sq = self.position.distance_squared_to(boid.position)
                if dist_sq < self.perception**2:
                    neighbors.append(boid)

        return neighbors

    def clamp_force(self, force: pg.Vector2):
        if force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)
        return force

    def separation(self, neighbors):
        direction = pg.Vector2(0, 0)
        for boid in neighbors:
            if (
                boid.position - self.position
            ).length_squared() < Boid.separation_distance**2:
                direction -= boid.position - self.position

        return self.clamp_force(direction)

    def cohesion(self, neighbors):
        if len(neighbors) == 0:
            return pg.Vector2(0, 0)
        direction = pg.Vector2()
        for boid in neighbors:
            direction += boid.position
        direction /= len(neighbors)
        direction = self.clamp_force(direction)
        return direction / 100  # Move 1% to the centre

    def alignment(self, neighbors):
        if len(neighbors) == 0:
            return pg.Vector2(0, 0)
        direction = pg.Vector2(0, 0)
        for boid in neighbors:
            direction += boid.velocity

        direction /= len(neighbors)
        direction = self.clamp_force(direction - self.velocity)
        return direction / 8
