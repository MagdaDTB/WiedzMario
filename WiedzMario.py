# use pygame
import pygame

# predefined global variables

# fill colors
BACKGROUND_FILL = (0, 128, 255)
PLAYER_FILL = (255, 128, 0)
SURFACE_FILL = (0, 153, 0)

# screen size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
PLAYER_SIZE = 40

# player stride
STRIDE = 4

# clock tick
TICK = 50

# class representing fixed position objects
class EnvSurface(pygame.sprite.Sprite):
	# constructor allowing to set positon, size and color of environment structures
	def __init__(self, pos_x, pos_y, width, height, fill_color):
		# call the parent constructor
		pygame.sprite.Sprite.__init__(self)
			
		# create a surface of a given size
		self.image = pygame.Surface([width, height])
		# fill it with given color
		self.image.fill(fill_color)
			
		# place the surface in desired position (defined by top left vertex)
		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y
			
       
# class representing the player
class Player(pygame.sprite.Sprite):
	# constructor allowing to set positon, size and color of the player
	def __init__(self, pos_x, pos_y, size, fill_color):
		# call the parent constructor
		pygame.sprite.Sprite.__init__(self) #super(Player, self).__init__(self)
			
		# set player size
		self.image = pygame.Surface([size, size])
		self.image.fill(fill_color)
	 
		# place the player in desired position (defined by top left vertex)
		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y
	 
		# set initial movement indicator to zero
		self.change_x = 0
		self.change_y = 0
		self.walls = None
		
    # update next movement depending on user's actions    
	def change_pos(self, move_x, move_y):
		self.change_x += move_x
		self.change_y += move_y

	# update player position depending on user's action and collision detection
	def update(self):
		# move player horizontally
		self.rect.x += self.change_x
		
		# check for collisions (x axis)
		collisions = pygame.sprite.spritecollide(self, self.walls, False)
		for col in collisions:
			# make sure that there are no overlapping pixels
			if self.change_x < 0:
				self.rect.left = col.rect.right
			else:
				self.rect.right = col.rect.left
		
		# move player vertically
		self.rect.y += self.change_y
	 
		# check for collisions (y axis)
		collisions = pygame.sprite.spritecollide(self, self.walls, False)
		for col in collisions:
			# make sure that there are no overlapping pixels
			if self.change_y < 0:
				self.rect.top = col.rect.bottom
			else:
				self.rect.bottom = col.rect.top
					
                
# initialize pygame
pygame.init()
 
# create the game screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# set the window title
pygame.display.set_caption('WiedzMario')
 
# store all sprites used in game
sprites = pygame.sprite.Group()
 
# store all environment structures
surfaces = pygame.sprite.Group()
 
# ground surface
env_surface = EnvSurface(0, 568, 1024, 200, SURFACE_FILL)
surfaces.add(env_surface)
sprites.add(env_surface)
 
# some other surfaces
env_surface = EnvSurface(100, 300, 400, 50, SURFACE_FILL)
surfaces.add(env_surface)
sprites.add(env_surface)
 
env_surface = EnvSurface(300, 150, 300, 30, SURFACE_FILL)
surfaces.add(env_surface)
sprites.add(env_surface)

env_surface = EnvSurface(600, 400, 424, 40, SURFACE_FILL)
surfaces.add(env_surface)
sprites.add(env_surface)
 
# create the player 
player = Player(20, 528, PLAYER_SIZE, PLAYER_FILL)
player.walls = surfaces
 
sprites.add(player)
 
clock = pygame.time.Clock()
 
exit_clicked = False

# the event loop 
while not exit_clicked:
	# process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_clicked = True
		# on key press
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_pos(-STRIDE, 0)
            elif event.key == pygame.K_RIGHT:
                player.change_pos(STRIDE, 0)
            elif event.key == pygame.K_UP:
                player.change_pos(0, -STRIDE)
            elif event.key == pygame.K_DOWN:
                player.change_pos(0, STRIDE)
		# on key release
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_pos(STRIDE, 0)
            elif event.key == pygame.K_RIGHT:
                player.change_pos(-STRIDE, 0)
            elif event.key == pygame.K_UP:
                player.change_pos(0, STRIDE)
            elif event.key == pygame.K_DOWN:
                player.change_pos(0, -STRIDE)
 
    # currently only updates player position
    sprites.update()
 
    # fill screen
    screen.fill(BACKGROUND_FILL)
 
	# draw scene
    sprites.draw(screen)
 
    pygame.display.flip()
 
    clock.tick(TICK)
 
# after (x) button is clicked
pygame.quit()

