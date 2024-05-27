import pygame
import json
from pprint import pprint
import time
import random
import math
from PIL import Image
import textwrap
from tkinter import colorchooser
import numpy
from nltk import flatten

pygame.init()

def flip(image):
    return pygame.transform.flip(image, True, False)

def scale(image, size):
    image = image
    return pygame.transform.scale(image, (size, size))

def scale2x(image):
    size = (image.get_size()[0]*2, image.get_size()[1]*2)
    return pygame.transform.scale(image, size)

def load(path, size=None):
    if size:
        return scale(pygame.image.load(str(path)), size)
    else:
        return pygame.image.load(str(path))

def replace_in_list(list1, item, index):
    i = list1.index(item)
    list1.pop(i)
    list1.insert(index, item)
    return list1

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

def get_image(sheet, width, hieght, image_number, width_ = 0):
    image = pygame.Surface((width, hieght), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (width * image_number, width_ * hieght, width, hieght))
    return image

def get_images_list(sheet, width, hieght, image_numbers, row, fliping=False):
    list_of_images = []
    if isinstance(row, int):
        for image_number in range(image_numbers[0], image_numbers[-1]):
            image = get_image(sheet, width, hieght, image_number, row)
            if fliping:
                list_of_images.append(flip(image))
            else:
                list_of_images.append(image)
    else:
        tilesize = int(row)
        n = hieght//tilesize
        for i in range(n):
            for image_number in range(image_numbers[0], image_numbers[-1]):
                image = get_image(sheet, width, hieght, image_number, i)
                if fliping:
                    list_of_images.append(flip(image))
                else:
                    list_of_images.append(image)

    return list_of_images

def set_bg(image_path, loading=True, pos=None):
    win = pygame.display.get_surface()
    width = win.get_width()
    height = win.get_height()
    bg = None
    if loading:
        bg = load(image_path)
    else:
        bg = image_path
    if pos == None:
        bg = scale(bg, width)
        win.blit(bg, (0, 0))
    else:
        win.blit(bg, pos)

def set_name(name):
    pygame.display.set_caption(str(name))

def play_sound(path, volume = 1):
    sound = pygame.mixer.Sound(str(path))
    sound.set_volume(volume)
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

        window.blit(load(bg), (0, 0))

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

def Text(win, font_ = None, text_ = '', size = 30, color = (255, 255, 255), pos = (0, 0), text_rect_string = 'text_rect.topleft', return_state='window'):
    font = pygame.font.Font(font_, size)
    text_text = font.render(text_, True, color)
    text_rect = text_text.get_rect()
    s = text_rect_string + ' = pos'
    exec(s)

    win.blit(text_text, text_rect)
    if return_state == 'window':
        return win
    elif return_state == 'rect':
        return text_rect
    else:
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

def parallax_bg(window, image_paths, scroll, how_long = 5, load=False):
    if load:
        images = image_paths
    else:
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

def click(index=0):
    return pygame.mouse.get_pressed()[index]

def side_collide(rect1, rect2, offset=5):
    if rect2.colliderect(rect1):
        if rect1.collidepoint(rect2.midright) and rect1.left >= rect2.right - offset:
            return 'right'
        elif rect1.collidepoint(rect2.midleft) and rect1.right <= rect2.left + offset:
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

def merge_images(image_paths = [], loading = True):
    if loading:
        test_image = load(image_paths[0])
    else:
        test_image = image_paths[0]
    width, height = test_image.get_width(), test_image.get_height()

    image_ = pygame.Surface((width, height))
    image_.fill((0, 0, 0))

    for image_path in image_paths:
        if loading:
            image = load(image_path)
        else:
            image = image_path
        image_.blit(image, (0, 0))
    
    image_.set_colorkey((0, 0, 0))

    return image_

def set_icon(path):
    icon = load(path)
    pygame.display.set_icon(icon)

def Group():
    return pygame.sprite.Group()

def Sprite():
    return pygame.sprite.Sprite

