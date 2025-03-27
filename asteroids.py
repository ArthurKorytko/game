import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIP_SPEED = 5
BULLET_SPEED = 7
COOLDOWN_TIME = 0.5
ASTEROID_SPEED = (2, 4)
LIVES = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

font = pygame.font.Font(None, 36)

ship_img = pygame.image.load("assets/ship.png")
asteroid_imgs = [
    pygame.image.load("assets/asteroid.png"),
    pygame.image.load("assets/asteroid2.png")
]
bullet_img = pygame.image.load("assets/bullet.png")
heart_img = pygame.image.load("assets/heart.png")

heart_img = pygame.transform.scale(heart_img, (30, 30))


class Ship:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT - 60
        self.image = pygame.transform.scale(ship_img, (50, 50))
        self.last_shot_time = 0

    def move(self, keys):
        if keys[pygame.K_a] and self.x > 0:
            self.x -= SHIP_SPEED
        if keys[pygame.K_d] and self.x < WIDTH - 50:
            self.x += SHIP_SPEED
        if keys[pygame.K_w] and self.y > HEIGHT // 2:
            self.y -= SHIP_SPEED
        if keys[pygame.K_s] and self.y < HEIGHT - 50:
            self.y += SHIP_SPEED

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= COOLDOWN_TIME:
            self.last_shot_time = current_time
            bullets.append(Bullet(self.x + 20, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(-100, -50)
        self.speed = random.uniform(*ASTEROID_SPEED)
        self.image = pygame.transform.scale(
            random.choice(asteroid_imgs), (50, 50))

    def move(self):
        global score, lives
        self.y += self.speed
        if self.y > HEIGHT:
            score -= 10
            self.reset()

    def reset(self):
        self.y = random.randint(-100, -50)
        self.x = random.randint(0, WIDTH - 50)
        self.speed = random.uniform(*ASTEROID_SPEED)
        self.image = pygame.transform.scale(
            random.choice(asteroid_imgs), (50, 50))

    def check_collision_with_ship(self, ship):
        global lives
        if ship.x < self.x + 50 and ship.x + 50 > self.x and ship.y < self.y + 50 and ship.y + 50 > self.y:
            lives -= 1
            self.reset()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.transform.scale(bullet_img, (10, 20))

    def move(self):
        self.y -= BULLET_SPEED

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def check_collisions():
    global score
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if asteroid.x < bullet.x < asteroid.x + 50 and asteroid.y < bullet.y < asteroid.y + 50:
                bullets.remove(bullet)
                asteroid.reset()
                score += 10
                break


def draw_lives():
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 35, 10))


ship = Ship()
asteroids = [Asteroid() for _ in range(5)]
bullets = []
score = 0
lives = LIVES

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ship.move(keys)
    if keys[pygame.K_SPACE]:
        ship.shoot()

    for asteroid in asteroids:
        asteroid.move()
        asteroid.check_collision_with_ship(ship)
    for bullet in bullets:
        bullet.move()

    check_collisions()

    bullets = [bullet for bullet in bullets if bullet.y > 0]

    ship.draw()
    for asteroid in asteroids:
        asteroid.draw()
    for bullet in bullets:
        bullet.draw()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 20))

    draw_lives()

    if lives <= 0:
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
