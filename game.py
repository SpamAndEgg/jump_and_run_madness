import pygame
import time
import random
from math import floor
from init_convolution import convolution
import visualisation

import threading


# SET OF AN OUTPUT FOR THE CONVOLUTIONAL NEURAL NETWORK IS SUPPOSED TO BE GIVEN OUT.
create_output = True

# Initiate pygame (First thing you have to do).
pygame.init()

# Define window width and height.
display_width = 800
display_height = 600
# Constants depending on screen size.
speed_run = display_width / 50
speed_jump = display_height / 15

# Define gravity [pixel per frame]
gravity = display_height / 100
max_fall_velocity = display_height / 25
this_frame = []

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


# Collision check with ground for player and enemy object.
def collision_check_ground(this_object):
    this_object.is_on_ground = False
    for i_ground in level.active_ground:
        x_collision = False
        on_ground_before = False
        y_collision = False
        # Check if object and this ground collide in x direction.
        if this_object.x_pos < i_ground[0] + i_ground[2] and this_object.x_pos + this_object.width > i_ground[0]:
            x_collision = True
        # Check if object had been on ground before.
        if this_object.x_pos - this_object.x_change < i_ground[0] + i_ground[2] and this_object.x_pos - \
                this_object.x_change + this_object.width > i_ground[0]:
            on_ground_before = True
        # Check if object and this ground collide in y direction.
        if this_object.y_pos < i_ground[1] + i_ground[3] and this_object.y_pos + this_object.height > i_ground[1]:
            y_collision = True

        if x_collision and y_collision:
            # Check if player hit ground from left or right.
            if this_object.x_change > 0 and not on_ground_before:
                this_object.x_pos = i_ground[0] - this_object.width
                this_object.x_velocity_flight = 0
                this_object.x_velocity = 0
            elif this_object.x_change < 0 and not on_ground_before:
                this_object.x_pos = i_ground[0] + i_ground[2]
                this_object.x_velocity_flight = 0
                this_object.x_velocity = 0
            # Check if player hit ground from top or bottom
            elif this_object.y_change > 0:
                # Player is on ground.
                this_object.y_pos = i_ground[1] - this_object.height
                this_object.is_on_ground = True
                this_object.y_velocity = 0
            elif this_object.y_change < 0:
                this_object.y_pos = i_ground[1] + i_ground[3]


class Player:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        # Max ever reached x position in level.
        self.x_pos_max = x_pos
        self.y_pos = y_pos
        self.x_change = []
        self.y_change = []
        self.x_velocity = 0
        self.x_velocity_flight = 0
        self.x_velocity_ground = 0
        self.y_velocity = 0
        self.is_on_ground = False
        self.width = character_width
        self.height = character_height

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
        # Update max. ever reached x position.
        if self.x_pos > self.x_pos_max:
            self.x_pos_max = self.x_pos
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
        elif self.x_pos > 6000:
            display_message('YEEHA, YOU WON THE GAME!!')

    def collision_check(self):
        self.x_change = self.x_velocity
        self.y_change = self.y_velocity
        #self.is_on_ground = False
        # Iterate over each ground element and check if a collision is detected.
        collision_check_ground(self)


