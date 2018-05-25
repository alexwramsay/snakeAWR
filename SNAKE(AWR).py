import pygame
import sys
import random
import os
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (45, 45, 45)
RED = (208, 44, 48)
GOLD = (212, 175, 55)
BRONZE = (108, 84, 30)
GREEN = (0, 255, 0)
SILVER = (113, 128, 128)
DIAMOND = (185, 242, 255)
PLATINUM = (90, 89, 89)

WIN_W = 500
WIN_H = 500
START_X = WIN_W / 2
START_Y = WIN_H / 2

SNAKE_SEG = APPLE = CELL = 10

pygame.init()


class Text:
    def __init__(self, size, text, xpos, ypos, color):
        self.font = pygame.font.SysFont("Arial Rounded MT Bold", size)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
        self.high_score = 0
        self.clock = pygame.time.Clock()
        self.play = self.intro = True
        self.score = 0
        self.snake_score = Text(15, "SNAKE SCORE: " + str(self.score), 75, 5, BLACK)
        self.snake_high_score = Text(15, "SNAKE HIGH SCORE: " + str(self.high_score), 420, 5, BLACK)
        self.outro = True
        self.background = pygame.image.load("image/3bc9070f040fe66.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_W, WIN_H))
        self.first = True
        self.fps = 60
        self.intro_backround = pygame.image.load("image/IntroBackground.jpg").convert_alpha()
        self.intro_backround = pygame.transform.scale(self.intro_backround, (WIN_W, WIN_H))
        self.intro_rect = self.intro_backround.get_rect()
        self.outro_backround = pygame.image.load("image/OutroBackground.jpg").convert_alpha()
        self.outro_backround = pygame.transform.scale(self.outro_backround, (WIN_W, WIN_H))
        self.outro_rect = self.outro_backround.get_rect()
        self.beg_time = pygame.time.get_ticks()
        self.title = Text(86, "SNAKE!", WIN_W / 2, WIN_H / 20, GREEN)
        self.big_title = Text(86, "SNAKE!", WIN_W / 2 + 5, WIN_H / 20 + 5, BLACK)
        self.s = Text(35, "Click Anywhere To Start", WIN_W / 2, WIN_H / 1.2, BLACK)
        self.run_order = 0
        self.game_over = Text(50, "Game Over", WIN_W / 2, WIN_H / 10, BLACK)
        self.score_outro = Text(40, "Your Score Was - " + str(self.score), WIN_W / 2, WIN_H / 5, BLACK)
        self.high_score_outro = Text(35, "High Score - " + str(self.high_score), WIN_W / 2, WIN_H / 3.5, BLACK)
        self.click = Text(35, "Click Anywhere To Restart", WIN_W / 2, WIN_H / 1.2, BLACK)

    def blink(self, s, s_rect):
        cur_time = pygame.time.get_ticks()
        if ((cur_time - self.beg_time) % 1000) < 500:
            self.screen.blit(s, s_rect)


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, pos):
        pygame.sprite.Sprite.__init__(self)
        self.height = SNAKE_SEG
        self.width = SNAKE_SEG
        self.image = pygame.Surface((SNAKE_SEG, SNAKE_SEG)).convert()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(x, y, SNAKE_SEG, SNAKE_SEG)
        self.dx = dx
        self.dy = dy
        self.position = pos

    def collide(self, apple):
        if self.rect.x < apple.rect.x + APPLE and self.rect.x + SNAKE_SEG > apple.rect.x and \
                        self.rect.y < apple.rect.y + APPLE and SNAKE_SEG + self.rect.y > apple.rect.y:
            return True

    def update(self, apple, run, snake_group, snake_array, iteration):
        apple = apple
        if self.position == 0:

            for s in snake_group:
                s.position += 1
            if self.dx == 0 and self.dy == -1:
                snake_add = Snake(self.rect.x, self.rect.y - 10, self.dx, self.dy, 0)
                snake_group.add(snake_add)
                snake_array.insert(0, snake_add)
            elif self.dx == 1 and self.dy == 0:
                snake_add = Snake(self.rect.x + 10, self.rect.y, self.dx, self.dy, 0)
                snake_group.add(snake_add)
                snake_array.insert(0, snake_add)
            elif self.dx == -1 and self.dy == 0:
                snake_add = Snake(self.rect.x - 10, self.rect.y, self.dx, self.dy, 0)
                snake_group.add(snake_add)
                snake_array.insert(0, snake_add)
            elif self.dx == 0 and self.dy == 1:
                snake_add = Snake(self.rect.x, self.rect.y + 10, self.dx, self.dy, 0)
                snake_group.add(snake_add)
                snake_array.insert(0, snake_add)

            for s in snake_group:
                if self.collide(s) and self != s:
                    run.play = False
                    run.outro = True
            if self.collide(apple):
                run.score += 1
                if run.score > run.high_score:
                    run.high_score = run.score
                    if iteration > 0 and run.first:
                        hs = Text(22, "You just got a new high score of" + str(run.score) + "!", WIN_W / 2, WIN_H /\
                                  1.2, BLACK)
                        run.screen.blit(hs.image, hs.rect)
                        pygame.display.flip()
                        time.sleep(1.5)
                        run.first = False
                run.snake_score = Text(15, "SNAKE SCORE: " + str(run.score), 75, 5, BLACK)
                run.snake_high_score = Text(15, "SNAKE HIGH SCORE: " + str(run.high_score), 420, 5, BLACK)
                run.score_outro = Text(40, "Your Score Was - " + str(run.score), WIN_W / 2, WIN_H / 5, BLACK)
                run.high_score_outro = Text(35, "High Score - " + str(run.high_score), WIN_W / 2, WIN_H / 3.5, BLACK)
                apple.reposition()

            else:
                for s in snake_group:
                    if s.position == len(snake_group.sprites()) - 1:
                        s.kill()
                        snake_array.remove(s)
                        break

            if run.score == 5 and run.run_order == 0:
                self.achievement(1, run)
                run.run_order = 1
            if run.score == 10 and run.run_order == 1:
                self.achievement(2, run)
                run.run_order = 2
            if run.score == 20 and run.run_order == 2:
                self.achievement(3, run)
                run.run_order = 3
            if run.score == 50 and run.run_order == 3:
                self.achievement(4, run)
                run.run_order = 4
            if run.score == 500 and run.run_order == 4:
                self.achievement(5, run)
                run.play = False
                run.outro = True

        key = pygame.key.get_pressed()
        for s in snake_group:
            if s.position == 0:
                if key[pygame.K_w] and not (len(snake_array) > 1 and snake_array[1].rect.y == s.rect.y - 10):
                    s.dy = -1
                    s.dx = 0
                elif key[pygame.K_s] and not (len(snake_array) > 1 and snake_array[1].rect.y == s.rect.y + 10):
                    s.dy = 1
                    s.dx = 0
                if key[pygame.K_a] and not (len(snake_array) > 1 and snake_array[1].rect.x == s.rect.x - 10):
                    s.dy = 0
                    s.dx = -1
                elif key[pygame.K_d] and not (len(snake_array) > 1 and snake_array[1].rect.x == s.rect.x + 10):
                    s.dy = 0
                    s.dx = 1
                if key[pygame.K_UP] and not (len(snake_array) > 1 and snake_array[1].rect.y == s.rect.y - 10):
                    s.dy = -1
                    s.dx = 0
                elif key[pygame.K_DOWN] and not (len(snake_array) > 1 and snake_array[1].rect.y == s.rect.y + 10):
                    s.dy = 1
                    s.dx = 0
                if key[pygame.K_LEFT] and not (len(snake_array) > 1 and snake_array[1].rect.x == s.rect.x - 10):
                    s.dy = 0
                    s.dx = -1
                elif key[pygame.K_RIGHT] and not (len(snake_array) > 1 and snake_array[1].rect.x == s.rect.x + 10):
                    s.dy = 0
                    s.dx = 1
        if self.rect.right > WIN_W or self.rect.left < 0 or self.rect.top < 0 or self.rect.bottom > WIN_H:
            run.play = False
            run.outro = True

    def achievement(self, num, run):
        # Limits frames per iteration of while loop
        run.clock.tick(10)
        if num == 1:
            a2 = Text(28, "You just earned a BRONZE MEDAL!", WIN_W / 2, WIN_H / 1.2, BRONZE)
            a1 = Text(19, "That was time well serpent!", WIN_W / 2, WIN_H / 1.1, BRONZE)
            run.screen.blit(a1.image, a1.rect)
            run.screen.blit(a2.image, a2.rect)
        if num == 2:
            a2 = Text(28, "You just earned a SILVER MEDAL!", WIN_W / 2, WIN_H / 1.2, SILVER)
            a1 = Text(19, "Now viper that smirk off your face!", WIN_W / 2, WIN_H / 1.1, SILVER)
            run.screen.blit(a1.image, a1.rect)
            run.screen.blit(a2.image, a2.rect)
        if num == 3:
            a2 = Text(28, "You just earned a GOLD MEDAL!", WIN_W / 2, WIN_H / 1.2, GOLD)
            a1 = Text(19, "...But don't stop shimmien' now!", WIN_W / 2, WIN_H / 1.1, GOLD)
            run.screen.blit(a1.image, a1.rect)
            run.screen.blit(a2.image, a2.rect)
        if num == 4:
            a2 = Text(28, "You just earned a PLATINUM MEDAL!", WIN_W / 2, WIN_H / 1.2, PLATINUM)
            a1 = Text(19, "You're lookin' like a snake!", WIN_W / 2, WIN_H / 1.1, PLATINUM)
            run.screen.blit(a1.image, a1.rect)
            run.screen.blit(a2.image, a2.rect)
        if num == 5:
            a2 = Text(28, "You just earned a DIAMOND MEDAL!", WIN_W / 2, WIN_H / 1.2, DIAMOND)
            a1 = Text(19, "No more hissterical jokes :(", WIN_W / 2, WIN_H / 1.1, DIAMOND)
            run.screen.blit(a1.image, a1.rect)
            run.screen.blit(a2.image, a2.rect)
        pygame.display.flip()
        time.sleep(3)


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rand_x = random.randrange(0, WIN_W, 10)
        rand_y = random.randrange(0, WIN_H, 10)
        self.x = rand_x
        self.y = rand_y
        self.image = pygame.Surface((APPLE, APPLE)).convert()
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (APPLE, APPLE))
        self.rect = pygame.Rect(self.x, self.y, APPLE, APPLE)

    def reposition(self):
        rand_x = random.randrange(0, WIN_W, 10)
        rand_y = random.randrange(0, WIN_H, 10)
        self.x = rand_x
        self.y = rand_y
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, APPLE, APPLE)


