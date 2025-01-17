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


SCAN_ORIGIN_X = GRID_ORIGIN_X + (QUADRANT_SIZE * SQUARE_SIZE) + 50
SCAN_ORIGIN_Y = GRID_ORIGIN_Y

SCAN_NAME_X = 0
SCAN_DIRECTION_X = 110
SCAN_DISTANCE_X = 215
SCAN_SHIELD_X = 300
SCAN_HULL_X = 360

PROMPT_ORIGIN_X = 80 
PROMPT_ORIGIN_Y = SCREEN_HEIGHT - 80
PROMPT_AREA = (PROMPT_ORIGIN_X, SCREEN_HEIGHT - 90, 300, 200)  # Bottom-left corner
COMPASS_ORIGIN_X = SCAN_ORIGIN_X
# Colors (RGB values)
WHITE = (255, 255, 255)
OFF_WHITE = (200, 200, 200)
LIGHT_GREY = (150, 150, 150)
GREY = (128, 128, 128)
MIDDLE_GREY = (100, 100, 100)
DARK_GREY = (50, 50, 50)
NEAR_BLACK = (25, 25, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (50, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GREEN =(0,50,0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)

# Define the shades from WHITE to BLACK
SHADE_COLOR_CYCLE = [WHITE, WHITE, OFF_WHITE, OFF_WHITE,LIGHT_GREY, GREY, MIDDLE_GREY, DARK_GREY, NEAR_BLACK, DARK_GREY, MIDDLE_GREY,GREY, LIGHT_GREY,OFF_WHITE,OFF_WHITE,WHITE,WHITE]
color_index = 0  # To track the current color index
color_change_timer = 0  # Timer to control the color cycling speed
COLOR_CHANGE_INTERVAL = 100  # Time in milliseconds between color changes

# Fonts
FONT22 = pygame.font.Font(None, 22)
FONT24 = pygame.font.Font(None, 24)


MAX_NUM_OF_BASES = 5

MAX_ENERGY = 3000
BASE_RELOAD_ENERGY = 3000
WARP_ENERGY_PER = 100
RAISE_SHIELD_PER = 50
SHIELD_LEVELS = [0, 25, 50, 75, 100]
MAX_CREW = 100
MAX_HULL = 1000
MAX_SHIELDS = 2000
BASE_RELOAD_SHIELD = 2000

MAX_TORPEDO_QTY = 10
TORPEDO_DAMAGE = 500
TORPEDO_SPEED = 0.5
TORPEDO_ENERGY_USAGE = 50

CHANCE_OF_TORPEDO_MISS = 0.01
MISS_CHANCE_INCREASE_PER = 0.01

ENERGY_CHARGE_TICK = 20
HULL_REPAIR_TICK = 5

STARDATE_PER_REPAIR_TICK = 0.015

CAPTAIN_BOX_SCALE = 3


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



ALL_PLANET_IMAGES = [
    {"name": "RAINBOW_IMAGE", "file": "rainbow.png"},
    {"name": "AZURE_IMAGE", "file": "azure.png"},
    {"name": "ACID_IMAGE", "file": "acid.png"},
    {"name": "ALKALI_IMAGE", "file": "alkali.png"},
    {"name": "AURIC_IMAGE", "file": "auric.png"},
    {"name": "CARBIDE_IMAGE", "file": "carbide.png"},
    {"name": "CRIMSON_IMAGE", "file": "crimson.png"},
    {"name": "CIMMERIAN_IMAGE", "file": "cimmerian.png"},
    {"name": "COPPER_IMAGE", "file": "copper.png"},
    {"name": "CHLORINE_IMAGE", "file": "chlorine.png"},
    {"name": "CHONDRITE_IMAGE", "file": "chondrite.png"},
    {"name": "CYANIC_IMAGE", "file": "cyanic.png"},
    {"name": "DUST_IMAGE", "file": "dust.png"},
    {"name": "EMERALD_IMAGE", "file": "emerald.png"},
    {"name": "FLOURESCENT_IMAGE", "file": "fluorescent.png"},
    {"name": "GREEN_IMAGE", "file": "green.png"},
    {"name": "HALIDE_IMAGE", "file": "halide.png"},
    {"name": "HYDROCARBON_IMAGE", "file": "hydrocarbon.png"},
    {"name": "IODINE_IMAGE", "file": "iodine.png"},
    {"name": "INFRARED_IMAGE", "file": "infrared.png"},
    {"name": "NOBLE_IMAGE", "file": "noble.png"},
    {"name": "METAL_IMAGE", "file": "metal.png"},
    {"name": "MAGMA_IMAGE", "file": "magma.png"},
    {"name": "MAROON_IMAGE", "file": "maroon.png"},
    {"name": "MAGNETIC_IMAGE", "file": "magnetic.png"},
    {"name": "OPALESCENT_IMAGE", "file": "opalescent.png"},
    {"name": "ORGANIC_IMAGE", "file": "organic.png"},
    {"name": "OOLITE_IMAGE", "file": "oolite.png"},
    {"name": "PELLUCID_IMAGE", "file": "pellucid.png"},
    {"name": "PRIMORDIAL_IMAGE", "file": "primordial.png"},
    {"name": "PURPLE_IMAGE", "file": "purple.png"},
    {"name": "PLUTONIC_IMAGE", "file": "plutonic.png"},
    {"name": "QUASI_DEGEN_IMAGE", "file": "quasidegenerate.png"},
    {"name": "SAPPHIRE_IMAGE", "file": "sapphire.png"},
    {"name": "RADIOACTIVE_IMAGE", "file": "radioactive.png"},
    {"name": "REDUX_IMAGE", "file": "redux.png"},
    {"name": "RUBY_IMAGE", "file": "ruby.png"},
    {"name": "SHATTERED_IMAGE", "file": "shattered.png"},
    {"name": "SELENIC_IMAGE", "file": "selenic.png"},
    {"name": "SLAVE_IMAGE", "file": "slaveshield.png"},
    {"name": "SUPERDENSE_IMAGE", "file": "superdense.png"},
    {"name": "TREASURE_IMAGE", "file": "treasure.png"},
    {"name": "VINYLOGOUS_IMAGE", "file": "vinylogous.png"},
    {"name": "TELLURIC_IMAGE", "file": "telluric.png"},
    {"name": "ULTRAMARINE_IMAGE", "file": "ultramarine.png"},
    {"name": "ULTRAVIOLET_IMAGE", "file": "ultraviolet.png"},
    {"name": "UREA_IMAGE", "file": "urea.png"},
    {"name": "LANTHANIDE_IMAGE", "file": "lanthanide.png"},
    {"name": "WATER_IMAGE", "file": "water.png"},
    {"name": "XENOLITHIC_IMAGE", "file": "xenolithic.png"},
    {"name": "YTTRIC_IMAGE", "file": "yttric.png"},
    {"name": "BLUEGASIMAGE", "file": "bluegas.png"},
    {"name": "GREENGASIMAGE", "file": "greengas.png"},
    {"name": "GREYGASIMAGE", "file": "greygas.png"},
    {"name": "PURPLEGASIMAGE", "file": "purplegas.png"},
    {"name": "REDGASIMAGE", "file": "redgas.png"},
    {"name": "VIOLETGASIMAGE", "file": "violetgas.png"},
    {"name": "YELLOWGASIMAGE", "file": "yellowgas.png"},
]

CRUISER_CAPTAIN_000 = pygame.image.load("cruiser-cap-000.png").convert_alpha() 

CRUISER_CAPTAIN_001 = pygame.image.load("cruiser-cap-001.png").convert_alpha() 
CRUISER_CAPTAIN_002 = pygame.image.load("cruiser-cap-002.png").convert_alpha()  
CRUISER_CAPTAIN_003 = pygame.image.load("cruiser-cap-003.png").convert_alpha() 
CRUISER_CAPTAIN_004 = pygame.image.load("cruiser-cap-004.png").convert_alpha() 
CRUISER_CAPTAIN_005 = pygame.image.load("cruiser-cap-005.png").convert_alpha() 
CRUISER_CAPTAIN_006 = pygame.image.load("cruiser-cap-006.png").convert_alpha() 
CRUISER_CAPTAIN_007 = pygame.image.load("cruiser-cap-007.png").convert_alpha() 
CRUISER_CAPTAIN_008 = pygame.image.load("cruiser-cap-008.png").convert_alpha() 
CRUISER_CAPTAIN_009 = pygame.image.load("cruiser-cap-009.png").convert_alpha() 
CRUISER_CAPTAIN_010 = pygame.image.load("cruiser-cap-010.png").convert_alpha() 
CRUISER_CAPTAIN_011 = pygame.image.load("cruiser-cap-011.png").convert_alpha() 
CRUISER_CAPTAIN_012 = pygame.image.load("cruiser-cap-012.png").convert_alpha() 
CRUISER_CAPTAIN_013 = pygame.image.load("cruiser-cap-013.png").convert_alpha() 
CRUISER_CAPTAIN_014 = pygame.image.load("cruiser-cap-014.png").convert_alpha() 

CRUISER_CAPTAIN_ADDITIONALS = [
    (CRUISER_CAPTAIN_001, -33, -9),
    (CRUISER_CAPTAIN_002, -33, -9),
    (CRUISER_CAPTAIN_003, -33, -9),
    (CRUISER_CAPTAIN_004, -33, -9),
    (CRUISER_CAPTAIN_005, -33, -9),
    (CRUISER_CAPTAIN_006, -44, -7),
    (CRUISER_CAPTAIN_007, -44, -7),
    (CRUISER_CAPTAIN_008, -44, -7),
    (CRUISER_CAPTAIN_009, 0, -5),
    (CRUISER_CAPTAIN_010, 0, -5),
    (CRUISER_CAPTAIN_011, 0, -5),
    (CRUISER_CAPTAIN_012, -19, -2),
    (CRUISER_CAPTAIN_013, -19, -2),
    (CRUISER_CAPTAIN_014, -19, -2),
]



# AUDIO CONSTANTS -------------------------------------------------------------
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

ALARM_CHANNEL = pygame.mixer.Channel(1)
RED_ALERT = pygame.mixer.Sound("alarm01.mp3")
POWER_UP = pygame.mixer.Sound("power_up2_clean.mp3")


WEAPON_CHANNEL = pygame.mixer.Channel(2)
WEAPON_CHANNEL.set_volume(0.25)
PHASER_SOUND = pygame.mixer.Sound("earthling-pd.wav")
MISSILE_SOUND = pygame.mixer.Sound("earthling-mx.wav")
SHIELD_UP = pygame.mixer.Sound("melnorme-charge.wav")
SHIELD_DOWN = pygame.mixer.Sound("melnorme-confuse.wav")
ENEMY_PHASER_SOUND = pygame.mixer.Sound("vux-laser.wav")

EXPLOSION_CHANNEL = pygame.mixer.Channel(3)
EXPLOSION_CHANNEL.set_volume(0.1)
SHIP_DEATH_SOUND = pygame.mixer.Sound("shipdies.wav")
MEDIUM_EXPLOSION = pygame.mixer.Sound("boom-medium.wav")
WARP_SOUND = pygame.mixer.Sound("tng_slowwarp_clean.mp3")
HURT = pygame.mixer.Sound("land_hrt.wav") 

MUSIC_CHANNEL = pygame.mixer.Channel(4)
MUSIC_CHANNEL.set_volume(.30)

VICTORY_DITTY = pygame.mixer.Sound("earthling-ditty.mp3")
VICTORY_DITTY_PLUS10 = pygame.mixer.Sound("earthling-ditty_plus10.mp3")
VICTORY_DITTY_MINUS10 = pygame.mixer.Sound("earthling-ditty_minus10.mp3")
VICTORY_DITTY_PLUS20 = pygame.mixer.Sound("earthling-ditty_plus20.mp3")
VICTORY_DITTY_MINUS20 = pygame.mixer.Sound("earthling-ditty_minus20.mp3")
VICTORY_DITTY_PLUS30 = pygame.mixer.Sound("earthling-ditty_plus30.mp3")
VICTORY_DITTY_MINUS30 = pygame.mixer.Sound("earthling-ditty_minus30.mp3")

ENEMY_DITTY = pygame.mixer.Sound("ilwrath-ditty.mp3")

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
        self.grid_x = random.randint(0,7)  # Starting grid position (column)
        self.grid_y = random.randint(0,7) # Starting grid position (row)
        self.last_move_direction = "up"
        
        self.stardate = 3801
        self.daysleft = 32

        self.condition = "GREEN"
        self.condition_color = GREEN

        self.quadrant_x = random.randint(0,7)
        self.quadrant_y = random.randint(0,7)

        self.torpedo_qty = 10

        self.energy = BASE_RELOAD_ENERGY

        

        self.shield_energy = BASE_RELOAD_SHIELD
        self.shields = 0
        self.shields_on = False
        self.shield_level = 0

        self.hull = MAX_HULL

        self.crew = MAX_CREW

        self.num_enemies = 0
        self.num_starbases = 0
        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)

        self.sensor_range = 1

        self.offset_x = 0 
        self.offset_y = 0 
        self.inDockingRange = None
        self.inOrbitRange = None
        self.docked = False
        self.inOrbit = False

        self.update_position()

        self.all_sectors = []  # Dictionary to store Sector objects for each (quadrant_x, quadrant_y)
        self.generate_all_sectors()  # Generate all sectors when the game starts
        self.current_quadrant = None
        self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)  # Ensure player starts on an empty square

        self.turn = 0

        self.crew_loss_timer = 0  # Tracks time for crew loss checks

        self.is_dead = False


    def generate_all_sectors(self):
        """Generate and store a sector for each (quadrant_x, quadrant_y)."""
        for quadrant_x in range(8):  # Loop through quadrant_x values (0 to 7)
            for quadrant_y in range(8):  # Loop through quadrant_y values (0 to 7)
                sector_key = (quadrant_x, quadrant_y)
                
                # Create a new sector and generate its content (stars, bases)
                sector = Sector(quadrant_x, quadrant_y)
                sector.generate(self, self.grid_x, self.grid_y)
                
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
                while (sector.is_star_at(self.grid_x, self.grid_y)) or (sector.is_base_at(self.grid_x, self.grid_y)) or (sector.is_enemy_at(self.grid_x, self.grid_y)) or (sector.is_planet_at(self.grid_x, self.grid_y)):
                    self.move_away_from_star_or_base(sector)

                if sector != self.current_quadrant: #ENTERING A NEW SECTOR

                    if self.current_quadrant != None:
                        for enemy in self.current_quadrant.enemies: # RESET ENEMY ENERGY IF PLAYER LEAVES
                            enemy.energy = random.randint(800 , 1200)



                    if sector.count_enemies() >=1 :
                        ALARM_CHANNEL.play(RED_ALERT,2)
                        # MUSIC_CHANNEL.play(ENEMY_DITTY)


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
            if not sector.is_star_at(nx, ny):
                if not sector.is_base_at(nx, ny):
                    if not sector.is_enemy_at(nx, ny):
                        if not sector.is_planet_at(nx, ny):
                            self.grid_x, self.grid_y = nx, ny
                            self.update_position()
                            print("Evasive!")
                            return
        
        print(f"Warning: No valid adjacent square found for the player. Staying at ({self.grid_x}, {self.grid_y}).")

    
    def check_hull_and_crew(self, delta_time):
        """Check if the player's hull is below 0 and potentially kill crew members."""
        if self.hull <= 0:
            self.crew_loss_timer += delta_time
            if self.crew_loss_timer >= 100:  # 500ms (half a second)
                self.crew_loss_timer = 0  # Reset the timer

                # 10% chance to lose a crew member
                if self.crew > 0:
                    if random.random() < 0.5:
                        self.crew -= random.randint(1,5)
                        if player.crew <= 0: 
                            player.crew = 0

                        EXPLOSION_CHANNEL.play(HURT)
                        print(f"Critical damage! Crew have been lost. Remaining crew: {self.crew}")
                        
                        
                        if random.random() < 0.1:
                            print("Hull Integrity Restored")
                            self.hull = 1 # chance hull is restored

                        if len(self.current_quadrant.enemies) <= 0:
                            print("Hull Integrity Restored")
                            self.hull = 1 # chance hull is restored


                else:
                    if not self.is_dead:
                        print("All crew members have been lost!")
                        self.explode(self.grid_x,self.grid_y,SQUARE_SIZE*1.5,2,2,sound=SHIP_DEATH_SOUND)
                        self.is_dead = True

                    # self.end_game()
            else:
                print("Hull breach detected!")
        else:
            self.crew_loss_timer = 0  # Reset the timer if the hull is stable


    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (round(self.grid_x) * SQUARE_SIZE) + self.offset_x
        player_draw_y = GRID_ORIGIN_Y + (round(self.grid_y) * SQUARE_SIZE) + self.offset_y
        self.rect.topleft = (player_draw_x, player_draw_y)


        # if self.hull <= 0:
        #     print("The player's ship's hull has been breached!")
        #     self.hull = 0
        #     # CHANCE OF CREW GETTING KILLED:
        #     if random.random() < .99:
        #         self.crew -= random.randint(1,5)
        #         if self.crew <= 0:
        #             self.crew = 0

        # if self.condition == "BLUE": 

        ### RECHARGE / REPAIR AT STARBASE ###
        if self.docked:
            repairing = False 
            if self.energy < BASE_RELOAD_ENERGY:
                self.energy += ENERGY_CHARGE_TICK
                repairing = True

            if self.torpedo_qty < MAX_TORPEDO_QTY:
                self.torpedo_qty += 1
                repairing = True

            if self.crew < MAX_CREW:
                self.crew += 1
                repairing = True

            if self.hull < MAX_HULL:
                self.hull += HULL_REPAIR_TICK
                repairing = True

            if self.shield_energy < BASE_RELOAD_SHIELD:
                self.shield_energy += ENERGY_CHARGE_TICK
                repairing = True

            if repairing:
                self.stardate += STARDATE_PER_REPAIR_TICK

            if self.shields_on == True:

                player.shields_toggle()

        # DON"T EXCEED LIMITED ####
        if self.shield_energy >= MAX_SHIELDS:
            self.shield_energy = MAX_SHIELDS

        if self.energy >= MAX_ENERGY:
            self.energy = MAX_ENERGY

        if self.hull >= MAX_HULL:
            self.hull = MAX_HULL

        if self.torpedo_qty >= MAX_TORPEDO_QTY:
            self.torpedo_qty = MAX_TORPEDO_QTY

        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)


    def toggle_dock(self, starbase):
        """
        Toggles the player's docking status.
        If condition is 'BLUE', docks the player and offsets the position towards the starbase.
        """
        if self.docked == False:
            if self.inDockingRange is not None:
                self.docked = True

                ALARM_CHANNEL.play(POWER_UP)

                # Calculate the offset
                self.offset_x = (starbase[0] - self.grid_x) * (SQUARE_SIZE // 2)
                self.offset_y = (starbase[1] - self.grid_y) * (SQUARE_SIZE // 2)

                # Apply the offset to the player's sprite position
                # self.rect.x += offset_x
                # self.rect.y += offset_y
                print("Docked at starbase!")

            else:
                self.docked = False
                print("Cannot dock unless condition is BLUE.")

        elif self.docked:
            self.docked = False
            self.offset_x = 0 
            self.offset_y = 0 
            print("Undocked from starbase!")

    def toggle_orbit(self, planet):
        """
        Toggles the player's docking status.
        If condition is 'BLUE', docks the player and offsets the position towards the starbase.
        """
        if self.inOrbit == False:
            if self.inOrbitRange is not None:
                self.inOrbit = True

                ALARM_CHANNEL.play(POWER_UP)

                # Calculate the offset
                self.offset_x = (planet[0] - self.grid_x) * (SQUARE_SIZE // 2)
                self.offset_y = (planet[1] - self.grid_y) * (SQUARE_SIZE // 2)

                # Apply the offset to the player's sprite position
                # self.rect.x += offset_x
                # self.rect.y += offset_y
                print("Entered Planetary Orbit!")

            else:
                self.inOrbit = False
                print("Cannot enter orbit unless in range")

        elif self.inOrbit:
            self.inOrbit = False
            self.offset_x = 0 
            self.offset_y = 0 
            print("Left Planetary Orbit!")




    def shields_toggle(self):
        global current_index
        if self.shields_on:
            print("toggle shield off")
            self.shields_on = False
            self.shields = 0
            self.shield_level = 0
            if self.shield_level > 0:
                WEAPON_CHANNEL.play(SHIELD_DOWN)

            current_index = SHIELD_LEVELS.index(player.shield_level)  # Find the current level's index


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

    def explode(self, x, y, max_size, start_size, growth_rate, sound=MEDIUM_EXPLOSION):
        global projectile_group
        """Handle explosion visuals and sound."""
        print('Explosion !')
        explosion_x = GRID_ORIGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion_y = GRID_ORIGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion = Explosion((explosion_x, explosion_y), max_size, start_size, growth_rate)
        projectile_group.add(explosion)
        EXPLOSION_CHANNEL.play(sound)

                
    def fire_phasers(self):
        """Fire phasers and damage enemies in the current sector, with a delay for each phaser blast."""
        phaser_power = prompt_phaser_power(SCREEN)
        num_enemy = self.current_quadrant.count_enemies()

        if phaser_power > 0:
            if phaser_power <= self.energy:
                
                self.energy -= phaser_power

                if num_enemy > 0:  # Only fire phasers if there are enemies present
                    damage = phaser_power // num_enemy

                    def fire_single_phaser(enemy):
                        WEAPON_CHANNEL.play(PHASER_SOUND)
                        """Handle the logic for firing a phaser at a single enemy."""
                        # Create and add a phaser blast
                        phaser_blast = Phaser_blast(self.grid_x, self.grid_y, enemy.grid_x, enemy.grid_y, WHITE)
                        projectile_group.add(phaser_blast)

                        distance = abs(math.sqrt((self.grid_x - enemy.grid_x) ** 2 + (self.grid_y - enemy.grid_y) ** 2))
                        range_reduction = (int(distance) - 1) * 5
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




                        # Handle enemy destruction
                        if enemy.hull <= 0:
                            print(f"{enemy.name} destroyed!")
                            EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)
                            enemy_x = GRID_ORIGIN_X + (enemy.grid_x * SQUARE_SIZE) + SQUARE_SIZE // 2
                            enemy_y = GRID_ORIGIN_Y + (enemy.grid_y * SQUARE_SIZE) + SQUARE_SIZE // 2
                            enemy_position = (enemy_x, enemy_y)
                            explosion = Explosion(enemy_position, max_size=SQUARE_SIZE, start_size=5, growth_rate=2)
                            projectile_group.add(explosion)


                            enemy.die()

                            # Check if all enemies are destroyed, and play victory sound
                            if len(self.current_quadrant.enemies) == 0:
                                print("last enemy destroyed")
                                play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 1)
                                # Re-enter the sector to ensure state consistency
                                self.enter_sector(self.quadrant_x, self.quadrant_y)

                        else:
                            self.explode(enemy.grid_x, enemy.grid_y, max_size=SQUARE_SIZE //4 , start_size=1, growth_rate=2)

                    # Schedule each phaser blast with a delay
                    for i, enemy in enumerate(self.current_quadrant.enemies):
                        delay = i * 0.25  # 0.3 seconds between each phaser blast
                        threading.Timer(delay, fire_single_phaser, args=(enemy,)).start()






                    # Update remaining enemies after all blasts are scheduled
                    self.current_quadrant.enemies = [e for e in self.current_quadrant.enemies if e.hull > 0]




                    
                    

                    # Re-enter the sector to ensure state consistency
                    self.enter_sector(self.quadrant_x, self.quadrant_y)
                else:
                    print("No Phaser Targets Available")
                    WEAPON_CHANNEL.play(PHASER_SOUND)
            else:
                print("Phaser Energy would exceed Available Energy")
        else:
            print("Zero Phaser Power Entered")





    def fire_torpedo(self):
        """Prompt the player to fire up to 3 torpedoes, selecting all targets first, then firing with delays."""
        max_torpedoes = 3
        num_torpedoes = prompt_numeric_input("Enter torpedoes to fire (0-3): ", 0, max_torpedoes)

        if num_torpedoes == 0:
            print("No torpedoes fired.")
            return

        if num_torpedoes > self.torpedo_qty:
            num_torpedoes = self.torpedo_qty
            print("Insufficient qty torpedoes.")

        # Collect target directions for each torpedo
        targets = []
        for i in range(num_torpedoes):
            rise = prompt_numeric_input(f"Enter direction for Torpedo {i + 1}: ", -GRID_SIZE, GRID_SIZE)
            run = prompt_numeric_input(f"Enter direction for Torpedo {i + 1}:  {rise} / ", -GRID_SIZE, GRID_SIZE)
            targets.append((rise, run))
            print(f"Direction selected for Torpedo {i + 1}: Rise: {rise}, Run: {run}")

        # Define a helper function to fire a single torpedo
        def fire_single_torpedo(index, rise, run):
            """Fire a single torpedo."""
            if self.torpedo_qty >= 1:
                if self.energy >= TORPEDO_ENERGY_USAGE:
                    torpedo = Torpedo(index + 1, self.grid_x, self.grid_y, rise, run)
                    projectile_group.add(torpedo)
                    self.torpedo_qty -= 1
                    self.energy -= TORPEDO_ENERGY_USAGE
                    print(f"Torpedo {index + 1} fired with direction Rise: {rise}, Run: {run}!")
                    WEAPON_CHANNEL.play(MISSILE_SOUND)

                    if self.torpedo_qty <= 0:
                        print("Torpedo Stock Depleted")
                else:
                    print("Insufficient energy for Torpedo")
            else:
                print("Torpedo Stock Depleted")

        # Fire each torpedo with a short delay between them
        for i, (rise, run) in enumerate(targets):
            delay = i * 0.25  # Delay of 0.25 seconds between torpedoes
            threading.Timer(delay, fire_single_torpedo, args=(i, rise, run)).start()

    def activate_warp(self):
        """Prompt the player to select a warp factor and move the player."""
        warp_factor = prompt_warp_factor(SCREEN)

        if warp_factor > 0:
            self.stardate += (1 * warp_factor)


            """Display a compass guide showing the warp direction numbers."""
            draw_compass()

            # Prompt the player to enter a direction (1-8)
            direction = prompt_numeric_input("Enter Warp Direction (1-9):", 1, 9, compass=True)

            # Calculate the new sector based on the warp factor and direction
            new_x, new_y = self.quadrant_x, self.quadrant_y

            if direction == 8:  # North
                new_y -= warp_factor
                self.last_move_direction = "up"
                self.image = self.orig_image

            elif direction == 9:  # Northeast
                new_x += warp_factor
                new_y -= warp_factor
                self.last_move_direction = "up"
                self.image = self.orig_image


            elif direction == 6:  # East
                new_x += warp_factor
                self.last_move_direction = "right"
                self.image = pygame.transform.rotate(self.orig_image, -90)

            elif direction == 3:  # Southeast
                new_x += warp_factor
                new_y += warp_factor
                self.last_move_direction = "down"
                self.image = pygame.transform.flip(self.orig_image, False, True)


            elif direction == 2:  # South
                new_y += warp_factor
                self.last_move_direction = "down"
                self.image = pygame.transform.flip(self.orig_image, False, True)

            elif direction == 1:  # Southwest
                new_x -= warp_factor
                new_y += warp_factor
                self.last_move_direction = "down"
                self.image = pygame.transform.flip(self.orig_image, False, True)


            elif direction == 4:  # West
                new_x -= warp_factor
                self.last_move_direction = "left"
                self.image = pygame.transform.rotate(self.orig_image, 90)

            elif direction == 7:  # Northwest
                new_x -= warp_factor
                new_y -= warp_factor
                self.last_move_direction = "up"
                self.image = self.orig_image

            new_x = round(new_x)
            new_y = round(new_y)


            # Clamp the new position to within the grid boundaries
            new_x = max(0, min(GRID_SIZE - 1, new_x))
            new_y = max(0, min(GRID_SIZE - 1, new_y))

            print(f"Warping to sector ({new_x}, {new_y}) at Warp {warp_factor}.")
            self.turn = 0

            # Adjust energy based on warp factor and shield status
            energy_cost = (warp_factor * WARP_ENERGY_PER)
            if self.shields_on:
                energy_cost *= 2

            self.energy -= energy_cost
            EXPLOSION_CHANNEL.play(WARP_SOUND)

            # Enter the new sector
            self.quadrant_x = new_x
            self.quadrant_y = new_y
            self.current_quadrant = self.enter_sector(new_x, new_y)
            self.update_position()




    def move(self, dx, dy):
        """Move the player in the grid, ensuring it stays within bounds and handles quadrant transitions."""
        # Check if the player will move out of the current sector (grid bounds)

        if player.docked : 
            player.toggle_dock((self.grid_x,self.grid_y))
            dx = 0
            dy = 0

        if player.inOrbit:
            player.toggle_orbit((self.grid_x,self.grid_y))
            dx = 0
            dy = 0

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        self.energy -= abs(dx)
        self.energy -= abs(dy)
        self.stardate += (1 * 0.95)

        if dx == 0 and dy == 0:
            print("Resting for Repairs...")
            self.energy += 1
            self.hull += 1

        # If within bounds, check if the new position is blocked by a star
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # Check if the new position has a star (blocking movement)
            if self.current_quadrant.is_star_at(new_x, new_y):
                print("Movement blocked by a star!")
                return  # Don't move if there's a star in the way

            if self.current_quadrant.is_base_at(new_x, new_y):
                print("Movement blocked by a base!")
                return  # Don't move if there's a star in the way

            if self.current_quadrant.is_enemy_at(new_x, new_y):
                print("Movement blocked by an enemy!")
                return  # Don't move if there's a star in the way


            if self.current_quadrant.is_planet_at(new_x, new_y):
                print("Movement blocked by an planet!")
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
                    self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)

                    EXPLOSION_CHANNEL.play(WARP_SOUND)
                    self.turn = 0

            elif dx == -1:  # Moving left
                if self.quadrant_x > 0:
                    self.quadrant_x -= 1
                    self.grid_x = GRID_SIZE - 1
                    self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
                    self.turn = 0

            elif dy == 1:  # Moving down
                if self.quadrant_y < QUADRANT_SIZE - 1:
                    self.quadrant_y += 1
                    self.grid_y = 0
                    self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
                    self.turn = 0

            elif dy == -1:  # Moving up
                if self.quadrant_y > 0:
                    self.quadrant_y -= 1
                    self.grid_y = GRID_SIZE - 1
                    self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
                    warp_factor = 1
                    print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
                    if self.shields_on:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)*2
                    else:
                        self.energy -= (warp_factor * WARP_ENERGY_PER)
                    EXPLOSION_CHANNEL.play(WARP_SOUND)
                    self.turn = 0
            
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

class Phaser_blast(pygame.sprite.Sprite):
    def __init__(self, origin_x, origin_y, enemy_x, enemy_y, color):
        super().__init__()


        self.color = color
        self.origin_x = GRID_ORIGIN_X + (origin_x * SQUARE_SIZE) + SQUARE_SIZE//2
        self.origin_y = GRID_ORIGIN_Y + (origin_y * SQUARE_SIZE) + SQUARE_SIZE//2
        self.enemy_x =  GRID_ORIGIN_X + (enemy_x * SQUARE_SIZE) + SQUARE_SIZE//2
        self.enemy_y =  GRID_ORIGIN_Y + (enemy_y * SQUARE_SIZE) + SQUARE_SIZE//2
        self.timer = 400  # Duration in milliseconds
        self.start_time = pygame.time.get_ticks()  # Get the current time when the blast is created

    def update(self):
        ...
        """Update the phaser blast's state."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.timer:
            self.kill()  # Remove the sprite after 1 second

    def out_of_bounds(self):
        """Check if the torpedo is out of quadrant bounds."""

        # return not (0 <= self.grid_x < GRID_SIZE and 0 <= self.grid_y < GRID_SIZE)
        return False

    def draw(self, screen):
        """Draw the phaser blast."""
        pygame.draw.line(SCREEN,self.color,(self.origin_x, self.origin_y),(self.enemy_x, self.enemy_y), 2)

class Torpedo(pygame.sprite.Sprite):
    def __init__(self, name, origin_x, origin_y, rise, run):
        super().__init__()

        self.name = "Torpedo " + str(name)

        # Starting position
        self.grid_x = origin_x
        self.grid_y = origin_y

        # Direction specified by rise/run
        self.rise = rise
        self.run = run

        self.speed = TORPEDO_SPEED
        self.damage = int(TORPEDO_DAMAGE * random.uniform(0.9, 1.1))  # ±10% random variance

        # Calculate movement vector based on rise/run
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

        self.near_targets = []
        self.miss_chance = CHANCE_OF_TORPEDO_MISS

    def calculate_direction_vector(self):
        """Calculate normalized direction vector based on rise and run."""
        magnitude = math.sqrt(self.rise ** 2 + self.run ** 2)
        if magnitude == 0:
            return (0, 0)  # Prevent division by zero if direction is (0, 0)
        return (self.run / magnitude, self.rise / magnitude)

    def move(self):
        """Move the torpedo along the calculated direction vector."""
        # Update grid position based on direction vector and speed
        self.grid_x += self.direction_vector[0] * self.speed
        self.grid_y += self.direction_vector[1] * self.speed

        # self.grid_x = round(self.grid_x)
        # self.grid_y = round(self.grid_y)

        # Update the rect position for rendering
        self.rect.center = (GRID_ORIGIN_X + self.grid_x * SQUARE_SIZE + SQUARE_SIZE // 2,
                            GRID_ORIGIN_Y + self.grid_y * SQUARE_SIZE + SQUARE_SIZE // 2)

    def out_of_bounds(self):
        """Check if the torpedo is out of quadrant bounds."""

        return not (GRID_ORIGIN_X <= self.rect.center[0] < (GRID_ORIGIN_X + GRID_SIZE*SQUARE_SIZE) and GRID_ORIGIN_Y <= self.rect.center[1] < GRID_ORIGIN_Y + GRID_SIZE*SQUARE_SIZE)

        # return not (0 <= self.grid_x < GRID_SIZE-1 and 0 <= self.grid_y < GRID_SIZE-1)

    def check_collision(self, enemies):
        """Check if the torpedo collides with any enemies."""
        # Snap to nearest grid for collision checks
        rounded_x = round(self.grid_x)
        rounded_y = round(self.grid_y)

        print(f"{self.name} @ ({rounded_x}, {rounded_y})")

        for enemy in player.current_quadrant.enemies:
            if rounded_x == enemy.grid_x and rounded_y == enemy.grid_y:

                if enemy not in self.near_targets:
                    self.near_targets.append(enemy)

                    if random.random() > self.miss_chance:

                        print(f"{self.name} * Hit Enemy {enemy.name} at ({enemy.grid_x}, {enemy.grid_y})! *")
                        return enemy

                    else:
                        print(f"{self.name} * Missed Enemy {enemy.name} at ({enemy.grid_x}, {enemy.grid_y})! * @ {self.miss_chance}")

        return None

    def update(self):
        """Update the torpedo's movement and check for collisions."""
        now = pygame.time.get_ticks()
        if now - self.last_update < self.travel_delay:
            return  # Not enough time has passed yet

        self.last_update = now  # Update the last move time

        self.move()

        # Check if the torpedo is out of bounds
        if self.out_of_bounds():
            print(f"{self.name} exited the quadrant.")
            projectile_group.remove(self)
            self.kill()
            return

        # Check collision with stars
        rounded_x = round(self.grid_x)
        rounded_y = round(self.grid_y)

        if player.current_quadrant.is_star_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a star @ {rounded_x}, {rounded_y}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        if player.current_quadrant.is_base_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a base @ {rounded_x}, {rounded_y}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        if player.current_quadrant.is_planet_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a planet @ {rounded_x}, {rounded_y}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        # Check for collisions with enemies
        hit_enemy = self.check_collision(player.current_quadrant.enemies)
        if hit_enemy:
            self.handle_enemy_hit(hit_enemy)

        self.miss_chance += MISS_CHANCE_INCREASE_PER

    def explode(self, x, y, max_size, start_size, growth_rate):
        """Handle explosion visuals and sound."""
        explosion_x = GRID_ORIGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion_y = GRID_ORIGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion = Explosion((explosion_x, explosion_y), max_size, start_size, growth_rate)
        projectile_group.add(explosion)
        EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)
        self.kill()
        projectile_group.remove(self)

    def handle_enemy_hit(self, enemy):
        """Handle hitting an enemy."""
        shields_before = enemy.shields
        hull_before = enemy.hull

        self.explode(enemy.grid_x, enemy.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)

        if self.damage >= enemy.shields:
            remaining_damage = self.damage - enemy.shields
            enemy.shields = 0
            enemy.hull -= remaining_damage
        else:
            enemy.shields -= self.damage

        
        print(f"     {enemy.name} Shields: {shields_before} -> {enemy.shields}")
        print(f"     {enemy.name} Hull: {hull_before} -> {enemy.hull}")

        if enemy.hull <= 0:
            print(f"     {enemy.name} Destroyed!")
            enemy.die()
            # player.current_quadrant.enemies.remove(enemy)
            self.explode(enemy.grid_x, enemy.grid_y, max_size=SQUARE_SIZE, start_size=5, growth_rate=2)
            EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)

            # Check if all enemies are destroyed, and play victory sound
            if len(player.current_quadrant.enemies) == 0:
                play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 1)

                # Re-enter the sector to ensure state consistency
                player.enter_sector(player.quadrant_x, player.quadrant_y)

    def draw(self, screen):
        """Draw the torpedo."""
        pygame.draw.circle(screen, WHITE, self.rect.center, 6)



