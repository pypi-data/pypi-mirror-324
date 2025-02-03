"""
asix.py
"""
import sys
from typing import List, Tuple, Optional
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from math import sin, cos, tan

class Core:
    def __init__(self, width: int = 800, height: int = 600, flag=None) -> None:
        pygame.init()

        if width is not None:
         if width < 1:
           print('\n')
           print('Error == Minimum width : 1px')
           self.width = 800
           print('Default Set : width(800px)')
         else:
            self.width = width
        else:
         print("Width is not defined")
        
        if height is not None:
         if height < 1:
            print('\n')
            print('Error == Minimum height : 1px')
            self.height = 600
            print('Default Set : height(600px)')
            print('\n')
         else:
            self.height = height
        else:
           print("Height is not defined")

        self.flag = flag

        self.clock = pygame.time.Clock()

        if not flag or flag == 'coreinf':
            self.screen = pygame.display.set_mode(
            (self.width, self.height))

        elif flag == 'optimize' or 'optimized':
            self.screen = pygame.display.set_mode(
            (self.width, self.height),
              pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.HWACCEL
        )
        elif flag == 'borderless':
            self.screen = pygame.display.set_mode(
            (self.width, self.height),
             pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.HWACCEL | pygame.NOFRAME
            )
        elif flag == 'resizable':
            self.screen = pygame.display.set_mode(
            (self.width, self.height),
              pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.HWACCEL
         )     
            
        icon_size = (32, 32)
        transparent = pygame.Surface(icon_size)
        transparent.fill((241, 243, 249, 255))
        pygame.display.set_icon(transparent)
        pygame.display.set_caption('')

        self.GLSO = {
                     'width':self.width,
                     'height':self.height,
                     'screen':self.screen,
                     'flags':self.flag,
                     'clock':self.clock, 
                     'font': None,
                     'type':"<Asix.Core>", 
                     'version': "7.1"
                     }
        
        if flag == 'coreinf':
           for par, val in self.GLSO.items():
             print(f'{par} : {val}')

    def __str__(self) -> str:
        return "<Asix.Core>"
    
    def icon(self, img):
        if img:
         pygame.display.set_icon(img)
        else:
           print("Error : Provide img object")
    
    def caption(self, title):
        if title:
         pygame.display.set_caption(title)
        else:
           print('Error : Provide title')
    
    @staticmethod
    def Font(filepath, size):
     return pygame.font.Font(filepath, size)
       
    def draw(self, color: List[Tuple[int, int, int]], *args) -> None:
        """
        Draw rectangles on the screen with specified colors.

        Parameters:
        - colors: A list of RGB tuples, where each tuple represents a color (e.g., [(255, 0, 0), (0, 255, 0), (0, 0, 255)]).
        - args: Variable number of rectangle definitions, either as pygame.Rect objects, tuples/lists of four integers, or strings in the format 'x, y, width, height'.
        """
        for rect in args:
            if isinstance(rect, pygame.Rect):
                pygame.draw.rect(self.screen, color, rect)
            elif isinstance(rect, (tuple, list)) and len(rect) == 4:
                pygame.draw.rect(self.screen, color, pygame.Rect(*rect))
            else:
                raise ValueError(
                    'Each argument must be a pygame.Rect object or a tuple/list of four integers.'
                    )
            
    def polygon(self, color, points, width=0):
       flipped_points = [(x, self.height - y) for x, y in points]
       pygame.draw.polygon(self.screen, color, flipped_points, width)
       

    def text(self, size: int, color: Tuple[int, int, int], text: str, x: int, y: int, font_type: Optional[str] = None, center: bool = True, rotation: int = 0) -> None:
        """
        Renders text on the screen at the given position with optional rotation.

        Parameters:
        - size: Font size.
        - color: The color of the text (as an RGB or RGBA tuple).
        - text: The string to render.
        - x, y: The position to render the text (top-left corner or center).
        - font_type: Optional custom font path (default is None, which uses Pygame's default font).
        - center: If True, centers the text at (x, y); otherwise, uses (x, y) as the top-left corner.
        - rotation: The angle to rotate the text in degrees (default is 0, no rotation).
        """
        font = pygame.font.Font(font_type, size)
        rendered_text = font.render(text, True, color)
        if rotation != 0:
            rendered_text = pygame.transform.rotate(rendered_text, rotation)
        text_rect = rendered_text.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(rendered_text, text_rect)

    def flip(self, clock: Optional[int] = None) -> None:
        pygame.display.flip()
        if clock:
            self.clock.tick(clock)

    @staticmethod
    def quit(*args) -> None:
        """
        Handles the window close event. If a quit event is detected, it closes the Pygame window
        and exits the program.
        """
        if args:
            for key in args:
                if key == 'esc':
                    key = 'ESCAPE'
                elif key == 'tab':
                    key = 'TAB'
                elif key == 'capslock':
                    key = 'CAPSLOCK'
                exec(f'Key = pygame.key.get_pressed()\nif Key[pygame.K_{key}]:\n    quit()\n')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def color(self, r: int=250, g: int=250, b: int=250) -> None:
        self.screen.fill((r, g, b))

    def blit(self, *args) -> None:
            self.screen.blit(args)

    def line(self, color: Tuple[int, int, int], start_pos: Tuple[int, int], end_pos: Tuple[int, int], width: int = 1) -> None:
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def update(self):
        pygame.display.update()

    def sleep(time:int) -> None:
        time.sleep(time)

    def globe(self, x, y, radius, fill_color, border_color=None, border_width=0):
     """
     Draws a circle on a given surface with customizable size, color, and border.

     :param surface: The pygame surface to draw on.
     :param position: A tuple (x, y) for the center of the circle.
     :param radius: Radius of the circle.
     :param fill_color: Color of the circle's fill, in (R, G, B) format.
     :param border_color: Color of the circle's border, in (R, G, B) format. Default is None (no border).
     :param border_width: Width of the border. Default is 0 (no border).
     """
     if border_color and border_width > 0:
        # Draw the border first
        pygame.draw.circle(self.screen, border_color, (x, y), radius)
        # Draw the inner circle on top, with a smaller radius to create the border effect
        inner_radius = max(0, radius - border_width)
        pygame.draw.circle(self.screen, fill_color, (x, y), inner_radius)
     else:
        # Draw only the filled circle
        pygame.draw.circle(self.screen, fill_color, (x, y), radius)

