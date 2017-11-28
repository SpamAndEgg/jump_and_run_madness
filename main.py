import pygame
import time
import random

# Initiate pygame (First thing you have to do).
pygame.init()

# Define window width and height.
display_width = 800
display_height = 600
# Constants depending on screen size.
speed_run = display_width / 50
speed_jump = display_height /15

# Define gravity [pixel per frame]
gravity = display_height/100
max_fall_velocity = display_height/25



# Setup window to display game (width, height).
Game_display = pygame.display.set_mode((display_width, display_height))

# LOAD IMAGES AND GET THE IMAGE SIZES
# Player
img_character = pygame.image.load('image/character.png')
img_char_size = img_character.get_rect()
character_width = img_char_size[2]
character_height = img_char_size[3]
# Monster
img_monster = pygame.image.load('image/monster.png')
img_monster_size = img_monster.get_rect()
monster_width = img_monster_size[2]
monster_height = img_monster_size[3]
# Monster dead
img_monster_dead = pygame.image.load('image/monster_dead.png')
img_monster_dead_size = img_monster_dead.get_rect()
monster_width_dead = img_monster_dead_size[2]
monster_height_dead = img_monster_dead_size[3]


class Player:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = 0
        self.x_velocity_flight = 0
        self.x_velocity_ground = 0
        self.y_velocity = 0
        self.is_on_ground = False

    def blit(self):
        x_pos_on_screen = self.x_pos - camera.left_edge
        Game_display.blit(img_character, (x_pos_on_screen, self.y_pos))

    def update_pos(self):
        # Update character position.
        self.y_velocity += gravity
        if self.y_velocity > max_fall_velocity:
            self.y_velocity = max_fall_velocity
        if self.is_on_ground:
            # Increase the x velocity stepwise.
            self.x_velocity += self.x_velocity_ground/10
            if abs(self.x_velocity) > abs(self.x_velocity_ground):
                self.x_velocity = self.x_velocity_ground
        else:
            self.x_velocity = self.x_velocity_flight

        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        self.collision_check()
        # Make sure the character won't leave the screen.
        if self.x_pos < 0:
            self.x_pos = 0
        #elif self.x_pos > display_width - character_width:
        #    self.x_pos = display_width - character_width
        if self.y_pos < 0:
            self.y_pos = 0
        elif self.y_pos > display_height - character_height:
            # If character goes outsite of bottom of screen he dies.
            display_message('YOU FELL THROUGH THE GROUND, NOW YOU ARE DEAD!!')

    def collision_check(self):
        x_change = self.x_velocity
        y_change = self.y_velocity
        self.is_on_ground = False
        # Iterate over each ground element and check if a collision is detected.
        for i_ground in level.active_ground:
            x_collision = False
            on_ground_before = False
            y_collision = False

            if self.x_pos < i_ground[0] + i_ground[2] and self.x_pos + character_width > i_ground[0]:
                x_collision = True

            if self.x_pos-x_change < i_ground[0] + i_ground[2] and self.x_pos-x_change + character_width > i_ground[0]:
                on_ground_before = True

            if self.y_pos < i_ground[1] + i_ground[3] and self.y_pos + character_height > i_ground[1]:
                y_collision = True

            if x_collision and y_collision:
                # Check if player hit ground from left or right.
                if x_change > 0 and not on_ground_before:
                    self.x_pos = i_ground[0] - character_width
                    self.x_velocity_flight = 0
                elif x_change < 0 and not on_ground_before:
                    self.x_pos = i_ground[0] + i_ground[2]
                    self.x_velocity_flight = 0
                # Check if player hit ground from top or bottom
                elif y_change > 0:
                    # Player is on ground.
                    self.y_pos = i_ground[1] - character_height
                    self.is_on_ground = True
                    self.y_velocity = 0
                elif y_change < 0:
                    self.y_pos = i_ground[1] + i_ground[3]



class Camera:
    def __init__(self):
        self.left_edge = 0
        self.right_edge = display_width
        # The push values define where the character
        self.push_left = display_width * 0.15
        self.push_right = display_width * 0.7
        # Define a max. camera x velocity. This is used to define how far the level ground will be loaded.
        self.max_velocity = 20

    def update(self):
        # When the player is outside the push boundaries, he/she pushes the camera equaly far to the side. One exeption
        # is the left boundary of the screen, the screen stays there.

        # Calculate the player position on the screen.
        player_x_pos_on_screen = player.x_pos - self.left_edge
        # Push camera to the right.
        if player_x_pos_on_screen > self.push_right:
            self.left_edge += player_x_pos_on_screen - self.push_right

        # Push camera to the left (not below level start tho).
        elif player_x_pos_on_screen < self.push_left:
            self.left_edge += player_x_pos_on_screen - self.push_left
            # Check if camera would go beyond level start.
            if self.left_edge < 0:
                self.left_edge = 0

        # Update the right edge of the screen.
        self.right_edge = self.left_edge + display_width


class Level:
    def __init__(self):
        # Grounds are saved in the format [x pos left top corner, y pos left top corner, width, height].
        self.ground = []
        self.active_ground = []
        self.x_pos = 0

    # Add a new ground box to the level.
    def add_ground(self, new_ground):
        self.ground.append(new_ground)

    # Give back the active ground that is displayed on the next frame (according to the player location).
    def update_ground(self):
        # Check each ground element if it lies within the camera frame plus max. camera velocity (so each element for
        # the next frame is given out).

        this_ground = []
        for i_ground in self.ground:
            # Check, if left edge of floor is not out of the right side of the camera and right edge of floor is not
            # out of the left side of the camera.
            left_ok = i_ground[0] + i_ground[2] > camera.left_edge
            right_ok = i_ground[0] < camera.right_edge
            if left_ok and right_ok:
                this_ground.append(i_ground)

        self.active_ground = this_ground

    def draw_ground(self):
        # Draw all the active ground on the screen.
        for i_ground in self.active_ground:
            # Store list in new variable (by value, not by pointer).
            this_ground = i_ground[:]
            # Update the x location of the ground on the screen.
            this_ground[0] -= camera.left_edge
            # Draw the ground on the screen.
            pygame.draw.rect(Game_display, black, this_ground)


