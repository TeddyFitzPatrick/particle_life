from consts import *


class Button:
    def __init__(self, text_str: str, x: int, y: int, font_size=48, text_color=WHITE):
        # Font
        self.font_size = font_size
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        # Text color
        self.text_color = text_color
        # Text render
        self.text_str = text_str
        self.rendered_text = self.font.render(text_str, True, WHITE)
        # Pos
        self.x, self.y = x, y
        # Rect and track pos
        self.rect = self.rendered_text.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def blit(self, window) -> None:
        window.blit(self.rendered_text, (self.x, self.y))

    def hovering(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_pressed(self) -> bool:
        return self.hovering() and pygame.mouse.get_pressed()[0]

    def update_text(self, new_text: str) -> None:
        self.rendered_text = self.font.render(new_text, True, self.text_color)

    def update_color(self, new_color: tuple[int, int, int]) -> None:
        self.text_color = new_color
        self.update_text(self.text_str)
