import pygame
from .paddle import Paddle
from .ball import Ball
import random

pygame.mixer.init()  # Initialize Pygame mixer

# Game Engine
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Load sound effects
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, self)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # Default target
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move(self.player, self.ai)

        # Check scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    # ---------------- Game Over & Replay ---------------- #
    def check_game_over(self, screen):
        winner = None

        if self.player_score >= self.winning_score:
            winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner = "AI Wins!"

        if winner:
            # Display winner message
            font_large = pygame.font.SysFont("Arial", 50)
            text_surface = font_large.render(winner, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            # Wait 1 second before showing replay menu
            pygame.time.wait(1000)
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 35)
        instructions = [
            "Choose Best of 3, 5, 7, or ESC to Exit:",
            "Press 3 -> Best of 3",
            "Press 5 -> Best of 5",
            "Press 7 -> Best of 7",
            "Press ESC -> Exit"
        ]

        screen.fill((0, 0, 0))
        for i, line in enumerate(instructions):
            text_surface = menu_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 60 + i*40))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 3
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 5
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 7
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

        # Reset scores and ball for new match
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