class Enemy:
    def __init__(self, x_enemy, y_enemy):
        self.x_speed = 7
        self.y_speed = 0
        self.x_pos = x_enemy
        self.x_pos_on_screen = []
        self.y_pos = y_enemy
        self.is_dead = False
        self.width = monster_width
        self.height = monster_height

    def blit(self):
        if self.is_dead:
            Game_display.blit(img_monster_dead, (self.x_pos_on_screen, self.y_pos))
        else:
            Game_display.blit(img_monster, (self.x_pos_on_screen, self.y_pos))

    def collision_check(self):
        is_headjump = False
        is_kill_player = False
        x_collision = False
        y_collision = False
        # Check if there is a collision from any side (top, right, down, left).
        if not self.is_dead:
            # Check if x range of monster and character overlap.
            if player.x_pos < self.x_pos + self.width and player.x_pos + character_width > self.x_pos:
                x_collision = True
            if player.y_pos + character_height > self.y_pos and player.y_pos < self.y_pos + self.height:
                y_collision = True
            if x_collision and y_collision:
                # Check for head collision.
                if player.y_pos + character_height - self.y_pos < character_height / 5:
                    is_headjump = True
                else:
                    is_kill_player = True

        # If the hero touches the monster (unless headjump) the hero dies.
        if is_kill_player:
            display_message('YOU WERE KILLED BY A HORRIBLE MONSTER!')
        # If the hero jumped on the monsters head, it dies.
        if is_headjump:
            self.is_dead = True
            self.x_speed = 0
            # Even out the hight differences of the two pictures for alive and dead monster.
            self.y_pos += monster_height - monster_height_dead

    # Update the enemy for the next frame.
    def update_pos(self):
        # Update x position.
        self.x_pos -= self.x_speed
        # Update y position. Therefore first check falling due to gravity.

    def draw(self):
        # Find position on screen.
        self.x_pos_on_screen = self.x_pos - camera.left_edge
        # Draw the enemy.
        self.blit()
        # Check collision with player.
        self.collision_check()



def Text_object(text, font):
    Text_surface = font.render(text, True, black)
    return Text_surface, Text_surface.get_rect()

def display_message(text_to_display):
    text_style = pygame.font.Font("data/SEASRN__.ttf", 12)
    Text_surface, Text_rectangle = Text_object(text_to_display, text_style)
    Text_rectangle.center = ((display_width/2), (display_height/2))
    Game_display.blit(Text_surface, Text_rectangle)

    pygame.display.update()

    time.sleep(2)
    game_loop()



# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# Set caption (name of window of game).
pygame.display.set_caption('Test Game')
# Handles frames per seconds (defined later on).
clock = pygame.time.Clock()


def game_loop():
    global player, level, monster, camera
    # Initiate the level.
    level = Level()
    # Add a ground to the level
    level.add_ground([500, display_height*.8, 100, 500])
    level.add_ground([200, display_height * 0.95, 10000, display_height * 0.05])
    level.add_ground([0,400,200,50])
    # Initiate the player.
    x_character = (display_width * 0.45)
    y_character = (display_height * 0.8)
    player = Player(x_character, y_character)
    # Initiate monsters.
    this_monster_start = display_width
    monster = []
    for i_monster in range(5):
        this_monster_start += random.randrange(monster_width, 1000)
        monster.append(Enemy(this_monster_start, y_character))


    # Initiate the camera.
    camera = Camera()

    # Initiate values
    x_change_char = 0
    y_change_char = 0

    x_change_camera = 0

    # Set parameters that end the game.
    is_game_over = False

    # MAIN GAME LOOP
    while not is_game_over:

        # Iterate over every event (per frame) happening.
        for event in pygame.event.get():
            # Check if user wants to quit the game.
            if event.type == pygame.QUIT:
                # Uninitiate pygame.
                pygame.quit()
                quit()
            # Arrow key events.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_velocity_ground = -speed_run
                if event.key == pygame.K_RIGHT:
                    player.x_velocity_ground = speed_run
                if event.key == pygame.K_UP:
                    if player.is_on_ground:
                        # Player starts jumping
                        player.y_velocity = -speed_jump
                        player.x_velocity_flight = player.x_velocity
                if event.key == pygame.K_DOWN:
                    # player.y_velocity = speed_jump
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_velocity_ground = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # player.y_velocity = 0
                    pass


        # Update the player position
        player.update_pos()

        # Update camera.
        camera.update()
        # Update the active ground for this frame.
        level.update_ground()

        for i_monster in monster:
            # Update the new position of the monster.
            i_monster.update_pos()

        # DRAW SCREEN
        # Paint background of the display.
        Game_display.fill(white)
        # Draw ground.
        level.draw_ground()

        pygame.draw.rect(Game_display, black, [500-camera.left_edge,110,200,60])
        # Draw new player position.
        player.blit()
        # Update monster positions.


        # Show new frame on screen. update allows to update single parameters if given as input parameters, otherwise it
        # updates the whole screen. Alternatively you could use the flip function, which always updates the whole screen.
        pygame.display.update()
        # Define frames per seckond.
        clock.tick(30)

# Start the game.
game_loop()
# Uninitiate pygame.
pygame.quit()
quit()