class Enemy:
    def __init__(self, x_enemy, y_enemy):
        self.x_velocity = -7
        self.x_base_velocity = -7
        self.y_velocity = 0
        self.x_change = []
        self.y_change = []
        self.x_pos = x_enemy
        self.last_x_pos = []
        self.x_pos_on_screen = []
        self.y_pos = y_enemy
        self.is_dead = False
        self.is_on_ground = False
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
        # COLLISION CHECK PLAYER
        # Check if there is a collision from any side (top, right, down, left).
        if not self.is_dead:
            # Check if x range of monster and character overlap.
            if player.x_pos < self.x_pos + self.width and player.x_pos + player.width > self.x_pos:
                x_collision = True
            if player.y_pos + player.height > self.y_pos and player.y_pos < self.y_pos + self.height:
                y_collision = True
            if x_collision and y_collision:
                # Check for head collision (player had been above monster head in last frame).
                if player.y_pos + player.height - player.y_velocity < self.y_pos:
                    is_headjump = True
                else:
                    is_kill_player = True

        # COLLISION CHECK LEVEL
        self.x_change = self.x_velocity
        self.y_change = self.y_velocity
        collision_check_ground(self)

        # If the hero touches the monster (unless headjump) the hero dies.
        if is_kill_player:
            display_message('YOU WERE KILLED BY A HORRIBLE MONSTER!')
        # If the hero jumped on the monsters head, it dies.
        if is_headjump:
            self.is_dead = True
            level.score += 1000
            self.x_velocity = 0
            # Even out the hight differences of the two pictures for alive and dead monster.
            #self.y_pos += monster_height - monster_height_dead
            self.height = monster_height_dead

    # Update the enemy for the next frame.
    def update_pos(self):
        # Update x position.
        self.x_pos += self.x_velocity
        # Update y position
        self.y_velocity += gravity
        if self.y_velocity > max_fall_velocity:
            self.y_velocity = max_fall_velocity
        # Update y position. Therefore first check falling due to gravity.
        self.y_pos += self.y_velocity
        # Check collision with player.
        self.collision_check()
        # If the monster can't move forward, reverse its running direction.
        if self.last_x_pos == self.x_pos and not self.is_dead:
            self.x_base_velocity *= -1
            self.x_velocity = self.x_base_velocity
        # Update the last position.
        self.last_x_pos = self.x_pos

    def draw(self):
        # Find position on screen.
        self.x_pos_on_screen = self.x_pos - camera.left_edge

        # Draw the enemy.
        self.blit()


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
        self.score = 0

    # Add a new ground box to the level.
    def add_ground(self, new_ground):
        self.ground.append(new_ground)

    # Give back the active ground that is displayed on the next frame (according to the player location).
    def update_ground(self):

        # PROBLEM: Ground elements are only dependant of character vision, enemies are not effected. Therefore the whole
        # gound is given back as active ground
        self.active_ground = self.ground

    def draw_ground(self):
        # Draw all the active ground on the screen.
        for i_ground in self.active_ground:
            # Store list in new variable (by value, not by pointer).
            this_ground = i_ground[:]
            # Update the x location of the ground on the screen.
            this_ground[0] -= camera.left_edge
            # Draw the ground on the screen.
            pygame.draw.rect(Game_display, black, this_ground)






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


def display_game_score(score):
    text_style = pygame.font.Font("data/SEASRN__.ttf", 12)
    Text_surface, Text_rectangle = Text_object(str(score), text_style)
    Text_rectangle.center = ((display_width/9), (display_height/9))
    Game_display.blit(Text_surface, Text_rectangle)


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


if create_output:

    import threading

    class VisualConvolutionThread(threading.Thread):

        def run(self):
            # Set up the animation window which will be updated every "interval_time" miliseconds.
            interval_time = 50
            def start_animation():
                global this_conv_frame
                import matplotlib.pyplot as plt
                from matplotlib.animation import FuncAnimation

                def update(frame):
                    img.set_data(this_conv_frame)

                def init():
                    img.set_data(this_conv_frame)

                fig, ax = plt.subplots(1, 1)
                img = ax.imshow(this_conv_frame, cmap='gist_gray_r', vmin=0, vmax=33488638)
                ani = FuncAnimation(fig, update, init_func=init, blit=False, interval=interval_time)
                plt.show()
                #input()
                return ani


            # Initiate the first image convolution
            this_frame = pygame.surfarray.array2d(Game_display)
            # calculate an input for the neural net by the kernel.
            this_conv_frame = convolution(this_frame)
            # Visualize the input convolution.
            ani = start_animation()

    visual_convolution = VisualConvolutionThread()
    visual_convolution.start()


