import sys
import os
import pygame


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['MARIO', 'правила:',
                  'ходить на стрелочки', 'всё']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += (HEIGHT - 100) / len(intro_text)
        intro_rect.centerx = WIDTH / 2
        intro_rect.centery = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    pygame.display.flip()
    pygame.time.wait(10)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    height = len(level_map)
    return list(map(lambda x: x.ljust(max_width, '.'), level_map)), max_width, height


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, walls_group)
        else:
            super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, event):
        if event.key == pygame.K_DOWN:
            self.rect.y += tile_height
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= tile_height
        if event.key == pygame.K_UP:
            self.rect.y -= tile_height
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += tile_height
        if event.key == pygame.K_RIGHT:
            self.rect.x += tile_width
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= tile_height
        if event.key == pygame.K_LEFT:
            self.rect.x -= tile_width
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += tile_height


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player


walls_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None

if __name__ == '__main__':
    map_file = "data/" + input('Введите имя файла с уровнем')
    if not os.path.isfile(map_file):
        print('Файл не найден')
        sys.exit()
    level, level_x, level_y = load_level(map_file)
    tile_width = tile_height = 50

    pygame.init()
    pygame.display.set_caption('марио')
    size = WIDTH, HEIGHT = tile_width * level_x, tile_height * level_y
    screen = pygame.display.set_mode(size)

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')

    clock = pygame.time.Clock()
    fps = 50
    running = True
    start_screen()
    player = generate_level(level)
    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_group.update(event)
        tiles_group.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()