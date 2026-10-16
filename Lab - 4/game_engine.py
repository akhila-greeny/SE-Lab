import pygame
from .player import Player
from .obstacle import Obstacle
from .sound import SoundManager

# Game Engine

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)
BLACK = (0, 0, 0)

JUMP_KEYS = (pygame.K_SPACE, pygame.K_UP, pygame.K_w)

# Starting speed, frames between obstacle spawns, and the speed ceiling for
# each difficulty. The ceiling is what keeps long runs fair (Task 1).
DIFFICULTIES = {
    "Easy":   {"start_speed": 5, "spawn_interval": 90, "max_speed": 11},
    "Medium": {"start_speed": 6, "spawn_interval": 70, "max_speed": 13},
    "Hard":   {"start_speed": 8, "spawn_interval": 55, "max_speed": 15},
}
DIFFICULTY_KEYS = {
    pygame.K_1: "Easy",
    pygame.K_2: "Medium",
    pygame.K_3: "Hard",
}

PLAYING = "playing"
GAME_OVER = "game_over"


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 40

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.sounds = SoundManager()

        self.speed_increase_per_frame = 0.003
        self.quit_requested = False

        self.start_game("Medium")

    def start_game(self, difficulty):
        """Reset everything for a fresh run at the chosen difficulty."""
        settings = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.speed = settings["start_speed"]
        self.max_speed = settings["max_speed"]
        self.spawn_interval = settings["spawn_interval"]

        self.player = Player(80, self.ground_y)
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0
        self.state = PLAYING

    @property
    def game_over(self):
        return self.state == GAME_OVER

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.state == PLAYING:
            if event.key in JUMP_KEYS and self.player.jump():
                self.sounds.play("jump")
        else:
            if event.key in DIFFICULTY_KEYS:
                self.start_game(DIFFICULTY_KEYS[event.key])
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.quit_requested = True

    def handle_input(self):
        # Reserved for continuously-held-key input; this runner only
        # needs an edge-triggered jump, handled in handle_event.
        pass

    def update(self):
        if self.state != PLAYING:
            return

        # Speed still ramps up, but now stops at the difficulty's ceiling.
        self.speed = min(self.speed + self.speed_increase_per_frame, self.max_speed)
        self.player.update()

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.obstacles.append(Obstacle(self.width, self.ground_y, self.speed))

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.speed = self.speed

        # Collision uses the swept rect (the whole path travelled this frame),
        # so a fast obstacle can never skip over the player's hitbox.
        player_rect = self.player.rect()
        for obstacle in self.obstacles:
            if obstacle.swept_rect().colliderect(player_rect):
                self.state = GAME_OVER
                self.sounds.play("game_over")
                return

        for obstacle in self.obstacles:
            if not obstacle.scored and obstacle.x + obstacle.width < self.player.x:
                obstacle.scored = True
                self.score += 1
                self.sounds.play("score")

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]

        self.distance += self.speed

    def render(self, screen):
        pygame.draw.line(screen, BROWN, (0, self.ground_y), (self.width, self.ground_y), 4)

        pygame.draw.rect(screen, WHITE, self.player.rect())
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, DARK_GREEN, obstacle.rect())

        if self.state == PLAYING:
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            level_text = self.small_font.render(self.difficulty, True, BLACK)
            screen.blit(level_text, (self.width - level_text.get_width() - 10, 12))
        else:
            self._render_game_over(screen)

    def _centered(self, screen, surface, y):
        screen.blit(surface, ((self.width - surface.get_width()) // 2, y))

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        self._centered(screen, self.big_font.render("GAME OVER", True, WHITE), 50)
        self._centered(screen, self.font.render(f"Final Score: {self.score}", True, WHITE), 135)
        self._centered(screen, self.small_font.render("Play again - choose a difficulty:", True, WHITE), 205)
        self._centered(screen, self.small_font.render("1 = Easy     2 = Medium     3 = Hard", True, WHITE), 245)
        self._centered(screen, self.small_font.render("Q or Esc = Exit", True, WHITE), 295)
