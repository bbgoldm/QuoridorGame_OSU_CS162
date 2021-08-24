# Author: Brent Goldman
# Date: 7/29/2021
# Description:  Quoridor board game simulation
# Associated Files: quoridor.py
"""
The purpose of this code is to use Pygame to
create a visual representation of Quoridor,
with a board, pawns, and fences.
The user can then click on the screen to
play the game, instead of typing commands
in through the terminal.

This file will call methods in quoridor.py
to determine if moves are legal and to
determine a winner.

Note, can use opengameart.org for images
"""

# import all the methods from Quoridor
from Quoridor import *

import pygame
from pygame.locals import *

pygame.font.init()

# Constants

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PEACH = (233, 190, 165)
GRAY = (200, 200, 200)
HALF_WHITE = (117, 117, 117)
WHITE = (255, 255, 255)
PAWN_COLOR_CLICKED = WHITE
FENCE_COLOR_CLICKED = WHITE

class Pawn(pygame.sprite.Sprite):
    """Create a pawn object using the sprite class"""
    pawn_width = 50  # width of rectangle
    pawn_height = 50  # height of rectangle
    image_color = PEACH

    def __init__(self, player, pawn_x, pawn_y, coord, pawn_color_unclicked):
        """
        Initialize a Pawn object

        player: integer for either player 1 or player 2
        pawn_x: x position of pawn on screen
        pawn_y: y position of pawn on screen
        coord: tuple coordinates needed for QuoridorGame validation
        pawn_color_unclicked: (R,G,B) color for the pawn when not clicked
        """
        super().__init__()  # inherit Sprite class
        self._player = player  # player name 1 or 2
        self._pawn_x = pawn_x  # x position of rectangle
        self._pawn_y = pawn_y  # y position of rectangle
        self._coord = coord  # tuple coordinates needed for QuoridorGame
        self._pawn_color_unclicked = pawn_color_unclicked # initial color of the pawn
        self.image = pygame.Surface([self.pawn_width, self.pawn_height])
        self.image.fill(self.image_color)
        # Note: Size of pawn is the last value
        self.pawn = pygame.draw.circle(self.image, self._pawn_color_unclicked, \
                                       (self.pawn_width // 2, self.pawn_height // 2), 10)
        self.rect = self.image.get_rect()
        self.rect.center = [self._pawn_x, self._pawn_y]

    def set_color(self, color):
        """Set color of pawn, using a tuple input"
        Does not return anything."""
        self.pawn = pygame.draw.circle(self.image, color, \
                                       (self.pawn_width // 2, self.pawn_height // 2), 10)

    def get_coord(self):
        """Return a tuple containing the x,y coordinates of rectangle used for QuoridorGame"""
        return self._coord

    def set_coord(self, coord):
        """Set the tuple for the x, y coordinates of a rectangle used for QuoridorGame"""
        self._coord = coord

    def get_player(self):
        """Return player number as int"""
        return self._player

    def get_pawn_color_unclicked(self):
        """Return initial pawn color as RGB"""
        return self._pawn_color_unclicked

    def move_pawn(self, x, y):
        """Move the pawn"""
        self.rect.center = [x, y]


class Rectangle(pygame.sprite.Sprite):
    """Create the rectangles for the board as sprite objects"""

    def __init__(self, rec_x, rec_y, coord):
        """"""
        super().__init__()  # inherit Sprite class
        rec_width = 50  # width of rectangle
        rec_height = 50  # height of rectangle
        rec_color = PEACH  # color of rectangle
        self._rec_x = rec_x  # x position of rectangle
        self._rec_y = rec_y  # y position of rectangle
        self._coord = coord  # # coordinates needed for QuoridorGame

        # Draw rectangle
        self.image = pygame.Surface([rec_width, rec_height])  # size of the rectangle
        self.image.fill(rec_color)  # rectangle color
        self.rect = self.image.get_rect()  # place a rect around the rectangle so it can be moved
        self.rect.center = [self._rec_x, self._rec_y]  # where to put the center of the rect

    def get_coord(self):
        """Return a tuple containing the x,y coordinates of rectangle used for QuoridorGame"""
        return self._coord

    def set_coord(self, coord):
        """Set the tuple for the x, y coordinates of a rectangle used for QuoridorGame"""
        self._coord = coord


class Marker(pygame.sprite.Sprite):
    """Create a fence marker object"""

    rec_color = BLACK #(255, 125, 255)  # color of rectangle

    def __init__(self, rec_x, rec_y, rec_width, rec_height, coord, angle):
        """"""
        super().__init__()  # inherit Sprite class
        self._rec_x = rec_x  # x position of marker
        self._rec_y = rec_y  # y position of marker
        self._coord = coord  # # coordinates needed for QuoridorGame
        self._rec_width = rec_width  # width of rectangle
        self._rec_height = rec_height  # height of rectangle
        self._angle = angle  # angle either 'v' or 'h'

        # Draw fence marker
        self.image = pygame.Surface([self._rec_width, self._rec_height])  # size of the rectangle
        self.image.fill(self.rec_color)  # rectangle color
        self.rect = self.image.get_rect()  # place a rect around the rectangle so it can be moved
        self.rect.center = [self._rec_x, self._rec_y]  # where to put the center of the rect

    def set_color(self, color):
        """Set color of pawn, using a tuple input"""
        self.image.fill(color)

    def rotate(self, screen):
        """Rotate fence 90 degrees"""
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_coord(self):
        """Return a tuple containing the x,y coordinates of rectangle used for QuoridorGame"""
        print("Marker.get_coord()")
        print(self._coord)
        return self._coord

    def set_coord(self, coord):
        """Set the tuple for the x, y coordinates of a rectangle used for QuoridorGame"""
        self._coord = coord

    def get_angle(self):
        """Return the angle of the marker"""
        return self._angle


class Fence(pygame.sprite.Sprite):
    """Create a fence object"""
    rec_width = 10  # width of rectangle
    rec_height = 50  # height of rectangle
    #rec_color = (255, 255, 255)  # color of fence

    def __init__(self, rec_x, rec_y, coord, player, fence_color):
        """"""
        super().__init__()  # inherit Sprite class
        self._rec_x = rec_x  # x position of rectangle
        self._rec_y = rec_y  # y position of rectangle
        self._coord = coord  # # coordinates needed for QuoridorGame
        self._player = player  # player #
        self._used = False # indicate whether the fence has been played
        self._fence_color_unclicked = fence_color # initial color of the fence

        # Draw fence
        self.image = pygame.Surface([self.rec_width, self.rec_height])  # size of the rectangle
        self.image.fill(self._fence_color_unclicked)  # rectangle color
        self.rect = self.image.get_rect()  # place a rect around the rectangle so it can be moved
        self.rect.center = [self._rec_x, self._rec_y]  # where to put the center of the rect

    def get_fence_color_unclicked(self):
        """Return the initial fence color"""
        return self._fence_color_unclicked

    def set_color(self, color):
        """Set color of pawn, using a tuple input"""
        self.image.fill(color)

    def set_used(self):
        """Mark the fence used so it can't be moved again"""
        self._used = True

    def get_used(self):
        """Return if the fence has been used or not"""
        return self._used

    def rotate(self, screen):
        """Rotate fence 90 degrees"""
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_coord(self):
        """Return a tuple containing the x,y coordinates of rectangle used for QuoridorGame"""
        return self._coord

    def set_coord(self, coord):
        """Set the tuple for the x, y coordinates of a rectangle used for QuoridorGame"""
        self._coord = coord

    def get_player(self):
        """Return the player number"""
        return self._player

    def move_fence(self, x, y):
        """Move the fence"""
        self.rect.center = [x, y]

class Text(pygame.sprite.Sprite):
    """Create text for the screen

        # Create title
        title = FONT.render('QUORIDOR', True, WHITE)
        p1_fence = FONT.render('P1 Fences', True, WHITE)
        rect = title.get_rect()
        rect.center = (coordx, coordy)
        #pygame.draw.rect(title, BLUE, rect, 1)
        """
    def __init__(self, text, rec_x, rec_y, size = 24, style = 'Arial'):
        """Initialize the Text object.  Set the locate, size of text,
        and Font"""
        super().__init__()  # inherit Sprite class
        self._rec_x = rec_x  # x position of rectangle
        self._rec_y = rec_y # y position of rectangle
        self._font = pygame.font.SysFont(style, size)
        self.image = self._font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [rec_x, rec_y]

class Simulate:
    """Simulate the Quoridor game"""

    def __init__(self):
        """"""
        # Create the game from quoridor.py
        self._myGame = QuoridorGame()


        # Constants for the board / screen
        screen_width = 700
        screen_height = 650
        screen_color = (75, 75, 75)

        # Create the surface
        # Create the screen
        self._screen = pygame.display.set_mode((screen_width, screen_height))
        self._screen.fill(screen_color)  # Change the background (google color picker)

        # Rectangle
        # Create a group for the rectangles
        self._rectangle_group = pygame.sprite.Group()
        # Create the rectangles and add to group
        self.create_rectangles()

        # Fences
        # Create a group for the fences
        self._fence_group = pygame.sprite.RenderClear()
        # Create the player fences and add to group
        self.create_fences(30, 160, 1, GREEN)  # Player 1
        self.create_fences(650, 160, 2, BLUE)  # Player 2

        # Fence Markers
        # Create a group for the fence markers
        self._marker_group = pygame.sprite.RenderClear()
        # Create the vertical fence markers
        #x_pos, y_pos, rec_width, rec_height, angle
        self.create_markers(150, 100, 10, 50, 'v')
        # Create the horizontal fence markers
        self.create_markers(120, 130, 50, 10, 'h')

        # Pawn
        # Create a group for the pawns
        # Create the pawns
        # Add the pawns to the pawn group
        self.pawn_group = pygame.sprite.Group()
        self.p1 = Pawn(1, 360, 100, (4, 0), GREEN)
        self.p2 = Pawn(2, 360, 580, (4, 8), BLUE)
        self.pawn_group.add(self.p1, self.p2)

        # Text
        # Create a group for the text
        self._text_group = pygame.sprite.Group()
        # Create title
        title = Text('Quoridor PyGame', 360, 30, 24, 'Arial')
        p1_txt = Text('P1 Fences', 50, 100, 16)
        p2_txt = Text('P2 Fences', 660, 100, 16)
        self._text_group.add(title, p1_txt, p2_txt)


    def create_markers(self, x_pos, y_pos, rec_width, rec_height, angle):
        """Create fence marker sprites.  The purpose of these sprites
        are to mark the locations where a fence can be placed.  When
        a fence and fence marker collide, the fence marker coordinates
        can be passed to the QuoridorGame to validate the move.

        x_pos: initial x coordinate for the screen
        y_pos: initial y coordinate for the screen
        rec_width: width of the marker on the screen
        rec_height: height of the marker on the screen
        angle: either 'v' for vertical or 'h' for horizontal"""

        init_x_pos = x_pos  # store the initial x position for screen

        if angle == 'v':
            rows = 9
            columns = 8
            x = 1  # initial x coord for QuoridorGame
            y = 0  # initial y coord for QuoridorGame
        else:  # angle == 'h'
            rows = 8
            columns = 9
            x = 0
            y = 1

        init_x = x  # store the initial x coord for QuoridorGame board
        for row in range(rows):
            for column in range(columns):
                self._new_marker = Marker(x_pos, y_pos, rec_width, rec_height, \
                                          (x, y), angle)
                self._marker_group.add(self._new_marker)
                x_pos += 60
                x += 1
            y_pos += 60
            y += 1
            x_pos = init_x_pos  # reset the x axis since going from top to bottom
            x = init_x  # reset the x axis for QuoridorGame board too

    def create_rectangles(self):
        """"""
        x_pos = 120  # initial x coordinate
        y_pos = 100  # initial y coordinate
        x = 0  # initial x for QuoridorGame
        y = 0  # initial y for QuoridorGame
        for row in range(9):
            for column in range(9):
                self._new_rectangle = Rectangle(x_pos, y_pos, (x, y))
                self._rectangle_group.add(self._new_rectangle)
                x_pos += 60
                x += 1
            y_pos += 60
            y += 1
            x_pos = 120
            x = 0

    def create_fences(self, x_pos, y_pos, player, color):
        """
        Create fence sprites.

        x_pos: initial x coordinate for the screen
        y_pos: initial y coordinate for the screen
        player: which player's fence, 1 or 2

        """
        init_x = x_pos
        x = 0  # initial x for QuoridorGame
        y = 0  # initial y for QuoridorGame
        for row in range(5):
            for column in range(2):
                self._new_fence = Fence(x_pos, y_pos, (x, y), player, color)
                self._fence_group.add(self._new_fence)
                x_pos += 30
                x += 1
            y_pos += 60
            y += 1
            x_pos = init_x
            x = 0


    def get_screen(self):
        return self._screen

    def deselect_object(self, fence_clicked, pawn_clicked):
        """Method will deselect previously selected """
        if fence_clicked != None:
            fence_color = fence_clicked.get_fence_color_unclicked()
            fence_clicked.set_color(fence_color)
            fence_clicked = None
        if pawn_clicked != None:
            pawn_color = pawn_clicked.get_pawn_color_unclicked()
            pawn_clicked.set_color(pawn_color)
            pawn_clicked = None
        return fence_clicked, pawn_clicked

    def play(self):
        """"""
        running = True
        pawn_clicked = None
        fence_clicked = None
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                # Check for a winner
                if self._myGame.get_winner() != None:
                    winner = self._myGame.get_winner()
                    # Put winner on middle of screen
                    win_txt = Text('PLAYER '+str(winner)+' WINS!', 350, 350)
                    self._text_group.add(win_txt)
                # Check for a keyboard button press
                if event.type == KEYDOWN:
                    # Check for Escape button
                    if event.key == K_ESCAPE:
                        # Exit game
                        running = False
                    # Check for Left button
                    if event.key == pygame.K_LEFT and fence_clicked != None:
                        # Rotate fence 90 degrees
                        fence_clicked.rotate(self._screen)
                # Check if X pushed
                elif event.type == QUIT:
                    # Exit game
                    running = False
                # Check if mouse clicked
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Keep track of mouse click
                    click = 0
                    # Get the x and y coordinates of the mouse
                    mouse_pos = pygame.mouse.get_pos()

                    if click == 0:
                        # Check if a pawn was clicked
                        for pawn in self.pawn_group:
                            # if pawn was selected
                            if pawn.rect.collidepoint(mouse_pos):
                                print("Pawn clicked")
                                # deselect previously selected pawn / fence
                                fence_clicked, pawn_clicked = \
                                    self.deselect_object(fence_clicked, pawn_clicked)
                                # save the pawn object
                                pawn_clicked = pawn
                                # get the player #
                                player = pawn_clicked.get_player()
                                # change pawns color
                                pawn_clicked.set_color(PAWN_COLOR_CLICKED)
                                click += 1

                    if click == 0:
                        # Check if a fence was clicked
                        for fence in self._fence_group:
                            # store if fence has been played yet
                            is_used = fence.get_used()
                            # if fence was selected
                            if fence.rect.collidepoint(mouse_pos) and is_used == False:
                                print("Fence clicked")
                                # deselect prev selected pawn / fence
                                fence_clicked, pawn_clicked = \
                                    self.deselect_object(fence_clicked, pawn_clicked)
                                # save the fence object
                                fence_clicked = fence
                                # get the player #
                                player = fence_clicked.get_player()
                                # change fence color
                                fence_clicked.set_color(FENCE_COLOR_CLICKED)
                                click += 1

                    if click == 0 and fence_clicked != None:
                        print("Check for where to move")
                        # Move a fence
                        # while fence_clicked != None:
                        # Check which fence marker was clicked
                        for marker in self._marker_group:
                            if marker.rect.collidepoint(mouse_pos) and click < 3:
                                # get screen coordinates of marker
                                x = marker.rect.centerx
                                y = marker.rect.centery
                                # get coord of marker
                                coord = marker.get_coord()
                                # get angle of marker
                                angle = marker.get_angle()
                                # call QuoridorGame move_pawn with the:
                                #   player and coordinates
                                # check the result
                                result = self._myGame.place_fence(player, angle, coord)
                                # if result is true then move was successful
                                # update move on screen
                                if result == True:
                                    # fence starts vertically, rotate fence
                                    # if horizontal marker clicked
                                    if angle == 'h':
                                        fence_clicked.rotate(self._screen)
                                    fence_clicked.move_fence(x, y)
                                    fence_clicked.set_used()
                                fence_color = fence_clicked.get_fence_color_unclicked()
                                fence_clicked.set_color(fence_color)
                                fence_clicked = None
                                click += 1

                    if click == 0 and pawn_clicked != None:
                        # Move a pawn
                        # while pawn_clicked != None:
                        # Check which rectangle was clicked
                        for rectangle in self._rectangle_group:
                            if rectangle.rect.collidepoint(mouse_pos) and click < 3:
                                # get screen coordinates of rectangle
                                x = rectangle.rect.centerx
                                y = rectangle.rect.centery
                                # get coord of rectangle
                                coord = rectangle.get_coord()
                                # call QuoridorGame move_pawn with the:
                                #   player and coordinates
                                # check the result
                                result = self._myGame.move_pawn(player, coord)
                                # if result is true then move was successful
                                # update move on screen
                                if result == True:
                                    pawn_clicked.move_pawn(x, y)
                                pawn_color = pawn_clicked.get_pawn_color_unclicked()
                                pawn_clicked.set_color(pawn_color)
                                pawn_clicked = None
                                click += 1

            # I was having an issue where an object was moved, such
            # as a fence, and a ghost of the object was left behind
            # in the original location.  The only way I could figure
            # out how to clear the ghost was to use the fill() method
            self._screen.fill((0, 0, 0))  # need this to remove the old fence after rotating
            self._rectangle_group.draw(self._screen)  # add rectangles to screen

            self.pawn_group.draw(self._screen)  # add pawns to screen
            self._marker_group.draw(self._screen)  # add pawns to screen
            self._fence_group.draw(self._screen)  # add fences to screen
            self._text_group.draw(self._screen) # add text ot screen
            pygame.display.flip()  # updates the screen


newGame = Simulate()
newGame.play()