def small_rect(rect, how_smaller):
    top = rect.top
    left = rect.left
    width = rect.width
    height = rect.height

    if isinstance(how_smaller, tuple):
        if isinstance(how_smaller[1], tuple):
            sx = how_smaller[0]
            sy = how_smaller[1][0] + how_smaller[1][1]

            rect1 = pygame.Rect(left + sx, top + sy, width - sx, height - sy)

            rect1.center = rect.center
            rect1.bottom = rect.bottom - how_smaller[1][1]

            return rect1   
        elif isinstance(how_smaller[1], tuple):
            sx = how_smaller[1][0] + how_smaller[1][1]
            sy = how_smaller[0]

            rect1 = pygame.Rect(left + sx, top + sy, width - sx, height - sy)

            rect1.center = rect.center
            rect1.right = rect.right - how_smaller[1][1]

            return rect1
        else:

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

def replace_color(image_surface, color_remove, color_change):
    # pygame.transform.threshold(image_surface, image_surface, color_remove, value, color_change, 1, None, True)
    # return image_surface
    array = pygame.PixelArray(image_surface)
    pygame.PixelArray.replace(array, color_remove, color_change)
    s = pygame.PixelArray.make_surface(array)
    return s

def outline(image, rect, color):
    winodw = pygame.display.get_surface()
    loc = rect.topleft
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0,0,0))
    mask_surf = replace_color(mask_surf, (225, 225, 225), color, value = (100, 100, 100))
    i = 1
    winodw.blit(mask_surf,(loc[0]-i,loc[1]))
    winodw.blit(mask_surf,(loc[0]+i,loc[1]))
    winodw.blit(mask_surf,(loc[0],loc[1]-i))
    winodw.blit(mask_surf,(loc[0],loc[1]+i))

def long_text(win, font = None, text_ = '', size = 30, color = (255, 255, 255), pos1 = (0, 0), text_rect_string = 'text_rect.topleft', split = 15):
    list1 = textwrap.wrap(text_, split)
            
    pos = pos1

    for text1 in range(len(list1)):
        pos = (pos1[0], pos1[1] + (text1 * size))
        win = Text(win, font, list1[text1], size, color, pos, text_rect_string)

    return win

def darken(image, value, color=(0, 0, 0)):
    surface = pygame.surface.Surface((image.get_width(), image.get_height()))
    dark = pygame.surface.Surface((image.get_width(), image.get_height()))
    dark.fill(color)
    dark.set_alpha(value)
    surface.blit(image, (0, 0))
    surface.blit(dark, (0, 0))
    return surface

def procentage_random(procentage):
    number = random.randint(0, 100)
    return True if number <= procentage else False

def button(image, rect, win = None, button_scale = 1.05, button_color = (0, 0, 0)):
    window = pygame.display.get_surface() if win == None else win
    img = image
    state = False
    r = rect
    hover_state = False
    if hover(rect):
        img = pygame.transform.scale(image, (image.get_width() * button_scale, image.get_height() * button_scale))
        r = img.get_rect()
        r.center = rect.center
        hover_state = True

        if click():
            state = True

    window.blit(img, r)
    if hover_state:
        pygame.draw.rect(window, button_color, r, 3)

    return state

def most_common_used_color(img_path, number=1):
    img_colors = sorted(Image.open(img_path).getcolors())[-1 - number][1][0:3]
    return img_colors

def dark_light(color):
    is_dark = 0
    is_light = 0
    half = 225/2

    for c in color:
        if c < half:
            is_dark += 1
        else:
            is_light += 1

    if is_light > is_dark:
        return 'd'
    else:
        return 'l'

def edit_color(color, value, method = 'd'):
    if method == 'd':
        return (color[0] - value, color[1] - value, color[2] - value)
    else:
        return (color[0] + value, color[1] + value, color[2] + value)

def image_preview(image, bg = (0, 0, 0)):
    if isinstance(image, str):
        img = load(image)
    else:
        img = image

    width = img.get_width()
    height = img.get_height()

    preview = pygame.display.set_mode((width, height))
    set_name('image preview')

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        preview.fill(bg)

        preview.blit(img, (0, 0))

        pygame.display.update()