def screenshot(surface: pygame.Surface, filename: str = 'screenshot.png') -> None:
    """
    Takes a screenshot of the Pygame window and saves it as an image file.
    
    Parameters:
    - surface: The Pygame surface to capture.
    - filename: The name of the file to save the screenshot as (default is 'screenshot.png').
    """
    pygame.image.save(surface, filename)
    print(f'Screenshot saved as {filename}')

def K(key: str) -> int:
    return getattr(pygame, f'K_{key}')

def key() -> pygame.key.ScancodeWrapper:
    return pygame.key.get_pressed()

def R(x: int, y: int, w: int, h: int) -> pygame.Rect:
    return pygame.Rect(x, y, w, h)

def iload(file: str) -> pygame.Surface:
    return pygame.image.load(file)

def isize(img: pygame.Surface, w: int, h: int) -> pygame.Surface:
    return pygame.transform.scale(img, (w, h))

def sic(center:int, radius:int, angle:int, typ:str, startmul:int=0, endmul:int=0):
          if typ == 's':
           return center + radius * sin(angle)
          if typ == 'c':
           return center + radius * cos(angle)
          if typ == 't':
           return center + radius * tan(angle) 

class DTYPE:
    def __init__(self):
        self.database = {}

    def store(self, key, value, Type=None):
        if Type:
         self.database[key] = (Type, value)
        else:
            self.database[key] = value

    def fetch(self, key, fallback='print("Entry Not Found")'):
        return self.database.get(key, exec(fallback))
    
    def delete(self, key):
         self.database.pop(key)


WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
GREY: tuple = (200, 200, 200)