def game_loop():
    global player, level, monster, camera, this_frame, this_conv_frame
    # Initiate the level.
    level = Level()
    # Add a ground to the level
    level.add_ground([500, display_height*.8, 100, 500])
    level.add_ground([200, display_height * 0.95, 10000, display_height * 0.05])
    level.add_ground([0,400,200,50])
    level.add_ground([800, display_height * 0.9, 1300, display_height * 0.1])
    level.add_ground([950, display_height * 0.85, 600, display_height * 0.15])
    level.add_ground([2000, display_height * 0.9, 2000, display_height * 0.1])
    level.add_ground([2100, display_height * 0.85, 1300, display_height * 0.15])
    level.add_ground([2200, display_height * 0.75, 200, display_height * 0.25])
    level.add_ground([5000, display_height * 0.8, 200, display_height * 0.2])
    # Initiate the player.
    x_character = (display_width * 0.45)
    y_character = (display_height * 0.8)
    player = Player(x_character, y_character)
    # Initiate monsters.
    this_monster_start = display_width
    monster = []
    for i_monster in range(5):
        this_monster_start += random.randrange(monster_width, 1000)
        monster.append(Enemy(this_monster_start, 0))


    # Initiate the camera.
    camera = Camera()

    # Initiate values
    is_pressed_arrow_left = False
    is_pressed_arrow_right = False



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
                    is_pressed_arrow_left = True
                if event.key == pygame.K_RIGHT:
                    player.x_velocity_ground = speed_run
                    is_pressed_arrow_right = True
                if event.key == pygame.K_UP:
                    if player.is_on_ground:
                        # Player starts jumping
                        player.y_velocity = -speed_jump
                        player.x_velocity_flight = player.x_velocity
                if event.key == pygame.K_DOWN:
                    # player.y_velocity = speed_jump
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    is_pressed_arrow_left = False
                if event.key == pygame.K_RIGHT:
                    is_pressed_arrow_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_velocity_ground = 0
                    # Check if the other arrow key is still pressed, so the character won't stop moving.
                    if is_pressed_arrow_left:
                        player.x_velocity_ground = -speed_run
                    elif is_pressed_arrow_right:
                        player.x_velocity_ground = speed_run

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # player.y_velocity = 0
                    pass

        # Update the player position
        player.update_pos()
        # Update monsters.
        for i_monster in monster:
            # Update the new position of the monster.
            i_monster.update_pos()

        # Update camera.
        camera.update()
        # Update the active ground for this frame.
        level.update_ground()




        # DRAW SCREEN
        # Paint background of the display.
        Game_display.fill(white)
        # Draw finish area.
        pygame.draw.rect(Game_display, green, [6000 - camera.left_edge, 200, display_height*0.7, display_height*0.3])
        # Draw ground.
        level.draw_ground()

        pygame.draw.rect(Game_display, black, [500-camera.left_edge,110,200,60])

        # Draw new player position.
        player.blit()
        # Update monster positions.
        for i_monster in monster:
            i_monster.draw()

        # Update game score.
        game_score = player.x_pos_max - x_character + level.score
        display_game_score(floor(game_score))

        # Show new frame on screen. update allows to update single parameters if given as input parameters, otherwise it
        # updates the whole screen. Alternatively you could use the flip function, which always updates the whole screen.
        pygame.display.update()

        if create_output:
            # Copy the current frame as array.
            # Note that array2d will temporarily copy lock the screen while raw pixels are copied into array.

            this_frame = pygame.surfarray.array2d(Game_display)

            #this_frame = np.zeros((800,600))
            # calculate an input for the neural net by the kernel.
            this_conv_frame = convolution(this_frame)

            # IMPLEMENT CONVOLUTION VISUALIZATION HERE


        # Define frames per seckond.
        clock.tick(30)

# Start the game.
game_loop()
# Uninitiate pygame.
pygame.quit()
quit()


class VisualizeConvolutionThread(threading.Thread):
    def run(self):
        global this_frame
        import visualisation
        # Initiate the first image convolution
        #this_frame = pygame.surfarray.array2d(Game_display)
        # Wait until "this_frame" was defined by game thread.
        defined_this_frame = False
        while not defined_this_frame:
            if this_frame.any():
                defined_this_frame = True
            else:
                time.sleep(0.1)

        # calculate an input for the neural net by the kernel.
        this_conv_frame = convolution(this_frame)
        # Delete the frame to set it free.
        #del this_frame
        # Visualize the input convolution.
        img = visualisation.start(this_conv_frame)

        while True:

            # Get the current frame as array.
            #this_frame = pygame.surfarray.array2d(Game_display)
            #this_frame = np.zeros((800,600))
            # calculate an input for the neural net by the kernel.
            this_conv_frame = convolution(this_frame)

            img.set_data(this_conv_frame)

            del this_frame
            # Update the convolutional image.
            #visualisation.update(img, img_ax, this_conv_frame)
            time.sleep(0.1)



