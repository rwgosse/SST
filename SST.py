import pygame
import sys
import random
import math
import threading

pygame.init()


# Initialize the screen #####################################################################################################
# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Star Trek")

clock = pygame.time.Clock()
FPS = 60  # Frames per second
### END SCREEN SET UP #######################################################################################################



### DEFINE CONSTANTS: #######################################################################################################
GRID_SIZE = 8
SQUARE_SIZE = 80

GRID_ORIGIN_X, GRID_ORIGIN_Y = SQUARE_SIZE, SQUARE_SIZE*2
REPORT_TITLE_MARGIN = 300
REPORT_STATUS_MARGIN = 150

# Constants for the quadrant map
QUADRANT_SIZE = 8  # 8x8 grid
QUADRANT_MARGIN = 20  # Margin from the right and bottom of the screen
QUADRANT_SQUARE_SIZE = 40  # Size of each square in the quadrant map
QUADRANT_ORIGIN_X = SCREEN_WIDTH - QUADRANT_SIZE * QUADRANT_SQUARE_SIZE - QUADRANT_MARGIN
QUADRANT_ORIGIN_Y = SCREEN_HEIGHT - QUADRANT_SIZE * QUADRANT_SQUARE_SIZE - QUADRANT_MARGIN


# Colors (RGB values)
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (50, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GREEN =(0,50,0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 50)

# Fonts
FONT24 = pygame.font.Font(None, 24)


MAX_ENERGY = 3000
WARP_ENERGY_PER = 100
RAISE_SHIELD_PER = 50
SHIELD_LEVELS = [0, 25, 50, 75, 100]

MAX_TORPEDO_QTY = 10
TORPEDO_DAMAGE = 500
TORPEDO_SPEED = 1
TORPEDO_ENERGY_USAGE = 50
### END CONSTANTS ###########################################################################################################

### LOAD ASSETS #############################################################################################################

# player_image = pygame.image.load("player.png").convert_alpha()
# font = pygame.font.Font(None, 36)

EARTHING_SHIP = pygame.image.load("earthling.png").convert_alpha() 
BASE_IMAGE = pygame.image.load("base.png").convert_alpha()
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (SQUARE_SIZE*.75, SQUARE_SIZE*.75))  # Scale to grid square size 

ENEMY_SHIP = pygame.image.load("avenger.png").convert_alpha() 

GRID_BACKGROUND = pygame.image.load("starfield.png").convert_alpha()
GRID_BACKGROUND = pygame.transform.scale(GRID_BACKGROUND, (GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE)) 

# AUDIO CONSTANTS -------------------------------------------------------------
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

ALARM_CHANNEL = pygame.mixer.Channel(1)
RED_ALERT = pygame.mixer.Sound("alarm01.mp3")

WEAPON_CHANNEL = pygame.mixer.Channel(2)
WEAPON_CHANNEL.set_volume(0.25)
PHASER_SOUND = pygame.mixer.Sound("earthling-pd.wav")
MISSILE_SOUND = pygame.mixer.Sound("earthling-mx.wav")
SHIELD_UP = pygame.mixer.Sound("melnorme-charge.wav")
SHIELD_DOWN = pygame.mixer.Sound("melnorme-confuse.wav")

EXPLOSION_CHANNEL = pygame.mixer.Channel(3)
EXPLOSION_CHANNEL.set_volume(0.1)
SHIP_DEATH_SOUND = pygame.mixer.Sound("shipdies.wav")
MEDIUM_EXPLOSION = pygame.mixer.Sound("boom-medium.wav")
WARP_SOUND = pygame.mixer.Sound("tng_slowwarp_clean.mp3")

MUSIC_CHANNEL = pygame.mixer.Channel(4)
MUSIC_CHANNEL.set_volume(.30)

VICTORY_DITTY = pygame.mixer.Sound("earthling-ditty.mp3")
VICTORY_DITTY_PLUS10 = pygame.mixer.Sound("earthling-ditty_plus10.mp3")
VICTORY_DITTY_MINUS10 = pygame.mixer.Sound("earthling-ditty_minus10.mp3")
VICTORY_DITTY_PLUS20 = pygame.mixer.Sound("earthling-ditty_plus20.mp3")
VICTORY_DITTY_MINUS20 = pygame.mixer.Sound("earthling-ditty_minus20.mp3")
VICTORY_DITTY_PLUS30 = pygame.mixer.Sound("earthling-ditty_plus30.mp3")
VICTORY_DITTY_MINUS30 = pygame.mixer.Sound("earthling-ditty_minus30.mp3")

VICTORY_DITTIES = [VICTORY_DITTY,VICTORY_DITTY_PLUS10, VICTORY_DITTY_MINUS10, VICTORY_DITTY_PLUS20,VICTORY_DITTY_MINUS20, VICTORY_DITTY_PLUS30, VICTORY_DITTY_MINUS30]
# -----------------------------------------------------------------------------


### END LOAD ASSETS #########################################################################################################


