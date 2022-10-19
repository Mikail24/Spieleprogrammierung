import os
import pygame
import time
import random


class Settings():                                   # Statische Klasse
    SCREENRECT = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    PATHFILE = os.path.dirname(os.path.abspath(__file__))
    PATHIMG = os.path.join(PATHFILE, "images")

    @staticmethod
    def get_imagepath(filename):
        return os.path.join(Settings.PATHIMG, filename)


class Alien(pygame.sprite.Sprite):
    def __init__(self, filename, colorkey=None) -> None:
        super().__init__()
        if colorkey is None:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert_alpha()
        else:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert()
            self.image.set_colorkey(colorkey)

        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.vel = [0, 0]

    def update(self) -> None:
        self.rect.left += self.vel[0]
        self.rect.top += self.vel[1]
        if self.rect.right >= Settings.SCREENRECT.width or self.rect.left < 0:
            self.vel[0] *= -1
        if self.rect.bottom >= Settings.SCREENRECT.height or self.rect.top < 0:
            self.vel[1] *= -1
        return super().update()


class Game():
    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()                                   # Subsysteme starten
        self.screen = pygame.display.set_mode(Settings.SCREENRECT.size)    # Bildschirm/Fenster dimensionieren
        self.clock = pygame.time.Clock()                     # Taktgeber

        self.all_aliens = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()

        self.background = pygame.image.load(Settings.get_imagepath("background03.png")).convert()
        self.background = pygame.transform.scale(self.background, Settings.SCREENRECT.size)

        cactus = Alien("icons8-kaktus-100.png", (0, 0, 0))
        cactus.rect.topleft = (0, 0)
        cactus.vel = [5, 2]
        self.all_aliens.add(cactus)

        baloon = Alien("icons8-baloon-64.png")
        baloon.rect.topleft = (0, 0)
        baloon.vel = [2, -1]
        self.all_aliens.add(baloon)

        cherry = Alien("icons8-cherry-64.png")
        cherry.rect.right = 900
        cherry.rect.bottom = 500
        cherry.vel = [0, 0]
        self.all_obstacles.add(cherry)

        strawberry = Alien("icons8-erdbeere-48.png")
        strawberry.rect.right = 500
        strawberry.rect.bottom = 200
        strawberry.vel = [0, 0]
        self.all_obstacles.add(strawberry)

        fruit = Alien("icons8-fruit-64.png")
        fruit.rect.right = 200
        fruit.rect.bottom = 550
        fruit.vel = [0, 0]
        self.all_obstacles.add(fruit)

        watermelon = Alien("icons8-wassermelone-48.png")
        watermelon.rect.right = 700
        watermelon.rect.bottom = 350
        watermelon.vel = [0, 0]
        self.all_obstacles.add(watermelon)

        raspberry = Alien("icons8-himbeere-48.png")
        raspberry.rect.right = 500
        raspberry.rect.bottom = 450
        raspberry.vel = [0, 0]
        self.all_obstacles.add(raspberry)

        self.entry_before = 0
        self.running = True                                  # Flagvariable

    def start(self):
        while self.running:                                  # Hauptprogrammschleife
            self.clock.tick(Settings.FPS)                    # Auf mind. 1/60s takten
            self.watch_for_events()
            self.update()
            self.draw()
            self.entry()
            self.vanish()

        pygame.quit()                                   # Subssysteme stoppen

    def watch_for_events(self):
        for event in pygame.event.get():            # Einlesen der Message-Queue
            if event.type == pygame.QUIT:           # Ist X angeklickt worden?
                self.running = False                     # Toggle Flag
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.all_aliens.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_aliens.draw(self.screen)
        self.all_obstacles.draw(self.screen)
        pygame.display.flip()

    def entry(self):
        path_cactus = [1, 4, 7, 9]
        path_baloon = [1, 4, 7, 9]

        if int(time.time()) >= self.entry_before + 1:
            cactus = Alien("icons8-kaktus-100.png")
            cactus.rect.topleft = (0, 0)
            cactus.vel = [4, random.choice(path_cactus)]
            self.all_aliens.add(cactus)

            baloon = Alien("icons8-baloon-64.png")
            baloon.rect.topleft = (0, 0)
            baloon.vel = [2, random.choice(path_baloon)]
            self.all_aliens.add(baloon)

            self.entry_before = int(time.time())


    def vanish(self):
        for sprite in self.all_aliens.sprites():
            if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                sprite.kill()

def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()