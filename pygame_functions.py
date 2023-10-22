import pygame
import json
from pprint import pprint
import time
import random


def flip(image):
    return pygame.transform.flip(image, True, False)

def scale(image, size):
    image = image
    return pygame.transform.scale(image, (size, size))

def load(path, size=None):
    if size:
        return scale(pygame.image.load(str(path)), size)
    else:
        return pygame.image.load(str(path))

def sprite_collide_group(sprite, group, colorkey = (0, 0, 0)):
    state = False
    sprite_ = None
    group_list = group.sprites()
    for i in group_list:
            i.image.set_colorkey(colorkey)
            sprite.image.set_colorkey(colorkey)
            mask = pygame.mask.from_surface(sprite.image)
            mask2 = pygame.mask.from_surface(i.image)
            if mask.overlap(mask2, (sprite.rect.x - i.rect.x + 1, sprite.rect.y - i.rect.y + 1)):
                state = True
                sprite_ = i

    return state, sprite_

def get_image(sheet, width, hieght, color, image_number, width_ = 0):
    image = pygame.Surface((width, hieght))
    image.blit(sheet, (0, 0), (width * image_number, width_ * hieght, width, hieght))
    image.set_colorkey((0, 0, 0))
    return image

def set_bg(image_path, loading=True):
    win = pygame.display.get_surface()
    width = win.get_width()
    height = win.get_height()
    bg = None
    if loading:
        bg = load(image_path)
    else:
        bg = image_path
    bg = scale(bg, width)
    win.blit(bg, (0, 0))

def play_sound(path):
    sound = pygame.mixer.Sound(str(path))
    sound.play()

def find_rect(bg):
    window = pygame.display.get_surface()
    ww = window.get_width()
    wh = window.get_height()

    mouse_click_num = 1
    click_state = True

    pos1 = None
    pos2 = None
    pos3 = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_r:
                    mouse_click_num = 1
                    click_state = True
                
                    pos1 = None
                    pos2 = None
                    pos3 = None

        if pygame.mouse.get_pressed()[0] == True and click_state:
            click_state = False
            if mouse_click_num == 1:
                pos1 = pygame.mouse.get_pos()
            elif mouse_click_num == 2:
                pos2 = pygame.mouse.get_pos()
            elif mouse_click_num == 3:
                pos3 = pygame.mouse.get_pos()
                

            mouse_click_num += 1

        if pygame.mouse.get_pressed()[0] == False:
            click_state = True

        set_bg(str(bg))

        posm = pygame.mouse.get_pos()

        if mouse_click_num == 2:
            pygame.draw.line(window, (0, 0, 255), pos1, posm, 3)
        if mouse_click_num == 3:
            pygame.draw.line(window, (0, 0, 255), pos1, pos2, 3)
            pygame.draw.line(window, (0, 0, 255), pos2, posm, 3)
        if mouse_click_num == 4:
            pos4 = (pos1[0], pos3[1])
            pygame.draw.line(window, (0, 0, 255), pos1, pos2, 3)
            pygame.draw.line(window, (0, 0, 255), pos2, pos3, 3)

            pygame.draw.line(window, (0, 0, 255), pos1, pos4, 3)
            pygame.draw.line(window, (0, 0, 255), pos3, pos4, 3)

        pygame.display.update()

    left = pos1[0]
    top = pos1[1]
    width = pos2[0] - pos1[0]
    height = pos3[1] - pos2[1]

    rect = pygame.rect.Rect(left, top, width, height)

    return rect