### DEFINE OBJECT CLASSES ###################################################################################################

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.orig_image = pygame.transform.scale(EARTHING_SHIP, (SQUARE_SIZE, SQUARE_SIZE))
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.grid_x = 4  # Starting grid position (column)
        self.grid_y = 3  # Starting grid position (row)
        self.last_move_direction = "up"
        


        self.stardate = 3801
        self.daysleft = 32

        self.condition = "GREEN"
        self.condition_color = GREEN

        self.quadrant_x = 0
        self.quadrant_y = 0

        self.torpedo_qty = 10
        self.energy = MAX_ENERGY

        self.hull = 1000

        self.shields = 0
        self.shields_on = False
        self.shield_level = 0
        self.num_enemies = 0
        self.num_starbases = 0
        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)

        self.sensor_range = 1

        self.update_position()

        self.all_sectors = []  # Dictionary to store Sector objects for each (quadrant_x, quadrant_y)
        self.generate_all_sectors()  # Generate all sectors when the game starts
        self.current_sector = None
        self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)  # Ensure player starts on an empty square


    def generate_all_sectors(self):
        """Generate and store a sector for each (quadrant_x, quadrant_y)."""
        for quadrant_x in range(8):  # Loop through quadrant_x values (0 to 7)
            for quadrant_y in range(8):  # Loop through quadrant_y values (0 to 7)
                sector_key = (quadrant_x, quadrant_y)
                
                # Create a new sector and generate its content (stars, bases)
                sector = Sector(quadrant_x, quadrant_y)
                sector.generate(self.grid_x, self.grid_y)
                
                # Store the sector in the visited_sectors dictionary
                self.all_sectors.append(sector)

    def enter_sector(self, quadrant_x, quadrant_y):
        """Ensure player enters the sector without starting on a star or base."""


        self.condition = "GREEN"

        enemy_count_ttl = 0
        starbase_count_ttl = 0
        for sector in self.all_sectors:
            enemy_count_ttl += sector.count_enemies()
            starbase_count_ttl += sector.count_bases()
        self.num_enemies = enemy_count_ttl
        self.num_starbases = starbase_count_ttl



        for sector in self.all_sectors:
            if (self.quadrant_x == sector.quadrant_x) and (self.quadrant_y == sector.quadrant_y):

                # Ensure player's starting position isn't on a star or base
                while sector.is_star_at(self.grid_x, self.grid_y) or sector.is_base_at(self.grid_x, self.grid_y) or sector.is_enemy_at(self.grid_x, self.grid_y):
                    self.move_away_from_star_or_base(sector)

                if sector != self.current_sector:


                    if sector.count_enemies() >=1 :
                        ALARM_CHANNEL.play(RED_ALERT,1)


                    for enemy in sector.enemies:
                        print(enemy.name, " : ", enemy.hull)



                return sector

    def move_away_from_star_or_base(self, sector):
        """Move the player to an adjacent empty square if their starting position is blocked by a star or base."""
        neighbors = [
            (self.grid_x, self.grid_y - 1),  # Up
            (self.grid_x, self.grid_y + 1),  # Down
            (self.grid_x - 1, self.grid_y),  # Left
            (self.grid_x + 1, self.grid_y)   # Right
        ]
        
        valid_neighbors = [
            (x, y) for x, y in neighbors if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE
        ]
        
        for nx, ny in valid_neighbors:
            if not sector.is_star_at(nx, ny) and not sector.is_base_at(nx, ny) and not sector.is_enemy_at(nx, ny):
                self.grid_x, self.grid_y = nx, ny
                return
        
        print(f"Warning: No valid adjacent square found for the player. Staying at ({self.grid_x}, {self.grid_y}).")

        

    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE)
        player_draw_y = GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE)
        self.rect.topleft = (player_draw_x, player_draw_y)

        if self.condition == "BLUE": 
            self.energy = MAX_ENERGY
            self.torpedo_qty = MAX_TORPEDO_QTY


        if self.energy >= MAX_ENERGY:
            self.energy = MAX_ENERGY
        if self.torpedo_qty >= MAX_TORPEDO_QTY:
            self.torpedo_qty = MAX_TORPEDO_QTY

        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)


    def shields_toggle(self):
        if self.shields_on:
            print("toggle shield off")
            self.shields_on = False
            self.shields = 0
            if self.shield_level > 0:
                WEAPON_CHANNEL.play(SHIELD_DOWN)
        else:
            
            if self.shield_level > 0:
                print("toggle shield on")
                if self.energy >= RAISE_SHIELD_PER:
                    self.shields_on = True
                    self.energy -= RAISE_SHIELD_PER
                    self.shields = self.shield_level * 10
                    WEAPON_CHANNEL.play(SHIELD_UP)
                else:
                    print("Energy too low for shields")
            else:
                print("Shield Level set too low")

                



        
    def fire_phasers(self,):
        """Fire phasers and damage enemies in the current sector."""
        num_enemy = self.current_sector.count_enemies()
        
        if num_enemy >= 1:

            phaser_power = prompt_phaser_power(SCREEN)
            if phaser_power > 0:

                if phaser_power <= self.energy:
                    
                    self.energy -= phaser_power

                    damage = phaser_power // num_enemy

                    WEAPON_CHANNEL.play(PHASER_SOUND)

                    # Apply damage to each enemy
                    for enemy in self.current_sector.enemies:
                        # Create and add a phasor blast
                        phasor_blast = Phasor_blast(self.grid_x, self.grid_y, enemy.grid_x, enemy.grid_y)
                        projectile_group.add(phasor_blast)

                        distance = abs(math.sqrt((self.grid_x - enemy.grid_x) ** 2 + (self.grid_y - enemy.grid_y) ** 2))
                        

                        range_reduction = (int(distance)-1) * 5

                        
                        remaining_damage = damage - range_reduction

                        # Add randomness to the damage
                        remaining_damage = int(remaining_damage * random.uniform(0.9, 1.1))  # ±10% random variance

                        print("range", int(distance), " @ ", remaining_damage, " DMG")

                        # Check and apply damage to shields first
                        if enemy.shields > 0:
                            shields_before = enemy.shields
                            if remaining_damage >= enemy.shields:
                                remaining_damage -= enemy.shields
                                enemy.shields = 0  # Shields are fully depleted
                                print(f"HIT! {enemy.name} SHIELDS: {shields_before} -> 0 (Shields Down!)")
                            else:
                                enemy.shields -= remaining_damage
                                print(f"HIT! {enemy.name} SHIELDS: {shields_before} -> {enemy.shields}")
                                remaining_damage = 0  # No damage left for the hull

                        # If there is remaining damage, apply it to the hull
                        if remaining_damage > 0:
                            hull_before = enemy.hull
                            enemy.hull -= remaining_damage
                            print(f"HIT! {enemy.name} HULL: {hull_before} -> {enemy.hull}")

                        # Reduce phaser power
                        phaser_power -= damage

                        # Remove destroyed enemies
                        remaining_enemies = []
                        for enemy in self.current_sector.enemies:
                            if enemy.hull <= 0:

                                print(f"{enemy.name} destroyed!")
                                EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)
                                enemy_x =  GRID_ORIGIN_X + (enemy.grid_x * SQUARE_SIZE) + SQUARE_SIZE//2
                                enemy_y =  GRID_ORIGIN_Y + (enemy.grid_y * SQUARE_SIZE) + SQUARE_SIZE//2
                                enemy_position = (enemy_x, enemy_y)
                                explosion = Explosion(enemy_position, max_size=SQUARE_SIZE, start_size=5)
                                projectile_group.add(explosion)
                                enemy.die()
                            else:
                                remaining_enemies.append(enemy)
                                EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)
                                enemy_x =  GRID_ORIGIN_X + (enemy.grid_x * SQUARE_SIZE) + SQUARE_SIZE//2
                                enemy_y =  GRID_ORIGIN_Y + (enemy.grid_y * SQUARE_SIZE) + SQUARE_SIZE//2
                                enemy_position = (enemy_x, enemy_y)
                                explosion = Explosion(enemy_position, max_size=SQUARE_SIZE//3, start_size=1)
                                projectile_group.add(explosion)

                        # Update the sector's enemies list
                        self.current_sector.enemies = remaining_enemies


                    # Check if all enemies are destroyed, and play victory sound
                    if len(self.current_sector.enemies) == 0:
                        play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 1)
                    

                    # Re-enter the sector to ensure state consistency
                    self.enter_sector(self.quadrant_x, self.quadrant_y)



    def fire_torpedo(self):


        """Prompt the player to fire up to 3 torpedoes, selecting all targets first, then firing simultaneously."""
        max_torpedoes = 3
        num_torpedoes = 0
        targets = []

        # Prompt the player for the number of torpedoes to fire
        while True:
            SCREEN.fill(BLACK, (0, SCREEN_HEIGHT - 100, 400, 100))  # Bottom-left corner
            prompt_surface = FONT24.render("Enter torpedoes to fire (0-3): ", True, WHITE)
            SCREEN.blit(prompt_surface, (10, SCREEN_HEIGHT - 80))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_0, pygame.K_KP0):
                        num_torpedoes = 0
                    elif event.key in (pygame.K_1, pygame.K_KP1):
                        num_torpedoes = 1
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        num_torpedoes = 2
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        num_torpedoes = 3

                    if 0 <= num_torpedoes <= max_torpedoes:
                        print(f"Player chose to fire {num_torpedoes} torpedoes.")
                        break
            else:
                continue  # Continue looping if no valid input was provided
            break

        # If no torpedoes are fired, exit early
        if num_torpedoes == 0:
            print("No torpedoes fired.")
            return

        # Prompt for each torpedo's target
        for i in range(num_torpedoes):
            prompt_text = f"Select target for torpedo {i + 1}: "
            target_x, target_y = prompt_sector_target(SCREEN, prompt_text)  # Assuming prompt_target() gets target coordinates
            targets.append((target_x, target_y))
            print(f"Target selected for torpedo {i + 1}: ({target_x}, {target_y})")

        # Fire all torpedoes at the same time
        for i, (target_x, target_y) in enumerate(targets):
            if self.torpedo_qty >=1:
                if self.energy >= TORPEDO_ENERGY_USAGE:
                    torpedo = Torpedo(self.grid_x, self.grid_y, target_x, target_y)
                    projectile_group.add(torpedo)
                    self.torpedo_qty -= 1
                    self.energy -= TORPEDO_ENERGY_USAGE
                    print(f"Torpedo {i + 1} fired towards sector ({target_x}, {target_y})!")
                    WEAPON_CHANNEL.play(MISSILE_SOUND)
                else:
                    print("Insufficient energy for Torpedo")
            else:
                 print("Torpedos Depleted")


    




    def activate_warp(self):
        """Prompt the player to select a warp factor and move the player."""
        warp_factor = prompt_warp_factor(SCREEN)

        if warp_factor > 0:
            # Ask for the direction (e.g., N, S, E, W)
            direction = prompt_direction(SCREEN,"Use Arrow Keys to Select Warp Direction:")

            # Calculate the new sector based on the warp factor and direction
            new_x, new_y = self.quadrant_x, self.quadrant_y
            if direction == "N":
                new_y -= warp_factor
                self.last_move_direction = "up"
                self.image = self.orig_image

            elif direction == "S":
                new_y += warp_factor
                self.last_move_direction = "down"
                self.image = pygame.transform.flip(self.orig_image, False, True)

            elif direction == "E":
                self.last_move_direction = "right"
                new_x += warp_factor
                self.image = pygame.transform.rotate(self.orig_image, -90)

            elif direction == "W":
                self.last_move_direction = "left"
                new_x -= warp_factor
                self.image = pygame.transform.rotate(self.orig_image, 90)

            # Clamp the new position to within the grid boundaries
            new_x = max(0, min(GRID_SIZE - 1, new_x))
            new_y = max(0, min(GRID_SIZE - 1, new_y))

            print(f"Warping to sector ({new_x}, {new_y}) at Warp {warp_factor}.")
            if self.shields_on:
                self.energy -= (warp_factor * WARP_ENERGY_PER)*2
            else:
                self.energy -= (warp_factor * WARP_ENERGY_PER)

            EXPLOSION_CHANNEL.play(WARP_SOUND)

            # Enter the new sector
            self.quadrant_x = new_x
            self.quadrant_y = new_y
            self.current_sector = self.enter_sector(new_x, new_y)
            self.update_position()





    def move(self, dx, dy):
        """Move the player in the grid, ensuring it stays within bounds and handles quadrant transitions."""
        # Check if the player will move out of the current sector (grid bounds)
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        self.energy -= abs(dx)
        self.energy -= abs(dy)

        if dx == 0 and dy == 0:
            self.energy += 1

        # If within bounds, check if the new position is blocked by a star
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # Check if the new position has a star (blocking movement)
            if self.current_sector.is_star_at(new_x, new_y):
                print("Movement blocked by a star!")
                return  # Don't move if there's a star in the way

            if self.current_sector.is_base_at(new_x, new_y):
                print("Movement blocked by a base!")
                return  # Don't move if there's a star in the way

            if self.current_sector.is_enemy_at(new_x, new_y):
                print("Movement blocked by an enemy!")
                return  # Don't move if there's a star in the way

            # Update position if no star is blocking
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_position()
        else:

            # Handle moving to the next quadrant if out of bounds (same as before)
            if dx == 1:  # Moving right
                if self.quadrant_x < QUADRANT_SIZE - 1:
                    self.quadrant_x += 1
                    self.grid_x = 0
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)

                    EXPLOSION_CHANNEL.play(WARP_SOUND)

            elif dx == -1:  # Moving left
                if self.quadrant_x > 0:
                    self.quadrant_x -= 1
                    self.grid_x = GRID_SIZE - 1
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
            elif dy == 1:  # Moving down
                if self.quadrant_y < QUADRANT_SIZE - 1:
                    self.quadrant_y += 1
                    self.grid_y = 0
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
            elif dy == -1:  # Moving up
                if self.quadrant_y > 0:
                    self.quadrant_y -= 1
                    self.grid_y = GRID_SIZE - 1
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
            
            self.update_position()

        # Update last_move_direction and rotate/flip the sprite (same as before)
        if dx == -1:
            self.last_move_direction = "left"
            self.image = pygame.transform.rotate(self.orig_image, 90)
        elif dx == 1:
            self.last_move_direction = "right"
            self.image = pygame.transform.rotate(self.orig_image, -90)
        elif dy == -1:
            self.last_move_direction = "up"
            self.image = self.orig_image
        elif dy == 1:
            self.last_move_direction = "down"
            self.image = pygame.transform.flip(self.orig_image, False, True)

