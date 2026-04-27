import pygame
import random

pygame.init()

class Sprite:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Bird(Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height)

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))

        self._gravity = 0.1
        self.speed_vertical = 0

    def gravity(self):
        if self.speed_vertical < 0:
            self.image = pygame.image.load("Images/sprite_0.png")
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.image.load("Images/sprite_1.png")
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        self.speed_vertical += self._gravity
        self.rect.y += self.speed_vertical

    def draw(self, window):
        window.blit(self.image, self.rect)

class Pipe(Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height)
        self.passed = False
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = 3

    def move(self):
        self.rect.x -= self.speed

    def draw(self, window):
        window.blit(self.image, self.rect)


pipes = []
pipe_timer = 0
pipe_delay = 120
gap = 170

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

bg = pygame.image.load("Images/fon.png")
bg = pygame.transform.scale(bg, (800, 600))

bird = Bird(100, 100, 60, 60, "Images/sprite_1.png")
score = 0

running_two = True
running = True
while running:
    window.fill((0, 0, 0))
    window.blit(bg, (0, 0))
    bird.draw(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running_two = False
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird.speed_vertical -= 0.3

    bird.gravity()

    pipe_timer += 1

    if pipe_timer >= pipe_delay:
        pipe_timer = 0

        gap_y = random.randint(200, 400)

        top_pipe = Pipe(800, gap_y - gap - 400, 100, 400, "Images/pipe2.png")
        bottom_pipe = Pipe(800, gap_y, 100, 400, "Images/pipe.png")

        pipes.append(top_pipe)
        pipes.append(bottom_pipe)

    for pipe in pipes:
        pipe.move()
        pipe.draw(window)

    pipes = [pipe for pipe in pipes if pipe.rect.right > 0]

    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect):
            running = False

        if not pipe.passed and pipe.rect.right < bird.rect.left:
            pipe.passed = True
            score += 0.5

    text = font.render(str(int(score)), True, (255, 255, 255))
    window.blit(text, (400, 0))

    if bird.rect.y + 60 >= 600:
        running = False
    if bird.rect.y <= 0:
        running = False

    clock.tick(60)
    pygame.display.update()

end_timer = 0

if running_two:
    while end_timer < 60:
        window.fill((0, 0, 0))
        window.blit(bg, (0, 0))

        end_text = font.render(f"The End", True, (255, 255, 255))
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))

        window.blit(end_text, (400 - end_text.get_width() // 2, 200))
        window.blit(score_text, (400 - score_text.get_width() // 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                end_timer = 60

        pygame.display.update()
        clock.tick(60)
        end_timer += 1

pygame.quit()