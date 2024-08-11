from consts import *


class Button:
    def __init__(self, text: str, x: int, y: int, font_size=48):
        # Font
        self.font_size = font_size
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        # Text render
        self.text = text
        self.rendered_text = self.font.render(text, True, WHITE)
        # Pos
        self.x, self.y = x, y
        # Rect and track pos
        self.rect = self.rendered_text.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        # Cooldown
        self.last_clicked_time = 0

    def blit(self, window) -> None:
        window.blit(self.rendered_text, (self.x, self.y))

    def hovering(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_pressed(self) -> bool:
        return self.hovering() and pygame.mouse.get_pressed()[0]

    def change_text_color(self, new_color: tuple) -> None:
        self.rendered_text = self.font.render(self.text, True, new_color)

    def update_text(self, new_text: str) -> None:
        self.rendered_text = self.font.render(new_text, True, WHITE)