#### end player class

class Phasor_blast(pygame.sprite.Sprite):
    def __init__(self, origin_x, origin_y, enemy_x, enemy_y):
        super().__init__()

        self.origin_x = GRID_ORIGIN_X + (origin_x * SQUARE_SIZE) + SQUARE_SIZE//2
        self.origin_y = GRID_ORIGIN_Y + (origin_y * SQUARE_SIZE) + SQUARE_SIZE//2
        self.enemy_x =  GRID_ORIGIN_X + (enemy_x * SQUARE_SIZE) + SQUARE_SIZE//2
        self.enemy_y =  GRID_ORIGIN_Y + (enemy_y * SQUARE_SIZE) + SQUARE_SIZE//2
        self.timer = 400  # Duration in milliseconds
        self.start_time = pygame.time.get_ticks()  # Get the current time when the blast is created

    def update(self):
        ...
        """Update the phasor blast's state."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.timer:
            self.kill()  # Remove the sprite after 1 second

    def draw(self, screen):
        """Draw the phasor blast."""
        pygame.draw.line(SCREEN,WHITE,(self.origin_x, self.origin_y),(self.enemy_x, self.enemy_y), 2)

class Torpedo(pygame.sprite.Sprite):
    def __init__(self, origin_x, origin_y, target_x, target_y):
        super().__init__()

        # Convert to zero-indexed if needed
        self.grid_x = origin_x
        self.grid_y = origin_y
        self.target_x = target_x - 1
        self.target_y = target_y - 1

        self.speed = TORPEDO_SPEED
        # Add randomness to the damage
        self.damage = int(TORPEDO_DAMAGE * random.uniform(0.9, 1.1))  # ±10% random variance


        # Calculate movement vector based on the target
        self.direction_vector = self.calculate_direction_vector()

        # Create the torpedo visual
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (2, 2), 2)
        self.rect = self.image.get_rect(
            center=(GRID_ORIGIN_X + self.grid_x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    GRID_ORIGIN_Y + self.grid_y * SQUARE_SIZE + SQUARE_SIZE // 2)
        )

        self.last_update = pygame.time.get_ticks()  # Track the last time the torpedo moved
        self.travel_delay = 100  # Milliseconds delay between moves


    def calculate_direction_vector(self):
        """Calculate normalized direction vector toward the target sector."""
        dx = self.target_x - self.grid_x
        dy = self.target_y - self.grid_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        print(self.grid_x, self.grid_y, self.target_x, self.target_y)

        if distance == 0:
            return (0, 0)  # Prevent division by zero if the target is the same sector

        # Normalize the direction vector
        return (dx / distance, dy / distance)

    def move(self):
        """Move the torpedo along the calculated direction vector."""
        # Update grid position based on direction vector and speed
        self.grid_x += self.direction_vector[0] * self.speed
        self.grid_y += self.direction_vector[1] * self.speed

        # Update the rect position for rendering
        self.rect.center = (GRID_ORIGIN_X + self.grid_x * SQUARE_SIZE + SQUARE_SIZE // 2,
                            GRID_ORIGIN_Y + self.grid_y * SQUARE_SIZE + SQUARE_SIZE // 2)

        print(self.grid_x, self.grid_y)


    def out_of_bounds(self):
        """Check if the torpedo is out of quadrant bounds."""
        return not (0 <= self.grid_x < GRID_SIZE and 0 <= self.grid_y < GRID_SIZE)

    def check_collision(self, enemies):
        """Check if the torpedo collides with any enemies."""

        # Snap to nearest grid for collision checks
        rounded_x = round(self.grid_x)
        rounded_y = round(self.grid_y)

        # Check collision with enemies
        for enemy in player.current_sector.enemies:  # Assuming you pass the current sector to the torpedo
            if rounded_x == enemy.grid_x and rounded_y == enemy.grid_y:
                print(f"Hit enemy at ({enemy.grid_x}, {enemy.grid_y})!")
                return enemy

        # for enemy in enemies:
        #     if enemy.grid_x == self.grid_x and enemy.grid_y == self.grid_y:
        #         return enemy

        if (rounded_x == self.target_x) and (rounded_y == self.target_y):
            print(f"reached target at ({self.target_x}, {self.target_y})!")
            projectile_group.remove(self)
            self.kill()
            explosion_x =  GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_y =  GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_position = (explosion_x, explosion_y)
            explosion = Explosion(explosion_position, max_size=SQUARE_SIZE//3, start_size=1)
            projectile_group.add(explosion)
            EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)

        return None


    def update(self):

        # Check if enough time has passed to move the torpedo
        now = pygame.time.get_ticks()
        if now - self.last_update < self.travel_delay:
            return  # Not enough time has passed yet

        self.last_update = now  # Update the last move time

        self.move()

        # Check if the torpedo is out of bounds
        if self.out_of_bounds():
            print("Torpedo exited the quadrant.")
            projectile_group.remove(self)
            self.kill()

        rounded_x = round(self.grid_x)
        rounded_y = round(self.grid_y)


        if player.current_sector.is_star_at(rounded_x, rounded_y):
            print("Torpedo collided with star.")
            projectile_group.remove(self)
            self.kill()
            explosion_x =  GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_y =  GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_position = (explosion_x, explosion_y)
            explosion = Explosion(explosion_position, max_size=SQUARE_SIZE//3, start_size=1)
            projectile_group.add(explosion)
            EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)
            
        if player.current_sector.is_base_at(rounded_x, rounded_y):
            print("Torpedo collided with base.")
            projectile_group.remove(self)
            self.kill()
            explosion_x =  GRID_ORIGIN_X + (rounded_x  * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_y =  GRID_ORIGIN_Y + (rounded_y * SQUARE_SIZE) + SQUARE_SIZE//2
            explosion_position = (explosion_x, explosion_y)
            explosion = Explosion(explosion_position, max_size=SQUARE_SIZE//3, start_size=1)
            projectile_group.add(explosion)
            EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)

        # Check for collisions with enemies
        hit_enemy = self.check_collision(player.current_sector.enemies)
        if hit_enemy:
            # Apply damage to the enemy
            shields_before = hit_enemy.shields
            hull_before = hit_enemy.hull

            if self.damage >= hit_enemy.shields:
                remaining_damage = self.damage - hit_enemy.shields
                hit_enemy.shields = 0
                hit_enemy.hull -= remaining_damage
            else:
                hit_enemy.shields -= self.damage

            print(f"Torpedo hit {hit_enemy.name}!")
            print(f"Shields: {shields_before} -> {hit_enemy.shields}")
            print(f"Hull: {hull_before} -> {hit_enemy.hull}")

            

            # Destroy the enemy if hull <= 0
            if hit_enemy.hull <= 0:
                print(f"{hit_enemy.name} destroyed!")
                hit_enemy.die()
                player.current_sector.enemies.remove(hit_enemy)
                # Create an explosion
                explosion_x = GRID_ORIGIN_X + hit_enemy.grid_x * SQUARE_SIZE + SQUARE_SIZE // 2
                explosion_y = GRID_ORIGIN_Y + hit_enemy.grid_y * SQUARE_SIZE + SQUARE_SIZE // 2
                explosion = Explosion((explosion_x, explosion_y), max_size=SQUARE_SIZE, start_size=5)
                projectile_group.add(explosion)
                EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)
            else:
                explosion_x =  GRID_ORIGIN_X + (rounded_x  * SQUARE_SIZE) + SQUARE_SIZE//2
                explosion_y =  GRID_ORIGIN_Y + (rounded_y * SQUARE_SIZE) + SQUARE_SIZE//2
                explosion_position = (explosion_x, explosion_y)
                explosion = Explosion(explosion_position, max_size=SQUARE_SIZE//3, start_size=1)
                projectile_group.add(explosion)
                EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)

            self.kill()
            projectile_group.remove(self)
        
            # Check if all enemies are destroyed, and play victory sound
            if len(player.current_sector.enemies) == 0:
                play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 1)

                # Re-enter the sector to ensure state consistency
                player.enter_sector(player.quadrant_x, player.quadrant_y)

        # Delay to simulate travel
        # pygame.time.wait(100)

    print("Torpedo sequence complete.")

    def draw(self, screen):
        """Draw the torpedo."""
        pygame.draw.circle(screen, WHITE, self.rect.center, 6)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, max_size=SQUARE_SIZE, start_size=SQUARE_SIZE//4, growth_rate=2):
        super().__init__()
        self.position = position  # Center of the explosion
        self.growth_rate = growth_rate
        self.max_size = max_size
        self.current_size = start_size
        self.color = WHITE

    def update(self):
        # Expand the explosion
        self.current_size += self.growth_rate
        self.color = random.choice([WHITE, RED, ORANGE, YELLOW])
        if self.current_size > self.max_size:
            self.kill()  # Remove the sprite once it reaches the max size

    def draw(self, screen):
        # Draw the explosion as a growing circle
        pygame.draw.circle(screen,self.color, self.position, self.current_size // 2)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = ENEMY_SHIP
        self.orig_image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.image = self.orig_image

        self.rect = self.image.get_rect()
        self.last_move_direction = random.choice(["up", "down", "left", "right"])
        self.update_position()

        self.name = "Avenger"

        self.torpedo_qty = 10
        self.energy = 1000 
        self.shields = random.randint(40, 60)
        self.hull = random.randint(150, 250)

    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE)
        player_draw_y = GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE)
        self.rect.topleft = (player_draw_x, player_draw_y)

        if self.last_move_direction == "left":
            self.image = pygame.transform.rotate(self.orig_image, 90)

        elif self.last_move_direction == "right":
            self.image = pygame.transform.rotate(self.orig_image, -90)

        elif self.last_move_direction == "up":
            self.image = self.orig_image

        elif self.last_move_direction == "down":
            self.image = pygame.transform.flip(self.orig_image, False, True)

    def die(self):
        self.kill()

    def update(self, current_sector):
        """Update enemy's position with a chance to move to an adjacent open sector square within boundaries."""
        if random.random() < 0.2:  # 20% chance to move
            adjacent_positions = self.get_adjacent_positions()

            # Check available adjacent positions
            available_positions = [
                pos for pos in adjacent_positions 
                if self.is_valid_position(pos)  # Check if the position is valid
            ]

            if available_positions:
                # Randomly pick an available adjacent position
                new_pos = random.choice(available_positions)
                old_x, old_y = self.grid_x, self.grid_y
                self.grid_x, self.grid_y = new_pos
                # Ensure get_move_direction is being called and returns a valid direction
                self.last_move_direction = self.get_move_direction(old_x, old_y, self.grid_x, self.grid_y)
                print(self.last_move_direction)  # Debugging the direction
                
                # Only update position if the direction was properly set
                
                
                if self.last_move_direction:
                    self.update_position()

    def get_move_direction(self, old_x, old_y, new_x, new_y):
        """Return the direction of movement based on the old and new positions."""
        # print(old_x, old_y, new_x, new_y)
        if new_x < old_x:
            return "left"
        elif new_x > old_x:
            return "right"
        elif new_y < old_y:
            return "up"
        elif new_y > old_y:
            return "down"

    def is_valid_position(self, position):
        """Check if a position is valid (not blocked by player, enemy, star, or starbase)."""
        x, y = position

        # Ensure the position is within the sector's boundaries
        # if not (0 <= x < player.current_sector.width and 0 <= y < player.current_sector.height):
        #     return False

        # Check if the position contains a star
        if player.current_sector.is_star_at(x, y):
            return False

        # Check if the position contains the player's square
        if (x, y) == (player.grid_x, player.grid_y):
            return False

        # Check if the position contains another enemy's square
        if player.current_sector.is_enemy_at(x, y):
            return False


        # Check if the position contains a starbase
        if player.current_sector.is_base_at(x, y):
            return False

        # Otherwise, the position is valid
        return True

    def get_adjacent_positions(self):
        """Return a list of adjacent grid positions (up, down, left, right) that are within sector boundaries."""
        # Ensure the positions are within bounds (0-7 for both x and y)
        adjacent_positions = [
            (self.grid_x, self.grid_y - 1),  # up
            (self.grid_x, self.grid_y + 1),  # down
            (self.grid_x - 1, self.grid_y),  # left
            (self.grid_x + 1, self.grid_y),  # right
        ]
        
        # Filter out positions that are outside the sector boundaries
        return [
            (x, y) for x, y in adjacent_positions if 0 <= x < 8 and 0 <= y < 8
        ]