def color_pick(initial_color = (0, 0, 0)):
    color = colorchooser.askcolor(initialcolor=initial_color)
    return color[0] if color != (None, None) else (initial_color)

def not_not_in_list(list1, thing):
    state = False
    for i in list1:
        if i == thing:
            pass
        else:
            state = True

    return state

def light(surface, position, radius, color=(255, 255, 255), glow=2, fall=1):
    r = radius*glow
    circle_surf = pygame.Surface((r*2, r*2))
    for i in range(r, radius, -fall):
        c = (
            color[0] - i if color[0] - i > 0 else 0,
            color[1] - i if color[1] - i > 0 else 0,
            color[2] - i if color[2] - i > 0 else 0,
        )
        pygame.draw.circle(circle_surf, c, (r, r), i)
    circle_surf.set_colorkey((0, 0, 0))
    surface.blit(circle_surf, (position[0]-r, position[1]-r), special_flags=pygame.BLEND_RGB_ADD)

class YSortCamera:
    def __init__(self):
        self.sprite_list = []
        self.win = pygame.display.get_surface()

    def draw(self, groups):
        self.sprite_list = []
        for group in groups:
            group.update()
            for image in group.sprites():
                self.sprite_list.append(image)

        for sprite in sorted(self.sprite_list, key=lambda sprite: sprite.rect.centery):
            self.win.blit(sprite.image, sprite.rect)

class DeathAnimation:
    def __init__(self, color, speed, max_alpha):
        self.color = color
        self.speed = speed
        self.alpha = 0
        self.win = pygame.display.get_surface()
        self.m_a = max_alpha

        self.image = pygame.surface.Surface((self.win.get_width(), self.win.get_height()))
        self.image.fill(self.color)

    def update(self):
        if self.alpha < self.m_a:
            self.alpha += self.speed

        if self.alpha >= 225:
            self.image.fill(self.color)
        else:
            self.image.set_alpha(self.alpha)
        self.win.blit(self.image, (0, 0))

class TextPopup:
    def __init__(self, time, window, speed):
        self.timer = Timer()
        self.time = time
        self.list_of_pops = []
        self.window = window
        self.speed = speed

    def add(self, font, size, text, color, position, pos_str = 'text_rect.topleft'):
        text_img = Text(self.window, font, text, size, color, (-1000, -1000), pos_str, 'image')
        img = pygame.surface.Surface((text_img.get_width(), text_img.get_height()), pygame.SRCALPHA)
        img.blit(text_img, (0, 0))
        text_rect = img.get_rect()
        s = pos_str + ' = position'
        exec(s)

        self.list_of_pops.append([img, text_rect, 225, time.time(), True])

    def update(self):
        for popup in self.list_of_pops:
            if popup[4] == True:
                ti = self.time - (time.time() - popup[3])
                if ti <= 0:
                    popup[4] = False
            else:
                if popup[2] - self.speed <= 0:
                    self.list_of_pops.remove(popup)
                else:
                    popup[2] -= self.speed
                    popup[0].set_alpha(popup[2])

            self.window.blit(popup[0], popup[1])

class SoundPlayer:
    def __init__(self, path = ''):
        self.path = path
        self.sound_state = True
        self.last_sound = None

    def play_sound(self, path, stop_the_last = None, volume = 1):
        if self.last_sound and stop_the_last:
            self.last_sound.stop()
        pathy = self.path + str(path)
        if self.sound_state:
            sound = pygame.mixer.Sound(str(pathy))
            sound.set_volume(volume)
            sound.play()
            self.last_sound = sound

    def stop_sound(self):
        if self.last_sound:
            self.last_sound.stop()
            
    def play_music(self, path, volume = 1):
        pathy = self.path + str(path)
        if self.sound_state:
            pygame.mixer.music.load(pathy)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.stop()

