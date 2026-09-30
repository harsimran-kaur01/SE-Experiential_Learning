import math
import pygame


class Puller:
    """A puller on one side of the rope that tilts based on pulling momentum."""

    MAX_TILT_DEGREES = 25

    def __init__(self, x, y, color, label, back_dir):
        """
        back_dir: direction 'backwards' is for this puller.
                  -1 for the left-side player (backwards = left),
                  +1 for the right-side computer (backwards = right).
        """
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.back_dir = back_dir
        self.font = pygame.font.SysFont(None, 24)

    @staticmethod
    def _rotate(point, pivot, angle):
        """Rotate a point around a pivot by angle (radians)."""
        dx = point[0] - pivot[0]
        dy = point[1] - pivot[1]
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return (
            pivot[0] + dx * cos_a - dy * sin_a,
            pivot[1] + dx * sin_a + dy * cos_a,
        )

    def render(self, surface, momentum=0.0):
        """
        Draw the puller tilted around its feet.

        momentum: -1 to 1.
          positive -> this puller is winning, leans back
          negative -> this puller is being dragged, leans forward
        """
        momentum = max(-1.0, min(1.0, momentum))

        # Positive angle moves the top of the body to the right on screen,
        # so multiply by back_dir to make "back" point away from the rope.
        angle = math.radians(momentum * self.MAX_TILT_DEGREES) * self.back_dir

        pivot = (self.x, self.y + 35)  # feet

        # Body corners, rotated around the feet.
        corners = [
            (self.x - 20, self.y - 35),
            (self.x + 20, self.y - 35),
            (self.x + 20, self.y + 35),
            (self.x - 20, self.y + 35),
        ]
        body_points = [
            tuple(round(v) for v in self._rotate(c, pivot, angle)) for c in corners
        ]
        pygame.draw.polygon(surface, self.color, body_points)

        # Arm reaching toward the rope (forward = opposite of back_dir).
        forward = -self.back_dir
        arm_start = self._rotate((self.x, self.y - 15), pivot, angle)
        arm_end = self._rotate((self.x + forward * 38, self.y - 10), pivot, angle)
        pygame.draw.line(
            surface,
            (240, 210, 180),
            (round(arm_start[0]), round(arm_start[1])),
            (round(arm_end[0]), round(arm_end[1])),
            8,
        )

        # Head follows the tilted body.
        head = self._rotate((self.x, self.y - 50), pivot, angle)
        pygame.draw.circle(
            surface, (240, 210, 180), (round(head[0]), round(head[1])), 16
        )

        # Label stays fixed under the puller.
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))
