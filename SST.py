import pygame
import sys
import random
import math

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
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_GREEN =(0,50,0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 50)

# Fonts
FONT24 = pygame.font.Font(None, 24)

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
        self.update_position()


        self.stardate = 3801
        self.daysleft = 32

        self.condition = "GREEN"
        self.condition_color = GREEN

        self.quadrant_x = 0
        self.quadrant_y = 0

        self.torpedo_qty = 10
        self.energy = 1000 
        self.shields = 0
        self.num_enemies = 20
        self.max_warp = 8

        self.sensor_range = 1


        self.all_sectors = []  # Dictionary to store Sector objects for each (quadrant_x, quadrant_y)
        self.generate_all_sectors()  # Generate all sectors when the game starts
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

        for sector in self.all_sectors:
            if (self.quadrant_x == sector.quadrant_x) and (self.quadrant_y == sector.quadrant_y):
                

        
 
                # Ensure player's starting position isn't on a star or base
                while sector.is_star_at(self.grid_x, self.grid_y) or sector.is_base_at(self.grid_x, self.grid_y) or sector.is_enemy_at(self.grid_x, self.grid_y):
                    self.move_away_from_star_or_base(sector)

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

        


    def move(self, dx, dy):
        """Move the player in the grid, ensuring it stays within bounds and handles quadrant transitions."""
        # Check if the player will move out of the current sector (grid bounds)
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

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
            elif dx == -1:  # Moving left
                if self.quadrant_x > 0:
                    self.quadrant_x -= 1
                    self.grid_x = GRID_SIZE - 1
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
            elif dy == 1:  # Moving down
                if self.quadrant_y < QUADRANT_SIZE - 1:
                    self.quadrant_y += 1
                    self.grid_y = 0
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
            elif dy == -1:  # Moving up
                if self.quadrant_y > 0:
                    self.quadrant_y -= 1
                    self.grid_y = GRID_SIZE - 1
                    self.current_sector = self.enter_sector(self.quadrant_x, self.quadrant_y)
            
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = ENEMY_SHIP
        self.orig_image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.image = self.orig_image

        self.rect = self.image.get_rect()
        self.last_move_direction = "up"
        self.update_position()

        self.torpedo_qty = 10
        self.energy = 1000 
        self.shields = 0

    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE)
        player_draw_y = GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE)
        self.rect.topleft = (player_draw_x, player_draw_y)


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
                return True
        return False




### END OBJECT CLASSES ######################################################################################################

### DEFINE FUNCIONS #########################################################################################################

def draw_sector_map(player):
    # Draw the grid background
    SCREEN.blit(GRID_BACKGROUND, (GRID_ORIGIN_X, GRID_ORIGIN_Y))


    # Draw grid lines
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            this_square_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
            this_square_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
            rect = pygame.Rect(this_square_x, this_square_y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)

            

            
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

            elif player.current_sector.is_enemy_at(col, row):
                enemy_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                enemy_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - ENEMY_SHIP.get_width()) // 2
                offset_y = (SQUARE_SIZE - ENEMY_SHIP.get_height()) // 2
                SCREEN.blit(ENEMY_SHIP, (enemy_screen_x + offset_x, enemy_screen_y + offset_y))
                pygame.draw.rect(SCREEN, RED, rect, 1)  # RED grid line


            elif col == player.grid_x and row == player.grid_y:
                pygame.draw.rect(SCREEN, GREEN, rect,1)  # Highlight in Green (or another color)
                

            else:
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Regular grid line

            # # Draw grid number for each square (optional)
            # number_text = FONT24.render("000", True, GREEN)
            # number_rect = number_text.get_rect(center=(this_square_x + SQUARE_SIZE // 2, this_square_y + SQUARE_SIZE // 2))
            # SCREEN.blit(number_text, number_rect)


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
    draw_report_line("STARDATE:", str(player.stardate), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("DAYS LEFT:", str(player.daysleft), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("CONDITION:", player.condition, report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("QUADRANT:", f"{player.quadrant_x + 1} , {player.quadrant_y + 1}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("SECTOR:", f"{player.grid_x + 1} , {player.grid_y + 1}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("TORPEDOS:", str(player.torpedo_qty), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("ENERGY:", str(player.energy), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("SHIELDS:", str(player.shields), report_pos_y)
    report_pos_y += FONT24.get_height()

    
    draw_report_line("ENEMIES:", str(player.num_enemies), report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("MAX WARP:", str(player.max_warp), report_pos_y)


# Draw each report line
def draw_report_line(title, value, y_pos):
    # Render and draw the title
    title_surface = FONT24.render(title, True, GREEN)
    title_rect = title_surface.get_rect(
        topleft=(SCREEN_WIDTH-REPORT_TITLE_MARGIN, y_pos)
    )
    SCREEN.blit(title_surface, title_rect)

    # Render and draw the value
    value_surface = FONT24.render(value, True, GREEN)
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

### END FUNCTIONS ###########################################################################################################

def main():
    running = True
    player = Player()

    

    while running:

        ### UPDATE EVERYTHING ###############################################################################################


        enemy_count_ttl = 0
        for sector in player.all_sectors:
            enemy_count_ttl += sector.count_enemies()
        player.num_enemies = enemy_count_ttl 

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

            elif event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)



        ### END UPDATES #####################################################################################################



        ### DRAW EVERYTHING #################################################################################################
        SCREEN.fill(BLACK)

        draw_sector_map(player)

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
