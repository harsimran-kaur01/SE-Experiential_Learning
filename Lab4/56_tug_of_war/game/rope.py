import pygame
import math


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"

        if self.marker_x >= self.right_win_x:
            return "COMPUTER"

        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.velocity = 0.0

    def render(self, surface):
        center_x = self.screen_width // 2

        # Calculate tension from how far the marker is from the center.
        distance_from_center = abs(self.marker_x - center_x)

        max_distance = max(center_x - self.left_win_x, self.right_win_x - center_x)

        tension = min(distance_from_center / max_distance, 1.0)

        # Stronger tension = larger vertical vibration.
        wave_amplitude = 2 + (10 * tension)

        # Time controls the animation.
        time = pygame.time.get_ticks() / 100.0

        points = []

        rope_start = 60
        rope_end = self.screen_width - 60
        segment_count = 40

        for i in range(segment_count + 1):
            x = rope_start + ((rope_end - rope_start) * i / segment_count)

            # The wave gets stronger as tension increases.
            wave = math.sin(time + i * 0.6) * wave_amplitude

            # Reduce the wave near the ends so the rope
            # stays visually anchored.
            edge_factor = math.sin(math.pi * i / segment_count)

            y = self.center_y + wave * edge_factor

            points.append((int(x), int(y)))

        # Draw rope.
        pygame.draw.lines(surface, (180, 140, 90), False, points, 10)

        # Left goal marker.
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4,
        )

        # Right goal marker.
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4,
        )

        # Center marker.
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (center_x, self.center_y - 20),
            (center_x, self.center_y + 20),
            2,
        )

        # Flag remains tied to marker_x.
        flag_rect = pygame.Rect(int(self.marker_x) - 12, self.center_y - 24, 24, 48)

        pygame.draw.rect(surface, (230, 40, 40), flag_rect, border_radius=4)

        pygame.draw.rect(surface, (255, 255, 255), flag_rect, width=2, border_radius=4)