class TextInput:
    def __init__(self, pos = (0, 0), bg_color_not_active = (0, 0, 0), bg_color_active=(0, 250, 0),\
                width = 100, hieght = 30, font = None, text_color = (255, 255, 255), font_size = 20):
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

        text_ = Text(self.font, str(self.text), self.font_size, self.text_color, (self.pos[0]+1, self.pos[1]+1))
        
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

    def draw(self, dt, target_fps, move_rects = []):
        if self.shake > 0 and self.shake_state:
            shake(self.window)
            self.shake -= 1
        window_width = self.window.get_width()
        if self.waves:
            for wave in self.waves:
                if wave[1] * 2 < (window_width * 2):
                    self.circle = pygame.draw.circle(self.window, self.color if wave[3] == None else wave[3], wave[0], wave[1], self.width)
                    wave[1] += self.speed * dt * target_fps

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

    def add(self, pos, color=None):
        self.shake = 10
        self.waves.append([pos, 1, 0, color])

class Bar:
    def __init__(self, position, width, hieght, background_color, color, outline_color = None, maximum = None, center = False):
        self.position = position if center == False else (position[0] - width//2, position[1] - hieght // 2)
        self.width = width
        self.height = hieght
        self.bg_color = background_color
        self.color = color
        self.step = self.width/100 if maximum == None else self.width/maximum
        self.out_color = outline_color
        img = pygame.Surface((width, hieght))
        self.rect = img.get_rect()
        self.rect.topleft = self.position

    def update(self, state):
        window = pygame.display.get_surface()
        pos = self.position
        bg_rect = pygame.draw.rect(window, self.bg_color, pygame.Rect(pos[0], pos[1], self.width, self.height))
        rect = pygame.draw.rect(window, self.color, pygame.Rect(pos[0], pos[1], state * self.step, self.height))
        if self.out_color:
            pygame.draw.rect(window, self.out_color, pygame.rect.Rect(pos[0], pos[1], self.width, self.height), 5)

        return rect

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

class ParticlesPremium:
    def __init__(self):
        self.many_state = False
        self.timer = Timer()
        self.many_particles_state = False
        self.the_number = 0

    def many_particles(self, colors = [], number=5, position = (0, 0), time=2, particles=None):
        if number > 0:
            if self.many_particles_state == True:
                if self.many_state == False:
                    self.the_number = 0
                    self.timer = Timer()
                    self.many_state = True
                if self.timer.tick(time) > 0:
                    pass
                else:
                    self.timer = Timer()
                    self.the_number += 1
                    particles.add(color=random.choice(colors), start_pos=position)
                if self.the_number > number:
                    self.the_number=0
                    self.many_particles_state = False
                    self.many_state = False
        else:
            if self.timer.tick(time) > 0:
                pass
            else:
                self.timer = Timer()
                self.the_number += 1
                particles.add(color=random.choice(colors), start_pos=position)

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
        self.level = None

    def level_open(self, path, index_start = (0, 0), index_width = (0, 0)):
        with open(str(path), 'r+') as level_file:
            text = json.load(level_file)
            layers = text.get('layers')
            data = dict(layers[0])
            list1 = data.get('data')
            # print(list)
            width = self.width
            # list1 = []
            state = 0
            list2 = []


            length = len(list1)
            wanted_parts = len(list1)//self.width
            # print(wanted_parts)

            if self.level == None:
                list1 = [list1[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]
            else:
                list1 = self.level

            self.level = list1

            for y in range(index_start[1], index_width[1]):
                l = list1[y]
                li = []
                for x in range(index_start[0], index_width[0]):
                    li.append(l[x])
                list2.append(li)

            return list2

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group, tylesize):
        super().__init__()

        self.image = image

        r = pygame.rect.Rect(0, 0, tylesize, tylesize)
        r.topleft = (x, y)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = r.bottomleft

        group.add(self)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_rect, image, group, speed = 15, direction = None):
        super().__init__()
        self.speed = speed
        self.image = load(image)
        self.rect = self.image.get_rect()
        self.rect.center = start_rect

        if direction:
            mouse_x, mouse_y = direction[0], direction[1]
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        dis_x = mouse_x - start_rect[0]
        dis_y = mouse_y - start_rect[1]

        self.angle = math.atan2(dis_y, dis_x)
        
        self.rotate_angle = (180 / math.pi) * -math.atan2(dis_y, dis_x)

        self.image = pygame.transform.rotate(self.image, self.rotate_angle)
        self.rect = self.image.get_rect()
        self.rect.center = start_rect

        group.add(self)

    def update(self, dt, target_fps):
        speed_x = math.cos(self.angle) * self.speed
        speed_y = math.sin(self.angle) * self.speed

        self.rect.centerx += speed_x * dt * target_fps
        self.rect.centery += speed_y * dt * target_fps