def main():
    pygame.display.set_caption('SNAKE!')
    run = Game()
    run.score = 0
    snake_group = pygame.sprite.Group()
    iteration = 0

    while True:
        run.score = 0
        snake = Snake(START_X, START_Y, 1, 0, 0)
        snake_group.add(snake)
        snake_array = [snake]
        apple = Apple()
        while run.intro:
            # Print background
            run.screen.fill(WHITE)
            run.screen.blit(run.intro_backround, run.intro_rect)
            run.screen.blit(run.title.image, run.title.rect)
            run.screen.blit(run.big_title.image, run.big_title.rect)
            # Blinking Text: Click here to start

            run.blink(run.s.image, run.s.rect)

            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    run.screen.blit(run.s.image, run.s.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.intro = False
                    run.play = True

            # Limits frames per iteration of while loop
            run.clock.tick(run.fps)
            # Writes to main surface
            pygame.display.flip()

        while run.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Keypresses

            for s in snake_group:
                s.update(apple, run, snake_group, snake_array, iteration)

            run.screen.blit(run.background, (0, 0))

            for s in snake_group:
                run.screen.blit(s.image, s.rect)
            run.screen.blit(apple.image, apple.rect)
            run.screen.blit(run.snake_score.image, run.snake_score.rect)
            run.screen.blit(run.snake_high_score.image, run.snake_high_score.rect)
            # Limits frames per iteration of while loop
            run.clock.tick(10)
            pygame.display.flip()

        while run.outro:
            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    pygame.time.wait(1500)
                    run.outro = False
                    run.intro = True
                    snake.rect.x = START_X
                    snake.rect.y = START_Y
                    for s in snake_group:
                        s.kill()
                    run.score = 0
                    run.snake_score = Text(15, "SNAKE SCORE: " + str(run.score), 75, 5, BLACK)
                    run.score_outro = Text(40, "Your Score Was - " + str(run.score), WIN_W / 2, WIN_H / 5, BLACK)
                    iteration += 1
                    run.first = True

            run.screen.blit(run.outro_backround, (0, 0))
            run.screen.blit(run.game_over.image, run.game_over.rect)
            run.screen.blit(run.score_outro.image, run.score_outro.rect)
            run.screen.blit(run.high_score_outro.image, run.high_score_outro.rect)
            run.blink(run.click.image, run.click.rect)

            # Limits frames per iteration of while loop
            run.clock.tick(run.fps)
            # Writes to main surface
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    main()