class Sector:
    def __init__(self, quadrant_x, quadrant_y):
        self.quadrant_x = quadrant_x
        self.quadrant_y = quadrant_y
        self.stars = []  # List to store star positions (each star is a tuple of (x, y))
        self.bases = []  # List to store base positions (each base is a tuple of (x, y))
        self.enemies = []

        self.visited = False
        self.last_star_count = 0
        self.last_base_count = 0
        self.last_enemy_count = 0



    def generate(self, player_x, player_y):
        """Generate stars and possibly a base for the sector."""
        num_stars = random.randint(2, 7)  # Random number of stars between 2 and 5
        
        # Randomly place stars in grid squares (ensure no duplicates or player position)
        while len(self.stars) < num_stars:
            star_x = random.randint(0, GRID_SIZE - 1)
            star_y = random.randint(0, GRID_SIZE - 1)
            star_pos = (star_x, star_y)
            
            # Ensure the star position isn't the same as the player's position
            if star_pos not in self.stars and star_pos != (player_x, player_y):
                self.stars.append(star_pos)  # Add star to the list if it's not a duplicate or the player's position
        
        # 10% chance of having a base in the sector
        if random.random() < 0.1:
            placing = True 
            while placing:
                grid_x, grid_y = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                base_pos = (grid_x, grid_y)
                if base_pos not in self.stars and base_pos not in self.bases and base_pos != (player_x, player_y):
                    self.bases.append(base_pos)  # Add base to the list
                    placing = False

        # 10% chance of having an enemy in the sector
        if random.random() < 0.25:
            num_of_enemies = random.randint(1,4)
            for i in range(num_of_enemies):
                placing = True 
                while placing:
                    grid_x, grid_y = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                    enemy_pos = (grid_x, grid_y)
                    if enemy_pos not in self.stars and enemy_pos not in self.bases and star_pos != (player_x, player_y):
                        if not self.is_enemy_at(grid_x, grid_y):
                            new_enemy = Enemy(grid_x, grid_y)
                            self.enemies.append(new_enemy)  # Add base to the list
                            placing = False
    
    def count_bases(self):
        """Count the number of bases in the sector."""
        return len(self.bases)

    def count_enemies(self):
        """Count the number of bases in the sector."""
        return len(self.enemies)


    def count_stars(self):
        """Count the number of stars in the sector."""
        return len(self.stars)
    
    def is_base_at(self, x, y):
        """Check if there is a base at the given coordinates."""
        return (x, y) in self.bases

    def is_star_at(self, x, y):
        """Check if there is a star at the given coordinates."""
        return (x, y) in self.stars

    def is_enemy_at(self, x, y):
        for enemy in self.enemies:
            if enemy.grid_x == x and enemy.grid_y == y:
                return enemy
        return False

    def is_empty(self, x, y):
        """Check if the sector at (x, y) is empty (no enemy)."""
        for enemy in self.enemies:
            if enemy.grid_x == x and enemy.grid_y == y:
                return False  # There's already an enemy in this sector
        return True  # The sector is empty




