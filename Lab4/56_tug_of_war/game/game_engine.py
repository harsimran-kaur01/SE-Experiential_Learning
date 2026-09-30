import random
import pygame

from game.rope import Rope
from game.player import Puller


MATCH_DURATION = (
    45  # seconds before Sudden Death (set to ~8 only while recording the demo)
)
SUDDEN_DEATH_MULTIPLIER = 2


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rope = Rope(width, height)

        self.player = Puller(100, height // 2, (50, 150, 255), "PLAYER", back_dir=-1)
        self.computer = Puller(
            width - 100, height // 2, (255, 80, 80), "COMPUTER", back_dir=1
        )

        # Game state.
        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        # Match timer.
        self.match_start_time = pygame.time.get_ticks()
        self.final_elapsed = 0
        self.sudden_death = False

        # Computer settings.
        self.computer_pull_cooldown = 180
        self.computer_surge_cooldown = 150

        self.computer_normal_strength_min = 0.7
        self.computer_normal_strength_max = 1.2

        self.computer_surge_strength_min = 0.8
        self.computer_surge_strength_max = 1.2

        self.computer_surge_threshold = 80
        self.computer_panic = False

        self.last_computer_pull = pygame.time.get_ticks()

        # Fonts.
        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def get_elapsed_seconds(self):
        """Live time while playing, frozen final time once the game is over."""
        if self.game_state == "PLAYING":
            return (pygame.time.get_ticks() - self.match_start_time) // 1000
        return self.final_elapsed

    def handle_event(self, event):
        # If the game is over, only allow restart.
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                # Only alternating keys pull (holding one key does nothing).
                if event.key != self.last_key:
                    pull_strength = (
                        SUDDEN_DEATH_MULTIPLIER if self.sudden_death else 1.0
                    )
                    self.rope.pull_left(pull_strength)
                    self.last_key = event.key

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()
        elapsed_seconds = self.get_elapsed_seconds()

        # Enter Sudden Death after the match duration.
        if elapsed_seconds >= MATCH_DURATION:
            self.sudden_death = True

        # Computer panic when the flag is close to the player's goal line.
        surge_limit = self.rope.left_win_x + self.computer_surge_threshold
        self.computer_panic = self.rope.marker_x <= surge_limit

        if self.computer_panic:
            cooldown = self.computer_surge_cooldown
            strength_min = self.computer_surge_strength_min
            strength_max = self.computer_surge_strength_max
        else:
            cooldown = self.computer_pull_cooldown
            strength_min = self.computer_normal_strength_min
            strength_max = self.computer_normal_strength_max

        if now - self.last_computer_pull >= cooldown:
            strength = random.uniform(strength_min, strength_max)

            if self.sudden_death:
                strength *= SUDDEN_DEATH_MULTIPLIER

            self.rope.pull_right(strength)
            self.last_computer_pull = now

        # Check whether somebody has won.
        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.final_elapsed = elapsed_seconds  # freeze the timer
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"

        self.computer_panic = False
        self.sudden_death = False

        self.final_elapsed = 0
        self.match_start_time = pygame.time.get_ticks()
        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))

        # Mud area.
        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        center_x = self.width // 2

        # Marker position relative to center: -1 (player goal) to +1 (computer goal).
        max_distance = max(
            center_x - self.rope.left_win_x, self.rope.right_win_x - center_x
        )
        position_ratio = (self.rope.marker_x - center_x) / max_distance
        position_ratio = max(-1.0, min(1.0, position_ratio))

        # Whoever is winning leans back, whoever is losing is dragged forward.
        player_momentum = -position_ratio
        computer_momentum = position_ratio

        self.rope.render(screen)
        self.player.render(screen, player_momentum)
        self.computer.render(screen, computer_momentum)

        # Instructions.
        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        # Match timer (frozen at the final time after the game ends).
        timer_surf = self.font_small.render(
            f"Time: {self.get_elapsed_seconds()}s", True, (240, 240, 240)
        )
        screen.blit(timer_surf, (self.width - timer_surf.get_width() - 20, 15))

        # Sudden Death label.
        if self.sudden_death and self.game_state == "PLAYING":
            sudden_surf = self.font_small.render("SUDDEN DEATH", True, (255, 180, 60))
            screen.blit(sudden_surf, (self.width - sudden_surf.get_width() - 20, 45))

        # Computer panic indicator.
        if self.computer_panic and self.game_state == "PLAYING":
            panic_surf = self.font_small.render(
                "COMPUTER PANIC!", True, (255, 120, 120)
            )
            screen.blit(panic_surf, (20, 15))

        # Game Over screen.
        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50),
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (
                    self.width // 2 - restart_surf.get_width() // 2,
                    self.height // 2 + 10,
                ),
            )
