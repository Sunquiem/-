import pygame
import random
import sys

# Константы
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 50
GRID_WIDTH = 15
GRID_HEIGHT = 10
FPS = 6

# Цвета
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

last_score = 0  # Последний результат счётчика
high_score = 0  # Рекордный результат счётчика


class Cvadro:
    def __init__(self):
        self.rect = pygame.Rect(375, HEIGHT - 100, CELL_SIZE, CELL_SIZE)  # Позиция внизу экрана

    def move(self, dx):
        if 0 <= self.rect.x + dx < WIDTH - CELL_SIZE:
            self.rect.x += dx

    def shoot(self):
        return Bullet(self.rect.centerx - 5, self.rect.top)


class Meteor:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, GRID_WIDTH - 1) * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)

    def fall(self):
        self.rect.y += CELL_SIZE


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)


class Game:
    def __init__(self):
        self.cvadro = Cvadro()
        self.meteors = []
        self.bullets = []
        self.score = 0
        self.game_over = False

    def spawn_meteor(self):
        meteor = Meteor()
        self.meteors.append(meteor)

    def update(self):
        global last_score, high_score
        if not self.game_over:
            for meteor in self.meteors:
                meteor.fall()
                if meteor.rect.y >= HEIGHT - CELL_SIZE:
                    self.game_over = True

            for bullet in self.bullets:
                for meteor in self.meteors:
                    if bullet.rect.colliderect(meteor.rect):
                        self.meteors.remove(meteor)
                        self.bullets.remove(bullet)
                        self.score += 1
                        last_score = self.score
                        if last_score > high_score:
                            high_score = last_score
                        self.spawn_meteor()
                        break

            for bullet in self.bullets:
                bullet.rect.y -= 10

            # Удаляем пули за пределами экрана
            self.bullets = [bullet for bullet in self.bullets if bullet.rect.y > 0]

    def draw(self, screen):
        # Рисуем сетку
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT - 100, CELL_SIZE):
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Рисуем Cvadro
        pygame.draw.rect(screen, PURPLE, self.cvadro.rect)
        pygame.draw.polygon(screen, WHITE, [(self.cvadro.rect.right - 5, self.cvadro.rect.top + 10),
                                            (self.cvadro.rect.right - 10, self.cvadro.rect.top + 5),
                                            (self.cvadro.rect.right - 5, self.cvadro.rect.top + 5)])  # Блик

        # Рисуем метеоры
        for meteor in self.meteors:
            pygame.draw.rect(screen, RED, meteor.rect)
            pygame.draw.polygon(screen, WHITE, [(meteor.rect.right - 5, meteor.rect.top + 10),
                                                (meteor.rect.right - 10, meteor.rect.top + 5),
                                                (meteor.rect.right - 5, meteor.rect.top + 5)])  # Блик

        # Рисуем пули
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet.rect)

        # Рисуем счёт
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, GREEN)
        screen.blit(score_text, (10, 560))


class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.font1 = pygame.font.Font(None, 42)

    def draw(self, screen):
        global last_score, high_score
        screen.fill(BLACK)
        title_text = self.font.render('Квадра-лайнер', True, GREEN)
        start_text = self.font.render('Начать игру', True, GREEN)
        hint_text = self.font1.render('Пробел, чтобы начать', True, GREEN)
        best_score_text = self.font1.render(f'     Лучший результат: {high_score}', True, GREEN)
        last_score_text = self.font1.render(f'   Последний результат: {last_score}', True, GREEN)

        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        hint_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        best_score_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        last_score_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(hint_text, hint_rect)
        screen.blit(best_score_text, best_score_rect)
        screen.blit(last_score_text, last_score_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Квадра-лайнер")
    clock = pygame.time.Clock()

    menu = Menu()
    game = Game()
    in_menu = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and in_menu:
                    in_menu = False
                    game.spawn_meteor()

            if not in_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        game.cvadro.move(-CELL_SIZE)
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        game.cvadro.move(CELL_SIZE)
                    if event.key == pygame.K_e or event.key == pygame.K_SPACE:
                        bullet = game.cvadro.shoot()
                        game.bullets.append(bullet)

        if not in_menu:
            game.update()

            if game.game_over:
                in_menu = True
                game = Game()  # Сбрасываем игру

        # Отрисовка
        if in_menu:
            menu.draw(screen)
        else:
            screen.fill(BLACK)
            game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