class Popup:
    def __init__(self, window, background_color, image, rect, alpha_duration, duration, alpha_speed = 3):
        self.background_color = background_color
        self.image = image
        self.original_image = image
        self.rect = rect
        self.alpha_duration = alpha_duration
        self.duration = duration
        self.alpha = 0
        self.timer = Timer()
        self.state = True
        self.alpha_speed = alpha_speed
        self.window = window

    def update(self):
        if self.state:
            t = self.timer.count()
            if t < self.alpha_duration:
                self.image.set_alpha(self.alpha)
                self.alpha += self.alpha_speed if self.alpha < 225 else 0
            elif t > self.alpha_duration and t < self.alpha_duration + self.duration:
                self.image.set_alpha(225)
                self.image = self.original_image
            elif t < self.alpha_duration*2 + self.duration and t > self.alpha_duration + self.duration:
                self.image.set_alpha(self.alpha)
                if self.alpha > 0:
                    self.alpha -= self.alpha_speed
                else:
                    self.state = False
            
            self.window.fill(self.background_color)
            self.window.blit(self.image, self.rect)

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

                # print(number)

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
                        s = str(image)
                        s = s[9:-1]
                        string = s.replace('x', '')
                        s = string[0:len(str(tile_size))*2]
                        # print(s)
                        if s == f'{tile_size}{tile_size}':
                            tile = Tile(x=(y*tile_size - start_posx*tile_size) + pos[0],
                                        y=(x*tile_size - start_posy*tile_size) + pos[1],
                                        image=image,
                                        group=group)
                        else:
                            self.special_state = False
                            thing = image(position=position, xy=(x, y), number=number)
                        
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
            self.real_scroll = 0
        groups = self.lo.draw(self.list1, self.tile_size, (int(self.real_scroll),
                                                   int(self.real_scroll + self.width)), (0, self.width))
        
        return groups

