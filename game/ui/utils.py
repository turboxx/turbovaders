import pygame


def renderText(win, text, color, size, position):
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    img = font.render(text, True, color)
    rect = img.get_rect()
    (x, y) = position
    rect.topleft = (x - rect.width / 2, y - size / 2)
    win.blit(img, rect)