### END OBJECT CLASSES ######################################################################################################

### DEFINE FUNCIONS #########################################################################################################

def draw_sector_map(player):
    # Draw the grid background
    SCREEN.blit(GRID_BACKGROUND, (GRID_ORIGIN_X, GRID_ORIGIN_Y))

    # condition_set_to = "GREEN"
    # Draw grid lines
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            this_square_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
            this_square_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
            rect = pygame.Rect(this_square_x, this_square_y, SQUARE_SIZE, SQUARE_SIZE)
            # pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)

            if player.current_sector.count_enemies() >= 1:
                player.condition = "RED"

            else:
                ...
                # player.condition = "GREEN"

            
            if player.current_sector.is_star_at(col, row): # Check if there is a star in this square
                # Draw a star in this square (could be a small circle or image)
                pygame.draw.circle(SCREEN, YELLOW, rect.center, 20)  # Yellow star
                pygame.draw.rect(SCREEN, YELLOW, rect, 1)  # yellow grid line



            elif player.current_sector.is_base_at(col, row):

                
                base_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                base_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                # Calculate offsets to center the image
                offset_x = (SQUARE_SIZE - BASE_IMAGE.get_width()) // 2
                offset_y = (SQUARE_SIZE - BASE_IMAGE.get_height()) // 2

                # Blit the image, applying the offsets
                SCREEN.blit(BASE_IMAGE, (base_screen_x + offset_x, base_screen_y + offset_y))
                pygame.draw.rect(SCREEN, BLUE, rect, 1)  # Blue grid line

                # Calculate distance
                distance = abs(math.sqrt((player.grid_x - col) ** 2 + (player.grid_y- row) ** 2))
                # print(distance)
                
                if (distance <=1):
                    if player.current_sector.count_enemies() <= 0:
                        player.condition = "BLUE"
                        player.update_position()
                    else:
                        player.condition = "RED"
                else:
                    player.condition = "GREEN"




            elif player.current_sector.is_enemy_at(col, row):
                this_enemy = player.current_sector.is_enemy_at(col, row)
                enemy_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                enemy_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - ENEMY_SHIP.get_width()) // 2
                offset_y = (SQUARE_SIZE - ENEMY_SHIP.get_height()) // 2

                SCREEN.blit(this_enemy.image, (enemy_screen_x + offset_x, enemy_screen_y + offset_y))

                if this_enemy.shields >=1 :
                    # Calculate the center of the square for the circle
                    center_x = enemy_screen_x + SQUARE_SIZE // 2
                    center_y = enemy_screen_y + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 2  # Radius is half the square size

                    # Draw a blue circle around the enemy
                    pygame.draw.circle(SCREEN, BLUE, (center_x, center_y), radius, 2)  # 2 is the thickness of the circle's border

                pygame.draw.rect(SCREEN, RED, rect, 1)  # RED grid line

            else:
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Regular grid line


            if col == player.grid_x and row == player.grid_y:
                if player.condition == "BLUE":
                    pygame.draw.rect(SCREEN, BLUE, rect,1)  # Highlight in Green (or another color)
                else:
                    pygame.draw.rect(SCREEN, GREEN, rect,1)  # Highlight in Green (or another color)
                
                if player.shields >=1 :
                    if player.shields_on:
                        player_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                        player_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                        # Calculate the center of the square for the circle
                        center_x = player_screen_x + SQUARE_SIZE // 2
                        center_y = player_screen_y + SQUARE_SIZE // 2
                        

                        # Draw a blue circle around the player
                        thickness = int(player.shield_level//10 ) -1

                        radius = SQUARE_SIZE // 2 + player.shield_level/25  # Radius is half the square size
                        pygame.draw.circle(SCREEN, BLUE, (center_x, center_y), radius, thickness)  # 2 is the thickness of the circle's border


            else:
                ...

                # pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Regular grid line

            # # Draw grid number for each square (optional)
            # number_text = FONT24.render("000", True, GREEN)
            # number_rect = number_text.get_rect(center=(this_square_x + SQUARE_SIZE // 2, this_square_y + SQUARE_SIZE // 2))
            # SCREEN.blit(number_text, number_rect)

            if player.condition == "RED":
                pygame.draw.rect(SCREEN, RED, (GRID_ORIGIN_X-1, GRID_ORIGIN_Y-1, GRID_SIZE * SQUARE_SIZE + 2 , GRID_SIZE * SQUARE_SIZE + 2), 2)  # RED grid line
            elif player.condition == "BLUE":
                pygame.draw.rect(SCREEN, BLUE, (GRID_ORIGIN_X-1, GRID_ORIGIN_Y-1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)  # BLUE grid line
            elif player.condition == "GREEN":
                pygame.draw.rect(SCREEN, GREEN, (GRID_ORIGIN_X-1, GRID_ORIGIN_Y-1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)  # GREEN grid line

            # Draw column headers (centered above the grid)
            if row == 0:  # Only draw column headers on the first row
                column_text = FONT24.render(str(col + 1), True, GREEN)
                column_text_rect = column_text.get_rect(
                    center=(this_square_x + SQUARE_SIZE // 2, GRID_ORIGIN_Y - SQUARE_SIZE // 2)
                )
                SCREEN.blit(column_text, column_text_rect)  


        # Draw row headers (centered to the left of the grid)
        row_text = FONT24.render(str(row + 1), True, GREEN)
        row_text_rect = row_text.get_rect(
            center=(GRID_ORIGIN_X - SQUARE_SIZE // 2, this_square_y + SQUARE_SIZE // 2)
        )
        SCREEN.blit(row_text, row_text_rect)



    # Draw the player
    SCREEN.blit(player.image, player.rect)



# draw the right side screen reports
def draw_reports(player):
    report_pos_y = GRID_ORIGIN_Y

    # Report data
    draw_report_line("STARDATE:", str(player.stardate), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("DAYS LEFT:", str(player.daysleft), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("CONDITION:", player.condition, report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("QUADRANT:", f"{player.quadrant_x + 1} , {player.quadrant_y + 1}", report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("SECTOR:", f"{player.grid_x + 1} , {player.grid_y + 1}", report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("TORPEDOS:", str(player.torpedo_qty), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("ENERGY:", str(player.energy), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("SHIELDS:", str(player.shields), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("SHIELD LEVEL:", str(player.shield_level), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("HULL STRENGTH:", str(player.hull), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    
    draw_report_line("ENEMIES:", str(player.num_enemies), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("STARBASES:", str(player.num_starbases), report_pos_y, player)
    report_pos_y += FONT24.get_height()

    draw_report_line("MAX WARP:", str(player.max_warp), report_pos_y, player)


# Draw each report line
def draw_report_line(title, value, y_pos, player):
    

    # Render and draw the value
    value_color = GREEN
    title_color =  GREEN

    if value == "GREEN": value_color = GREEN
    elif value == "BLUE": value_color = BLUE
    elif value == "RED": value_color = RED

    if (title == "SHIELDS:"): 
        if player.shields_on:
            value_color = WHITE
            title_color = WHITE
            title = "SHIELDS UP:"
        else:
            value_color = GREEN 
            title = "SHIELDS DOWN:"

        if player.current_sector.enemies:
            if (player.shield_level <= 25) or (not player.shields_on) or (player.shields < 250):
               value_color = YELLOW 
               title_color = YELLOW


    elif  title == "SHIELD LEVEL:":
        if player.shields_on:
            value_color = WHITE
            title_color = WHITE
        else:
            value_color = GREEN 

    # Render and draw the title
    title_surface = FONT24.render(title, True, title_color)
    title_rect = title_surface.get_rect(
        topleft=(SCREEN_WIDTH-REPORT_TITLE_MARGIN, y_pos)
    )
    SCREEN.blit(title_surface, title_rect)

    value_surface = FONT24.render(value, True, value_color)
    value_rect = value_surface.get_rect(
        topleft=(SCREEN_WIDTH-REPORT_STATUS_MARGIN, y_pos)
    )
    SCREEN.blit(value_surface, value_rect)

# Function to draw the quadrant map with numbers

# def count_bases_in_sector(self, col, row):
#         """Count the number of bases in the given sector."""
#         sector_key = (col, row)
#         sector_info = self.visited_sectors.get(sector_key, {'stars': [], 'base': None})
#         return 1 if sector_info['base'] else 0

# def count_sector_stars(player, col, row):
#         """Retrieve the stars for the current sector."""
#         sector_key = (col, row)
#         return len(player.visited_sectors.get(sector_key, {'stars': []})['stars'])

def draw_alert_info(screen):
    """Draw information about the sector and player's condition above the sector map."""
    # Define text positions and spacing
    padding = 10
    line_height = 20
    sector_info_x = GRID_ORIGIN_X
    sector_info_y = GRID_ORIGIN_Y - 100 #(line_height * 3) - padding  # Position above the map

    # Draw player condition on the right
    player_info_x = GRID_ORIGIN_X + (8 * SQUARE_SIZE)
    player_info_y = GRID_ORIGIN_Y - 100 #(line_height * 3) - padding  # Position above the map- (line_height * 3) - padding  # Align with sector info

    # Clear the area above the map
    screen.fill(BLACK, (0, 0, SCREEN_WIDTH, GRID_ORIGIN_Y))

    

    if player.current_sector.enemies:

        # Display sector information
        sector_title = FONT24.render(f"COMBAT AREA", True, RED)
        screen.blit(sector_title, (sector_info_x, sector_info_y))

        if (player.shield_level <= 25) or (not player.shields_on) or (player.shields < 250):
            shield_title = FONT24.render(f"SHIELDS DANGEROUSLY LOW", True, YELLOW)
            screen.blit(shield_title, (sector_info_x + 180, sector_info_y + line_height))

    elif player.condition == "BLUE":

        # Display sector information
        sector_title = FONT24.render(f"DOCKED WITH STARBASE", True, BLUE)
        screen.blit(sector_title, (sector_info_x, sector_info_y))

        
    else:
        ...
        # no_enemy_text = FONT24.render("No enemies detected.", True, GREEN)
        # screen.blit(no_enemy_text, (sector_info_x, sector_info_y))

    # Display player condition aligned to the right edge of the sector map

    color = GREEN

    if player.condition == "RED":
        color = RED

    if player.condition == "GREEN":
        color = GREEN

    if player.condition == "BLUE":
        color = BLUE

    player_condition = FONT24.render(
        f"CONDITION: {player.condition}",True,color)
    screen.blit(player_condition, (player_info_x - player_condition.get_width(), player_info_y))






def draw_quadrant_map(player):
    for row in range(QUADRANT_SIZE):
        for col in range(QUADRANT_SIZE):
            # Calculate the position of each square
            this_square_x = QUADRANT_ORIGIN_X + col * QUADRANT_SQUARE_SIZE
            this_square_y = QUADRANT_ORIGIN_Y + row * QUADRANT_SQUARE_SIZE

            # Draw the square for the quadrant map
            rect = pygame.Rect(this_square_x, this_square_y, QUADRANT_SQUARE_SIZE, QUADRANT_SQUARE_SIZE)

            this_sector = None

            for sector in player.all_sectors:
                if (col == sector.quadrant_x) and (row == sector.quadrant_y):
                    this_sector = sector

            grid_color = DARK_GREEN

            if col == player.quadrant_x and row == player.quadrant_y:
                grid_color = GREEN
                colorC = GREEN





            num_enemy = this_sector.count_enemies()
            num_bases = this_sector.count_bases()
            num_stars = this_sector.count_stars()

            if is_adjacent_or_same_sector(player.current_sector, this_sector):

                this_sector.last_star_count = num_enemy
                this_sector.last_base_count = num_bases
                this_sector.last_enemy_count = num_stars
                this_sector.visited = True

                textA  = str(num_enemy)
                textB  = str(num_bases)
                textC  = str(num_stars)

                colorA = RED if num_enemy > 0 else DARK_GREEN
                colorB = BLUE if num_bases > 0 else DARK_GREEN
                colorC = GREEN if num_stars > 0 else DARK_GREEN

            elif this_sector.visited:
                textA  = str(this_sector.last_star_count)
                textB  = str(this_sector.last_base_count)
                textC  = str(this_sector.last_enemy_count)

                colorA = DARK_RED if num_enemy > 0 else DARK_GREEN
                colorB = DARK_BLUE if num_bases > 0 else DARK_GREEN
                colorC = DARK_GREEN if num_stars > 0 else DARK_GREEN

            else:
                textA  = "*"
                textB  = "*"
                textC  = "*"

                colorA = DARK_GREY
                colorB = DARK_GREY
                colorC = DARK_GREY

            textA_surface = FONT24.render(textA, True, colorA)
            textB_surface = FONT24.render(textB, True, colorB)
            textC_surface = FONT24.render(textC, True, colorC)

            # Calculate positions for the text
            total_width = textA_surface.get_width() + textB_surface.get_width() + textC_surface.get_width()
            start_x = QUADRANT_ORIGIN_X + (col * QUADRANT_SQUARE_SIZE) + (QUADRANT_SQUARE_SIZE - total_width) // 2
            start_y = QUADRANT_ORIGIN_Y + (row * QUADRANT_SQUARE_SIZE) + (QUADRANT_SQUARE_SIZE - textA_surface.get_height()) // 2

            # Blit each piece of text in sequence
            SCREEN.blit(textA_surface, (start_x, start_y))
            SCREEN.blit(textB_surface, (start_x + textA_surface.get_width(), start_y))
            SCREEN.blit(textC_surface, (start_x + textA_surface.get_width() + textB_surface.get_width(), start_y))

           
            pygame.draw.rect(SCREEN, grid_color, rect,1)  # Highlight in red (or another color)
            
            
def is_adjacent_or_same_sector(player_sector, target_sector):
    """
    Check if the target sector is at a distance of 1 or less from the player's current sector.
    
    Args:
        player_sector (tuple): The player's current sector coordinates (quadrant_x, quadrant_y).
        target_sector (tuple): The target sector coordinates (quadrant_x, quadrant_y).

    Returns:
        bool: True if the distance is 1 or less, False otherwise.
    """
    # Calculate distance
    distance = math.sqrt((player_sector.quadrant_x - target_sector.quadrant_x) ** 2 + (player_sector.quadrant_y - target_sector.quadrant_y) ** 2)
    
    # distance = abs(player_sector.quadrant_x - target_sector.quadrant_x) + abs(player_sector.quadrant_y - target_sector.quadrant_y)
    return distance <= 1.85

def play_delayed_sound(channel, sound, delay):
    threading.Timer(delay, lambda: channel.play(sound)).start()

def prompt_phaser_power(screen):
    """Display a prompt for the player to enter phaser power."""
    input_text = ""
    prompt_active = True

    while prompt_active:
        screen.fill(BLACK, (0, SCREEN_HEIGHT - 100, 300, 100))  # Bottom-left corner
        prompt_surface = FONT24.render("Enter Phaser Power (0-2000):", True, WHITE)
        screen.blit(prompt_surface, (10, SCREEN_HEIGHT - 80))

        input_surface = FONT24.render(input_text, True, WHITE)
        screen.blit(input_surface, (10 + prompt_surface.get_width() + 10 , SCREEN_HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm input
                    if input_text.isdigit():
                        power = int(input_text)
                        if 0 <= power <= 2000:
                            return power
                        else:
                            input_text = ""  # Reset on invalid input
                    else:
                        input_text = ""  # Reset on invalid input
                elif event.key == pygame.K_BACKSPACE:  # Remove last character
                    input_text = input_text[:-1]
                else:  # Add new character
                    if len(input_text) < 4 and event.unicode.isdigit():  # Limit input length
                        input_text += event.unicode

def prompt_warp_factor(screen):
    """Display a prompt for the player to enter warp factor."""
    input_text = ""
    prompt_active = True

    while prompt_active:
        screen.fill(BLACK, (0, SCREEN_HEIGHT - 100, 300, 100))  # Bottom-left corner
        prompt_surface = FONT24.render("Enter Warp Factor (0-10):", True, WHITE)
        screen.blit(prompt_surface, (10, SCREEN_HEIGHT - 80))

        input_surface = FONT24.render(input_text, True, WHITE)
        screen.blit(input_surface, (10 + prompt_surface.get_width() + 10 , SCREEN_HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm input
                    if input_text.isdigit():
                        factor = int(input_text)
                        if 0 <= factor <= 8:
                            return factor
                        else:
                            input_text = ""  # Reset on invalid input
                    else:
                        input_text = ""  # Reset on invalid input
                elif event.key == pygame.K_BACKSPACE:  # Remove last character
                    input_text = input_text[:-1]
                else:  # Add new character
                    if len(input_text) < 2 and event.unicode.isdigit():  # Limit input length
                        input_text += event.unicode

def prompt_direction(screen,prompt_text):
    """Prompt the player to select a direction for warp using arrow keys."""
    directions = {"N": "North", "S": "South", "E": "East", "W": "West"}
    direction = None

    while direction not in directions:
        # Clear the prompt area
        SCREEN.fill(BLACK, (0, SCREEN_HEIGHT - 100, 400, 100))  # Clear specific area for prompt
        # Display the prompt
        prompt_surface = FONT24.render(prompt_text, True, WHITE)
        SCREEN.blit(prompt_surface, (10, SCREEN_HEIGHT - 80))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "N"
                elif event.key == pygame.K_DOWN:
                    direction = "S"
                elif event.key == pygame.K_RIGHT:
                    direction = "E"
                elif event.key == pygame.K_LEFT:
                    direction = "W"

                if direction in directions:
                    print(f"Direction selected: {directions[direction]}")
                    return direction

def prompt_sector_target(screen, prompt_text):
    """Prompt the player to input a sector target (e.g., 3,4)."""
    input_text = ""
    while True:
        # Clear the prompt area
        SCREEN.fill(BLACK, (0, SCREEN_HEIGHT - 100, 400, 100))  # Clear specific area for prompt
        
        # Display the prompt and current input
        prompt_surface = FONT24.render(f"{prompt_text} {input_text}", True, WHITE)
        SCREEN.blit(prompt_surface, (10, SCREEN_HEIGHT - 80))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to submit
                    try:
                        target = tuple(map(int, input_text.split(",")))
                        if len(target) == 2:
                            print(f"Target sector selected: {target}")
                            return target
                    except ValueError:
                        pass  # Invalid input; ignore and re-prompt
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                elif event.unicode.isdigit() or event.unicode == ",":
                    input_text += event.unicode  # Append valid character








### END FUNCTIONS ###########################################################################################################

def main():
    running = True
    global player
    global projectile_group

    player = Player()
    projectile_group = pygame.sprite.Group() 

    current_index = SHIELD_LEVELS.index(player.shield_level)  # Find the current level's index

    while running:

        ### UPDATE EVERYTHING ###############################################################################################


        # enemy_count_ttl = 0
        # for sector in player.all_sectors:
        #     enemy_count_ttl += sector.count_enemies()
        # player.num_enemies = enemy_count_ttl

        
        key_pressed = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

            elif event.type == pygame.KEYDOWN:  # Check for key presses
                key_pressed = True
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event.key == pygame.K_SPACE:
                    player.move(0, 0)

                elif event.key == pygame.K_p:
                    player.fire_phasers()

                elif event.key == pygame.K_t:
                    player.fire_torpedo()

                elif event.key == pygame.K_w:
                    player.activate_warp()

                elif event.key == pygame.K_s:
                    player.shields_toggle()

                elif event.key == pygame.K_KP_PLUS:
                    # Increase the shield level
                    if current_index < len(SHIELD_LEVELS) - 1:
                        current_index += 1
                        player.shield_level = SHIELD_LEVELS[current_index]
                        print(f"Shield level increased to {player.shield_level}%")
                        if player.shields_on:
                            player.shields = player.shield_level * 10
                            WEAPON_CHANNEL.play(SHIELD_UP)
                        else:
                            player.shields =0
                        player.energy -= RAISE_SHIELD_PER

                elif event.key == pygame.K_KP_MINUS:
                    # Decrease the shield level
                    if current_index > 0:
                        current_index -= 1
                        player.shield_level = SHIELD_LEVELS[current_index]
                        print(f"Shield level decreased to {player.shield_level}%")
                        if player.shields_on:
                            player.shields = player.shield_level * 10
                            WEAPON_CHANNEL.play(SHIELD_DOWN)
                            if player.shield_level <= 0:
                                player.shields_on = False
                        else:
                            player.shields = 0

                if key_pressed:#### ENEMY TURN ??
                    for enemy in player.current_sector.enemies:
                        enemy.update(player.current_sector)



        ### END UPDATES #####################################################################################################



        ### DRAW EVERYTHING #################################################################################################
        SCREEN.fill(BLACK)

        draw_alert_info(SCREEN)

        draw_sector_map(player)

        # for enemy in player.current_sector.enemies:
        #     enemy.update(player.current_sector)

        projectile_group.update() 
        for projectile in projectile_group:
            projectile.draw(SCREEN)

        draw_reports(player)

        draw_quadrant_map(player)

        

        ### END DRAWINGS ####################################################################################################


        ### FLIP AND TICK ###
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
