import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Model")
BG_IMG = pygame.image.load("stars-galaxy.jpg")
SCALE = 250e6 / 400
FPS = 30
SEC_PER_YEAR = 10
SEC_PER_FRAME = 3600 * 24 * 365 / (FPS * SEC_PER_YEAR)
G = 6.67e-11  # N.m2/kg2


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


    def gravity(self, other):
        # gravity adds the acceleration from another planet
        dx_km = other.x_km - self.x_km
        dy_km = other.y_km - self.y_km
        dist_m_sqr = (dx_km * 1e3) ** 2 + (dy_km * 1e3) ** 2
        grav_amp = G * other.mass_kg / dist_m_sqr
        grav_ang = math.atan2(dy_km, dx_km)
        self.ax_kms2 += grav_amp * math.cos(grav_ang) / 1000
        self.ay_kms2 += grav_amp * math.sin(grav_ang) / 1000

    def advance(self, period_s):
        self.x_km += self.vx_kms * period_s
        self.y_km += self.vy_kms * period_s
        self.vx_kms += self.ax_kms2 * period_s
        self.vy_kms += self.ay_kms2 * period_s
        print(f"vx: {self.vx_kms}, vy: {self.vy_kms}, vtotal: {math.sqrt(self.vx_kms**2 + self.vy_kms**2)}")
        self.ax_kms2 = 0
        self.ay_kms2 = 0

    def draw(self):
        pygame.draw.circle(win, self.color, (int(WIDTH / 2 + self.x_km / SCALE - self.radius_px / 2),
                                             int(HEIGHT / 2 + self.y_km / SCALE - self.radius_px / 2)), self.radius_px)


def main():

    # create planets
    planets = \
        [Planet("Sun", 1.989e30, 0, (255, 204, 51), 30, 0, 0, True),
         Planet("Mercury", 0.3285e24, 57.9e6, (56, 56, 56), 5, 0, 47.4)]#,
         #Planet("Venus", 4.87e24, 108.2e6, (230, 230, 230), 10, 90, 35.0),
         #Planet("Earth", 5.97e24, 149.6e6, (47, 106, 105), 12, 180, 29.8),
         #Planet("Mars", 0.642e24, 228.0e6, (153, 61, 0), 9, 270, 24.1)]

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.blit(BG_IMG, (0, 0))
        for planet in planets:
            if not planet.is_star:
            #    for other in planets:
            #        if other.name != planet.name:
                planet.gravity(planets[0])
                planet.advance(SEC_PER_FRAME)
            planet.draw()

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