def hover(rect, click=None):
    pos = pygame.mouse.get_pos()

    if rect.collidepoint(pos):
        if click:
            if pygame.mouse.get_pressed()[0] == True:
                state = True
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def Text(font_ = False, text_ = '', size = 30, color = (255, 255, 255), pos = (0, 0), center = None):
    font = None
    if font_:
        font = pygame.font.Font(font_, size)
    else:
        font1 = pygame.font.get_default_font()
        font = pygame.font.Font(font1, size)


    text_text = font.render(text_, True, color)
    text_rect = text_text.get_rect()
    if center:
        text_rect.topright = (pos[0] + text_text.get_width()//2, pos[1])
    else:
        text_rect.topleft = pos

    win = pygame.display.get_surface()
    win.blit(text_text, text_rect)
    return text_text

def get_map(size, file, pos=None, cow_pos=None, tile_size1=5, tile_size2 = 100):
        window = load(file)
        image = pygame.Surface(size)
        image.blit(window, (0, 0), (0, 0, size[0], size[1]))
        w = tile_size2//tile_size1
        real_pos = (pos[0]//w, pos[1]//w)
        pygame.draw.circle(image, (255, 0, 0), real_pos, 5, 5)
        if cow_pos:
            pygame.draw.circle(image, (255, 255, 255), (cow_pos[0]//w, cow_pos[1]//w), 5, 5)
        return image

def shake(window, the_shake=10, color = None):
    win = pygame.display.get_surface()
    size = win.get_size()
    screen = pygame.Surface(size)
    screen.blit(window, (0, 0))
    ofset = (random.randint(0, the_shake) - the_shake//2, random.randint(0, the_shake) - the_shake//2)
    if color:
        win.fill(color)
    win.blit(screen, ofset)

def go_to_position(rect, pos, speed=5):
    x = pos[0]
    y = pos[1]

    if rect.center != pos:
        if x < rect.left:
            rect.left -= speed
        elif x > rect.right:
            rect.right += speed

        if y < rect.top:
            rect.top -= speed
        elif y > rect.bottom:
            rect.bottom += speed

    return rect

def parallax_bg(window, image_paths, scroll, how_long = 5):
    images = []

    for image_path in image_paths:
        images.append(load(image_path).convert_alpha())

    images_width = images[0].get_width()

    for x in range(how_long):
        speed = 1
        for image in images:
            window.blit(image, ((x * images_width) - scroll * speed, 0))
            speed += 0.2

    return (images_width * how_long) - (images_width * 2)

def animate(images, frame, speed = 0.2):
    image = None
    frame += speed
    if frame >= len(images):
        frame = 0

    image = images[int(frame)]

    return image, frame

def click():
    return pygame.mouse.get_pressed()[0]

def side_collide(rect1, rect2, offset=5):
    if rect2.colliderect(rect1):
        if (rect1.collidepoint(rect2.topright)\
            or rect1.collidepoint(rect2.bottomright)) and rect1.left >= rect2.right - offset:
            return 'right'
        elif (rect1.collidepoint(rect2.topleft)\
            or rect1.collidepoint(rect2.bottomleft)) and rect1.right <= rect2.left + offset:
            return 'left'
        elif rect1.collidepoint(rect2.midbottom) and rect1.top >= rect2.bottom - offset:
            return 'bottom'
        elif rect1.collidepoint(rect2.midtop) and rect1.bottom <= rect2.top + offset:
            return 'top'
        else:
            return None
    else:
        return None

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def merge_images(image_paths = []):
    test_image = load(image_paths[0])
    width, height = test_image.get_width(), test_image.get_height()

    image_ = pygame.Surface((width, height))
    image_.fill((0, 0, 0))

    for image_path in image_paths:
        image = load(image_path)
        image_.blit(image, (0, 0))
    
    image_.set_colorkey((0, 0, 0))

    return image_

def set_icon(path):
    icon = load(path)
    pygame.display.set_icon(icon)

def Group():
    return pygame.sprite.Group()

def small_rect(rect, how_smaller):
    top = rect.top
    left = rect.left
    width = rect.width
    height = rect.height

    if isinstance(how_smaller, tuple):
        sx = how_smaller[0]
        sy = how_smaller[1]

        rect1 = pygame.Rect(left + sx, top + sy, width - sx, height - sy)

        rect1.center = rect.center

        return rect1
    else:
        s = how_smaller

        rect1 = pygame.Rect(left + s, top + s, width - s, height - s)

        rect1.center = rect.center

        return rect1

def long_text(font = False, color = (), size = 30, text_ = '', split = 10, pos1 = ()):
    skip_list = [' ', ',', '.', '!', '?']

    good_text = []
    for char in text_:
        good_text.append(char)

    list1 = []
    number = 0
    string = ''
    for char in range(len(good_text)):
        if number < split - 1 and char < len(good_text) - 1:
            string += good_text[char]
            number += 1
        else:
            index = char
            if index < len(good_text) - 1:
                second_char = good_text[index + 1]
            else:
                second_char = None
            number = 0
            string += good_text[char]
            if second_char:
                if second_char in skip_list or good_text[char] in skip_list:
                    pass
                else:
                    string += '-'
            list1.append(string)
            string = ''

    pos = pos1

    pos = pos1

    for text1 in list1:
        text2 = Text(False, text1, size, color, pos, False)
        pos = (pos1[0], pos[1] + text2.get_height())

class DeathAnimation:
    def __init__(self, color, speed, max_alpha):
        self.color = color
        self.speed = speed
        self.alpha = 0
        self.win = pygame.display.get_surface()
        if max_alpha < 224:
            self.m_a = max_alpha
        else:
            self.m_a = 225

        self.image = pygame.surface.Surface((self.win.get_width(), self.win.get_height()))
        self.image.fill(self.color)

    def update(self):
        if self.alpha < self.m_a:
            self.alpha += self.speed

        self.image.set_alpha(self.alpha)
        self.win.blit(self.image, (0, 0))

class TextInput:
    def __init__(self, pos = (0, 0), bg_color_not_active = (0, 0, 0), bg_color_active=(0, 250, 0),\
                width = 100, hieght = 30, font = 'fonts/font.otf', text_color = (255, 255, 255), font_size = 20):
        self.pos = pos
        self.bg_c_a = bg_color_active
        self.bg_c_n_a = bg_color_not_active
        self.width = width
        self.hieght = hieght
        self.font = font
        self.font_size = font_size
        self.text_color = text_color

        self.text = ''

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.hieght)

        self.active = False
    
    def get_text(self):
        if hover(self.rect, True):
            self.active = True
        if pygame.mouse.get_pressed()[0] == True:
            if hover(self.rect) == False:
                self.active = False

            
        win = pygame.display.get_surface()
        if self.active:
            box = pygame.draw.rect(win, self.bg_c_a, self.rect)
        else:
            box = pygame.draw.rect(win, self.bg_c_n_a, self.rect)

        text_ = Text('fonts/font.otf', str(self.text), self.font_size, self.text_color, (self.pos[0]+1, self.pos[1]+1))
        
        return self.text

    def eventing(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

class HitWave:
    def __init__(self, speed = 5, color = (255, 255, 255), width=3, shake = True, force = 5, live = 3):
        self.speed = speed
        self.waves = []
        self.color = color
        self.window = pygame.display.get_surface()
        self.width = width
        self.shake = 0
        self.shake_state = shake
        self.force = force
        self.live = live

    def draw(self, move_rects = []):
        if self.shake > 0 and self.shake_state:
            shake(self.window)
            self.shake -= 1
        window_width = self.window.get_width()
        if self.waves:
            for wave in self.waves:
                if wave[1] * 2 < (window_width * 2):
                    self.circle = pygame.draw.circle(self.window, self.color, wave[0], wave[1], self.width)
                    wave[1] += self.speed

                    for rect in move_rects:
                        collide = side_collide(self.circle, rect)
                        if collide:
                            if wave[2] <= self.live:
                                if collide == 'right':
                                    rect.left -= self.force
                                    wave[2] += 1
                                if collide == 'left':
                                    rect.right += self.force
                                    wave[2] += 1
                                if collide == 'bottom':
                                    rect.top -= self.force
                                    wave[2] += 1
                                if collide == 'top':
                                    rect.bottom += self.force
                                    wave[2] += 1

                else:
                    self.waves.remove(wave)

    def add(self, pos):
        self.shake = 10
        self.waves.append([pos, 1, 0])

class Bar:
    def __init__(self, position, width, hieght, background_color, color, step, number = None):
        self.position = position
        self.width = width
        self.height = hieght
        self.bg_color = background_color
        self.color = color
        self.step = self.width // step

    def update(self, state):
        window = pygame.display.get_surface()
        pos = self.position
        bg_rect = pygame.draw.rect(window, self.bg_color, pygame.Rect(pos[0], pos[1], self.width, self.height))
        if self.color == 'multi':
            stap = state//self.step
            if stap == 0:
                rect = pygame.draw.rect(window, (211,33,44), pygame.Rect(pos[0], pos[1], state * self.step, self.height))
            if stap == 1:
                rect = pygame.draw.rect(window, (255,104,30), pygame.Rect(pos[0], pos[1], state * self.step, self.height))
            if stap == 2:
                rect = pygame.draw.rect(window, (6,193,86), pygame.Rect(pos[0], pos[1], state * self.step, self.height))
        else:
            rect = pygame.draw.rect(window, self.color, pygame.Rect(pos[0], pos[1], state * self.step, self.height))

class Particles:
    def __init__(self, time=2, pos=(250, 250), shrink=0.2, radius=10, color=(255, 255, 255),
                  col=None, on_btn = False, direction=[[1, -1], [1, -1]], shape=1):
        self.particles = []
        self.timer = 0
        self.time = time
        self.pos = pos
        self.shrink = shrink
        self.radius = radius
        self.color = color
        self.col = col
        self.on_btn = on_btn
        if len(direction[0]) > 1:
            direction[0].append(0)
        self.dir_x = direction[0]
        self.dir_y = direction[1]

        self.shape = shape

    def add(self, start_pos = None, color = None, shape=None):
        self.timer += self.time
        if self.timer > 1:
            self.timer = 0
            pos_y, pos_x = None, None
            if start_pos:
                pos_x, pos_y = start_pos[0], start_pos[1]
            else:
                pos_x = self.pos[0]
                pos_y = self.pos[1]
            radius = self.radius
            direction_y = random.choice(self.dir_x)
            diraction_x = random.choice(self.dir_y)
            list = [[pos_x, pos_y], radius, (diraction_x, direction_y)]
            if color:
                list.append(color)
            else:
                list.append(self.color)

            if shape:
                list.append(shape)
            else:
                list.append(self.shape)

            self.particles.append(list)

            return True

    def delete(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

    def draw(self):
        window = pygame.display.get_surface()
        if self.particles:
            self.delete()
            for particle in self.particles:
                particle[0][1] += particle[2][1]
                particle[0][0] += particle[2][0]
                particle[1] -= self.shrink
                color = particle[3]
                shape = particle[4]
                if shape == 1:
                    pygame.draw.circle(window, color, particle[0], int(particle[1]))
                elif shape == 2:
                    left, top = particle[0][0] - particle[1], particle[0][1] - particle[1]
                    width, height = particle[1]*2, particle[1]*2
                    rect = pygame.rect.Rect(left, top, width, height)
                    pygame.draw.rect(window, color, rect, 0)
                else:
                    left, top = particle[0][0] - particle[1], particle[0][1] - particle[1]
                    width, height = particle[1]*2, particle[1]*2

                    image = load(shape)
                    image = scale(image, width)

                    window.blit(image, (left, top))

    def add_many(self, number=5, start_pos = None, color = None, shape=None):
        for i in range(0, number):
            self.timer = 0
            pos_y, pos_x = None, None
            if start_pos:
                pos_x, pos_y = start_pos[0], start_pos[1]
            else:
                pos_x = self.pos[0]
                pos_y = self.pos[1]
            radius = self.radius
            direction_y = random.choice(self.dir_x)
            diraction_x = random.choice(self.dir_y)
            list = [[pos_x, pos_y], radius, (diraction_x, direction_y)]

            if color:
                list.append(color)
            else:
                list.append(self.color)

            if shape:
                list.append(shape)
            else:
                list.append(self.shape)

            self.particles.append(list)           

class Button:
    def __init__(self, win, image_path, xy =  (0, 0), scale = 1, animate = False, sprites = None, speed = 1, load=None):
        if load:
            image = image_path
        else:
            image = pygame.image.load(str(image_path))
        w = image.get_width()
        h = image.get_height()
        self.win = win
        self.image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.clicked = False
        self.scale = scale

        if animate == True:
            self.animate = animate
            self.sprites = []
            for sprite_path in sprites:
                if load:
                    image = sprite_path
                else:
                    image = pygame.image.load(str(sprite_path))
                w = image.get_width()
                h = image.get_height()
                self.sprites.append(pygame.transform.scale(image, (int(w * scale), int(h * scale))))
            self.animate_speed = speed
            self.animate_frame = 0

    def draw(self):
        state = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == False and self.clicked == True:
                self.clicked = False

        self.win.blit(self.image, self.rect)

        return self.clicked
    
    def animate_sprites(self):
        self.animate_frame += self.animate_speed
        if self.animate_frame >= len(self.sprites):
            self.animate_frame = 0

        self.image = self.sprites[int(self.animate_frame)]

class Animator:
    def __init__(self, person, sprites, speed):
        self.person = person
        self.sprites = sprites
        self.speed = speed
        self.animation_frame = 0
        self.person.image = self.sprites[int(self.animation_frame)]

        self.dop_animation_frame = 0
        self.state = True

    def animate(self):
        self.animation_frame += self.speed

        if self.animation_frame >= len(self.sprites):
            self.animation_frame = 0

        self.person.image = self.sprites[int(self.animation_frame)]
    
    def animate_frame(self):
        self.state = True

    def update(self, sprites, speed):
        if self.state:
            self.dop_animation_frame += speed
            if self.dop_animation_frame >= len(sprites):
                self.dop_animation_frame = 0
                self.state = False

        self.person.image = sprites[int(self.dop_animation_frame)]

class Timer:
    def __init__(self, sound_path = None):
        self.start_time = time.time()
        self.sound_state = False
        self.current_time = 0
        if sound_path:
            self.sound_path = sound_path
            self.sound_state = True

    def tick(self, the_time):
        timer_time = the_time - (time.time() - self.start_time)
        t = int(time.time() - self.start_time)
        if self.sound_state:
            if t > self.current_time:
                self.current_time = t
                play_sound(str(self.sound_path))
        return timer_time
    
    def count(self):
        timer_time = (time.time() - self.start_time)
        t = int(time.time() - self.start_time)
        if self.sound_state:
            if t > self.current_time:
                self.current_time = t
                play_sound(str(self.sound_path))
        return timer_time
    
    def get_time(self, the_time):
        return the_time - (time.time() - self.start_time)
    
class LevelOpenerBigMap:
    def __init__(self, width):
        self.width = width

    def level(self, path):
        with open(str(path), 'r+') as level_file:
            text = json.load(level_file)
            layers = text.get('layers')
            data = dict(layers[0])
            list = data.get('data')
            # print(list)
            width = self.width
            # print(list)
            list1 = []
            state = 0
            
            size = len(list)//width

            for i in range(size + 1):
                list2 = list[state:state+size]
                state += size
                list2.append(0)
                list1.append(list2)

            return list1

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        group.add(self)

class Map:
    def __init__(self, start_pos=(0, 0), end_pos=(10, 10), level_path='', tile_size=100):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.tile_size = tile_size

        self.window = pygame.Surface((end_pos[0] * tile_size, end_pos[1] * tile_size))
        self.window.fill((207,121,87))
        level = Level()

        g_g = pygame.sprite.Group()
        w_g = pygame.sprite.Group()
        sa_g = pygame.sprite.Group()
        sh_g = pygame.sprite.Group()
        f_g = pygame.sprite.Group()
        h_g = pygame.sprite.Group()

        g_g.empty()
        w_g.empty()
        sa_g.empty()
        sh_g.empty()
        f_g.empty()
        h_g.empty()
        g_g, w_g, g_g, sa_g, sh_g, f_g, g_g, g_g, h_g = level.draw(level_path,
                                                tile_size, int(start_pos[0]),
                                                int(end_pos[0]),
                                                int(start_pos[1]), int(end_pos[1]), pos=(0, 0))
        w_g.draw(self.window)
        sa_g.draw(self.window)
        sh_g.draw(self.window)
        f_g.draw(self.window)
        h_g.draw(self.window)

        pygame.image.save(self.window, 'images/map.png')

class Level:
    def __init__(self, numbers = [], images = [], groups = []):
        self.numbers = numbers
        self.images = images
        self.groups = groups
        self.special_state = True
        self.load_state = True
        self.level = []

    def draw(self, path, tile_size, pos_x, pos_y, pos = (0, 0)):
        l_o = LevelOpenerBigMap(int(pos_x[1]-pos_x[0]))
        if self.load_state:
            if path.__class__ == list:
                self.level = path
            else:
                self.level = l_o.level(str(path))
                self.load_state = False

        start_posx, end_posx = pos_x[0], pos_x[1]
        start_posy, end_posy = pos_y[0], pos_y[1]

        for group1 in self.groups:
            for group2 in group1:
                group2.empty()

        for x in range(start_posy, end_posy):
            for y in range(start_posx, end_posx):
                number = self.level[x][y]
                group = None

                position = ((y*tile_size - start_posx*tile_size) + pos[0],
                            (x*tile_size - start_posy*tile_size) + pos[1])

                for number_list in self.numbers:
                    if number in number_list:
                        image = self.images[self.numbers.index(number_list)][number_list.index(number)]
                        number1 = self.numbers.index(number_list)
                        number2 = number_list.index(number)
                        if len(self.groups[number1]) > number2:
                            group = self.groups[self.numbers.index(number_list)][number_list.index(number)]
                        else:
                            group = self.groups[self.numbers.index(number_list)][0]
                        if str(image) == f'<Surface({tile_size}x{tile_size}x32 SW)>':
                            tile = Tile(x=(y*tile_size - start_posx*tile_size) + pos[0],
                                        y=(x*tile_size - start_posy*tile_size) + pos[1],
                                        image=image,
                                        group=group)
                        else:
                            self.special_state = False
                            thing = image(position, (x, y))
                        
        list1 = []

        for group1 in self.groups:
            for group2 in group1:
                list1.append(group2)

        return list1

class ChunkLevel:
    def __init__(self, chunks = [], numbers = [], images = [], groups = [], width=10, tile_size = 64):
        self.chunks = chunks
        self.numbers = numbers
        self.images = images
        self.groups = groups
        self.width = width
        self.tile_size = tile_size
        self.real_scroll = 0
        self.number = 0

        chunks_for_exept = self.chunks

        self.bmo = LevelOpenerBigMap(width = width)
        self.lo = Level(self.numbers, self.images, self.groups)

        if len(chunks) > 0:
            self.current_level = random.choice(chunks)
            chunks_for_exept.remove(self.current_level)

        self.list1 = self.bmo.level(self.current_level)

        self.add_new()

        for i in range(len(self.list1) - 1):
            self.list1[i].pop(self.width)

        pprint(self.list1)

    def remove(self):
        for row in range(len(self.list1)):
            self.list1[row] = self.list1[row][self.width: -1]

        self.list1[-1].append(0)

    def add_new(self):
        self.next_level = random.choice(self.chunks)
        list2 = self.bmo.level(self.next_level)

        for i in range(len(list2)):
            for j in range(len(list2[i])):
                self.list1[i].append(list2[i][j])

        self.list1[-1].pop(-1)

    def level(self, scroll_x = 0, switch_scroll = 5):
        if self.real_scroll < switch_scroll - 1:
            self.real_scroll += scroll_x
        else:
            self.remove()
            self.add_new()
            pprint(self.list1)
            self.real_scroll = 1
        groups = self.lo.draw(self.list1, self.tile_size, (int(self.real_scroll),
                                                   int(self.real_scroll + self.width)), (0, self.width))
        
        return groups