class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, max_size, start_size, growth_rate):
        super().__init__()
        self.position = position  # Center of the explosion

        self.grid_x = self.position[0]
        self.grid_y = self.position[1]
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

    def out_of_bounds(self):
        """Check if the torpedo is out of quadrant bounds."""

        return False

    def draw(self, screen):
        # Draw the explosion as a growing circle
        pygame.draw.circle(screen,self.color, self.position, self.current_size // 2)



class Base(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()

        self.name = "STARBASE"
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.shields = 0
        self.hull = 0

### ENEMY CLASS ####
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

        self.name = "AVENGER"

        self.torpedo_qty = 10
        self.energy = random.randint(800 , 1200)
        self.shields = random.randint(40, 60)
        self.hull = random.randint(150, 250)

        self.speed = 2

        # Timer to trigger movement after player action
        self.trigger_update_time = None
        self.response_delay = 500  # Delay in milliseconds

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
        if self in player.current_quadrant.enemies:
            player.current_quadrant.enemies.remove(self)
        self.kill()

    def enemy_fire_phaser(self, player):
        """Enemy fires its phaser at the player."""

        if self.energy >= 100:  # Ensure the enemy has enough energy
            # Calculate the distance to the player
            distance = abs(self.grid_x - player.grid_x) + abs(self.grid_y - player.grid_y)

            # Base phaser power (e.g., 300)
            phaser_power = random.randint(300, 500)
            # Adjust damage based on distance (similar to player's phaser)
            if distance == 0:
                damage = int(phaser_power * 0.9)
            elif distance <= 5:
                damage = int(phaser_power * 0.6)
            elif distance <= 10:
                damage = int(phaser_power * 0.35)
            else:
                damage = 0  # No effect beyond 10 sectors

            # Apply damage to the player's shields and hull
            if player.shields > 0:
                absorbed = min(player.shields, damage)
                player.shields -= absorbed
                player.shield_energy -= absorbed
                damage -= absorbed

            if damage > 0 and player.hull > 0:
                player.hull -= damage

                

            # Deduct energy cost for firing
            self.energy -= 100

            # Visual/feedback (e.g., phaser beam)
            print(f"{self.name} fires phaser at the player! Distance: {distance}, Damage: {damage}")
            # Create and add a phaser blast

            phaser_blast = Phaser_blast(self.grid_x, self.grid_y, player.grid_x, player.grid_y, GREEN)
            projectile_group.add(phaser_blast)
            WEAPON_CHANNEL.play(ENEMY_PHASER_SOUND)


            # Check if the player has been destroyed
            if player.hull < (MAX_HULL * .25):
                
                print("CRITICAL DAMAGE!")
                if player.hull <= 0:
                    player.hull = 0
                    # CHANCE OF CREW GETTING KILLED:
                    # if random.random() < .5:
                    #     player.crew -= random.randint(1,5)
                    #     if player.crew <= 0:
                    #         player.crew = 0


            if player.crew <= 0:
                print("The player's ship has been destroyed!")


    def trigger_update(self, players_turn):
        """Set the trigger time to start the update process."""
        print("trigger update")
        self.trigger_update_time = pygame.time.get_ticks()
        if players_turn and player.turn != 0:
            players_turn = False

    def update(self, current_sector, players_turn):
        """Update enemy's position with a chance to move to an adjacent open sector square within boundaries."""
        # print(players_turn)
        """Update enemy's position a short time after being triggered."""
        if self.trigger_update_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.trigger_update_time >= self.response_delay:
                
                

                if len(projectile_group) == 0:
                    self.trigger_update_time = None  # Reset trigger

                    if not players_turn:
                        players_turn = True

                    

                    if random.random() < .50:  # 20% chance to move
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
                            # print(self.last_move_direction)  # Debugging the direction
                            
                            # Only update position if the direction was properly set
                            
                            
                            if self.last_move_direction:
                                self.update_position()

                    if random.random() < .75:
                        self.enemy_fire_phaser(player)



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
        # if not (0 <= x < player.current_quadrant.width and 0 <= y < player.current_quadrant.height):
        #     return False

        # Check if the position contains a star
        if player.current_quadrant.is_star_at(x, y):
            return False

        # Check if the position contains the player's square
        if (x, y) == (player.grid_x, player.grid_y):
            return False

        # Check if the position contains another enemy's square
        if player.current_quadrant.is_enemy_at(x, y):
            return False


        # Check if the position contains a starbase
        if player.current_quadrant.is_base_at(x, y):
            return False

        # Check if the position contains a starbase
        if player.current_quadrant.is_planet_at(x, y):
            return False

        # Otherwise, the position is valid
        return True

    def get_adjacent_positions(self):
        """Return a list of positions within the enemy's speed distance, considering sector boundaries."""
        adjacent_positions = []

        # Loop through a range of positions based on the enemy's speed
        for dx in range(-self.speed, self.speed + 1):  # dx ranges from -speed to +speed
            for dy in range(-self.speed, self.speed + 1):  # dy ranges from -speed to +speed
                # Calculate the new position
                new_x = self.grid_x + dx
                new_y = self.grid_y + dy

                # Check if the new position is within the sector boundaries
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Add the position to the list if it's within bounds
                    # Ensure it's not the current position itself (i.e., don't add (0,0) if no movement)
                    if dx != 0 or dy != 0:
                        adjacent_positions.append((new_x, new_y))
        
        return adjacent_positions


class Planet:
    def __init__(self, grid_x, grid_y, quadrant_x, quadrant_y, name=None, planet_type=None):
        """
        Initialize a Planet object.

        :param grid_x: The x-coordinate of the planet within the grid (sector).
        :param grid_y: The y-coordinate of the planet within the grid (sector).
        :param quadrant_x: The x-coordinate of the quadrant the planet is in.
        :param quadrant_y: The y-coordinate of the quadrant the planet is in.
        :param name: Optional name of the planet (randomly generated if not provided).
        :param planet_type: Optional type of the planet (e.g., Earth-like, gas giant).
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.quadrant_x = quadrant_x
        self.quadrant_y = quadrant_y
        self.name = name
        self.size = random.randint(1, 10)  # Size (e.g., 1 = small, 10 = massive)
        self.planet_type = planet_type
        self.resources = self.generate_resources()
        self.inhabited = random.choice([True, False])  # Randomly determine if the planet is inhabited

        random_planet = random.choice(ALL_PLANET_IMAGES)

        self.image = pygame.image.load(random_planet["file"]).convert_alpha()
        planet_image_size_factor = self.size / 10
        planet_image_size_factor = max(0.6, min(1, planet_image_size_factor)) 
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE*planet_image_size_factor, SQUARE_SIZE*planet_image_size_factor))  # Scale to grid square size 

        self.shields = 0 
        self.hull = 0 


    def generate_name(self, sector_planets, sector_planet_index):
        """
        Generate a name for the planet by appending a letter (A, B, C, etc.) 
        based on its index in the sector.
        """
        base_name = get_quadrant_name(self.quadrant_x, self.quadrant_y)
        if len(sector_planets) > 1:
            suffix = chr(97 + sector_planet_index)  # Convert index to ASCII (A=65, B=66, etc.)
            return f"{base_name} - {suffix}"
        else:
            return f"{base_name}"




    def generate_planet_type(self):
        """Randomly assign a type to the planet."""
        planet_types = ["Earth-like", "Gas Giant", "Frozen", "Desert", "Volcanic", "Oceanic"]
        return random.choice(planet_types)

    def generate_resources(self):
        """Randomly determine resource levels for the planet."""
        return {
            "minerals": random.randint(0, 100),
            "water": random.randint(0, 100),
            "energy": random.randint(0, 100)
        }

    def __str__(self):
        """String representation of the planet for debugging and display."""
        inhabited_status = "Inhabited" if self.inhabited else "Uninhabited"
        return (
            f"Planet {self.name} ({self.planet_type})\n"
            f"Location: Quadrant ({self.quadrant_x}, {self.quadrant_y}) | Grid ({self.grid_x}, {self.grid_y})\n"
            f"Size: {self.size}\n"
            f"Resources: {self.resources}\n"
            f"Status: {inhabited_status}"
        )


class Sector:
    def __init__(self, quadrant_x, quadrant_y):
        self.quadrant_x = quadrant_x
        self.quadrant_y = quadrant_y
        self.stars = []  # List to store star positions (each star is a tuple of (x, y))
        self.bases = []  # List to store base positions (each base is a tuple of (x, y))
        self.enemies = []
        self.planets = []

        self.visited = False
        self.last_star_count = 0
        self.last_base_count = 0
        self.last_enemy_count = 0



    def generate(self, player, player_x, player_y):
        """Generate stars, planets, bases, and enemies for the sector."""

        # Create a weighted list for the number of stars
        weighted_numbers = [1, 7, 8, 9] + [2, 3, 4, 5, 6] * 4
        num_stars = random.choice(weighted_numbers)

        # Randomly place stars or planets in grid squares (ensure no duplicates or player position)
        while len(self.stars) + len(self.planets) < num_stars:
            obj_x = random.randint(0, GRID_SIZE - 1)
            obj_y = random.randint(0, GRID_SIZE - 1)
            obj_pos = (obj_x, obj_y)

            # Ensure the position isn't the same as the player's position or a duplicate in either stars or planets
            if obj_pos != (player_x, player_y) and obj_pos not in self.stars:
                
                # Check for any planet in self.planets that shares the same position
                planet_exists = any(planet.grid_x == obj_x and planet.grid_y == obj_y for planet in self.planets)
                base_exists = any(base.grid_x == obj_x and base.grid_y == obj_y for base in self.bases)

                if not planet_exists and not base_exists :
                    # Random chance to create a planet (10% chance, adjust as needed)
                    if random.random() < 0.1:  # 10% chance for a planet
                        new_planet = Planet(obj_x, obj_y, self.quadrant_x, self.quadrant_y)
                        self.planets.append(new_planet)
                    # else:
                        # new_star = Star(obj_x, obj_y, self.quadrant_x, self.quadrant_y)
                        # self.stars.append(new_star)
                    else:  # Otherwise, add a star
                        self.stars.append(obj_pos)

        for i, planet in enumerate(self.planets):
            planet.name = planet.generate_name(self.planets,i)

        # Ensure there's a maximum number of bases across all sectors
        starbase_count_ttl = sum(sector.count_bases() for sector in player.all_sectors)
        if starbase_count_ttl < MAX_NUM_OF_BASES:
            if random.random() < 0.1:  # 10% chance of having a base in the sector
                placing = True
                while placing:
                    grid_x, grid_y = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                    base_pos = (grid_x, grid_y)
                    base = Base(grid_x, grid_y)
                    if base_pos not in self.stars and base_pos not in self.bases and base_pos != (player_x, player_y):
                        # Check for any planet in self.planets that shares the same position
                        planet_exists = any(planet.grid_x == obj_x and planet.grid_y == obj_y for planet in self.planets)
                        base_exists = any(base.grid_x == obj_x and base.grid_y == obj_y for base in self.bases)

                        if not planet_exists and not base_exists :
                            self.bases.append(base)  # Add base to the list
                            placing = False

        # 25% chance of having enemies in the sector
        if random.random() < 0.25:
            num_of_enemies = random.randint(1, 4)
            for _ in range(num_of_enemies):
                placing = True
                while placing:
                    grid_x, grid_y = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                    enemy_pos = (grid_x, grid_y)
                    if enemy_pos not in self.stars and enemy_pos not in self.bases and enemy_pos != (player_x, player_y):
                        # Check for any planet in self.planets that shares the same position
                         # Check for any planet in self.planets that shares the same position
                        planet_exists = any(planet.grid_x == obj_x and planet.grid_y == obj_y for planet in self.planets)
                        base_exists = any(base.grid_x == obj_x and base.grid_y == obj_y for base in self.bases)

                        if not planet_exists and not base_exists :

                            if not self.is_enemy_at(grid_x, grid_y):
                                new_enemy = Enemy(grid_x, grid_y)
                                self.enemies.append(new_enemy)  # Add enemy to the list
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
        for base in self.bases:
            if base.grid_x == x and base.grid_y == y:
                return base
        return False

    def is_star_at(self, x, y):
        """Check if there is a star at the given coordinates."""
        return (x, y) in self.stars

    def is_enemy_at(self, x, y):
        for enemy in self.enemies:
            if enemy.grid_x == x and enemy.grid_y == y:
                return enemy
        return False

    def is_planet_at(self, x, y):

        for planet in self.planets:  # Assuming `self.planets` is a list of Planet objects
            if planet.grid_x == x and planet.grid_y == y:
                return planet  # Return the Planet object
        return None  # Return None if no planet is found


    def is_empty(self, x, y):
        """Check if the sector at (x, y) is empty (no enemy)."""
        for enemy in self.enemies:
            if enemy.grid_x == x and enemy.grid_y == y:
                return False  # There's already an enemy in this sector
        return True  # The sector is empty




### END OBJECT CLASSES ######################################################################################################

### DEFINE FUNCIONS #########################################################################################################

def draw_sector_map():
    # Draw the grid background
    SCREEN.blit(GRID_BACKGROUND, (GRID_ORIGIN_X, GRID_ORIGIN_Y))

    player.inDockingRange = None
    player.inOrbitRange = None

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            this_square_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
            this_square_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
            rect = pygame.Rect(this_square_x, this_square_y, SQUARE_SIZE, SQUARE_SIZE)

            # Check and update player condition
            if player.current_quadrant.count_enemies() >= 1:
                player.condition = "RED"

            # Check for stars
            if player.current_quadrant.is_star_at(col, row):
                pygame.draw.circle(SCREEN, YELLOW, rect.center, 20)  # Yellow star
                pygame.draw.rect(SCREEN, YELLOW, rect, 1)  # Yellow grid line

            # Check for planets
            elif player.current_quadrant.is_planet_at(col, row):  # Add planet drawing logic
                planet = player.current_quadrant.is_planet_at(col, row)
                planet_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                planet_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - planet.image.get_width()) // 2
                offset_y = (SQUARE_SIZE - planet.image.get_height()) // 2

                # Draw the planet's image
                SCREEN.blit(planet.image, (planet_screen_x + offset_x, planet_screen_y + offset_y))
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Dark green grid line for planets

                # Check orbit range
                distance = abs(math.sqrt((player.grid_x - col) ** 2 + (player.grid_y - row) ** 2))
                if distance <= 1:
                    if player.current_quadrant.count_enemies() <= 0:
                        player.condition = "GREEN"
                        player.update_position()
                        player.inOrbitRange = (col, row)

                        if player.inOrbit:
                            player.condition = "GREEN"
                    else:
                        player.condition = "RED"

            # Check for bases
            elif player.current_quadrant.is_base_at(col, row):
                base_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                base_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - BASE_IMAGE.get_width()) // 2
                offset_y = (SQUARE_SIZE - BASE_IMAGE.get_height()) // 2

                SCREEN.blit(BASE_IMAGE, (base_screen_x + offset_x, base_screen_y + offset_y))
                pygame.draw.rect(SCREEN, BLUE, rect, 1)  # Blue grid line for bases

                # Check docking range
                distance = abs(math.sqrt((player.grid_x - col) ** 2 + (player.grid_y - row) ** 2))
                if distance <= 1:
                    if player.current_quadrant.count_enemies() <= 0:
                        player.condition = "GREEN"
                        player.update_position()
                        player.inDockingRange = (col, row)

                        if player.docked:
                            player.condition = "BLUE"
                    else:
                        player.condition = "RED"

            # Check for enemies
            elif player.current_quadrant.is_enemy_at(col, row):
                this_enemy = player.current_quadrant.is_enemy_at(col, row)
                enemy_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                enemy_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - ENEMY_SHIP.get_width()) // 2
                offset_y = (SQUARE_SIZE - ENEMY_SHIP.get_height()) // 2

                SCREEN.blit(this_enemy.image, (enemy_screen_x + offset_x, enemy_screen_y + offset_y))

                if this_enemy.shields >= 1:
                    center_x = enemy_screen_x + SQUARE_SIZE // 2
                    center_y = enemy_screen_y + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 2  # Radius is half the square size
                    pygame.draw.circle(SCREEN, BLUE, (center_x, center_y), radius, 2)  # Blue shield

                pygame.draw.rect(SCREEN, RED, rect, 1)  # Red grid line for enemies

            # Default grid square
            else:
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Regular grid line

            # Highlight the player position
            if col == player.grid_x and row == player.grid_y:
                if player.condition == "BLUE":
                    pygame.draw.rect(SCREEN, BLUE, rect, 1)  # Highlight in blue
                else:
                    pygame.draw.rect(SCREEN, GREEN, rect, 1)  # Highlight in green

                # Draw player's shields
                if player.shields >= 1 and player.shields_on:
                    player_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                    player_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                    center_x = player_screen_x + SQUARE_SIZE // 2
                    center_y = player_screen_y + SQUARE_SIZE // 2
                    thickness = max(int(player.shield_level // 10) - 1, 1)
                    radius = SQUARE_SIZE // 2 + player.shield_level / 25
                    pygame.draw.circle(SCREEN, BLUE, (center_x, center_y), radius, thickness)

            # Draw sector borders based on condition
            if player.condition == "RED":
                pygame.draw.rect(SCREEN, RED, (GRID_ORIGIN_X - 1, GRID_ORIGIN_Y - 1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)
            elif player.condition == "BLUE":
                pygame.draw.rect(SCREEN, BLUE, (GRID_ORIGIN_X - 1, GRID_ORIGIN_Y - 1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)
            elif player.condition == "GREEN":
                pygame.draw.rect(SCREEN, GREEN, (GRID_ORIGIN_X - 1, GRID_ORIGIN_Y - 1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)

            # Draw column headers
            if row == 0:  # Only draw column headers on the first row
                column_text = FONT24.render(str(col + 1), True, GREEN)
                column_text_rect = column_text.get_rect(
                    center=(this_square_x + SQUARE_SIZE // 2, GRID_ORIGIN_Y - SQUARE_SIZE // 2)
                )
                SCREEN.blit(column_text, column_text_rect)

        # Draw row headers
        row_text = FONT24.render(str(row + 1), True, GREEN)
        row_text_rect = row_text.get_rect(
            center=(GRID_ORIGIN_X - SQUARE_SIZE // 2, this_square_y + SQUARE_SIZE // 2)
        )
        SCREEN.blit(row_text, row_text_rect)

    # Draw the player
    if not player.is_dead:
        SCREEN.blit(player.image, player.rect)



# draw the right side screen reports
def draw_reports():
    report_pos_y = GRID_ORIGIN_Y

    # Report data
    draw_report_line("STARDATE:", f"{player.stardate:.2f}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("DAYS LEFT:", str(player.daysleft), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("CONDITION:", player.condition, report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("QUADRANT:", f"{player.quadrant_x + 1} , {player.quadrant_y + 1}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("SECTOR:", f"{player.grid_x + 1} , {player.grid_y + 1}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("------------------------------", f"-------------", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("TORPEDOS:", str(player.torpedo_qty), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("ENERGY:", str(round(player.energy)), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("------------------------------", f"-------------", report_pos_y)
    report_pos_y += FONT24.get_height()


    draw_report_line("SHIELD ENERGY:", str(round(player.shield_energy)), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("SHIELDS:", str(round(player.shields)), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("SHIELD LEVEL:", f"{player.shield_level}%", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("------------------------------", f"-------------", report_pos_y)
    report_pos_y += FONT24.get_height()


    draw_report_line("HULL STRENGTH:", str(round(player.hull)), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("CREW:", f"{player.crew}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("------------------------------", f"-------------", report_pos_y)
    report_pos_y += FONT24.get_height()


    
    draw_report_line("ENEMIES:", str(player.num_enemies), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("STARBASES:", str(player.num_starbases), report_pos_y)
    report_pos_y += FONT24.get_height()

    # draw_report_line("MAX WARP:", str(player.max_warp), report_pos_y, player)


# Draw each report line
def draw_report_line(title, value, y_pos):
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    flash_on = (current_time // 500) % 2 == 0  # Flash on/off every 500 milliseconds
    

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

        if player.current_quadrant.enemies:
            if (not player.shields_on) or (player.shields < 500): #(player.shield_level <= 25)
                if not flash_on: value_color = BLACK
                value_color = YELLOW 
                title_color = YELLOW
               

            if player.shields < 100:
                value_color = RED 
                title_color = RED
                

            if player.shields <= 0:
                title = "SHIELDS DOWN:"
        else: # no enemies
            if player.shields_on:
                if (player.shields < 500): #(player.shield_level <= 25)
                    if not flash_on: value_color = BLACK
                    value_color = YELLOW 
                    title_color = YELLOW
                    
                if player.shields < 100:
                    value_color = RED 
                    title_color = RED
                    
                if player.shields <= 0:
                    title = "SHIELDS DOWN:"



    elif  title == "SHIELD LEVEL:":
        if player.shields_on:
            value_color = WHITE
            title_color = WHITE
        else:
            value_color = GREEN 

    elif title == "CONDITION:":
        if player.condition == "RED":
            if not flash_on: value_color = BLACK

    elif title == "HULL STRENGTH:":
        if player.hull < (MAX_HULL * .80):
            value_color = YELLOW
            if not flash_on: value_color = BLACK

        if player.hull <= (MAX_HULL * 0.5):
            value_color = RED
            if not flash_on: value_color = BLACK


    # Render and draw the title
    title_surface = FONT24.render(title, True, title_color)
    title_rect = title_surface.get_rect(
        topleft=(QUADRANT_ORIGIN_X, y_pos)
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

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    flash_on = (current_time // 500) % 2 == 0  # Flash on/off every 500 milliseconds


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

    

    if player.current_quadrant.enemies:

        # Display sector information
        sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, RED)
        screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))

        # Display sector information
        sector_title = FONT24.render(f"COMBAT AREA", True, RED)
        screen.blit(sector_title, (sector_info_x, sector_info_y))

        if (player.shield_level <= 25) or (not player.shields_on) or (player.shields < 250):
            shield_title = FONT24.render(f"SHIELDS DANGEROUSLY LOW", True, YELLOW)
            screen.blit(shield_title, (sector_info_x + 180, sector_info_y + line_height))

    elif player.inDockingRange is not None:

        if player.docked:
            sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, BLUE)
            screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))
            # Display sector information
            sector_title = FONT24.render(f"DOCKED WITH STARBASE", True, BLUE)
            screen.blit(sector_title, (sector_info_x, sector_info_y))
        else:
            sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, GREEN)
            screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))
            # Display sector information
            sector_title = FONT24.render(f"IN DOCKING RANGE WITH STARBASE", True, BLUE)
            screen.blit(sector_title, (sector_info_x, sector_info_y))

    elif player.inOrbitRange is not None:

        if player.inOrbit:

            sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, GREEN)
            screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))
            sector_title = FONT24.render(f"IN PLANETARY ORBIT", True, BLUE)
            screen.blit(sector_title, (sector_info_x, sector_info_y))
        else:
            sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, GREEN)
            screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))
            sector_title = FONT24.render(f"IN ORBITAL RANGE WITH PLANET", True, BLUE)
            screen.blit(sector_title, (sector_info_x, sector_info_y))
    else:
        ...
        sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, GREEN)
        screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))

    # Display player condition aligned to the right edge of the sector map

    color = GREEN

    
        

    if player.condition == "GREEN":
        color = GREEN

    if player.condition == "BLUE":
        color = BLUE

    if player.condition =="RED":
        color = RED
        if flash_on:
            player_condition = FONT24.render(
                f" ** CONDITION: {player.condition} **",True,color)
            screen.blit(player_condition, (player_info_x - player_condition.get_width(), player_info_y-FONT24.get_height()))
    else:
        player_condition = FONT24.render(
            f"CONDITION: {player.condition}",True,color)
        screen.blit(player_condition, (player_info_x - player_condition.get_width(), player_info_y-FONT24.get_height()))





def draw_quadrant_map(player):

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    flash_on = (current_time // 500) % 2 == 0  # Flash on/off every 500 milliseconds


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

            





            num_enemy = this_sector.count_enemies()
            num_bases = this_sector.count_bases()
            num_stars = this_sector.count_stars()

            if is_adjacent_or_same_sector(player.current_quadrant, this_sector):

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

            grid_color = DARK_GREEN

            if col == player.quadrant_x and row == player.quadrant_y:
                if flash_on: 
                    grid_color = GREEN
                    colorA = RED if num_enemy > 0 else GREEN
                    colorB = BLUE if num_bases > 0 else GREEN
                    colorC = GREEN if num_stars > 0 else GREEN
                else:
                    grid_color = DARK_GREEN
                    colorA = DARK_RED if num_enemy > 0 else DARK_GREEN
                    colorB = DARK_BLUE if num_bases > 0 else DARK_GREEN
                    colorC = DARK_GREEN if num_stars > 0 else DARK_GREEN


                # colorC = GREEN

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
            
            # Draw column headers (centered above the grid)
            if row == 0:  # Only draw column headers on the first row
                column_text = FONT24.render(str(col + 1), True, GREEN)
                column_text_rect = column_text.get_rect(
                    center=(this_square_x + QUADRANT_SQUARE_SIZE // 2, QUADRANT_ORIGIN_Y - QUADRANT_SQUARE_SIZE // 2)
                )
                SCREEN.blit(column_text, column_text_rect) 

        # Draw row headers (centered to the left of the grid)
        row_text = FONT24.render(str(row + 1), True, GREEN)
        row_text_rect = row_text.get_rect(
            center=(QUADRANT_ORIGIN_X - QUADRANT_SQUARE_SIZE // 2, this_square_y + QUADRANT_SQUARE_SIZE // 2)
        )
        SCREEN.blit(row_text, row_text_rect) 

            
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

def prompt_shields_transfer(screen):
    """Prompt the player to transfer energy between shields and energy reserves."""
    input_text = ""
    prompt_active = True

    while prompt_active:
        # Clear and display the prompt area
        SCREEN.fill(BLACK)
        prompt_surface = FONT24.render("Enter Energy Transfer Amount (+/-):", True, WHITE)
        screen.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

        # Display the current input
        input_surface = FONT24.render(input_text, True, WHITE)
        screen.blit(input_surface, (PROMPT_ORIGIN_X + prompt_surface.get_width() + 10, PROMPT_ORIGIN_Y))
        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width() + input_surface.get_width(),PROMPT_ORIGIN_Y)
        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Confirm input
                    try:
                        transfer_amount = int(input_text)
                        if transfer_amount > 0:  # Transferring energy to shields
                            if player.energy >= transfer_amount:
                                if player.shield_energy + transfer_amount <= MAX_SHIELDS:
                                    player.energy -= transfer_amount
                                    player.shield_energy += transfer_amount
                                    if player.shield_level > 0:
                                        player.shields = (player.shield_energy / 100) * player.shield_level
                                    else:
                                        player.shields = 0
                                    print(f"Transferred {transfer_amount} energy to shields.")
                                else:
                                    print("Transfer would exceed maximum shield capacity.")
                            else:
                                print("Not enough energy to transfer.")
                        elif transfer_amount < 0:  # Transferring energy back to reserves
                            transfer_back = abs(transfer_amount)
                            if player.shield_energy >= transfer_back:
                                if player.energy + transfer_back <= MAX_ENERGY:
                                    player.energy += transfer_back
                                    player.shield_energy -= transfer_back
                                    if player.shield_level > 0:
                                        player.shields = (player.shield_energy / 100) * player.shield_level
                                    else:
                                        player.shields = 0
                                    print(f"Transferred {transfer_back} energy back to reserves.")
                                else:
                                    print("Transfer would exceed maximum energy capacity.")
                            else:
                                print("Not enough energy in shields to transfer back.")
                        else:
                            print("No energy transferred.")
                        return  # Exit the prompt once a valid transfer occurs
                    except ValueError:
                        print("Invalid input. Please enter a valid numeric value.")
                        input_text = ""  # Reset on invalid input
                elif event.key == pygame.K_BACKSPACE:  # Remove the last character
                    input_text = input_text[:-1]
                else:  # Add new character
                    if len(input_text) < 6 and (event.unicode.isdigit() or (event.unicode == '-' and len(input_text) == 0)):
                        input_text += event.unicode





def prompt_phaser_power(screen):
    """Display a prompt for the player to enter phaser power."""
    input_text = ""
    prompt_active = True

    while prompt_active:
        SCREEN.fill(BLACK)
        prompt_surface = FONT24.render("Enter Phaser Power (0-2000):", True, WHITE)
        screen.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

        input_surface = FONT24.render(input_text, True, WHITE)
        screen.blit(input_surface, (PROMPT_ORIGIN_X + prompt_surface.get_width() + 10 , PROMPT_ORIGIN_Y))

        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width() + input_surface.get_width(),PROMPT_ORIGIN_Y)

        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Confirm input
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

def draw_cursor(x,y):
    global color_index, color_change_timer

    # Update the color every `color_change_interval` milliseconds
    if pygame.time.get_ticks() - color_change_timer > COLOR_CHANGE_INTERVAL:
        color_index = (color_index + 1) % len(SHADE_COLOR_CYCLE)  # Cycle to the next color
        color_change_timer = pygame.time.get_ticks()

    # Get the current color from the list
    current_color = SHADE_COLOR_CYCLE[color_index]

    # Calculate the rectangle's position
    rect_x = x + 10  # Add some padding to the right of the text
    rect_y = y - 5
    rect_width = FONT24.get_height()  # Rectangle width equals the height of the text
    rect_height = FONT24.get_height() + 5 

    # Draw the rectangle with the current color
    pygame.draw.rect(SCREEN, current_color, (rect_x, rect_y, rect_width, rect_height))

def prompt_warp_factor(screen):
    """Display a prompt for the player to enter warp factor."""
    input_text = ""
    prompt_active = True

    while prompt_active:
        SCREEN.fill(BLACK)
        prompt_surface = FONT24.render("Enter Warp Factor (0-10):", True, WHITE)
        screen.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

        input_surface = FONT24.render(input_text, True, WHITE)
        screen.blit(input_surface, (PROMPT_ORIGIN_X + prompt_surface.get_width() + 10 , PROMPT_ORIGIN_Y))

        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width() + input_surface.get_width(),PROMPT_ORIGIN_Y)




        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Confirm input
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
        SCREEN.fill(BLACK)
        # Display the prompt
        prompt_surface = FONT24.render(prompt_text, True, WHITE)
        SCREEN.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width(),PROMPT_ORIGIN_Y)


        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

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

def draw_compass():
    """Display a compass guide showing the warp direction numbers."""


    guide_text = [
        "     7    8    9    ",
        "        ·   ·   ·   ",
        "          · · ·   ",
        "  4 - - -   - - - 6    ",
        "          · · ·   ",
        "        ·   ·   ·   ",
        "     1    2    3    ",
    ]

    y_offset = PROMPT_ORIGIN_Y - 50  # Adjust based on where you want to display it
    for line in guide_text:
        text_surface = FONT24.render(line, True, GREEN)
        SCREEN.blit(text_surface, (COMPASS_ORIGIN_X, y_offset))
        y_offset += FONT24.get_height()


def prompt_sector_target(screen, prompt_text):
    """Prompt the player to input a sector target (e.g., 3,4)."""
    input_text = ""
    while True:
        # Clear the prompt area
        SCREEN.fill(BLACK)  # Bottom-left corner
        
        # Display the prompt and current input
        prompt_surface = FONT24.render(f"{prompt_text} {input_text}", True, WHITE)
        SCREEN.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))
        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width(),PROMPT_ORIGIN_Y)


        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

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


def get_quadrant_name(quadrant_x, quadrant_y):
    """Generate a name for a quadrant based on its coordinates."""
    # Define names for rows based on quadrant_x

    quadrant_x =  quadrant_x+1

    list_one = ["ANTARES", "RIGEL", "PROCYON", "VEGA", "CANOPUS", "ALTAIR", "SAGITTARIUS", "POLLUX"]
    list_two = ["SIRIUS", "DENEB", "CAPELLA", "BETELGEUSE", "ALDEBARAN", "REGULUS", "ARCTURUS", "SPICA"]

    # Determine which list to use
    if quadrant_x <= 4:
        chosen_list = list_one
        adjusted_column = quadrant_x  # No adjustment for columns 1-4
    else:
        chosen_list = list_two
        adjusted_column = quadrant_x - 4  # Subtract 4 for columns >= 5

    adjusted_column = ["", "I", "II", "III", "IV"][adjusted_column]

    # Ensure coordinates are within valid bounds
    if 0 <= quadrant_y < len(chosen_list):
        quadrant_name = f"{chosen_list[quadrant_y]} {adjusted_column}"
        return quadrant_name
    else:
        return "Unknown Quadrant"  # Return a fallback name for invalid coordinates


# def calculate_direction_and_distance(player_x, player_y, enemy_x, enemy_y):
#     """Calculate the direction (rise/run) and distance between the player and an enemy."""
#     rise = enemy_y - player_y
#     run = enemy_x - player_x

#     direction = f"{rise}/{run}" if run != 0 else f"{rise}/0"

#     distance = round(((rise ** 2) + (run ** 2)) ** 0.5, 2)
#     return direction, distance

def calculate_direction_and_distance(player_x, player_y, enemy_x, enemy_y):
    """Calculate the direction (rise/run) and distance between the player and an enemy."""
    rise = enemy_y - player_y
    run = enemy_x - player_x

    # Simplify the fraction using GCD
    if run != 0:  # Avoid division by zero
        divisor = math.gcd(rise, run)
        rise //= divisor
        run //= divisor
    elif rise != 0:  # Handle vertical direction where run is 0
        rise = rise // abs(rise)  # Normalize rise to -1 or 1 for vertical direction

    direction = f"{rise} / {run}" if run != 0 else f"{rise} / 0"
    
    # Calculate the distance
    distance = round(((enemy_y - player_y) ** 2 + (enemy_x - player_x) ** 2) ** 0.5, 2)
    return direction, distance

def display_enemy_readout(screen):
    """
    Display a line-by-line readout of enemies in the player's current sector,
    sorted by increasing distance, with column headers and fixed x positions for each value.
    """
    y_offset = 0

    # Header text
    header_text = FONT24.render("SHORT RANGE SCAN:", True, GREEN)
    screen.blit(header_text, (SCAN_ORIGIN_X + 120, SCAN_ORIGIN_Y))
    y_offset += FONT24.get_height()
    separator_text = FONT24.render("-----------------------------------------------------------------------------------------", True, GREEN)
    screen.blit(separator_text, (SCAN_ORIGIN_X - 10, SCAN_ORIGIN_Y + y_offset))

    # Column headers
    y_offset += FONT24.get_height()
    column_headers = [("NAME", SCAN_NAME_X, "left"), ("DIRECTION", SCAN_DIRECTION_X, "center"), ("DISTANCE", SCAN_DISTANCE_X, "center"), 
                      ("SHIELD", SCAN_SHIELD_X, "center"), ("HULL", SCAN_HULL_X, "center")]

    for header, x_offset, alignment in column_headers:
        header_text = FONT24.render(header, True, GREEN)

        if alignment == "left":
            # Align the "Name" header to the left
            screen.blit(header_text, (SCAN_ORIGIN_X + x_offset, SCAN_ORIGIN_Y + y_offset))
        elif alignment == "center":
            # Center align the other headers
            text_width = header_text.get_width()
            column_center = SCAN_ORIGIN_X + x_offset + (100 - text_width) // 2
            screen.blit(header_text, (column_center, SCAN_ORIGIN_Y + y_offset))

    # Add a separator line below the column headers
    y_offset += FONT24.get_height()
    separator_text = FONT24.render("-----------------------------------------------------------------------------------------", True, GREEN)
    screen.blit(separator_text, (SCAN_ORIGIN_X - 10, SCAN_ORIGIN_Y + y_offset))

    # Create a list of enemies with their distances and directions
    targets_with_distances = []

    for enemy in player.current_quadrant.enemies:
        if enemy.grid_x == player.grid_x and enemy.grid_y == player.grid_y:
            continue  # Skip if the enemy is on the same square as the player

        # Calculate direction and distance
        direction, distance = calculate_direction_and_distance(
            player.grid_x, player.grid_y, enemy.grid_x, enemy.grid_y
        )
        targets_with_distances.append((enemy, direction, distance))


    # Add starbase information if present
    # if player.current_quadrant.has_starbase:
    for starbase in player.current_quadrant.bases:
        # starbase_grid_x, starbase_grid_y = base[0], base[1]
        direction, distance = calculate_direction_and_distance(
            player.grid_x, player.grid_y, starbase.grid_x, starbase.grid_y
        )
        targets_with_distances.append((starbase, direction, distance))

    # for planet in player.current_quadrant.planets:
    #     # starbase_grid_x, starbase_grid_y = base[0], base[1]
    #     direction, distance = calculate_direction_and_distance(
    #         player.grid_x, player.grid_y, planet.grid_x, planet.grid_y
    #     )
    #     targets_with_distances.append((planet, direction, distance))

    # Sort enemies by distance
    targets_with_distances.sort(key=lambda x: x[2])  # Sort by distance (x[2])

    for planet in player.current_quadrant.planets:
        # starbase_grid_x, starbase_grid_y = base[0], base[1]
        direction, distance = calculate_direction_and_distance(
            player.grid_x, player.grid_y, planet.grid_x, planet.grid_y
        )
        targets_with_distances.append((planet, direction, distance))

    # Display each enemy
    y_offset += FONT24.get_height()
    for target, direction, distance in targets_with_distances:
        this_font = FONT24
        text_color = GREEN
        if type(target) == Enemy: text_color = RED
        elif type(target) == Planet: 
            text_color = GREEN
            this_font = FONT22
        elif  type(target) == Base: 
            text_color = BLUE
            if player.docked: 
                direction = "DOCKED"
                distance  = "DOCKED"
        

        # Render enemy name
        target_name_text = this_font.render(target.name, True, text_color)
        screen.blit(target_name_text, (SCAN_ORIGIN_X + SCAN_NAME_X -10, SCAN_ORIGIN_Y + y_offset))

        # Render enemy direction
        direction_text = this_font.render(direction, True, text_color)
        direction_x = SCAN_ORIGIN_X + SCAN_DIRECTION_X + (100 - direction_text.get_width()) // 2
        screen.blit(direction_text, (direction_x, SCAN_ORIGIN_Y + y_offset))

        # Render enemy distance
        distance_text = this_font.render(f"{distance}", True, text_color)
        distance_x = SCAN_ORIGIN_X + SCAN_DISTANCE_X + (100 - distance_text.get_width()) // 2
        screen.blit(distance_text, (distance_x, SCAN_ORIGIN_Y + y_offset))

        # Render enemy shield

        shield_text = this_font.render(f"{target.shields}", True, text_color)
        if target.shields <= 0:
            shield_text = this_font.render(f"--", True, GREY)

        shield_x = SCAN_ORIGIN_X + SCAN_SHIELD_X + (100 - shield_text.get_width()) // 2
        screen.blit(shield_text, (shield_x, SCAN_ORIGIN_Y + y_offset))

        # Render enemy hull
        hull_text = this_font.render(f"{target.hull}", True, text_color)
        if target.hull <= 0:
            hull_text = this_font.render(f"--", True, GREY)
        hull_x = SCAN_ORIGIN_X + SCAN_HULL_X + (100 - hull_text.get_width()) // 2
        screen.blit(hull_text, (hull_x, SCAN_ORIGIN_Y + y_offset))

        y_offset += FONT24.get_height()  # Increment y-offset for the next enemy



def prompt_numeric_input(prompt_text, min_value, max_value, compass=False):
    """Prompts the player for numeric input (including negative numbers) and shows input as it's typed."""
    input_text = ""  # Start with an empty string
    while True:
        SCREEN.fill(BLACK)

        
        # Render the prompt and current input
        prompt_surface = FONT24.render(f"{prompt_text} {input_text}", True, WHITE)
        SCREEN.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

        if compass:
            draw_compass()

        draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width(),PROMPT_ORIGIN_Y)
        
        draw_all_to_screen()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character
                    input_text = input_text[:-1]
                elif (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS) and len(input_text) == 0:
                    # Allow minus sign at the beginning (for negative numbers)
                    input_text = "-" + input_text
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE or event.key == pygame.K_COMMA or event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                    # On return, we will attempt to parse the input
                    try:
                        user_input = int(input_text)
                        if min_value <= user_input <= max_value:
                            return user_input
                    except ValueError:
                        pass  # Ignore if input isn't a valid number, continue waiting

                # Handle input from the number keys (0-9)
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += chr(event.key)

                # Handle input from the numeric keypad keys (0-9)
                elif event.key == pygame.K_KP0:
                    input_text += "0"
                elif event.key == pygame.K_KP1:
                    input_text += "1"
                elif event.key == pygame.K_KP2:
                    input_text += "2"
                elif event.key == pygame.K_KP3:
                    input_text += "3"
                elif event.key == pygame.K_KP4:
                    input_text += "4"
                elif event.key == pygame.K_KP5:
                    input_text += "5"
                elif event.key == pygame.K_KP6:
                    input_text += "6"
                elif event.key == pygame.K_KP7:
                    input_text += "7"
                elif event.key == pygame.K_KP8:
                    input_text += "8"
                elif event.key == pygame.K_KP9:
                    input_text += "9"

        # Wait a bit for smooth input response
        pygame.time.wait(100)

def display_computer_active_text():
    global color_index, color_change_timer

    if players_turn == True:

        # # Update the color every `color_change_interval` milliseconds
        # if pygame.time.get_ticks() - color_change_timer > COLOR_CHANGE_INTERVAL:
        #     color_index = (color_index + 1) % len(SHADE_COLOR_CYCLE)  # Cycle to the next color
        #     color_change_timer = pygame.time.get_ticks()

        # Get the current color from the list
        current_color = SHADE_COLOR_CYCLE[color_index]

        # Render the text with the current color
        computer_active_text = "COMPUTER ACTIVE AND AWAITING COMMAND:"
        computer_active_title = FONT24.render(computer_active_text, True, current_color)

        # Calculate the center position relative to the sector map
        map_center_x = GRID_ORIGIN_X + (GRID_SIZE * SQUARE_SIZE) // 2
        text_width = computer_active_title.get_width()
        centered_x = map_center_x - (text_width // 2)

        # Display the text centered X-wise
        SCREEN.blit(computer_active_title, (centered_x, PROMPT_ORIGIN_Y))

        # Calculate the rectangle's position
        draw_cursor(centered_x + text_width,PROMPT_ORIGIN_Y)
        # rect_x = centered_x + text_width + 10  # Add some padding to the right of the text
        # rect_y = PROMPT_ORIGIN_Y - 5
        # rect_width = computer_active_title.get_height()  # Rectangle width equals the height of the text
        # rect_height = computer_active_title.get_height() + 5 

        # # Draw the rectangle with the current color
        # pygame.draw.rect(SCREEN, current_color, (rect_x, rect_y, rect_width, rect_height))

def draw_captain(overlay_images, key_pressed=False):
    # Define the size of the box
    box_width = 55 * CAPTAIN_BOX_SCALE
    box_height = 30 * CAPTAIN_BOX_SCALE
    
    # Calculate the position for the box (right of center at the bottom)
    box_x = QUADRANT_ORIGIN_X - box_width - 50  # 10 pixels offset from the right edge
    box_y = SCREEN_HEIGHT - box_height - 25  # 10 pixels offset from the bottom edge

    # Draw the grey outline for the box
    pygame.draw.rect(SCREEN, GREY, (box_x-2, box_y-2, box_width+4, box_height+4), 2)  # 2 is the outline thickness

    BASE_IMAGE = pygame.transform.scale(CRUISER_CAPTAIN_000, (box_width, box_height))  # Scale to box size

    # Draw the 'CRUISER_CAPTAIN_000' background image inside the box
    SCREEN.blit(BASE_IMAGE, (box_x, box_y))

    if key_pressed:
        # Select a few images randomly from the additional list
        num_images_to_draw = random.randint(1, 3)  # Change the range to adjust how many images to pick
        selected_images = random.sample(CRUISER_CAPTAIN_ADDITIONALS, num_images_to_draw)

        # Store the selected images with their offsets
        overlay_images.clear()  # Clear any previous overlay images
        for image, x_offset, y_offset in selected_images:
            overlay_images.append((image, x_offset, y_offset))

    # Draw the stored overlay images (even if key_pressed is False)
    for image, x_offset, y_offset in overlay_images:
        overlay_image = pygame.transform.scale(image, (image.get_width()*CAPTAIN_BOX_SCALE, image.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size
        x_offset, y_offset = abs(x_offset), abs(y_offset)
        SCREEN.blit(overlay_image, (box_x + x_offset*CAPTAIN_BOX_SCALE, box_y + y_offset*CAPTAIN_BOX_SCALE))


def draw_all_to_screen(): # for use when in a prompt.
    global projectile_group
    draw_alert_info(SCREEN)
    
    draw_sector_map()
    
    projectile_group.update() 
    for projectile in projectile_group:
        if not projectile.out_of_bounds():
            projectile.draw(SCREEN)

    draw_reports()
    display_enemy_readout(SCREEN)
    draw_quadrant_map(player)

    draw_captain(overlay_images,key_pressed)



### END FUNCTIONS ###########################################################################################################

def main():
    running = True
    global player
    global projectile_group
    global current_index
    global players_turn
    global overlay_images
    global key_pressed

    player = Player()
    projectile_group = pygame.sprite.Group() 

    current_index = SHIELD_LEVELS.index(player.shield_level)  # Find the current level's index
    players_turn = True

    # List to store overlay images and their offsets
    overlay_images = []

    while running:

        ### UPDATE EVERYTHING ###############################################################################################


        # enemy_count_ttl = 0
        # for sector in player.all_sectors:
        #     enemy_count_ttl += sector.count_enemies()
        # player.num_enemies = enemy_count_ttl


        delta_time = clock.tick(60)  # Get the time since the last frame (in ms)
        # Simulate hull and crew check
        player.check_hull_and_crew(delta_time)

        # Example condition to stop the game loop (modify as needed)
        if player.crew <= 0:
            ...
            # running = False

        
        key_pressed = False


        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            

            elif event.type == pygame.KEYDOWN:  # Check for key presses

                if players_turn and (len(projectile_group) ==0) :

                    
                    
                    if event.key == pygame.K_LEFT:
                        player.move(-1, 0)
                        key_pressed = True
                        

                    elif event.key == pygame.K_RIGHT:
                        player.move(1, 0)
                        key_pressed = True
                    elif event.key == pygame.K_UP:
                        player.move(0, -1)
                        key_pressed = True
                    elif event.key == pygame.K_DOWN:
                        player.move(0, 1)
                        key_pressed = True
                    elif event.key == pygame.K_SPACE: # REST
                        player.move(0, 0)
                        key_pressed = True

                    elif event.key == pygame.K_r: #REST
                        player.move(0, 0)
                        key_pressed = True

                    elif event.key == pygame.K_p:
                        if not player.docked: player.fire_phasers()
                        key_pressed = True

                    elif event.key == pygame.K_t:
                        if not player.docked: player.fire_torpedo()
                        key_pressed = True

                    elif event.key == pygame.K_w:
                        if not player.docked: player.activate_warp()
                        key_pressed = False

                    elif event.key == pygame.K_s:
                        key_pressed = False
                        # player.shields_toggle()
                        if not player.docked: prompt_shields_transfer(SCREEN)





                    elif event.key == pygame.K_d:
                        key_pressed =  True
                        if player.inDockingRange is not None:
                            player.toggle_dock(player.inDockingRange)

                    elif event.key == pygame.K_o:
                        key_pressed =  True
                        if player.inOrbitRange is not None:
                            player.toggle_orbit(player.inOrbitRange)

                    elif event.key == pygame.K_KP_PLUS:

                        key_pressed = False
                        if not player.docked: 
                            # Increase the shield level
                            player.shields_on = True
                            if current_index < len(SHIELD_LEVELS) - 1:
                                current_index += 1
                                player.shield_level = SHIELD_LEVELS[current_index]
                                print(f"Shield level increased to {player.shield_level}%")
                                if player.shields_on:
                                    player.shields = (player.shield_energy / 100) * player.shield_level
                                    WEAPON_CHANNEL.play(SHIELD_UP)
                                else:
                                    player.shields =0
                                player.energy -= RAISE_SHIELD_PER


                    elif event.key == pygame.K_KP_MINUS:
                        key_pressed = False
                        if not player.docked: 
                            # Decrease the shield level
                            if current_index > 0:
                                current_index -= 1
                                player.shield_level = SHIELD_LEVELS[current_index]
                                print(f"Shield level decreased to {player.shield_level}%")
                                if player.shields_on:
                                    WEAPON_CHANNEL.play(SHIELD_DOWN)
                                    if player.shield_level <= 0:
                                        player.shields_on = False
                                        player.shields = 0
                                    else:
                                        player.shields = (player.shield_energy / 100) * player.shield_level
                                else:
                                    player.shields = 0




                    if key_pressed and (player.turn != 0):#### ENEMY TURN ??
                        for enemy in player.current_quadrant.enemies:
                            if enemy.trigger_update_time is None:
                                enemy.trigger_update(players_turn)

                    
                player.turn += 1

                            





        ### END UPDATES #####################################################################################################



        ### DRAW EVERYTHING #################################################################################################
        SCREEN.fill(BLACK)

        display_computer_active_text()

        draw_alert_info(SCREEN)

        draw_sector_map()

        for enemy in player.current_quadrant.enemies:
            enemy.update(player.current_quadrant,players_turn)

        projectile_group.update() 
        for projectile in projectile_group:
            if not projectile.out_of_bounds():
                projectile.draw(SCREEN)

        draw_reports()

        display_enemy_readout(SCREEN)

        draw_quadrant_map(player)

        draw_captain(overlay_images,key_pressed)

        while player.is_dead:

            delta_time = clock.tick(60)  # Get the time since the last frame (in ms)
            # Simulate hull and crew check
            player.check_hull_and_crew(delta_time)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    player.is_dead = False

            SCREEN.fill(BLACK)
            draw_all_to_screen()
            ### FLIP AND TICK ###
            pygame.display.flip()
            # Cap the frame rate
            clock.tick(FPS)

        

        ### END DRAWINGS ####################################################################################################


        ### FLIP AND TICK ###
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
