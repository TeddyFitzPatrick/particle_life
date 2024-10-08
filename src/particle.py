from consts import *
from math import sqrt, atan2, pow, cos, sin, fabs


def bound_check(position: list[int]) -> None:
    if position[0] > WINDOW_SIZE[0]:
        position[0] -= WINDOW_SIZE[0] * 0.8
    elif position[0] < WINDOW_SIZE[0] / 5:
        position[0] += WINDOW_SIZE[0] * 0.8
    if position[1] > WINDOW_SIZE[1]:
        position[1] -= WINDOW_SIZE[1]
    elif position[1] < 0:
        position[1] += WINDOW_SIZE[1]


class Particle:
    def __init__(self, color, initial_position, velocity=(0, 0)):
        self.color = color
        self.position = list(initial_position)
        self.velocity = list(velocity)

    def apply_force(self, particles, matrix, R_MIN, R_MAX):
        R_ZENITH = int((R_MIN + R_MAX) / 2)
        for particle in particles:
            if fabs(particle.position[0] - self.position[0]) > R_MAX:
                continue
            elif fabs(particle.position[1] - self.position[1]) > R_MAX:
                continue
            elif particle == self:
                continue
            # Find the distance between other particle and self
            r = sqrt(pow(particle.position[0] - self.position[0], 2) + pow(particle.position[1] - self.position[1], 2))
            if r > R_MAX:
                # Check if its adjacent via simulation borders
                continue
            # Calculate X/Y force unit vectors
            delta_x, delta_y = particle.position[0] - self.position[0], particle.position[1] - self.position[1]
            angle_radians = atan2(delta_y, delta_x)
            x_hat, y_hat = cos(angle_radians), sin(angle_radians)
            # Magnitude of force
            force_magnitude = None
            # 0 to R_MIN
            if r < R_MIN:
                force_magnitude = r / R_MIN - 1
            # R_MIN to ZENITH
            elif r < R_ZENITH:
                force_magnitude = 0.2 * (r - R_MIN) / (R_ZENITH - R_MIN)
                force_magnitude *= matrix[self.color][particle.color]
            # ZENITH to R_MAX
            elif r <= R_MAX:
                force_magnitude = 0.2 * (r - R_MAX) / (R_ZENITH - R_MAX)
                force_magnitude *= matrix[self.color][particle.color]
            # Apply acceleration to the particle's velocity
            self.velocity[0] += force_magnitude * x_hat
            self.velocity[1] += force_magnitude * y_hat
            # Apply border repulsions

    def update(self, friction: float):
        # Friction
        self.velocity[0] *= (1 - friction)
        self.velocity[1] *= (1 - friction)
        # Update Pos
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        bound_check(self.position)

    def dampen(self, factor):
        return self.color[0] / factor, self.color[1] / factor, self.color[2] / factor

    def render(self, window, particle_radius, show_radius=False, R_MIN=0, R_MAX=0):
        R_ZENITH = int((R_MIN + R_MAX) / 2)
        pygame.draw.circle(window, self.color, self.position, particle_radius)
        if show_radius:
            pygame.draw.circle(window, RED, self.position, R_MIN, 1)
            pygame.draw.circle(window, WHITE, self.position, R_ZENITH, 1)
            pygame.draw.circle(window, BLUE, self.position, R_MAX, 1)