class BigLevel:
    def __init__(self, numbers, images, groups, level_path, ww, wh, tile_size, whole_map_width_in_tiles, whole_map_height_in_tiles):
        self.numbers = numbers
        self.images = images
        self.groups = []
        self.bg = []
        self.bg_img = pygame.Surface((whole_map_width_in_tiles * tile_size, whole_map_height_in_tiles * tile_size)).convert()
        for i, g in enumerate(groups):
            for index, group in enumerate(g):
                if group == None:
                    self.bg.append([group, numbers[i]])
                else:
                    self.groups.append([group, numbers[i]])

        # if len(numbers) == len(images) and len(images) == len(groups):
        #     pass
        # else:
        #     raise Warning('your classes are not the same length!!!!')
        
        self.level_path = level_path
        self.ww = ww
        self.wh = wh
        self.tile_size = tile_size
        self.level_opener = LevelOpenerBigMap(whole_map_width_in_tiles)
        self.level = None
        self.scrolls = (None, None)
        self.width_tiles = ww//tile_size
        self.height_tiles = wh//tile_size

        self.tiles_n = [0, 0]
        self.add_n = [0, 0]

        self.map_width = whole_map_width_in_tiles
        self.map_height = whole_map_height_in_tiles

        self.limit_w = (self.map_width * self.tile_size) - self.ww - 1
        self.limit_h = (self.map_height * self.tile_size) - self.wh - 1

        self.image_state = False

    def draw(self, scrolls):
        if self.image_state == False:
            self.make_img()
        if scrolls != self.scrolls and self.image_state:
            self.scrolls = scrolls

            self.update_scrolls()

            self.update_pos()
            
            self.get_level()

            self.update_groups()

            for y in range(len(self.level)):
                row = self.level[y]
                for x in range(len(row)):
                    number = int(row[x])
                    if number != 0:
                        s = False
                        for bg_group_list in self.bg:
                            if number in bg_group_list[1]:
                                s = True
                        if s == False:
                            index1 = self.find_in_list(self.numbers, number)
                            index2 = self.numbers[index1].index(number)
                            image = self.images[index1][index2]
                            position = ((x*self.tile_size) - self.add_n[0], (y*self.tile_size) - self.add_n[1])
                            group = self.groups[index1][0]

                            if isinstance(image, str):
                                t = Tile(position[0], position[1], load(image), group, self.tile_size)
                            elif isinstance(image, pygame.Surface):
                                t = Tile(position[0], position[1], image, group, self.tile_size)
                            else:
                                thing = image(position=position, xy=(self.tiles_n[0] + x, self.tiles_n[1] + y), number=number)

            self.image_state = True

        # self.update_scrolls()
        # self.update_pos()

        return [group[0] for group in self.groups], self.scrolls, self.bg_img, (0 - (self.tiles_n[0] * self.tile_size) - self.add_n[0], 0 - (self.tiles_n[1] * self.tile_size) - self.add_n[1])

    def update_pos(self):
        self.tiles_n = [0, 0]
        self.add_n = [0, 0]

        for i in range(len(self.scrolls)):
            scroll = self.scrolls[i]
            self.tiles_n[i] = int(scroll/self.tile_size)
            if self.scrolls[0] < 0 or self.scrolls[1] < 0 or self.scrolls[0] > self.limit_w or self.scrolls[1] > self.limit_h:
                pass
            else:
                self.add_n[i] = scroll - (self.tiles_n[i] * self.tile_size)

    def get_level(self):
        self.level = self.level_opener.level_open(self.level_path, self.tiles_n, (self.width_tiles + self.tiles_n[0] + 2, self.height_tiles + self.tiles_n[1] + 2))

    def update_scrolls(self):

        if self.scrolls[0] < 0:
            self.scrolls[0] = 0

        if self.scrolls[1] < 0:
            self.scrolls[1] = 0

        if self.scrolls[0] > self.limit_w:
            self.scrolls[0] = self.limit_w - (self.tile_size-1)

        if self.scrolls[1] > self.limit_h:
            self.scrolls[1] = self.limit_h - (self.tile_size-1)

    def update_groups(self):
        for group_lists in self.groups:
            group_lists[0].empty()

    def find_in_list(self, list1, obj):
        n = False
        for i, l in enumerate(list1):
            if obj in l:
                n = i
                break
        return n

    def make_img(self):
        full_level = self.level_opener.level_open(self.level_path, (0, 0), (self.map_width, self.map_height))
        
        for y in range(len(full_level)):
                row = full_level[y]
                for x in range(len(row)):
                    number = int(row[x])
                    if number != 0:
                        index1 = self.find_in_list(self.numbers, number)
                        index2 = self.numbers[index1].index(number)
                        image = self.images[index1][index2]
                        group = None
                        position = ((x*self.tile_size) - self.add_n[0], (y*self.tile_size) - self.add_n[1])
                        try:
                            for group_list in self.groups:
                                if index2 in group_list[index1]:
                                    group = group_list[0]
                        except IndexError:
                            group = None
                        if group != None:
                            if isinstance(image, str):
                                t = Tile(position[0], position[1], load(image), group, self.tile_size)
                            elif isinstance(image, pygame.Surface):
                                t = Tile(position[0], position[1], image, group, self.tile_size)
                            else:
                                thing = image(position=position, xy=(self.tiles_n[0] + x, self.tiles_n[1] + y), number=number)
                        else:
                            if self.image_state == False and isinstance(image, pygame.Surface):
                                self.bg_img.blit(image, ((self.tiles_n[0] + x) * self.tile_size, (self.tiles_n[1] + y) * self.tile_size))

        numbers = []
        for bg_list in self.bg:
            index = self.numbers.index(bg_list[1])
            numbers.append(index)

            self.images.pop(index)
            self.numbers.pop(index)
        self.image_state = True
