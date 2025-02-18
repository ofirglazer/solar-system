import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Model")

BG_IMG = pygame.image.load("stars-galaxy.jpg")
SCALE = 1700e6 / 400
TIMESTEP = 3600 * 24  # 1 day in seconds
SEC_PER_YEAR = 10
FPS = 90

SEC_PER_FRAME = 3600 * 24 * 365 / (FPS * SEC_PER_YEAR)
G = 6.67428e-11  # N.m2/kg2


class Planet:
    def __init__(self, name, mass_kg, orbit_km, color, radius_px, init_angle, init_vel_kms, is_star=False):
        self.name = name
        self.mass_kg = mass_kg
        self.color = color
        self.radius_px = radius_px  # TODO real radii proportions
        self.x_km = orbit_km * math.cos(math.radians(init_angle))
        self.y_km = orbit_km * math.sin(math.radians(init_angle))
        self.vx_kms = init_vel_kms * math.sin(math.radians(init_angle))
        self.vy_kms = -init_vel_kms * math.cos(math.radians(init_angle))
        self.is_star = is_star

        self.ax_kms2 = 0
        self.ay_kms2 = 0
        self.orbit_point = [(int(WIDTH / 2 + self.x_km / SCALE - self.radius_px / 2),
                                             int(HEIGHT / 2 + self.y_km / SCALE - self.radius_px / 2))]

    def gravity(self, planets):
        # gravity adds the acceleration from another planet

        for other in planets:
            if other.name != self.name:
                dx_km = other.x_km - self.x_km
                dy_km = other.y_km - self.y_km
                dist_m_sqr = (dx_km * 1e3) ** 2 + (dy_km * 1e3) ** 2
                grav_amp = G * other.mass_kg / dist_m_sqr
                grav_ang = math.atan2(dy_km, dx_km)
                self.ax_kms2 += grav_amp * math.cos(grav_ang) / 1000
                self.ay_kms2 += grav_amp * math.sin(grav_ang) / 1000

    def advance(self, period_s):
        self.vx_kms += self.ax_kms2 * period_s
        self.vy_kms += self.ay_kms2 * period_s
        self.x_km += self.vx_kms * period_s
        self.y_km += self.vy_kms * period_s
        # print(f"{self.name} orbit: {math.sqrt(self.x_km**2 + self.y_km**2)}")
        self.ax_kms2 = 0
        self.ay_kms2 = 0
        self.orbit_point.append((int(WIDTH / 2 + self.x_km / SCALE - self.radius_px / 2),
                                             int(HEIGHT / 2 + self.y_km / SCALE - self.radius_px / 2)))

    def draw(self):
        pygame.draw.circle(win, self.color, (int(WIDTH / 2 + self.x_km / SCALE - self.radius_px / 2),
                                             int(HEIGHT / 2 + self.y_km / SCALE - self.radius_px / 2)), self.radius_px)
        if not self.is_star:
            pygame.draw.lines(win, self.color, False, self.orbit_point, 2)


def main():

    # create planets
    planets = \
        [Planet("Sun", 1.98892e30, 0, (255, 204, 51), 5, 0, 0, True),
         Planet("Mercury", 0.33e24, 57.8952e6, (56, 56, 56), 1, 0, 47.4),
         Planet("Venus", 4.8685e24, 108.1608e6, (230, 230, 230), 2, 90, 35.02),
         Planet("Earth", 5.97e24, 149.6e6, (47, 106, 105), 2, 180, 29.783),
         Planet("Mars", 0.639e24, 227.9904e6, (153, 61, 0), 2, 270, 24.077),
         Planet("Jupiter", 1898e24, 778.5e6, (176, 127, 53), 4, 270, 13.1),
         Planet("Saturn", 568e24, 1432.0e6, (176, 143, 54), 4, 270, 9.7)]

    running = True
    clock = pygame.time.Clock()

    day_count = 0.0
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.blit(BG_IMG, (0, 0))
        for planet in planets:
            planet.gravity(planets)
            if not planet.is_star:
                planet.advance(TIMESTEP)
            planet.draw()
        day_count += 0.25
        # print(f"day count: {day_count}")

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
