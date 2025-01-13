import pygame
import sys

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

# Colors (RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
FONT24 = pygame.font.Font(None, 24)

### END CONSTANTS ###########################################################################################################

### LOAD ASSETS #############################################################################################################

# player_image = pygame.image.load("player.png").convert_alpha()
# font = pygame.font.Font(None, 36)

EARTHING_SHIP = pygame.image.load("earthling.png").convert_alpha() 

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
        self.grid_x = 0  # Starting grid position (column)
        self.grid_y = 0  # Starting grid position (row)
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

    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (self.grid_x * SQUARE_SIZE)
        player_draw_y = GRID_ORIGIN_Y + (self.grid_y * SQUARE_SIZE)
        self.rect.topleft = (player_draw_x, player_draw_y)

    def move(self, dx, dy):
        """Move the player in the grid, ensuring it stays within bounds."""
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_position()

        # Update last_move_direction
        if dx == -1:
            self.last_move_direction = "left"
            self.image = pygame.transform.rotate(self.orig_image,90)
        elif dx == 1:
            self.last_move_direction = "right"
            self.image = pygame.transform.rotate(self.orig_image,-90)
        elif dy == -1:
            self.last_move_direction = "up"
            self.image = self.orig_image
        elif dy == 1:
            self.last_move_direction = "down"
            self.image = pygame.transform.flip(self.orig_image, False, True) 

### END OBJECT CLASSES ######################################################################################################

### DEFINE FUNCIONS #########################################################################################################

def draw_combat_grid(player):
    # Draw the grid background
    SCREEN.blit(GRID_BACKGROUND, (GRID_ORIGIN_X, GRID_ORIGIN_Y))

    # Draw grid lines
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            this_square_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
            this_square_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
            rect = pygame.Rect(this_square_x, this_square_y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, GREEN, rect, 1)

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


### END FUNCTIONS ###########################################################################################################

def main():
    running = True
    player = Player()


    while running:

        ### UPDATE EVERYTHING ###############################################################################################

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

        draw_combat_grid(player)

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

        ### END DRAWINGS ####################################################################################################


        ### FLIP AND TICK ###
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
