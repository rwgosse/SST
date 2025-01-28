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

# Fonts
FONT22 = pygame.font.Font(None, 22)
FONT24 = pygame.font.Font(None, 24)

# DIMENSIONS 
GRID_SIZE = 8
SQUARE_SIZE = 80

GRID_ORIGIN_X, GRID_ORIGIN_Y = SQUARE_SIZE, SQUARE_SIZE*2
GRID_END_X = GRID_ORIGIN_X + (SQUARE_SIZE * GRID_SIZE)

# Constants for the quadrant map
QUADRANT_SIZE = 8  # 8x8 grid
QUADRANT_MARGIN = 20  # Margin from the right and bottom of the screen
QUADRANT_SQUARE_SIZE = 40  # Size of each square in the quadrant map
QUADRANT_ORIGIN_X = SCREEN_WIDTH - QUADRANT_SIZE * QUADRANT_SQUARE_SIZE - QUADRANT_MARGIN
QUADRANT_ORIGIN_Y = SCREEN_HEIGHT - QUADRANT_SIZE * QUADRANT_SQUARE_SIZE - QUADRANT_MARGIN

SCAN_ORIGIN_X = GRID_ORIGIN_X + (QUADRANT_SIZE * SQUARE_SIZE) + 50
SCAN_ORIGIN_Y = GRID_ORIGIN_Y - 25
SCAN_NAME_X = 0
SCAN_DIRECTION_X = 110
SCAN_DISTANCE_X = 215
SCAN_SHIELD_X = 300
SCAN_HULL_X = 360

REPORTS_ORIGIN_Y = SCAN_ORIGIN_Y
REPORT_TITLE_MARGIN = 300
REPORT_STATUS_MARGIN = 150






PROMPT_ORIGIN_X = 80 
PROMPT_ORIGIN_Y = SCREEN_HEIGHT - 80
PROMPT_AREA = (PROMPT_ORIGIN_X, SCREEN_HEIGHT - 90, 300, 200)  # Bottom-left corner
COMPASS_ORIGIN_X = SCAN_ORIGIN_X

CAPTAIN_BOX_SCALE = 3
CAPTAIN_BOX_WIDTH  = 55 * CAPTAIN_BOX_SCALE
CAPTAIN_BOX_HEIGHT = 30 * CAPTAIN_BOX_SCALE
CAPTAIN_BOX_ORIGIN_X = GRID_END_X + CAPTAIN_BOX_WIDTH

CREW_ORIGIN_X = GRID_ORIGIN_X + 10
CREW_ORIGIN_Y = GRID_ORIGIN_Y + 10
CREW_DETAIL_START_X = CREW_ORIGIN_X + 20
CREW_DETAIL_START_Y  = CREW_ORIGIN_Y + 20
CREW_BOX_SIZE_WIDTH = (SQUARE_SIZE * GRID_SIZE) - 40

LOG_ORIGIN_X = SCAN_ORIGIN_X -10
LOG_ORIGIN_Y = GRID_ORIGIN_Y + (SQUARE_SIZE*4)
LOG_WIDTH = 440  # Width of the log display
LOG_HEIGHT = SQUARE_SIZE*3.5  # Height of the log display
LOG_PADDING = 10  # Padding inside the log box
MAX_LOG_ENTRIES = 20  # Maximum number of events in the log


# Colors (RGB values)
WHITE = (255, 255, 255)
OFF_WHITE = (200, 200, 200)
LIGHT_GREY = (150, 150, 150)
GREY = (128, 128, 128)
MIDDLE_GREY = (100, 100, 100)
DARK_GREY = (50, 50, 50)
NEAR_BLACK = (25, 25, 25)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MIDDLE_RED = (160, 0, 0)
LOWER_RED = (100, 0, 0)
DARK_RED = (50, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GOLD       = (255,215,0)
MIDDLE_YELLOW = (180, 180, 0)
DARK_YELLOW = (60, 60, 0)
GREEN = (0, 255, 0)
MIDDLE_GREEN = (0,150,0)
DARK_GREEN =(0,50,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (35,35,255)
DARK_BLUE = (0, 0, 128)
DARK_PURPLE     = (139,0,139) # Mageneta technically speaking
PURPLE = (255,0,255) 

# Define the shades from WHITE to BLACK
SHADE_COLOR_CYCLE = [WHITE, WHITE, OFF_WHITE, OFF_WHITE,LIGHT_GREY, GREY, MIDDLE_GREY, DARK_GREY, NEAR_BLACK, DARK_GREY, MIDDLE_GREY,GREY, LIGHT_GREY,OFF_WHITE,OFF_WHITE,WHITE,WHITE]
TORPEDO_COLOR_CYCLE = [WHITE,RED,ORANGE,YELLOW,GOLD,DARK_RED, DARK_YELLOW]
GREEN_COLOR_CYCLE = [GREEN,YELLOW,MIDDLE_GREEN,DARK_GREEN]
color_index = 0  # To track the current color index
color_change_timer = 0  # Timer to control the color cycling speed
COLOR_CHANGE_INTERVAL = 100  # Time in milliseconds between color changes






### GAME CONSTANTS ### 


DEPARTMENT_LIST = ["Command", "Pilot", "Communications", "Engineering", "Tactical", "Security", "Intelligence", "Bio-Science", "Physical-Science", "Medical"]
RANK_LIST = ["Crewman", "Able Crewman", "Chief", "Ensign", "2nd Lt.", "1st Lt.", "Lt. Cmdr", "Commander", "Captain"]
CREWNAMELIST = ["Belt","Buck","Bukowski","Adama", "Carter","Chu","Chin","Decker","Ender","Graeme","Hendryx","Halleck","Hawkins","Hodgkinds","Jeevo","Jenkins","Kirk","Kilgore","Pike","Pirx","Rigby", "Riker", "Solo","Spiff","Trent","Tuf", "Troy", "VanRijn", "Vance", "Wu", "Witherspoon", "Yam"]
CREWNAMELIST.extend(["Aero","Aether","Allen","Anderson","Armstrong","Asimov","Barnhardt","Beam","Bester","Blish","Blixseth","Brackett","Bradbury","Burroughs","Campbell","Carlyle","Chandler","Clarke","Clement","Clive","Comet","Corbett","Crockett","Dawnstar","De Camp","Del Rey","Dent","Doyle","Earhart","Felsmark","Fifer","Finnegan","Grail","Grim","Hammond","Harlin","Hathway","Hawks","Heinlein","Herrmann","Holmes","Howard","Jones","Kazantsev","Lanning","Lansing","Leiber","Lester","Levitan","Merril","Meteor","Miller","Moore","Morningstar","O’Malley","Oliver","Pohl","Powers","Quartermain","Quinn","Raymond","Reith","Rhodan","Rocklynne","Savage","Scheer","Shin","Slayton","Smith","Sprague","Starfury","Starke","Starskimmer","Van Vogt","Vega","West","Wilhelm","Wyndham","Zelas"])
CREWNAMELIST.extend(["Aguerra","Cairn ","Crusher","Delis ","Flashman","Haggard","Hart","Hornwrack","Jax","Kandel","Lee","McIntyre","Silenus","Vinge","Wae","Wergard","Zodiac"])
ANDROID_NAMES = ["QT","TC","Alpha","Beta","Scrap","Ratchet","Sparkle","Igioid","Max","Copper","Ano","C3","R4","Mechi","Ayc","Bult","Otis","Spark"]
PKUNK_NAMES = ["Weeny", "Wikki", "Beeki", "Birdi", "Braky", "Girdy", "Awkky", "Chrupp", "Awwky","Brakky","Buzzard","Crow","Ernie","Fuzzy","Hooter","Jay","Polly","Poppy","Raven","Screech","Tweety","Twitta","WudStok","Yompin"]

ALLIED_SPECIES_LIST = ["Human","Human","Human","Human","Android","Pkunk"] # add on later... more allied species


POSITIVE_CHARACTER_TRAITS = ["accepts authority","accepts what’s given","affectionate","aspiring","candid","caring","accepts change","cheerful","considerate","cooperative","courageous","courteous","decisive","devoted","determined","does what is necessary","perseveres","enthusiastic","expansive","faith in life","faith in oneself","faith in others","flexible","forgiving","focused","freedom given to others","friendly","frugal","generous","goodwill","grateful","hard-working","honest","humble","interested","involved","jealous","kind","mature","modest","open-minded","optimistic","perfects","persistent","positive","practical","punctual","realistic","reliable","respectful","responsibility; takes-","responsible","responsive","self-confident","self-directed","self-disciplined","self-esteem","self-giving","self-reliant","selfless","sensitive","serious","sincere","social independence","sympathetic","systematic","takes others point of view","thoughtful towards others","trusting","unpretentious","unselfish","willing does","work-oriented","achieved; has-","adventurous","substance-free","alert","aware of opportunities","calm","clean","clear goals","clear thoughts","completes","comprehends","conscious","conscious of one’s weaknesses","constructive","content-oriented","creative","delegates","deliberative","detail-oriented","develops mental capabilities","directed","disciplined","dynamic","educated","education exceed previous generation","education greater than present level of achievement","education greater than previous generation","efficient","effort taking","effort achieves results","energetic","enterprising","entrepreneurial","envisions the unseen","experienced (in area)","fatigue-free","goal-oriented","good","graceful","has enough time","health robust","high goals","higher social interests","idea-driven","imaginative","improves self","in rapidly expanding field of work","initiates (has initiative)","innovative","insightful","intelligent","knowledgeable","knowledgeable in a particular area","leads others","lives from the depths of life","lucky; things go your way","money circulated for improvement","motivated","nerves strong","objective","observant","organized","patient","personable","physical stamina","polite","previous success in family life","previous success in school","previous success in work","productive interactions with others","professional (acts)","professional qualification achieved","regular","relationship with other(s) positive","resourceful","results-oriented","risk-taker","sees the whole picture","seeks improvement","spiritual","stamina","strong; physically-","strong; psychologically-","stress-free","(has had) supportive family or friends","tough","trustworthy","wealthy","wealth in present generation","well-behaved","work is in harmony with personal life","capacity to judge others","careful","communication skills","(can) exercise authority","delegation skills","leadership skills","listening skills","management skills","motivating skills","negotiating skills","organization skills","planning skills","problem-solving skills","public speaking skills","reconciling problems","skilled","speaking skills","teamwork skills","technical work skills","time management skills","verbal skills","writing skills","affectionate family upbringing","high mental abilities in family","parents attained high social status","parents motivated","parents rose & accomplished","(inheritance) physical attributes are fine","(had) previous success (in school","prosperity in family upbringing","psychological health and well-being","prosperity in surrounding society","supportive social environment","loyal","ambitious","thoughtful","right","endures","thrifty","tolerant","sustaining","willingness","has direction","strong constitution","mannered","inner connection","relaxed","graceful with objects","conflicts at higher level skills","talented exceptionally in particular area","gave direction","works hard",]
NEGATIVE_CHARACTER_TRAITS = ["rebellious","ignores, rejects what’s given","distant, cold, aloof","self-satisfied, unmotivated","closed, guarded, secretive","uncaring, unfeeling, callous","rejects change","cheerless, gloomy, sour, grumpy","inconsiderate, thoughtless","uncooperative, unhelpful, combative","cowering, fearful","rude, impolite","indecisive","uncommitted, uncaring, hostile","indecisive, unsure","does what is convenient","relents, gives up","unenthusiastic, apathetic, indifferent","kept back, tight, constricting","life can’t be trusted","lack of faith in self","others can’t be relied on","inflexible, rigid, unbending, stubborn","unforgiving, resentful, spiteful","unfocused, scattered","authoritarian, controlling","unfriendly, distant, aloof, hostile","wasteful, spendthrift","stingy, miserly, selfish","ill-will, malice, hatred","ungrateful, unappreciative","lazy","dishonest, deceiving, lying","arrogant, conceited, ego-centric","indifferent, uncaring","complacent, indifferent","jealous, envious, covetous","unkind, uncaring, cruel, mean","immature","vain","narrow, close, small-minded, intolerant","pessimistic","allows imperfection","flagging, fleeting, unsustaining","negative","impractical, not viable","late, not on time","unrealist, impractical","unreliable, undependable","disrespectful, rude, impolite","blames others","unresponsive, unreceptive","lack of self confidence, insecure","directed by externals","undisciplined, unrestrained, indulgent","self-esteem, confidence – low","self-centered","dependent","selfish","Insensitive, indifferent","frivolous, silly, trivial","insincere, dishonest","social approval required","unsympathetic, unfeeling","unsystematic, disorganized, disorderly, random","insists on own view","thoughtless, inconsiderate, callous","suspicious, mistrusting","pretentious, affected, ostentatious","unwilling, reluctant, recalcitrant","convenience first","hasn’t achieve","conventional","substance-abuse (alcohol, drug)","dull","ignorant of opportunities","excitable, nervous","dirty, unkempt","lack of, jumbled goals; directionless","muddled thoughts, confused","leaves hanging, doesn’t complete","doesn’t comprehend","unconscious","unconscious of one’s strengths","destructive, complaining","outer, surface, form-oriented","uncreative","tries to do everything","reckless","scrimps on details","leaves mental capacities as is","directionless, unfocused","dissipating","passive","uneducated","education not exceed previous generation","education less than present level of achievement","education less than previous generation","inefficient","lack of effort","effort wasted","listless","enterprising, not","entrepreneurial, not","visionless","inexperienced (in area)","tired, fatigued","unfocused, addled, scattered","goalless, directionless","evil","clumsy","never has enough time","poor health, weak constitution","low, no goals","lower, no social interests","ideas don’t motivate to act","unimaginative","stays the same","in static or declining field","lacks initiative","conservative","lacks insight, blind to, ignorant of","stupid","ignorant, uniformed","no knowledge in a particular area","submits, yields to others","lives on the surface of life, superficial","unlucky","money hoarded for security","unmotivated","nerves weak","subjective, biased","blind to, oblivious to","disorganized","impatient, expectant","non-engaging, distant, cold","lack of stamina","impolite, ill mannered, rude","previous failure in family life","previous failure in school","previous failure in work","chit-chatting","amateurish (acts)","no professional qualification","late","irregular, erratic","relationship with other(s) negative","unresourceful, helpless","irresponsible","does for doing’s sake, being merely occupied","averse to risk","seeing only parts of the picture","self-satisfied","lacks any spiritual, inner connection","weak; physically-","weak; psychologically-","stressed, tense","(has had) indifferent, uncaring family or friends","weak, soft","untrustworthy","impoverished","poverty in present generation","ill behaved","work is in conflict with personal life","unable to judge others","careless, clumsy","communication skills, lack of","cannot exercise authority","delegation skills, lack of","leadership skills, lack of","listening skills, lack of","management skills, lack of","motivating skills, lack of","negotiating skills, lack of","organization skills, lacks","planning skills, lack of","problem-solving skills, lack of","public speaking skills, lack of","reconciling problems, conflicts at higher level skills, lack of","unskilled","not skilled, talented exceptionally in particular area","speaking skills, lack of","teamwork skills, lack of","technical work skills, lack of","time management skills, lack of","verbal skills, lack of","writing skills, lack of","indifferent, hostile family upbringing","poor mental abilities in family","parents have low social status","parents demotivated, gave no direction","parents remained in same position","(inheritance) physical attributes are poor","(had) previous failure (in school, work, family life)","poverty in family upbringing","psychological problems","poverty in surrounding society","indifferent social environment",]

EXTRA_SKILL_LIST = ["Animal Handling","Architecture","Artist","Bioengineering","Code-Breaking","Computer Hacking","Computer-Programming","Diplomacy","Electronics Operation","Expert Skill","Explosives","Forgery","Gambling","Hidden Lore","History","Intelligence Analysis","Interrogation","Law","Leadership","Logistics","Mathematics","Meditation","Melee-Combat","Merchant","Mimicry","Observation","Photography","Politics","Ranged-Combat","Smuggling","Spacer","Stealth","Survival","Traps","Weird Science"]




MAX_NUM_OF_BASES = 5
MAX_NUM_OF_PLANETS_PER = 2 
MAX_ENERGY = 3000
BASE_RELOAD_ENERGY = 3000
WARP_ENERGY_PER = 100
RAISE_SHIELD_PER = 50
SHIELD_LEVELS = [0, 25, 50, 75, 100]
MAX_CREW = 18
MIN_CREW_FOR_STARSHIP = 5
MAX_HULL = 1000
MAX_SHIELDS = 2000
BASE_RELOAD_SHIELD = 2000

MAX_TORPEDO_QTY = 10
PLAYER_TORPEDO_DAMAGE = 1000
TORPEDO_DAMAGE = 500
TORPEDO_SPEED = 0.25
TORPEDO_ENERGY_USAGE = 50

CHANCE_OF_TORPEDO_MISS = 0.01
MISS_CHANCE_INCREASE_PER = 0.01

ENERGY_CHARGE_TICK = 20
HULL_REPAIR_TICK = 5

TRANSPORTER_ENERGY_USAGE = 5

STARDATE_PER_REPAIR_TICK = 0.015

CARGO_MAX = 100
AWAY_TEAM_SIZE = 5 



### END CONSTANTS ###########################################################################################################

### LOAD ASSETS #############################################################################################################

# player_image = pygame.image.load("player.png").convert_alpha()
# font = pygame.font.Font(None, 36)

EARTHING_SHIP = pygame.image.load("earthling.png").convert_alpha() 
BASE_IMAGE = pygame.image.load("base.png").convert_alpha()
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (SQUARE_SIZE*.75, SQUARE_SIZE*.75))  # Scale to grid square size 

DRONE_SHIP = pygame.image.load("drone.png").convert_alpha() 
AVENGER_SHIP = pygame.image.load("avenger.png").convert_alpha() 
INTRUDER_SHIP = pygame.image.load("intruder.png").convert_alpha() 
GUARDIAN_SHIP = pygame.image.load("guardian.png").convert_alpha() 
ELUDER_SHIP = pygame.image.load("spathi.png").convert_alpha()
PODSHIP_SHIP = pygame.image.load("podship.png").convert_alpha()
DREADNAUGHT_SHIP = pygame.image.load("urq.png").convert_alpha() 

# Define a list of possible enemies with their respective images
ENEMY_SHIP_LIST = [
    ("DRONE", DRONE_SHIP),
    ("INTRUDER", INTRUDER_SHIP),
    ("GUARDIAN", GUARDIAN_SHIP),
    ("AVENGER", AVENGER_SHIP),
    ("ELUDER", ELUDER_SHIP),
    ("PODSHIP", PODSHIP_SHIP),
    ("DREADNAUGHT", DREADNAUGHT_SHIP)

]

CREWMAN_IMAGE = pygame.image.load("crewman.png").convert_alpha() 

LANDER_IMAGE = pygame.image.load("lander-000.png").convert_alpha()  

WORMHOLE_IMAGE = pygame.image.load("wormhole.png").convert_alpha()  

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
CRUISER_CAPTAIN_000 = pygame.transform.scale(CRUISER_CAPTAIN_000, (CAPTAIN_BOX_WIDTH, CAPTAIN_BOX_HEIGHT))  # Scale to box size

CRUISER_CAPTAIN_001 = pygame.image.load("cruiser-cap-001.png").convert_alpha()
CRUISER_CAPTAIN_001 = pygame.transform.scale(CRUISER_CAPTAIN_001, (CRUISER_CAPTAIN_001.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_001.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_002 = pygame.image.load("cruiser-cap-002.png").convert_alpha()  
CRUISER_CAPTAIN_002 = pygame.transform.scale(CRUISER_CAPTAIN_002, (CRUISER_CAPTAIN_002.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_002.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_003 = pygame.image.load("cruiser-cap-003.png").convert_alpha() 
CRUISER_CAPTAIN_003 = pygame.transform.scale(CRUISER_CAPTAIN_003, (CRUISER_CAPTAIN_003.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_003.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_004 = pygame.image.load("cruiser-cap-004.png").convert_alpha() 
CRUISER_CAPTAIN_004 = pygame.transform.scale(CRUISER_CAPTAIN_004, (CRUISER_CAPTAIN_004.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_004.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_005 = pygame.image.load("cruiser-cap-005.png").convert_alpha() 
CRUISER_CAPTAIN_005 = pygame.transform.scale(CRUISER_CAPTAIN_005, (CRUISER_CAPTAIN_005.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_005.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_006 = pygame.image.load("cruiser-cap-006.png").convert_alpha() 
CRUISER_CAPTAIN_006 = pygame.transform.scale(CRUISER_CAPTAIN_006, (CRUISER_CAPTAIN_006.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_006.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_007 = pygame.image.load("cruiser-cap-007.png").convert_alpha() 
CRUISER_CAPTAIN_007 = pygame.transform.scale(CRUISER_CAPTAIN_007, (CRUISER_CAPTAIN_007.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_007.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_008 = pygame.image.load("cruiser-cap-008.png").convert_alpha() 
CRUISER_CAPTAIN_008 = pygame.transform.scale(CRUISER_CAPTAIN_008, (CRUISER_CAPTAIN_008.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_008.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_009 = pygame.image.load("cruiser-cap-009.png").convert_alpha() 
CRUISER_CAPTAIN_009 = pygame.transform.scale(CRUISER_CAPTAIN_009, (CRUISER_CAPTAIN_009.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_009.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_010 = pygame.image.load("cruiser-cap-010.png").convert_alpha() 
CRUISER_CAPTAIN_010 = pygame.transform.scale(CRUISER_CAPTAIN_010, (CRUISER_CAPTAIN_010.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_010.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_011 = pygame.image.load("cruiser-cap-011.png").convert_alpha() 
CRUISER_CAPTAIN_011 = pygame.transform.scale(CRUISER_CAPTAIN_011, (CRUISER_CAPTAIN_011.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_011.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_012 = pygame.image.load("cruiser-cap-012.png").convert_alpha() 
CRUISER_CAPTAIN_012 = pygame.transform.scale(CRUISER_CAPTAIN_012, (CRUISER_CAPTAIN_012.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_012.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_013 = pygame.image.load("cruiser-cap-013.png").convert_alpha() 
CRUISER_CAPTAIN_013 = pygame.transform.scale(CRUISER_CAPTAIN_013, (CRUISER_CAPTAIN_013.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_013.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 

CRUISER_CAPTAIN_014 = pygame.image.load("cruiser-cap-014.png").convert_alpha() 
CRUISER_CAPTAIN_014 = pygame.transform.scale(CRUISER_CAPTAIN_013, (CRUISER_CAPTAIN_014.get_width()*CAPTAIN_BOX_SCALE, CRUISER_CAPTAIN_014.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size 


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
NEXT_LINE   = pygame.mixer.Sound("menusnd01.wav")
NEXT_LINE.set_volume(.30)


WEAPON_CHANNEL = pygame.mixer.Channel(2)
WEAPON_CHANNEL.set_volume(0.25)
PHASER_SOUND = pygame.mixer.Sound("earthling-pd.wav")
MISSILE_SOUND = pygame.mixer.Sound("earthling-mx.wav")
SHIELD_UP = pygame.mixer.Sound("melnorme-charge.wav")
SHIELD_DOWN = pygame.mixer.Sound("melnorme-confuse.wav")
ENEMY_PHASER_SOUND = pygame.mixer.Sound("vux-laser.wav")
ENEMY_TORPEDO = pygame.mixer.Sound("mycon-plasmoid.wav")  

EXPLOSION_CHANNEL = pygame.mixer.Channel(3)
EXPLOSION_CHANNEL.set_volume(0.50)
SHIP_DEATH_SOUND = pygame.mixer.Sound("shipdies.wav")
SHIP_DEATH_SOUND.set_volume(0.50)
MEDIUM_EXPLOSION = pygame.mixer.Sound("boom-medium.wav")
WARP_SOUND = pygame.mixer.Sound("tng_slowwarp_clean.mp3")
WARP_SOUND.set_volume(0.50)
HURT = pygame.mixer.Sound("land_hrt.wav") 
PORTAL = pygame.mixer.Sound("portal.wav")
TRANSPORTER_SOUND = pygame.mixer.Sound("transporter.mp3")
TRANSPORTER_SOUND.set_volume(0.50)
CLOAK_SOUND = pygame.mixer.Sound("cloak.wav")
DECLOAK_SOUND = pygame.mixer.Sound("decloak.wav")

SHUTTLE_LAUNCH = pygame.mixer.Sound("land_lau.wav")
SHUTTLE_LAUNCH.set_volume(0.50)
SHUTTLE_RETURN = pygame.mixer.Sound("land_awa.wav")
SHUTTLE_RETURN.set_volume(0.50)

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

        self.name = "Player"
        
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

        # self.crew = MAX_CREW

        self.soulsOnBoard        = pygame.sprite.Group()
        self.crewMax             = MAX_CREW # Crew Pods Added. You now have increased crew capacity, but to gain more crew you must recruit at a colony.
        self.lastCasualties      = 0 
        while (len(self.soulsOnBoard) < self.crewMax):
            self.addCrewman(random.choice(ALLIED_SPECIES_LIST))
        self.crewQty             = len(self.soulsOnBoard)
        self.landers             = 2


        self.num_enemies = 0
        self.num_starbases = 0
        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)

        self.sensor_range = 1

        self.offset_x = 0 
        self.offset_y = 0 
        self.inDockingRange = None
        self.inOrbitRange = None
        self.orbiting_planet = None
        self.away_team_on_planet = False
        self.dilithium_crystals = 0 

        self.cargo_max = CARGO_MAX
        self.cargo = 0

        self.docked = False
        self.inOrbit = False

        self.last_warp_factor = 1

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
        print("Galaxy creation complete")

    def enter_sector(self, quadrant_x, quadrant_y, wormhole=False):
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
                while (sector.is_star_at(self.grid_x, self.grid_y)) or (sector.is_base_at(self.grid_x, self.grid_y)) or (sector.is_enemy_at(self.grid_x, self.grid_y)) or (sector.is_planet_at(self.grid_x, self.grid_y)) or (sector.is_wormhole_at(self.grid_x, self.grid_y)):
                    self.move_away_from_star_or_base(sector)

                if sector != self.current_quadrant: #ENTERING A NEW SECTOR

                    if self.current_quadrant != None:
                        for enemy in self.current_quadrant.enemies: # RESET ENEMY ENERGY IF PLAYER LEAVES
                            enemy.energy = enemy.full_energy
                            enemy.shields = enemy.full_shields
                            enemy.hull = enemy.full_hull
                    
                    if wormhole:
                        log_event("")
                        log_event(f"** Entered Wormhole **", PURPLE)

                    else:
                        log_event("")
                        log_event(f"Warping to quadrant ({self.quadrant_x+1}, {self.quadrant_y+1}) at Warp {self.last_warp_factor}.", WHITE)

                    # log_event(f"NOW ENTERING {get_quadrant_name(sector.quadrant_x, sector.quadrant_y)} QUADRANT")

                    if sector.count_enemies() >=1 :
                        ALARM_CHANNEL.play(RED_ALERT,2)
                        # MUSIC_CHANNEL.play(ENEMY_DITTY)
                        log_event(f"NOW ENTERING {get_quadrant_name(sector.quadrant_x, sector.quadrant_y)} QUADRANT", RED)
                        log_event(f"COMBAT AREA - CONDITION RED", RED)


                        for enemy in sector.enemies:
                            print(enemy.name, " : ", enemy.hull)

                    else:
                        log_event(f"NOW ENTERING {get_quadrant_name(sector.quadrant_x, sector.quadrant_y)} QUADRANT",GREEN)

                    




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
                            if not sector.is_wormhole_at(nx, ny):
                                self.grid_x, self.grid_y = nx, ny
                                self.update_position()
                                print("Evasive!")
                                return
        
        print(f"Warning: No valid adjacent square found for the player. Staying at ({self.grid_x}, {self.grid_y}).")


    def addCrewman(self, species):
        if (len(self.soulsOnBoard) == 0): # MINIMUM COMMAND STAFF
                recruit = Crewman("Human","Captain","Command", self.stardate)
                recruitSuccess = True
        elif (len(self.soulsOnBoard) == 1): # MINIMUM COMMAND STAFF
            recruit = Crewman("Human","Commander","Command", self.stardate)
            recruitSuccess = True
        elif (len(self.soulsOnBoard) == 2): # MINIMUM COMMAND STAFF
            department = random.choice(["Command","Engineering"])
            recruit = Crewman("Human","Lt. Cmdr",department, self.stardate)
            recruitSuccess = True
        
        elif (len(self.soulsOnBoard) == 3): # MINIMUM COMMAND STAFF
            recruit = Crewman("Human","1st Lt.","Medical", self.stardate)
            recruitSuccess = True

        elif (len(self.soulsOnBoard) == 4): # MINIMUM COMMAND STAFF
            department = random.choice(["Command", "Pilot", "Engineering", "Tactical", "Security", "Intelligence", "Physical-Science","Bio-Science"])
            recruit = Crewman("Human","1st Lt.",department, self.stardate)
            recruitSuccess = True

        elif (len(self.soulsOnBoard) <= 5): # MINIMUM COMMAND STAFF
            department = random.choice(["Command", "Pilot", "Engineering", "Tactical", "Security","Physical-Science", "Bio-Science"])
            recruit = Crewman("Human","2nd Lt.",department, self.stardate)
            recruitSuccess = True

        elif (len(self.soulsOnBoard) <= MIN_CREW_FOR_STARSHIP+2): # MINIMUM COMMAND STAFF
            department = random.choice(["Command", "Pilot", "Engineering", "Tactical", "Security","Physical-Science", "Bio-Science"])
            recruit = Crewman("Human","Ensign",department, self.stardate)
            recruitSuccess = True

        elif (len(self.soulsOnBoard) == MIN_CREW_FOR_STARSHIP+3): # MINIMUM COMMAND STAFF
            department = random.choice(["Pilot", "Engineering", "Tactical", "Security","Physical-Science", "Bio-Science"])
            recruit = Crewman("Human","Chief",department, self.stardate)
            recruitSuccess = True
        
        else:
            department = random.choice(DEPARTMENT_LIST)
            recruit = Crewman(species,"Crewman",department, self.stardate)
            recruitSuccess = True 

        for soul in self.soulsOnBoard:
            if recruit.name == soul.name:
                recruitSuccess = False 
        if recruitSuccess:
            self.soulsOnBoard.add(recruit)
        else:
            recruit.kill()

    
    def check_hull_and_crew(self, delta_time):
        """Check if the player's hull is below 0 and potentially kill crew members."""

        self.soulsOnBoard.update(self)
        self.crewQty = len(self.soulsOnBoard)

        if self.hull <= 0:
            self.crew_loss_timer += delta_time
            if self.crew_loss_timer >= 100:  # 500ms (half a second)
                self.crew_loss_timer = 0  # Reset the timer

                # 10% chance to lose a crew member
                if self.crewQty > 0:
                    if random.random() < 0.5:
                        # self.crew -= random.randint(1,5)
                        killqty = random.randint(1,5)


                        
                        for i in range(killqty):
                            souls = self.soulsOnBoard.sprites()
                            if len(souls) <= 0:
                                break
                            casualty = souls[-1]
                            log_event(f"{casualty.fullInfo()} KILLED !")
                            casualty.kill()
                        self.crewQty = len(self.soulsOnBoard)

                        # if player.crewQty <= 0: 
                        #     player.crew = 0

                        EXPLOSION_CHANNEL.play(HURT)
                        print(f"Critical damage! Crew have been lost. Remaining crew: {self.crewQty}")
                        log_event(f" ** Critical damage! Crew have been lost. Remaining crew: {self.crewQty} **", ORANGE)
                        
                        
                        if random.random() < 0.1:
                            print("Hull Integrity Restored")
                            log_event("Hull Integrity Restored")
                            self.hull = 1 # chance hull is restored

                        if len(self.current_quadrant.enemies) <= 0:
                            print("Hull Integrity Restored")
                            log_event("Hull Integrity Restored")
                            self.hull = 1 # chance hull is restored


                else:
                    if not self.is_dead:
                        print("All crew members have been lost!")
                        log_event("All crew members have been lost!", ORANGE)
                        self.explode(self.grid_x,self.grid_y,SQUARE_SIZE*1.5,2,2,sound=SHIP_DEATH_SOUND)
                        self.is_dead = True

                    # self.end_game()
            else:
                print("Hull breach detected!")
                log_event(f"** ! HULL BREACH DETECTED ! **", ORANGE)
        else:
            self.crew_loss_timer = 0  # Reset the timer if the hull is stable


    def update_position(self):
        """Update the player's rect position based on the grid coordinates."""
        player_draw_x = GRID_ORIGIN_X + (round(self.grid_x) * SQUARE_SIZE) + self.offset_x
        player_draw_y = GRID_ORIGIN_Y + (round(self.grid_y) * SQUARE_SIZE) + self.offset_y
        self.rect.topleft = (player_draw_x, player_draw_y)


        self.soulsOnBoard.update(self)
        self.crewQty = len(self.soulsOnBoard)


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
        repairing = False 

        if self.docked:
            
            if self.energy < BASE_RELOAD_ENERGY:
                self.energy += ENERGY_CHARGE_TICK
                repairing = True

            if self.torpedo_qty < MAX_TORPEDO_QTY:
                self.torpedo_qty += 1
                repairing = True

            if self.crewQty < self.crewMax:
                if self.away_team_on_planet:
                    if self.crewQty < (self.crewMax-AWAY_TEAM_SIZE):
                        # self.crew += 1
                        self.addCrewman(random.choice(ALLIED_SPECIES_LIST))
                        repairing = True
                        self.crewQty = len(self.soulsOnBoard)
                else:
                    self.addCrewman(random.choice(ALLIED_SPECIES_LIST))
                    repairing = True
                    self.crewQty = len(self.soulsOnBoard)
                

            if self.hull < MAX_HULL:
                self.hull += HULL_REPAIR_TICK
                repairing = True

            if self.shield_energy < BASE_RELOAD_SHIELD:
                self.shield_energy += ENERGY_CHARGE_TICK
                repairing = True

            if self.cargo > 0:
                self.cargo -= 1



        elif self.inOrbit:

            if self.energy < BASE_RELOAD_ENERGY//4:
                self.energy += ENERGY_CHARGE_TICK//2
                repairing = True
                if self.energy > BASE_RELOAD_ENERGY//4:
                    self.energy = BASE_RELOAD_ENERGY//4

            if self.hull < MAX_HULL*.75:
                self.hull += HULL_REPAIR_TICK//2
                repairing = True
                if self.hull > MAX_HULL*.75:
                    self.hull = MAX_HULL*.75 


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

        if self.cargo < 0: self.cargo = 0

        self.max_warp = min(10, self.energy // WARP_ENERGY_PER)


    def toggle_dock(self, starbase):
        """
        Toggles the player's docking status.
        If condition is 'BLUE', docks the player and offsets the position towards the starbase.
        """
        if self.docked == False:
            if self.inDockingRange is not None:
                self.docked = True
                self.stardate += (.1 * 0.95)

                ALARM_CHANNEL.play(POWER_UP)

                # Calculate the offset
                self.offset_x = (starbase[0] - self.grid_x) * (SQUARE_SIZE // 2)
                self.offset_y = (starbase[1] - self.grid_y) * (SQUARE_SIZE // 2)

                # Apply the offset to the player's sprite position
                # self.rect.x += offset_x
                # self.rect.y += offset_y
                print("Docked at starbase!")
                log_event("** DOCKED AT STARBASE **", LIGHT_BLUE)

            else:
                self.docked = False
                print("Cannot dock unless condition is BLUE.")

        elif self.docked:
            self.docked = False
            self.stardate += (.1 * 0.95)
            self.offset_x = 0 
            self.offset_y = 0 
            print("Undocked from starbase!")
            log_event("** UNDOCKED **", LIGHT_BLUE)

    def toggle_orbit(self, planet):
        """
        Toggles the player's docking status.
        If condition is 'BLUE', docks the player and offsets the position towards the starbase.
        """
        if self.inOrbit == False:
            if self.inOrbitRange is not None:
                self.inOrbit = True
                self.stardate += (.1 * 0.95)

                ALARM_CHANNEL.play(POWER_UP)

                # Calculate the offset
                self.offset_x = (planet[0] - self.grid_x) * (SQUARE_SIZE // 2)
                self.offset_y = (planet[1] - self.grid_y) * (SQUARE_SIZE // 2)

                # Apply the offset to the player's sprite position
                # self.rect.x += offset_x
                # self.rect.y += offset_y
                print("Entered Planetary Orbit!")
                
                self.orbiting_planet = player.current_quadrant.is_planet_at(planet[0],planet[1])
                log_event(f"** ENTERED STANDARD ORBIT OF {self.orbiting_planet.name} **")

            else:
                self.inOrbit = False
                self.orbiting_planet = None
                print("Cannot enter orbit unless in range")

        elif self.inOrbit:
            self.inOrbit = False
            self.orbiting_planet = None
            self.stardate += (.1 * 0.95)
            self.offset_x = 0 
            self.offset_y = 0 
            print("Left Planetary Orbit!")
            log_event("** LEFT STANDARD ORBIT **")


    def land_away_team(self):
        global key_pressed
        """Prompt the player to transfer energy between shields and energy reserves."""
        input_text = ""
        prompt_active = True
        key_pressed = False

        while prompt_active:
            # Clear and display the prompt area
            SCREEN.fill(BLACK)
            prompt_surface = FONT24.render("By: (T)ransporter or (S)huttlecraft?", True, WHITE)
            SCREEN.blit(prompt_surface, (PROMPT_ORIGIN_X, PROMPT_ORIGIN_Y))

            # Display the current input
            input_surface = FONT24.render(input_text, True, WHITE)
            SCREEN.blit(input_surface, (PROMPT_ORIGIN_X + prompt_surface.get_width() + 10, PROMPT_ORIGIN_Y))
            draw_cursor(PROMPT_ORIGIN_X + prompt_surface.get_width() + input_surface.get_width(),PROMPT_ORIGIN_Y)
            draw_all_to_screen()
            pygame.display.flip()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.land_away_team_with_transporter()
                        key_pressed = True
                        return

                    elif event.key == pygame.K_s:
                        self.land_away_team_with_shuttle()
                        key_pressed = True
                        return

    def land_away_team_with_shuttle(self):
        ##Use a shuttlecraft to land an away team on a planet or return them to the ship.

        # Check if the ship is in orbit around the planet
        if not self.orbiting_planet:
            print("You must be in standard orbit to use a shuttlecraft.")
            return


        if self.orbiting_planet.landers >= 1 and not self.orbiting_planet.away_team_on_planet: # Shuttle already n planet returns to the ship
            self.orbiting_planet.landers    -= 1
            self.landers                    += 1 
            log_event(f"SHUTTLE RECALLED TO SHIP", WHITE)
            EXPLOSION_CHANNEL.play(SHUTTLE_RETURN)
            self.stardate += (.1 * 0.95)
            return

        if self.away_team_on_planet and not self.orbiting_planet.away_team_on_planet:
            log_event(f"NO AWAY TEAM AVAILABLE")
            return

        # Determine if the away team is currently on the planet or the ship
        if self.away_team_on_planet and self.orbiting_planet.away_team_on_planet:
            # Returning the away team to the ship using a shuttle

            if self.orbiting_planet.landers >= 1: # Shuttle on planet returns to the ship
                self.orbiting_planet.landers    -= 1
                self.landers                    += 1 

            elif self.landers <= 0: # Send Shuttle to planet to retrieve away team
                    print("No shuttlecraft available!")
                    log_event("NO SHUTTLECRAFT AVAILABLE", RED)
                    return

            else:
                print(f"Sending shuttle to pick up the away team from {self.orbiting_planet.name}...")
                log_event(f"SENDING SHUTTLE TO AWAY TEAM", WHITE)
                self.landers                    -= 1  # Deduct one shuttle for the mission
                self.orbiting_planet.landers    += 1
                EXPLOSION_CHANNEL.play(SHUTTLE_LAUNCH)
                self.stardate += (.1 * 0.95)
                return



            print(f"Shuttle has successfully returned with the away team.")
            log_event(f"SHUTTLE RETURNED WITH AWAY TEAM", GREEN)
            EXPLOSION_CHANNEL.play(SHUTTLE_RETURN)
            self.stardate += (.1 * 0.95)


            # Successfully retrieve the away team
            self.away_team_on_planet = False
            self.orbiting_planet.away_team_on_planet = False
            player.soulsOnBoard.add(self.orbiting_planet.away_team)
            self.orbiting_planet.away_team.empty()
            print(f"The away team has successfully returned to the ship.")

            # Perform mining
            mined_crystals = self.orbiting_planet.mine_dilithium()


            

        elif not self.away_team_on_planet:
            # Sending the away team to the planet using a shuttle
            if len(player.soulsOnBoard) < AWAY_TEAM_SIZE:
                print("Not enough crew members on board to form an away team!")
                log_event("NOT ENOUGH CREW TO FORM AWAY TEAM", RED)
                return

            # Select 5 crew members for the away team
            away_team = pygame.sprite.Group() 
            away_team.add(self.soulsOnBoard.sprites()[:AWAY_TEAM_SIZE]) 

            if self.landers <= 0: # Send Shuttle to planet to retrieve away team
                print("No shuttlecraft available!")
                log_event("NO SHUTTLECRAFT AVAILABLE", RED)
                return

            
            # if self.orbiting_planet.landers >= 1: # Shuttle already n planet returns to the ship
            #     self.orbiting_planet.landers    -= 1
            #     self.landers                    += 1 
            #     log_event(f"SHUTTLE RECALLED TO SHIP", WHITE)
            #     EXPLOSION_CHANNEL.play(SHUTTLE_RETURN)
            #     self.stardate += (.1 * 0.95)
            #     return




            self.landers                    -= 1  # Deduct one shuttle for the mission
            self.orbiting_planet.landers    += 1

            print(f"Shuttle dispatched to {self.orbiting_planet.name}...")
            log_event(f"SHUTTLE DISPATCHED TO {self.orbiting_planet.name}", WHITE)


            # Successfully land the away team
            self.away_team_on_planet = True
            self.orbiting_planet.away_team_on_planet = True
            print(f"Transported {len(away_team)} crew members to {self.orbiting_planet.name}.")
            print(f"The away team has successfully landed on {self.orbiting_planet.name}.")
            log_event(f"AWAY TEAM HAS LANDED ON {self.orbiting_planet.name}.", WHITE)
            EXPLOSION_CHANNEL.play(SHUTTLE_LAUNCH)
            self.stardate += (.1 * 0.95)
            self.soulsOnBoard.remove(away_team)
            self.orbiting_planet.away_team.add(away_team)

    def land_away_team_with_transporter(self):
        """
        Use the transporter to land an away team on a planet or return them to the ship.
        Transporting requires the ship to be in standard orbit, shields down, and is not always guaranteed to succeed.
        """
        # Check if the ship is in orbit around the planet
        if not self.orbiting_planet: #self.is_in_orbit(planet): 
            print("You must be in standard orbit to use the transporter.")
            return

        # Check if the shields are down
        if self.shields > 0:
            print("Shields must be down to use the transporter.")
            return

        if self.energy < TRANSPORTER_ENERGY_USAGE:
            print("Not enough energy for transporter")
            return

        if self.away_team_on_planet and not self.orbiting_planet.away_team_on_planet:
            log_event(f"NO AWAY TEAM AVAILABLE")
            return

        


        # Determine if the away team is currently on the planet or the ship
        if self.away_team_on_planet and self.orbiting_planet.away_team_on_planet :
            # Returning the away team to the ship
            self.energy -= TRANSPORTER_ENERGY_USAGE

            print(f"Attempting to beam up the away team from {self.orbiting_planet.name}...")
            log_event("")
            log_event(f"Attempting beam up from {self.orbiting_planet.name}...")
            WEAPON_CHANNEL.play(TRANSPORTER_SOUND)

            # Check for transporter malfunction (small chance of failure)
            if random.random() < 0.075:  # 5% chance of malfunction
                print("Transporter malfunction! The away team is temporarily lost in the buffer!")
                log_event(f"** TRANSPORTER MALFUNCTION **", RED)
                self.transport_malfunction_recovery(self.orbiting_planet.away_team)
                return

        elif not self.away_team_on_planet:
            # Beaming down to the planet
            """Transport 5 crew members to the planet."""
            if len(player.soulsOnBoard) < AWAY_TEAM_SIZE:
                print("Not enough crew members on board to form an away team!")
                log_event("NOT ENOUGH CREW TO FORM AWAY TEAM", RED)
                return

            # Select 5 crew members for the away team
            away_team = pygame.sprite.Group() 
            away_team.add(self.soulsOnBoard.sprites()[:AWAY_TEAM_SIZE])
            

            
            self.energy -= TRANSPORTER_ENERGY_USAGE
            print(f"Attempting to beam down to {self.orbiting_planet.name}...")
            log_event("")
            log_event(f"Attempting to beam down to {self.orbiting_planet.name}...")
            WEAPON_CHANNEL.play(TRANSPORTER_SOUND)

            # Check for transporter malfunction (small chance of failure)
            if random.random() < 0.075:  # 5% chance of malfunction
                print("Transporter malfunction! The away team is temporarily lost in the buffer!")
                log_event(f"** TRANSPORTER MALFUNCTION **", RED)
                self.transport_malfunction_recovery(away_team)
                return

        # Successfully transport the away team
        
        if self.away_team_on_planet and self.orbiting_planet.away_team_on_planet:
            self.away_team_on_planet = False
            self.orbiting_planet.away_team_on_planet = False
            print(f"The away team has successfully returned to the ship.")
            log_event(f"AWAY TEAM HAS RETURNED TO THE SHIP", WHITE)

            # Move the away team back to the ship
            player.soulsOnBoard.add(self.orbiting_planet.away_team)
            print(f"Beamed up {len(self.orbiting_planet.away_team)} crew members from {self.orbiting_planet.name}.")
            self.orbiting_planet.away_team.empty()  # Clear the away team from the planet

             # Perform mining if the team is on the planet
            mined_crystals = self.orbiting_planet.mine_dilithium()
            






        elif not self.away_team_on_planet:
            self.away_team_on_planet = True
            self.orbiting_planet.away_team_on_planet = True
            print(f"Transported {len(away_team)} crew members to {self.orbiting_planet.name}.")
            print(f"The away team has successfully beamed down to {self.orbiting_planet.name}.")
            log_event(f"AWAY TEAM HAS BEAMED DOWN TO {self.orbiting_planet.name}.", WHITE)
            # player.soulsOnBoard = player.soulsOnBoard.sprites()[AWAY_TEAM_SIZE:]  # Remove them from the ship
            self.soulsOnBoard.remove(away_team)
            self.orbiting_planet.away_team.add(away_team)  # Add them to the planet

        else:
            ...

           

    def transport_malfunction_recovery(self,away_team):
        """
        Handle transporter malfunction recovery. Assume it takes some time or effort to resolve.
        """
        print("Engineering is working to recover the transporter signal...")
        # time.sleep(2)  # Simulate recovery time
        WEAPON_CHANNEL.stop()
        ALARM_CHANNEL.play(RED_ALERT)

        

        killqty = random.choice([0,0,0,1,1,1,2])

        if killqty == 0 :
            print("The transporter signal has been re-established. All crew members are safe.")
            log_event(f"All crew members are safe.")
            self.crewQty = len(self.soulsOnBoard)
            return


        
        for i in range(killqty):
            souls = away_team.sprites()
            casualty = souls[-1]
            print("The transporter signal has been re-established.")
            log_event(f"    {casualty.fullInfo()} -- KILLED !", RED)

            casualty.kill()
            EXPLOSION_CHANNEL.play(HURT)

        self.crewQty = len(self.soulsOnBoard)

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
        num_enemy = self.current_quadrant.count_enemies_not_cloaked()
        print("Firing Phasors @: " + str(num_enemy) + " Targets.")
        log_event(f"** FIRING PHASERS **  @ {phaser_power} Power", WHITE)

        if phaser_power > 0:
            if phaser_power <= self.energy:
                
                self.energy -= phaser_power

                if num_enemy > 0:  # Only fire phasers if there are enemies present
                    damage = phaser_power / num_enemy

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
                        log_event(f"** HIT! {enemy.name} - {remaining_damage} DAMAGE", RED)

                        # Check and apply damage to shields first
                        if enemy.shields > 0:
                            shields_before = enemy.shields
                            if remaining_damage >= enemy.shields:
                                remaining_damage -= enemy.shields
                                enemy.shields = 0  # Shields are fully depleted
                                print(f"HIT! {enemy.name} SHIELDS: {shields_before} -> 0 (Shields Down!)")
                                log_event(f"     {enemy.name} :: SHIELDS DOWN ::", LIGHT_BLUE)
                                
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
                            log_event(f"     {enemy.name} :: !! DESTROYED !! ::)", RED)
                            EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)
                            enemy_x = GRID_ORIGIN_X + (enemy.grid_x * SQUARE_SIZE) + SQUARE_SIZE // 2
                            enemy_y = GRID_ORIGIN_Y + (enemy.grid_y * SQUARE_SIZE) + SQUARE_SIZE // 2
                            enemy_position = (enemy_x, enemy_y)
                            explosion = Explosion(enemy_position, max_size=SQUARE_SIZE, start_size=5, growth_rate=2)
                            projectile_group.add(explosion)

                            for crewman in player.soulsOnBoard:
                                crewman.xp += random.randint(0,5)


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
                    # for i, enemy in enumerate(self.current_quadrant.enemies):
                    #     print(" Phasor Target " + str(i))
                    #     delay = i * 0.25  # 0.3 seconds between each phaser blast
                    #     threading.Timer(delay, fire_single_phaser, args=(enemy,)).start()


                    # Schedule each phaser blast with a delay
                    # Use a copy of the enemies list to avoid index issues when modifying the list
                    enemies_copy = self.current_quadrant.enemies[:]

                    for i, enemy in enumerate(enemies_copy):  # Iterate over a copy
                        if not enemy.cloak_enabled:
                            print("Phaser Target " + str(i))
                            delay = i * 0.25  # 0.25 seconds between each phaser blast
                            threading.Timer(delay, fire_single_phaser, args=(enemy,)).start()
                        else:
                            print("Unable to lock onto " + enemy.name)
                            # log_event(f"-- UNABLE TO LOCK ONTO {enemy.name}", WHITE)





                    # Update remaining enemies after all blasts are scheduled
                    self.current_quadrant.enemies = [e for e in self.current_quadrant.enemies if e.hull > 0]




                    
                    

                    # Re-enter the sector to ensure state consistency
                    self.enter_sector(self.quadrant_x, self.quadrant_y)
                else:
                    print("No Phaser Targets Available")
                    log_event("No Phaser Targets Available", WHITE)
                    WEAPON_CHANNEL.play(PHASER_SOUND)
            else:
                print("Phaser Energy would exceed Available Energy")
                log_event("Phaser Energy would exceed Available Energy", WHITE)
        else:
            print("Zero Phaser Power Entered")
            log_event("Zero Phaser Power Entered", WHITE)





    def fire_torpedo(self):
        """Prompt the player to fire up to 3 torpedoes, selecting all targets first, then firing with delays."""
        max_torpedoes = 3
        num_torpedoes = prompt_numeric_input("Enter torpedoes to fire (0-3): ", 0, max_torpedoes)

        if num_torpedoes == 0:
            print("No torpedoes fired.")
            log_event("No torpedoes fired.", WHITE)
            return

        if num_torpedoes > self.torpedo_qty:
            num_torpedoes = self.torpedo_qty
            print("Insufficient qty torpedoes.")
            log_event("Insufficient qty torpedoes.", WHITE)

        # Collect target directions for each torpedo
        targets = []
        for i in range(num_torpedoes):
            rise = prompt_numeric_input(f"Enter direction for Torpedo {i + 1}: ", -GRID_SIZE, GRID_SIZE)
            run = prompt_numeric_input(f"Enter direction for Torpedo {i + 1}:  {rise} / ", -GRID_SIZE, GRID_SIZE)
            targets.append((rise, run))
            print(f"Direction selected for Torpedo {i + 1}: Rise: {rise}, Run: {run}")
            log_event(f"Direction selected for Torpedo {i + 1}: Rise: {rise}, Run: {run}", WHITE)

        # Define a helper function to fire a single torpedo
        def fire_single_torpedo(index, rise, run):
            """Fire a single torpedo."""
            if self.torpedo_qty >= 1:
                if self.energy >= TORPEDO_ENERGY_USAGE:
                    torpedo = Torpedo(index + 1, self, self.grid_x, self.grid_y, rise, run)
                    projectile_group.add(torpedo)
                    self.torpedo_qty -= 1
                    self.energy -= TORPEDO_ENERGY_USAGE
                    print(f"Torpedo {index + 1} fired with direction Rise: {rise}, Run: {run}!")
                    # log_event(f"Torpedo {index + 1} fired with direction Rise: {rise}, Run: {run}!")
                    WEAPON_CHANNEL.play(MISSILE_SOUND)

                    if self.torpedo_qty <= 0:
                        print("Torpedo Stock Depleted")
                        log_event("Torpedo Stock Depleted", WHITE)
                else:
                    print("Insufficient energy for Torpedo")
                    log_event("Insufficient energy for Torpedo", WHITE)
            else:
                print("Torpedo Stock Depleted")
                log_event("Torpedo Stock Depleted", WHITE)

        # Fire each torpedo with a short delay between them
        for i, (rise, run) in enumerate(targets):
            delay = i * 0.25  # Delay of 0.25 seconds between torpedoes
            threading.Timer(delay, fire_single_torpedo, args=(i, rise, run)).start()

    def activate_warp(self):
        """Prompt the player to select a warp factor and move the player."""
        warp_factor = prompt_warp_factor(SCREEN)

        if warp_factor > 0:
            self.stardate += (.1 * warp_factor)


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

            print(f"Warping to quadrant ({new_x}, {new_y}) at Warp {warp_factor}.")
            # log_event(f"Warping to quadrant ({new_x+1}, {new_y+1}) at Warp {warp_factor}.")
            self.last_warp_factor = warp_factor
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


    def check_if_entered_hole(self, new_x, new_y):
        # Check if the player enters a wormhole
        for wormhole in self.current_quadrant.wormholes:
            if new_x == wormhole.grid_x and new_y == wormhole.grid_y:
                print(f"Player entered wormhole at ({new_x}, {new_y})!")
                # log_event(f"Player entered wormhole at ({new_x+1}, {new_y+1})!", PURPLE)

                # Find a different quadrant with a wormhole
                possible_quadrants = []

                for sector in self.all_sectors:
                    if sector != self.current_quadrant:
                        if sector.count_wormholes() > 0:
                            possible_quadrants.append(sector)
                

                if possible_quadrants:
                    # Randomly choose a new quadrant with a wormhole
                    new_quadrant = random.choice(possible_quadrants)
                    new_wormhole = random.choice(new_quadrant.wormholes)

                    # Teleport the player to a position adjacent to the new wormhole
                    self.grid_x = max(0, min(new_wormhole.grid_x + random.choice([-1, 1]), GRID_SIZE - 1))
                    self.grid_y = max(0, min(new_wormhole.grid_y + random.choice([-1, 1]), GRID_SIZE - 1))
                    
                    self.quadrant_x = new_quadrant.quadrant_x
                    self.quadrant_y = new_quadrant.quadrant_y
                    self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y, wormhole=True)
                    print(f"Player teleported to Quadrant ({new_quadrant.quadrant_x}, {new_quadrant.quadrant_y}) at ({self.grid_x}, {self.grid_y}).")
                    # log_event(f"Player teleported to Quadrant ({new_quadrant.quadrant_x+1}, {new_quadrant.quadrant_y+1}) at ({self.grid_x}, {self.grid_y}).", PURPLE)
                    EXPLOSION_CHANNEL.play(PORTAL)
                    self.turn = 0
                    # break
                    self.update_position()
                    return True
                else:
                    self.grid_x = max(0, min(new_x + random.choice([-1, 1]), GRID_SIZE - 1))
                    self.grid_y = max(0, min(new_y + random.choice([-1, 1]), GRID_SIZE - 1))
                    print("No other wormhole found in the galaxy!")
                    EXPLOSION_CHANNEL.play(PORTAL)
                    return False

    def move(self, dx, dy):
        """Move the player in the grid, ensuring it stays within bounds and handles quadrant transitions."""
        # Handle docking/orbiting states
        if self.docked:
            self.toggle_dock((self.grid_x, self.grid_y))
            dx, dy = 0, 0
        if self.inOrbit:
            self.toggle_orbit((self.grid_x, self.grid_y))
            dx, dy = 0, 0

        # Calculate tentative new position
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        # Adjust energy and stardate based on movement
        self.energy -= abs(dx) + abs(dy)
        self.stardate += 0.1 * 0.95  # Small stardate increment per move

        # Resting action (no movement)
        if dx == 0 and dy == 0:
            print("Resting for Repairs...")
            self.energy += 1
            self.hull += 1

        # Rotate or flip sprite based on movement direction
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

        # Check if movement stays within the current quadrant
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # Block movement if there's an obstacle (star, base, etc.)
            if self.current_quadrant.is_star_at(new_x, new_y):
                print("Movement blocked by a star!")
                log_event("Movement blocked by a star!")
                return
            if self.current_quadrant.is_base_at(new_x, new_y):
                print("Movement blocked by a base!")
                log_event("Movement blocked by a base!")
                return
            if self.current_quadrant.is_enemy_at(new_x, new_y):
                print("Movement blocked by an enemy!")
                log_event("Movement blocked by an enemy!")
                return
            if self.current_quadrant.is_planet_at(new_x, new_y):
                print("Movement blocked by a planet!")
                log_event("Movement blocked by a planet!")
                return
            if self.check_if_entered_hole(new_x, new_y):  # Check for wormholes
                return

            # No obstacles, move within the quadrant
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_position()
        else:
            # Handle quadrant transition
            quadrant_shift_x, quadrant_shift_y = 0, 0

            # Determine new quadrant and grid coordinates
            if new_x < 0:  # Moving left out of bounds
                quadrant_shift_x = -1
                new_x += GRID_SIZE
            elif new_x >= GRID_SIZE:  # Moving right out of bounds
                quadrant_shift_x = 1
                new_x -= GRID_SIZE

            if new_y < 0:  # Moving up out of bounds
                quadrant_shift_y = -1
                new_y += GRID_SIZE
            elif new_y >= GRID_SIZE:  # Moving down out of bounds
                quadrant_shift_y = 1
                new_y -= GRID_SIZE

            # Calculate new quadrant coordinates
            new_quadrant_x = self.quadrant_x + quadrant_shift_x
            new_quadrant_y = self.quadrant_y + quadrant_shift_y

            # Check if new quadrant is valid (within galaxy bounds)
            if 0 <= new_quadrant_x < QUADRANT_SIZE and 0 <= new_quadrant_y < QUADRANT_SIZE:
                self.quadrant_x = new_quadrant_x
                self.quadrant_y = new_quadrant_y
                self.grid_x = new_x
                self.grid_y = new_y
                self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)

                # Calculate warp cost
                warp_factor = max(abs(quadrant_shift_x), abs(quadrant_shift_y))
                energy_cost = warp_factor * WARP_ENERGY_PER
                if self.shields_on:
                    energy_cost *= 2
                self.energy -= energy_cost

                # Play warp sound
                EXPLOSION_CHANNEL.play(WARP_SOUND)
                self.turn = 0

                print(f"Warping to sector ({self.quadrant_x}, {self.quadrant_y}) at Warp {warp_factor}.")
            else:
                # Out of galaxy bounds, restrict movement
                self.grid_x = max(0, min(self.grid_x, GRID_SIZE - 1))
                self.grid_y = max(0, min(self.grid_y, GRID_SIZE - 1))
                print("Cannot warp beyond galaxy boundaries!")

            # Update position after quadrant transition
            self.update_position()


    # def move(self, dx, dy):
    #     """Move the player in the grid, ensuring it stays within bounds and handles quadrant transitions."""
    #     # Check if the player will move out of the current sector (grid bounds)

    #     # ALARM_CHANNEL.play(NEXT_LINE)

    #     if player.docked : 
    #         player.toggle_dock((self.grid_x,self.grid_y))
    #         dx = 0
    #         dy = 0

    #     if player.inOrbit:
    #         player.toggle_orbit((self.grid_x,self.grid_y))
    #         dx = 0
    #         dy = 0

    #     new_x = self.grid_x + dx
    #     new_y = self.grid_y + dy


    #     self.energy -= abs(dx)
    #     self.energy -= abs(dy)
    #     self.stardate += (.1 * 0.95)

    #     if dx == 0 and dy == 0:
    #         print("Resting for Repairs...")
    #         self.energy += 1
    #         self.hull += 1


    #     # Update last_move_direction and rotate/flip the sprite (same as before)
    #     if dx == -1:
    #         self.last_move_direction = "left"
    #         self.image = pygame.transform.rotate(self.orig_image, 90)
    #     elif dx == 1:
    #         self.last_move_direction = "right"
    #         self.image = pygame.transform.rotate(self.orig_image, -90)
    #     elif dy == -1:
    #         self.last_move_direction = "up"
    #         self.image = self.orig_image
    #     elif dy == 1:
    #         self.last_move_direction = "down"
    #         self.image = pygame.transform.flip(self.orig_image, False, True)


    #     # If within bounds, check if the new position is blocked by a star
    #     if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
    #         # Check if the new position has a star (blocking movement)
    #         if self.current_quadrant.is_star_at(new_x, new_y):
    #             print("Movement blocked by a star!")
    #             log_event("Movement blocked by a star!")
    #             return  # Don't move if there's a star in the way

    #         if self.current_quadrant.is_base_at(new_x, new_y):
    #             print("Movement blocked by a base!")
    #             log_event("Movement blocked by a base!")
    #             return  # Don't move if there's a star in the way

    #         if self.current_quadrant.is_enemy_at(new_x, new_y):
    #             print("Movement blocked by an enemy!")
    #             log_event("Movement blocked by an enemy!")
    #             return  # Don't move if there's a star in the way


    #         if self.current_quadrant.is_planet_at(new_x, new_y):
    #             print("Movement blocked by an planet!")
    #             log_event("Movement blocked by an planet!")
    #             return  # Don't move if there's a star in the way

    #         # Check if the player enters a wormhole
    #         if self.check_if_entered_hole(new_x, new_y):
    #             return

    #         # Update position if no star is blocking
    #         self.grid_x = new_x
    #         self.grid_y = new_y
    #         self.update_position()
    #     else:


    #         # Handle moving to the next quadrant if out of bounds 
    #         if dx == 1:  # Moving right
    #             if self.quadrant_x < QUADRANT_SIZE - 1:
    #                 self.quadrant_x += 1
    #                 self.grid_x = 0
    #                 self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
    #                 warp_factor = 1
    #                 print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")

    #                 if self.shields_on:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)*2
    #                 else:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)

    #                 EXPLOSION_CHANNEL.play(WARP_SOUND)
    #                 self.turn = 0

    #         elif dx == -1:  # Moving left
    #             if self.quadrant_x > 0:
    #                 self.quadrant_x -= 1
    #                 self.grid_x = GRID_SIZE - 1
    #                 self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
    #                 warp_factor = 1
    #                 print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
    #                 if self.shields_on:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)*2
    #                 else:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)
    #                 EXPLOSION_CHANNEL.play(WARP_SOUND)
    #                 self.turn = 0

    #         elif dy == 1:  # Moving down
    #             if self.quadrant_y < QUADRANT_SIZE - 1:
    #                 self.quadrant_y += 1
    #                 self.grid_y = 0
    #                 self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
    #                 warp_factor = 1
    #                 print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
    #                 if self.shields_on:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)*2
    #                 else:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)
    #                 EXPLOSION_CHANNEL.play(WARP_SOUND)
    #                 self.turn = 0

    #         elif dy == -1:  # Moving up
    #             if self.quadrant_y > 0:
    #                 self.quadrant_y -= 1
    #                 self.grid_y = GRID_SIZE - 1
    #                 self.current_quadrant = self.enter_sector(self.quadrant_x, self.quadrant_y)
    #                 warp_factor = 1
    #                 print(f"Warping to sector ({self.quadrant_x,}, {self.quadrant_y}) at Warp {warp_factor}.")
    #                 if self.shields_on:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)*2
    #                 else:
    #                     self.energy -= (warp_factor * WARP_ENERGY_PER)
    #                 EXPLOSION_CHANNEL.play(WARP_SOUND)
    #                 self.turn = 0
            
    #         self.update_position()

    def successive_move(self):
        """Prompt the player for speed and direction, then move successively."""

        try:
            # Prompt for speed and direction
            direction = prompt_numeric_input("Enter direction: ", 0,9, compass=True)
            speed = prompt_numeric_input("Enter speed (number of steps): ",0,10)
            delay = 10
            

            # Translate direction input to dx, dy
            direction_map = {
                8: (0, -1),  # Up
                2: (0, 1),   # Down
                4: (-1, 0),  # Left
                6: (1, 0),   # Right
                7: (-1,-1),
                9: (+1,-1),
                1: (-1, 1),
                3: (1,1)
            }

            if direction not in direction_map:
                print("Invalid direction. Use 8=N, 2=S, 4=W, 6=E.")
                return

            dx, dy = direction_map[direction]

            # Perform successive movement
            for _ in range(speed):
                delay = 0
                # Call the existing move function for each step
                self.move(dx, dy)
                print(f"Moved to ({self.grid_x}, {self.grid_y}).")
                if self.energy <= 0:
                    print("Energy depleted! Stopping movement.")
                    break

                while delay < 10:
                    # Add delay between each move
                    delay += 1
                    SCREEN.fill(BLACK)
                    draw_all_to_screen()
                    pygame.display.flip()
                    clock.tick(FPS)

        except ValueError:
            print("Invalid input. Please enter integers for speed and direction.")



        

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
    def __init__(self, name, owner, origin_x, origin_y, rise, run):
        super().__init__()

        self.name = "Torpedo " + str(name)
        self.owner = owner

        if self.owner != player:
            self.name =  str(name) + " Torpedo "

        # Starting position
        self.grid_x = origin_x
        self.grid_y = origin_y

        # Direction specified by rise/run
        self.rise = rise
        self.run = run

        self.size = 7

        self.speed = TORPEDO_SPEED
        if self.owner == player:
            self.damage = int(PLAYER_TORPEDO_DAMAGE * random.uniform(0.9, 1.1))  # ±10% random variance
        else:
            self.damage = int(TORPEDO_DAMAGE * random.uniform(0.9, 1.1))  # ±10% random variance
            self.size = 7

        # Calculate movement vector based on rise/run
        self.direction_vector = self.calculate_direction_vector()

        # Create the torpedo visual

        self.color = WHITE 
        if owner == player: 
            self.color_list = TORPEDO_COLOR_CYCLE
        else:               
            self.color_list = GREEN_COLOR_CYCLE

        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (2, 2), 2)
        self.rect = self.image.get_rect(
            center=(GRID_ORIGIN_X + self.grid_x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    GRID_ORIGIN_Y + self.grid_y * SQUARE_SIZE + SQUARE_SIZE // 2)
        )

        self.last_update = pygame.time.get_ticks()  # Track the last time the torpedo moved
        self.travel_delay = 50  # Milliseconds delay between moves

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


        # # Check for collisions
        # for entity in all_entities:
        #     if entity != self.owner and self.rect.colliderect(entity.rect):
        #         # Handle collision
        #         self.handle_collision(entity)
        #         return  # Destroy the torpedo after a single collision

        target_list = []
        target_list.extend(player.current_quadrant.enemies)
        target_list.append(player)

        for target in target_list:
            # print('Target:' + target.name)
            if rounded_x == target.grid_x and rounded_y == target.grid_y:
                if target != self.owner: #and self.rect.colliderect(enemy.rect):
                    if target not in self.near_targets:
                        self.near_targets.append(target)

                        if random.random() > self.miss_chance:

                            print(f"{self.name} * Hit Target {target.name} at ({target.grid_x}, {target.grid_y})! *")
                            log_event(f"{self.name} ** HIT! {target.name} - {self.damage } DAMAGE", RED)
                            return target

                        else:
                            print(f"{self.name} * Missed Target {target.name} at ({target.grid_x}, {target.grid_y})! * @ {self.miss_chance}")
                            log_event(f"{self.name}  -- MISS !", WHITE)
        return None

    def update(self):
        """Update the torpedo's movement and check for collisions."""

        self.color = random.choice(self.color_list)

        now = pygame.time.get_ticks()
        if now - self.last_update < self.travel_delay:
            return  # Not enough time has passed yet

        self.last_update = now  # Update the last move time

        self.move()

        # Check if the torpedo is out of bounds
        if self.out_of_bounds():
            print(f"{self.name} exited the quadrant.")
            log_event(f"{self.name} left the quadrant.", WHITE)
            projectile_group.remove(self)
            self.kill()
            return

        # Check collision with stars
        rounded_x = round(self.grid_x)
        rounded_y = round(self.grid_y)

        if player.current_quadrant.is_star_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a star @ {rounded_x}, {rounded_y}.")
            log_event(f"{self.name} collided with a star @ {rounded_x+1}, {rounded_y+1}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        if player.current_quadrant.is_base_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a base @ {rounded_x}, {rounded_y}.")
            log_event(f"{self.name} collided with a base @ {rounded_x+1}, {rounded_y+1}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        if player.current_quadrant.is_planet_at(rounded_x, rounded_y):
            print(f"{self.name} collided with a planet @ {rounded_x}, {rounded_y}.")
            log_event(f"{self.name} collided with a planet @ {rounded_x+1}, {rounded_y+1}.")
            self.explode(self.grid_x, self.grid_y, max_size=SQUARE_SIZE //3 , start_size=1, growth_rate=2)
            return

        
        

        # Check for collisions with enemies    
        hit_enemy = self.check_collision(player.current_quadrant.enemies)
        if hit_enemy:
            self.handle_enemy_hit(hit_enemy)

        self.miss_chance += MISS_CHANCE_INCREASE_PER

    def explode(self, x, y, max_size, start_size, growth_rate, explosion_sound=MEDIUM_EXPLOSION):
        """Handle explosion visuals and sound."""
        explosion_x = GRID_ORIGIN_X + x * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion_y = GRID_ORIGIN_Y + y * SQUARE_SIZE + SQUARE_SIZE // 2
        explosion = Explosion((explosion_x, explosion_y), max_size, start_size, growth_rate)
        projectile_group.add(explosion)
        EXPLOSION_CHANNEL.play(explosion_sound)
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
            enemy.shield_energy = 0
            enemy.hull -= remaining_damage
            log_event(f"     {enemy.name} :: SHIELDS DOWN ::", BLUE)
        else:
            enemy.shields -= self.damage
            enemy.shield_energy -= self.damage

        
        print(f"     {enemy.name} Shields: {shields_before} -> {enemy.shields}")
        print(f"     {enemy.name} Hull: {hull_before} -> {enemy.hull}")
        EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)

        if enemy.hull <= 0:
            print(f"     {enemy.name} Destroyed!")
            log_event(f"     {enemy.name} :: !! DESTROYED !! ::)", RED)
            
            # player.current_quadrant.enemies.remove(enemy)
            self.explode(enemy.grid_x, enemy.grid_y, max_size=SQUARE_SIZE, start_size=5, growth_rate=2,explosion_sound=SHIP_DEATH_SOUND)
            # EXPLOSION_CHANNEL.play(SHIP_DEATH_SOUND)

            if enemy != player:
                for crewman in player.soulsOnBoard:
                    crewman.xp += random.randint(0,5)
                enemy.die()


            # Check if all enemies are destroyed, and play victory sound
            if len(player.current_quadrant.enemies) == 0:
                play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 1)

                # Re-enter the sector to ensure state consistency
                player.enter_sector(player.quadrant_x, player.quadrant_y)

        else: # ENEMY SURVIVED
            ...
            # EXPLOSION_CHANNEL.play(MEDIUM_EXPLOSION)

    def draw(self, screen):
        """Draw the torpedo."""
        pygame.draw.circle(screen, self.color, self.rect.center, self.size)



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

class Star(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, quadrant_x, quadrant_y):
        super().__init__()
        self.name = "Star"
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.quadrant_x = quadrant_x
        self.quadrant_y = quadrant_y

        self.size = random.choice([16,22,26])
        # Dwarf Star
        # Giant Star
        # Supergiant Star

        self.star_color_types = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "WHITE"]
        self.colorA = random.choice([MIDDLE_RED, ORANGE, MIDDLE_YELLOW, MIDDLE_GREEN, DARK_BLUE, OFF_WHITE])
        self.colorB = brighten_color(self.colorA, 50)
        self.colorC = brighten_color(self.colorA, 100)
        self.colorD = (*self.colorC[:3], 50) #(*self.colorC[:3], 50)   # Red with 50% transparency

class Base(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()

        self.name = "STARBASE"
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.shields = 0
        self.hull = 0
        self.cloak_enabled = False

class Wormhole(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()

        self.name = "WORMHOLE"
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.orig_image = WORMHOLE_IMAGE
        self.orig_image = pygame.transform.scale(self.orig_image, (SQUARE_SIZE+10, SQUARE_SIZE+10))
        self.image = self.orig_image

        # self.rect = self.image.get_rect()  # Set the rect for positioning
        # self.rect.topleft = (grid_x * TILE_SIZE, grid_y * TILE_SIZE)  # Position on the grid


        self.shields = 0
        self.hull = 0
        self.hasCloakingDevice = False
        self.cloak_enabled = False 

        self.rotation_angle = 0  # Current rotation angle
        self.last_update_time = pygame.time.get_ticks()  # Time tracker for rotation

    def update(self):
        """Rotate the wormhole image by 90 degrees every second."""
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if 1 second (1000 milliseconds) has passed
        if current_time - self.last_update_time >= 500:
            # Update the last update time
            self.last_update_time = current_time

            # Increment the rotation angle by 90 degrees
            self.rotation_angle = (self.rotation_angle - 45) % 360

            # Rotate the original image and update the current image
            self.image = pygame.transform.rotate(self.orig_image, self.rotation_angle)

            # # Update the rect to keep it centered
            # self.rect = self.image.get_rect(center=self.rect.center)


### ENEMY CLASS ####
class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, name="INTRUDER", image=INTRUDER_SHIP):
        super().__init__()

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.orig_image = image
        self.image = self.orig_image

        # self.orig_image = pygame.transform.scale(self.orig_image, (SQUARE_SIZE, SQUARE_SIZE))
        self.image = self.orig_image

        self.rect = self.image.get_rect()
        self.last_move_direction = random.choice(["up", "down", "left", "right"])
        self.update_position()

        self.name = name

        self.torpedo_qty = 10
        self.torpedo_damage = TORPEDO_DAMAGE

        self.hasCloakingDevice = False
        self.cloak_enabled = False

        if self.name == "DRONE":
            self.full_energy = random.randint(500, 1000)
            self.full_shields = random.randint(50, 75)
            self.full_hull = random.randint(50, 75)
            self.min_phasor = 50
            self.max_phasor = 100
            self.speed = 2
            self.torpedo_qty = 0
            self.torpedo_damage = 0

        if self.name == "INTRUDER":
            self.full_energy = random.randint(600, 1200)
            self.full_shields = random.randint(50, 100)
            self.full_hull = random.randint(50, 100)
            self.min_phasor = 100
            self.max_phasor = 200
            self.speed = 1
            self.torpedo_damage = TORPEDO_DAMAGE/4

        if self.name == "GUARDIAN":
            self.full_energy = random.randint(600, 1200)
            self.full_shields = random.randint(50, 100)
            self.full_hull = random.randint(50, 100)
            self.min_phasor = 100
            self.max_phasor = 200
            self.speed = 3
            self.torpedo_damage = TORPEDO_DAMAGE/4

        elif self.name == "ELUDER":
            self.full_energy = random.randint(600, 1200)
            self.full_shields = random.randint(100, 200)
            self.full_hull = random.randint(100, 200)
            self.min_phasor = 150
            self.max_phasor = 250
            self.speed = 3
            self.torpedo_damage = TORPEDO_DAMAGE/4



        elif self.name == "AVENGER":
            self.full_energy = random.randint(800 , 1600)
            self.full_shields = random.randint(75, 100)
            self.full_hull = random.randint(150, 200)
            self.min_phasor = 200
            self.max_phasor = 450
            self.speed = 1
            self.torpedo_damage = TORPEDO_DAMAGE/2
            self.hasCloakingDevice = True

        elif self.name == "PODSHIP":
            self.full_energy = random.randint(800 , 1600)
            self.full_shields = random.randint(75, 100)
            self.full_hull = random.randint(150, 200)
            self.min_phasor = 200
            self.max_phasor = 450
            self.speed = 1
            self.torpedo_damage = TORPEDO_DAMAGE * 0.75

        elif self.name == "DREADNAUGHT":
            self.full_energy = random.randint(1200 , 2000)
            self.full_shields = random.randint(500, 800)
            self.full_hull = random.randint(500, 800)
            self.min_phasor = 300
            self.max_phasor = 600
            self.speed = 2
            self.torpedo_damage = TORPEDO_DAMAGE


        self.energy = self.full_energy
        self.shields = self.full_shields
        self.hull = self.full_hull



        self.shield_energy = self.energy

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

    def enemy_fire_torpedo(self, player, projectile_group):
        """
        Enemy fires a torpedo at the player's current position.

        :param player: The player object.
        :param projectile_group: The sprite group to manage projectiles.
        """
        # Ensure the enemy has enough torpedoes and energy
        if self.torpedo_qty > 0 and self.energy >= TORPEDO_ENERGY_USAGE:
            # Calculate direction (rise, run) based on the player's position
            rise = player.grid_y - self.grid_y
            run = player.grid_x - self.grid_x

            # Create the torpedo
            torpedo = Torpedo(self.name, self, self.grid_x, self.grid_y, rise, run)
            projectile_group.add(torpedo)

            # Deduct energy and torpedo stock
            self.energy -= TORPEDO_ENERGY_USAGE
            self.torpedo_qty -= 1

            # Print feedback and play sound
            print(f"{self.name} fires a torpedo at the player! Direction: Rise: {rise}, Run: {run}")
            log_event(f"** ! {self.name} FIRES A TORPEDO ! **", RED)
            WEAPON_CHANNEL.play(ENEMY_TORPEDO)

            # Check if the enemy's torpedoes are depleted
            if self.torpedo_qty <= 0:
                print(f"{self.name} has no torpedoes left!")
        else:
            if self.torpedo_qty <= 0:
                print(f"{self.name} has no torpedoes left!")
            if self.energy < TORPEDO_ENERGY_USAGE:
                print(f"{self.name} has insufficient energy to fire a torpedo!")


    def enemy_fire_phaser(self, player):
        """Enemy fires its phaser at the player."""

        # Base phaser power (e.g., 300)
        phaser_power = random.randint(self.min_phasor, self.max_phasor)

        if self.energy >= phaser_power:  # Ensure the enemy has enough energy
            # Calculate the distance to the player
            distance = abs(self.grid_x - player.grid_x) + abs(self.grid_y - player.grid_y)

            
            # Adjust damage based on distance (similar to player's phaser)
            if distance == 0:
                damage = int(phaser_power * 0.9)
            elif distance <= 5:
                damage = int(phaser_power * 0.6)
            elif distance <= 10:
                damage = int(phaser_power * 0.35)
            else:
                damage = 0  # No effect beyond 10 sectors

            print(f"{self.name} fires phaser at the player! Distance: {distance}, Damage: {damage}")
            log_event(f"** ! {self.name} FIRES PHASERS ! ** Damage: {damage}", RED)

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


            if player.crewQty <= 0:
                print("The player's ship has been destroyed!")


    def trigger_update(self, players_turn):
        """Set the trigger time to start the update process."""
        print("trigger update")
        self.trigger_update_time = pygame.time.get_ticks()
        if players_turn and player.turn != 0:
            players_turn = False

    def successive_move(self):

        move_speed = random.randint(1,self.speed)
        self.oldPOS = (self.grid_x, self.grid_y)

        # Perform successive movement
        for _ in range(move_speed):
            delay = 0
            # Call the existing move function for each step
            self.move()
            
            if self.energy <= 0:
                print("Energy depleted! Stopping movement.")
                break

            while delay < 20:
                # Add delay between each move
                delay += 1
                SCREEN.fill(BLACK)
                draw_all_to_screen()
                pygame.display.flip()
                clock.tick(FPS)


    def move(self):



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
            print(f"Enemy Moved to ({new_pos}).")
            
            
            if self.last_move_direction:
                self.update_position()

    def toggle_cloak(self):

        if self.hasCloakingDevice:
            if not self.cloak_enabled:
                self.cloak_enabled = True 
                EXPLOSION_CHANNEL.play(CLOAK_SOUND)
                log_event(f"* {self.name} ACTIVATED CLOAK *",PURPLE)

            elif self.cloak_enabled:
                self.cloak_enabled = False 
                EXPLOSION_CHANNEL.play(DECLOAK_SOUND)
                log_event(f"* {self.name} DECLOAKED *",PURPLE)



    def update(self, current_sector, players_turn):
        """Update enemy's position with a chance to move to an adjacent open sector square within boundaries."""
        # print(players_turn)
        """Update enemy's position a short time after being triggered."""
        if self.trigger_update_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.trigger_update_time >= self.response_delay:
                if len(projectile_group) == 0:
                    self.trigger_update_time = None  # Reset trigger

                    if random.random() < .50:  # 50% chance to move
                        self.successive_move()

                    if self.hasCloakingDevice:
                        if random.random() < .50 :
                            self.toggle_cloak()

                    if (random.random() < .75) and not self.cloak_enabled:
                        if (random.random() < .50) or (self.torpedo_qty <= 0):
                            self.enemy_fire_phaser(player)
                        else:
                            self.enemy_fire_torpedo(player, projectile_group)

                    if not players_turn:
                        players_turn = True



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

        if self.oldPOS == position:
            print("old position")
            return False

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

        # Check if the position contains a wormhole
        if player.current_quadrant.is_wormhole_at(x, y):
            return False

        # Otherwise, the position is valid
        return True

    def get_adjacent_positions(self):
        """Return a list of positions within the enemy's speed distance, considering sector boundaries."""
        adjacent_positions = []

        # this_speed = self.speed 
        this_speed = 1

        # Loop through a range of positions based on the enemy's speed
        for dx in range(-this_speed, this_speed+1):  # dx ranges from -speed to +speed
            for dy in range(-this_speed, this_speed+1):  # dy ranges from -speed to +speed
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


        random_planet = random.choice(ALL_PLANET_IMAGES)

        self.image = pygame.image.load(random_planet["file"]).convert_alpha()
        planet_image_size_factor = self.size / 10
        planet_image_size_factor = max(0.5, min(0.80, planet_image_size_factor)) 
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE*planet_image_size_factor, SQUARE_SIZE*planet_image_size_factor))  # Scale to grid square size 

        self.shields = 0 
        self.hull = 0 

        self.away_team_on_planet = False
        self.away_team = pygame.sprite.Group() # List to store crew members on the planet
        self.landers = 0
        self.cloak_enabled = False

        self.mined_out = False

        print("planet init complete")


    def generate_name(self, sector_planets, sector_planet_index):
        """
        Generate a name for the planet by appending a letter (A, B, C, etc.) 
        based on its index in the sector.
        """
        print("generate name")
        base_name = get_quadrant_name(self.quadrant_x, self.quadrant_y)
        if len(sector_planets) > 1:
            suffix = chr(97 + sector_planet_index)  # Convert index to ASCII (A=65, B=66, etc.)
            print(f"generated name {base_name} - {suffix}")
            return f"{base_name} - {suffix}"

        else:
            print(f"generated name {base_name}")
            return f"{base_name}"

    def mine_dilithium(self):
        mined_crystals = 0

        if not self.mined_out:
            mined_crystals = random.randint(0,100)
            print(f"The away team mined {mined_crystals} units of dilithium crystals!")
            log_event(f"The away team mined {mined_crystals} units of dilithium crystals!", PURPLE)

            if random.random() > 0.50: 
                self.mined_out = True
                print(f"The planet is now completely mined.")
                log_event(f"The planet is now completely mined.", PURPLE)
        else:
            print(f"The planet is completely mined.")
            log_event(f"The planet is completely mined.", PURPLE)


        # add crystals to the players cargohold
        if (player.cargo + mined_crystals) > player.cargo_max:
            print("No more cargo space")
            log_event(f"- CARGO BAY FULL -")

            allcargo = player.cargo + mined_crystals
            lost = allcargo - player.cargo_max
            mined_crystals = mined_crystals - lost
            player.cargo = player.cargo_max

        else:
            player.cargo += mined_crystals

        return mined_crystals




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
        self.stars = []  # List of star positions (tuples)
        self.bases = []  # List of base objects
        self.enemies = []  # List of enemy objects
        self.planets = []  # List of planet objects
        self.wormholes = [] # list of wormhole objects

        self.visited = False
        self.last_star_count = 0
        self.last_base_count = 0
        self.last_enemy_count = 0

    def is_position_occupied(self, x, y):
        """Check if a position is occupied by any object in the sector."""
        # Check for stars
        if any(star.grid_x == x and star.grid_y == y for star in self.stars):
            return True
        # Check for planets
        if any(planet.grid_x == x and planet.grid_y == y for planet in self.planets):
            return True
        # Check for bases
        if any(base.grid_x == x and base.grid_y == y for base in self.bases):
            return True
        # Check for enemies
        if any(enemy.grid_x == x and enemy.grid_y == y for enemy in self.enemies):
            return True

        # Check for wormholes
        if any(wormhole.grid_x == x and wormhole.grid_y == y for wormhole in self.wormholes):
            return True

        return False

    def generate(self, player, player_x, player_y):
        """Generate stars, planets, bases, enemies, and potentially wormholes for the sector."""
        # Create a weighted list for the number of stars
        weighted_numbers = [1, 7, 8, 9] + [2, 3, 4, 5, 6] * 4
        num_stars = random.choice(weighted_numbers)

        # Randomly place stars or planets
        max_attempts = 100  # Prevent infinite loops

        while len(self.stars) + len(self.planets) < num_stars:
            for _ in range(max_attempts):
                obj_x = random.randint(0, GRID_SIZE - 1)
                obj_y = random.randint(0, GRID_SIZE - 1)
                if (obj_x, obj_y) != (player_x, player_y) and not self.is_position_occupied(obj_x, obj_y):
                    if (random.random() < 0.2) and (len(self.planets) < MAX_NUM_OF_PLANETS_PER):  # 20% chance to create a planet
                        new_planet = Planet(obj_x, obj_y, self.quadrant_x, self.quadrant_y)
                        self.planets.append(new_planet)
                    else:  # Otherwise, add a star
                        new_star = Star(obj_x, obj_y, self.quadrant_x, self.quadrant_y)
                        self.stars.append(new_star)
                    break  # Successfully placed an object, move to the next
            else:
                print("Max attempts reached while placing stars/planets.")
                break

        # Ensure there's at least one star
        if len(self.stars) == 0:
            for _ in range(max_attempts):
                star_x = random.randint(0, GRID_SIZE - 1)
                star_y = random.randint(0, GRID_SIZE - 1)
                if (star_x, star_y) != (player_x, player_y) and not self.is_position_occupied(star_x, star_y):
                    new_star = Star(star_x, star_y, self.quadrant_x, self.quadrant_y)
                    self.stars.append(new_star)
                    break
            else:
                print("Max attempts reached while placing the mandatory star.")

        # Assign names to planets
        for i, planet in enumerate(self.planets):
            planet.name = planet.generate_name(self.planets, i)

        # Place bases
        starbase_count_ttl = sum(sector.count_bases() for sector in player.all_sectors)
        if starbase_count_ttl < MAX_NUM_OF_BASES and random.random() < 0.1:  # 10% chance for a base
            for _ in range(max_attempts):
                base_x = random.randint(0, GRID_SIZE - 1)
                base_y = random.randint(0, GRID_SIZE - 1)
                if (base_x, base_y) != (player_x, player_y) and not self.is_position_occupied(base_x, base_y):
                    new_base = Base(base_x, base_y)
                    self.bases.append(new_base)
                    break
            else:
                print("Max attempts reached while placing bases.")

        # Place enemies
        if random.random() < 0.25:  # 25% chance of enemies
            # Randomly select an enemy
            enemy_name, enemy_image = random.choice(ENEMY_SHIP_LIST)
            num_of_enemies = random.randint(1, 4)
            for _ in range(num_of_enemies):
                for _ in range(max_attempts):
                    enemy_x = random.randint(0, GRID_SIZE - 1)
                    enemy_y = random.randint(0, GRID_SIZE - 1)
                    if (enemy_x, enemy_y) != (player_x, player_y) and not self.is_position_occupied(enemy_x, enemy_y):
                        new_enemy = Enemy(enemy_x, enemy_y, enemy_name, enemy_image)
                        self.enemies.append(new_enemy)
                        break
                else:
                    print("Max attempts reached while placing enemies.")

        # Place wormholes
        wormhole_count_ttl = sum(sector.count_wormholes() for sector in player.all_sectors)  # Total wormholes across all sectors
        if wormhole_count_ttl < 4 and random.random() < 0.05:  # 5% chance to create a wormhole
            for _ in range(max_attempts):
                wormhole_x = random.randint(0, GRID_SIZE - 1)
                wormhole_y = random.randint(0, GRID_SIZE - 1)
                if (wormhole_x, wormhole_y) != (player_x, player_y) and not self.is_position_occupied(wormhole_x, wormhole_y):
                    new_wormhole = Wormhole(wormhole_x, wormhole_y)
                    self.wormholes.append(new_wormhole)
                    break
            else:
                print("Max attempts reached while placing wormholes.")




    
    def count_bases(self):
        """Count the number of bases in the sector."""
        return len(self.bases)

    def count_enemies(self):
        """Count the number of enemy in the sector."""
        return len(self.enemies)

    def count_enemies_not_cloaked(self):
        """Count the number of enemy in the sector."""
        count = 0 
        for enemy in self.enemies:
            if not enemy.cloak_enabled:
                count += 1

        return count


    def count_stars(self):
        """Count the number of stars in the sector."""
        return len(self.stars)

    def count_wormholes(self):
        """Count the number of stars in the wormholes."""
        return len(self.wormholes)
    
    def is_base_at(self, x, y):
        """Check if there is a base at the given coordinates."""
        for base in self.bases:
            if base.grid_x == x and base.grid_y == y:
                return base
        return False

    def is_star_at(self, x, y):
        for star in self.stars:
            if star.grid_x == x and star.grid_y == y:
                return star
        return False

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

    def is_wormhole_at(self, x, y):

        for wormhole in self.wormholes:  # Assuming `self.planets` is a list of Planet objects
            if wormhole.grid_x == x and wormhole.grid_y == y:
                return wormhole  # Return the Planet object
        return None  # Return None if no planet is found


    def is_empty(self, x, y):
        """Check if the sector at (x, y) is empty (no enemy)."""
        for enemy in self.enemies:
            if enemy.grid_x == x and enemy.grid_y == y:
                return False  # There's already an enemy in this sector
        return True  # The sector is empty


## DEFINE CREWMAN ## =========================================================================================
class Crewman(pygame.sprite.Sprite):
    count = 0
    def __init__(self,species,rank,department,stardate):
        Crewman.count += 1
        super(Crewman, self).__init__()

        self.species = species

        self.rank = rank
        self.serialNumber = Crewman.count
        self.enrollmentDate = stardate #calender.show()
        self.lastDayOfShoreLeave = stardate #calender.day
        self.yesterday = stardate #calender.day
        self.homeworld = "None"
        
        self.strength = random.randint(20,40)
        self.health  = random.randint(25,40)
        self.stamina = random.randint(40,70)
        self.bravery = random.randint(10,60)
        self.reactions = random.randint(30,60) 
        self.accuracy = random.randint(40,70) 
        self.psiStrength = random.randint(0,100)
        self.psiSkill = 00 

        self.command        = random.randint(10,60) 
        self.piloting       = random.randint(10,60) 
        self.communications = random.randint(10,60) 
        self.engineering    = random.randint(10,60) 
        self.tactical       = random.randint(10,60) 
        self.security       = random.randint(10,60) 
        self.physicalScience  = random.randint(10,60)
        self.bioScience       = random.randint(10,60)  
        self.medical        = random.randint(10,60)  

        


        self.department = department
        self.shirtColor = GOLD

        if self.department in ["Command", "Pilot", "Communications"]:
            self.shirtColor = RED
            if self.department == "Command":
                self.command += random.randint(20,40) 
            elif self.department == "Pilot":
                self.piloting += random.randint(20,40) 
            elif self.department == "Communications":
                self.communications += random.randint(20,40) 


        elif self.department in ["Engineering","Tactical","Security","Intelligence"]:
            self.shirtColor = GOLD
            if self.department == "Engineering":
                self.engineering += random.randint(20,40)
            elif self.department == "Tactical":
                self.tactical += random.randint(20,40) 
            elif self.department == "Security":
                self.security += random.randint(20,40)
            elif self.department == "Intelligence":
                self.command += random.randint(10,30)
                self.tactical += random.randint(10,30)
                self.security += random.randint(10,30)
                self.communications += random.randint(10,30)
                self.shirtColor = LIGHT_GREY 

        elif self.department in ["Medical"]:
            self.shirtColor = LIGHT_BLUE
            self.medical += random.randint(20,40) 

        elif self.department in ["Physical-Science"]:
            self.shirtColor = PURPLE
            self.physicalScience += random.randint(20,40)

        elif self.department in ["Bio-Science"]:
            self.shirtColor = GREEN
            self.bioScience += random.randint(20,40)  


        else: self.shirtColor = GOLD


        if self.species == "Android":


            self.name = random.choice(ANDROID_NAMES) + "-" + str('{0:03d}'.format(random.randint(000,999)))


            self.strength = round(self.strength/10)*10
            self.health = round(self.health/10)*10
            self.stamina = round(self.stamina/10)*10
            self.bravery = 00
            self.reactions = round(self.reactions/10)*10
            self.accuracy = round(self.accuracy/10)*10
            self.psiStrength = 00
            self.command = round(self.command/10)*10
            self.piloting = round(self.piloting/10)*10
            self.communications = round(self.communications/10)*10
            self.engineering = round(self.engineering/10)*10
            self.tactical = round(self.tactical/10)*10
            self.security = round(self.security/10)*10
            self.physicalScience = round(self.physicalScience/10)*10
            self.bioScience = round(self.bioScience/10)*10
            self.medical = round(self.medical/10)*10

        elif self.species == "Pkunk": #and (plot.pkunkDateA != None and not plot.pkunkMoveStarted):


            self.name = random.choice(PKUNK_NAMES) + "-" + random.choice(PKUNK_NAMES)
            self.homeworld = "Gamma Krueger I"


            self.strength = self.strength -10
            self.health = self.health -10
            self.stamina = self.stamina 
            self.bravery = self.bravery +10
            self.reactions = self.reactions +10
            self.accuracy = self.accuracy 
            self.psiStrength = random.randint(50,100)
            self.psiSkill = random.randint(40,100)
            self.command = self.command 
            self.piloting = self.piloting +10
            self.communications = self.communications +10
            self.engineering = self.engineering -10
            self.tactical = self.tactical 
            self.security = self.security -10
            self.physicalScience = self.physicalScience +20
            self.bioScience = self.bioScience
            self.medical = self.medical -10

        else:
            self.species = "Human"
            self.name = random.choice(CREWNAMELIST)
            
            if self.serialNumber <= MAX_CREW:
                chanceFromEarth = random.randint(0,100)
                if chanceFromEarth >= 70 and chanceFromEarth < 80:
                    self.homeworld = "Mars"
                elif chanceFromEarth >= 80 and chanceFromEarth < 90:
                    self.homeworld = "Ceres"
                elif chanceFromEarth >= 90:
                    self.homeworld = "Earth"
                else: self.homeworld = "Unzervalt"
            else: self.homeworld = "Earth"

        numofextraskills = random.randint(0,2)
        count = 0
        self.extraSkills = []
        while count < numofextraskills:
            count += 1
            self.extraSkills.append(random.choice(EXTRA_SKILL_LIST))
        

        self.xp      = 00 

        self.goodTraits = []
        numofextraTraits = random.randint(0,2)
        count = 0
        while count < numofextraTraits:
            count += 1
            ndTrait = random.choice(POSITIVE_CHARACTER_TRAITS)
            if not (ndTrait in self.goodTraits):
                self.goodTraits.append(ndTrait)

        self.badTraits = []
        if random.randint(0,100) > 60:
            self.badTraits.append(random.choice(NEGATIVE_CHARACTER_TRAITS))

    def getEnrollmentDate(self):
        return round(self.enrollmentDate,2)

    def getSerialNumber(self):
        return '{0:05d}'.format(self.serialNumber)

    def info(self):
        text = ""

        if self.species == "Android":
            text += self.name

        else:
            
            if self.rank in ["Crewman", "Able Crewman"]:
                ...
                # text += "  "


            if self.department == "Medical": #in ["Science" or "Medical"]:
                    text += "Dr. " + self.name

            elif self.rank not in ["Crewman", "Able Crewman"]:
                    text += self.rank + " " + self.name

            else:
                if self.department == "Intelligence": 
                    text += "Agent " + self.name
                else:
                    text += self.name

            ## SHOW THE CREWMANS RANK
            # if self.rank == "Able Crewman":
            #     text += " //"
            # elif self.rank == "Chief":
            #     text += " ///"
            # elif self.rank == "Ensign":
            #     text += " <*>"
            # elif self.rank == "2nd Lt.":
            #     text += " <*^>"
            # elif self.rank == "1st Lt.":
            #     text += " <**>"
            # elif self.rank == "Lt. Cmdr":
            #     text += " <**^>"
            # elif self.rank == "Commander":
            #     text += " <***>"
            # elif self.rank == "Captain":
            #     text += " <****>"

        return text

    def fullInfo(self):
        text = ""
        if self.species == "Android":
            text += self.name
        else:

            if self.rank == "Able Crewman":
                text += " // "
            elif self.rank == "Chief":
                text += " /// "
            elif self.rank == "Ensign":
                text += " <*> "
            elif self.rank == "2nd Lt.":
                text += " <*^> "
            elif self.rank == "1st Lt.":
                text += " <**> "
            elif self.rank == "Lt. Cmdr":
                text += " <**^> "
            elif self.rank == "Commander":
                text += " <***> "
            elif self.rank == "Captain":
                text += " <****> "


            if self.department == "Medical": #in ["Science" or "Medical"]:
                text += "Dr. " + self.name

            elif self.rank not in ["Crewman", "Able Crewman"]:
                    text += self.rank + " " + self.name

            else:
                if self.department == "Intelligence": 
                    text += "Agent " + self.name
                else:
                    text += self.rank + " " + self.name


        return text


    def getName(self):
        text = ""

        if self.department == "Medical": #in ["Science" or "Medical"]:
                text += "Dr. " + self.name

        elif self.rank not in ["Crewman", "Able Crewman"]:
                text += self.rank + " " + self.name

        else:
            text += self.name

        return text

    def update(self,player):
        ...

        if self.species == "Android": # NO XP FOR ROBOTS 
            self.xp = 0


        if player.stardate > self.lastDayOfShoreLeave+1:
            if player.stardate > self.yesterday:
                self.yesterday = player.stardate
                self.xp += .1

        # if player.orbitingSubPlanet != None:
        #     if type(player.orbitingSubPlanet) is Starbase:
        #         if player.orbitingSubPlanet.isAllied:
        #             self.lastDayOfShoreLeave = calender.day

        #             if self.xp >= 10 and self.rank == "Crewman": # become able
        #                 self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 30 and self.rank == "Able Crewman": # become chief
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "Chief":
        #                         count += 1
        #                 if count == 0:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 30 and self.rank == "Chief": # become lt.
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "2nd Lt.":
        #                         count += 1
        #                 if count <= 1:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 2)] # skip ensign rank when promoting chiefs

        #             elif self.xp >= 30 and self.rank == "Ensign": # promote if available 2nd lt posistion
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "2nd Lt." and crewmate.department != "Medical":
        #                         count += 1
        #                 if count <= 1:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 60 and self.rank == "2nd Lt.": # promote if available 1st lt posistion
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "1st Lt." and crewmate.department != "Medical":
        #                         count += 1
        #                 if count == 0:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 80 and self.rank == "1st Lt.": # promote if available 2nd lt posistion
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "Lt. Cmdr" and crewmate.department != "Medical":
        #                         count += 1
        #                 if count == 0:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 100 and self.rank == "Lt. Cmdr": # promote if available 2nd lt posistion
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "Commander" and crewmate.department != "Medical":
        #                         count += 1
        #                 if count == 0:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]

        #             elif self.xp >= 120 and self.rank == "Commander": # promote if available 2nd lt posistion
        #                 crew = player.soulsOnBoard.sprites()
        #                 count = 0
        #                 for crewmate in crew:
        #                     if crewmate.rank == "Captain" and crewmate.department != "Medical":
        #                         count += 1
        #                 if count == 0:
        #                     self.rank = RANK_LIST[(RANK_LIST.index(self.rank) + 1)]
             
        #             elif self.xp >= 365 and self.rank == "Captain": # promote if available 2nd lt posistion
        #                 ...

   

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
                this_star = player.current_quadrant.is_star_at(col, row)

                # pygame.draw.circle(SCREEN, this_star.colorD, rect.center, this_star.size + 10, 4)  # Yellow star
                

                pygame.draw.circle(SCREEN, this_star.colorA, rect.center, this_star.size)  # Yellow star
                pygame.draw.circle(SCREEN, this_star.colorB, rect.center, this_star.size - (this_star.size/10)*2)  # Yellow star
                pygame.draw.circle(SCREEN, this_star.colorC, rect.center, this_star.size - (this_star.size/10)*4)  # Yellow star
                
                # Now add a semi-transparent overlay that is wider and centered
                transparent_radius = this_star.size + (this_star.size/10)*5  # Make it slightly larger than the outermost circle
                transparent_diameter = transparent_radius * 2

                # Create a smaller surface for the transparent circle
                circle_surface = pygame.Surface((transparent_diameter, transparent_diameter), pygame.SRCALPHA)

                # Draw the semi-transparent circle onto the new surface
                semi_transparent_color = this_star.colorD  # RGB + Alpha (50% transparency)
                local_center = (transparent_radius, transparent_radius)  # Center within the surface
                pygame.draw.circle(circle_surface, semi_transparent_color, local_center, transparent_radius)

                # Blit the semi-transparent surface onto the main screen
                SCREEN.blit(circle_surface, (rect.centerx - transparent_radius, rect.centery - transparent_radius))

                # pygame.draw.rect(SCREEN, YELLOW, rect, 1)  # Yellow grid line
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # GREEN grid line

            # Check for planets
            elif player.current_quadrant.is_planet_at(col, row):  # Add planet drawing logic
                planet = player.current_quadrant.is_planet_at(col, row)
                planet_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                planet_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - planet.image.get_width()) // 2
                offset_y = (SQUARE_SIZE - planet.image.get_height()) // 2

                # Draw the planet's image
                SCREEN.blit(planet.image, (planet_screen_x + offset_x, planet_screen_y + offset_y))

                grid_color = DARK_GREEN
                if planet == player.orbiting_planet: grid_color = GREEN
                pygame.draw.rect(SCREEN, grid_color, rect, 1)  # Dark green grid line for planets

                

                # Draw the lander indicator (LANDER_IMAGE)
                if planet.landers > 0:
                    lander_x = planet_screen_x + 4
                    lander_y = planet_screen_y + SQUARE_SIZE - LANDER_IMAGE.get_height() - 4
                    SCREEN.blit(LANDER_IMAGE, (lander_x, lander_y))

                # Draw the away team indicator (CREWMAN_IMAGE)
                if planet.away_team_on_planet:
                    crewmember_x = planet_screen_x + SQUARE_SIZE - CREWMAN_IMAGE.get_width() - 4
                    crewmember_y = planet_screen_y + SQUARE_SIZE - CREWMAN_IMAGE.get_height() - 4
                    SCREEN.blit(CREWMAN_IMAGE, (crewmember_x, crewmember_y))




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
                grid_color = DARK_BLUE

                # Check docking range
                distance = abs(math.sqrt((player.grid_x - col) ** 2 + (player.grid_y - row) ** 2))
                if distance <= 1:
                    if player.current_quadrant.count_enemies() <= 0:
                        player.condition = "GREEN"
                        player.update_position()
                        player.inDockingRange = (col, row)

                        if player.docked:
                            player.condition = "BLUE"
                            grid_color = BLUE
                    else:
                        player.condition = "RED"

                pygame.draw.rect(SCREEN, grid_color, rect, 1)  # Blue grid line for bases


            # Check for wormholes
            elif player.current_quadrant.is_wormhole_at(col, row):
                this_hole = player.current_quadrant.is_wormhole_at(col, row)
                this_hole.update()
                base_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                base_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                offset_x = (SQUARE_SIZE - this_hole.image.get_width()) // 2
                offset_y = (SQUARE_SIZE - this_hole.image.get_height()) // 2


                SCREEN.blit(this_hole.image, (base_screen_x + offset_x, base_screen_y + offset_y))
                # pygame.draw.rect(SCREEN, BLUE, rect, 1)  # Blue grid line for bases

                # # Check docking range
                # distance = abs(math.sqrt((player.grid_x - col) ** 2 + (player.grid_y - row) ** 2))
                # if distance <= 1:
                #     if player.current_quadrant.count_enemies() <= 0:
                #         player.condition = "GREEN"
                #         player.update_position()
                #         player.inDockingRange = (col, row)

                #         if player.docked:
                #             player.condition = "BLUE"
                #     else:
                #         player.condition = "RED"


           # Check for enemies
            elif player.current_quadrant.is_enemy_at(col, row):
                this_enemy = player.current_quadrant.is_enemy_at(col, row)

                if not this_enemy.cloak_enabled:
                
                    # Calculate the top-left corner of the grid square
                    enemy_screen_x = GRID_ORIGIN_X + (col * SQUARE_SIZE)
                    enemy_screen_y = GRID_ORIGIN_Y + (row * SQUARE_SIZE)
                    
                    # Calculate the offset to center the enemy image within the grid square
                    offset_x = (SQUARE_SIZE - this_enemy.image.get_width()) // 2
                    offset_y = (SQUARE_SIZE - this_enemy.image.get_height()) // 2

                    # Draw the enemy image centered in the grid square
                    SCREEN.blit(this_enemy.image, (enemy_screen_x + offset_x, enemy_screen_y + offset_y))

                    # If the enemy has shields, draw a blue circle around it
                    if this_enemy.shields >= 1:
                        center_x = enemy_screen_x + (SQUARE_SIZE // 2)  # X-coordinate of the square's center
                        center_y = enemy_screen_y + (SQUARE_SIZE // 2)  # Y-coordinate of the square's center
                        # radius = SQUARE_SIZE // 2  # Radius is half the square size
                        radius = max(this_enemy.image.get_width(),this_enemy.image.get_height())
                        radius = 4 + radius/2 
                        pygame.draw.circle(SCREEN, BLUE, (center_x, center_y), radius, 2)  # Blue outline for shields

                    # Draw a red grid line around the square for visual clarity
                    pygame.draw.rect(SCREEN, LOWER_RED, (enemy_screen_x, enemy_screen_y, SQUARE_SIZE, SQUARE_SIZE), 1)
                
                else: # CLOAKED
                    pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)  # Regular grid line


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
    report_pos_y = REPORTS_ORIGIN_Y

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

    draw_report_line("SHUTTLECRAFT:", str(player.landers), report_pos_y)
    report_pos_y += FONT24.get_height()


    draw_report_line("------------------------------", f"-------------", report_pos_y)
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

    draw_report_line("CREW:", f"{player.crewQty} / {MAX_CREW}", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("------------------------------", f"-------------", report_pos_y)
    report_pos_y += FONT24.get_height()

    draw_report_line("CARGO:", f"{player.cargo} / {player.cargo_max}", report_pos_y)
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
        if player.hull < (MAX_HULL * .75):
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

    if title =="SHUTTLECRAFT:":
        # Draw the lander indicator (LANDER_IMAGE)
        offset_x = 10
        for i in range(player.landers):
            SCREEN.blit(LANDER_IMAGE, (SCREEN_WIDTH-REPORT_STATUS_MARGIN+value_surface.get_width()+offset_x, y_pos-3))
            offset_x += (LANDER_IMAGE.get_width() + 3)

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
            sector_title = FONT24.render(f"** STANDARD PLANETARY ORBIT **", True, GREEN)
            screen.blit(sector_title, (sector_info_x, sector_info_y))
        else:
            sector_title = FONT24.render(f"QUADRANT : {player.quadrant_x+1} , {player.quadrant_y+1}   ( {get_quadrant_name(player.quadrant_x,player.quadrant_y)} )", True, GREEN)
            screen.blit(sector_title, (sector_info_x, sector_info_y-FONT24.get_height()))
            sector_title = FONT24.render(f"- IN ORBITAL RANGE WITH PLANET -", True, GREEN)
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

    if player.away_team_on_planet:
        if flash_on:
            player_condition = FONT24.render(f"AWAY MISSION IN PROGRESS",True,color)
            screen.blit(player_condition, (player_info_x - player_condition.get_width(), player_info_y))




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
                colorB = LIGHT_BLUE if num_bases > 0 else DARK_GREEN
                colorC = YELLOW if num_stars > 0 else DARK_GREEN
                if len(this_sector.wormholes) > 0: colorC  = PURPLE

            elif this_sector.visited:
                textA  = str(this_sector.last_star_count)
                textB  = str(this_sector.last_base_count)
                textC  = str(this_sector.last_enemy_count)

                colorA = DARK_RED if num_enemy > 0 else DARK_GREEN
                colorB = DARK_BLUE if num_bases > 0 else DARK_GREEN
                colorC = DARK_YELLOW if num_stars > 0 else DARK_GREEN
                if len(this_sector.wormholes) > 0: colorC  = DARK_PURPLE

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
                    colorB = LIGHT_BLUE if num_bases > 0 else GREEN
                    colorC = YELLOW if num_stars > 0 else GREEN
                    if len(this_sector.wormholes) > 0: colorC  = PURPLE
                else:
                    grid_color = DARK_GREEN
                    colorA = DARK_RED if num_enemy > 0 else DARK_GREEN
                    colorB = DARK_BLUE if num_bases > 0 else DARK_GREEN
                    colorC = DARK_YELLOW if num_stars > 0 else DARK_GREEN
                    if len(this_sector.wormholes) > 0: colorC  = DARK_PURPLE


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
                                    log_event(f"Transferred {transfer_amount} energy to shields.", LIGHT_BLUE)
                                else:
                                    print("Transfer would exceed maximum shield capacity.")
                                    log_event("Transfer would exceed maximum shield capacity.", RED)
                            else:
                                print("Not enough energy to transfer.")
                                log_event("Not enough energy to transfer.", RED)
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
                                    log_event(f"Transferred {transfer_back} energy back to reserves.", LIGHT_BLUE)
                                else:
                                    print("Transfer would exceed maximum energy capacity.")
                                    log_event("Transfer would exceed maximum energy capacity.", RED)
                            else:
                                print("Not enough energy in shields to transfer back.")
                                log_event("Not enough energy in shields to transfer back.", RED)
                        else:
                            print("No energy transferred.")
                            log_event("No energy transferred.", RED)
                        return  # Exit the prompt once a valid transfer occurs
                    except ValueError:
                        print("Invalid input. Please enter a valid numeric value.")
                        input_text = ""  # Reset on invalid input
                elif event.key == pygame.K_BACKSPACE:  # Remove the last character
                    input_text = input_text[:-1]
                else:  # Add new character
                    if len(input_text) < 6 and (event.unicode.isdigit() or (event.unicode == '-' and len(input_text) == 0)):
                        input_text += event.unicode


def prompt_crew_roster():
    global showing_roster
    global roster_selected_line
    global projectile_group
    global key_pressed
    global overlay_images


    key_pressed = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            showing_roster = False

        elif event.type == pygame.KEYDOWN:  # Check for key presses
            key_pressed = True
            if event.key == pygame.K_c:
                print("toggle roster off")
                key_pressed = False
                showing_roster = False
                ALARM_CHANNEL.play(NEXT_LINE)
            if event.key == pygame.K_UP:

                if len(player.soulsOnBoard) > 0:
                    if roster_selected_line != 0:
                        roster_selected_line -= 1
                        ALARM_CHANNEL.play(NEXT_LINE)
                    else:
                        ALARM_CHANNEL.play(NEXT_LINE)
                        roster_selected_line = len(player.soulsOnBoard)-1

                else: no.play()
            if event.key == pygame.K_DOWN:

                if len(player.soulsOnBoard) > 0:
                    if roster_selected_line < (len(player.soulsOnBoard)-1):
                        roster_selected_line += 1
                        ALARM_CHANNEL.play(NEXT_LINE)
                    else:
                        ALARM_CHANNEL.play(NEXT_LINE)
                        roster_selected_line = 0
                else: ... #no.play()

    # print("show roster")
    SCREEN.fill(BLACK)



    ##draw_all_to_screen()
    
    draw_alert_info(SCREEN)
    
    # draw_sector_map()
    
    # projectile_group.update() 
    # for projectile in projectile_group:
    #     if not projectile.out_of_bounds():
    #         projectile.draw(SCREEN)

    draw_reports()
    display_enemy_readout(SCREEN)
    draw_quadrant_map(player)

    draw_captain(overlay_images,key_pressed)
    draw_log(SCREEN)

    if showing_roster:
        showRoster()

    

    pygame.display.flip()
    # Cap the frame rate
    clock.tick(FPS)

def getRankforSort(obj):
    return RANK_LIST.index(obj.rank)

# def showRoster():
#     global roster_selected_line

#     line         = 0
#     space        = 0
#     row          = 0
#     columnSpace  = 0
#     extracrewcount = 0 


#     crewMuster = player.soulsOnBoard.sprites()
#     crewMuster.sort(key = getRankforSort, reverse = True)

    

#     for crewmate in crewMuster:
#         crewMateText = ""
#         if line == roster_selected_line:
#             highlighted_choice = crewmate
#             crewMateText = "-"
#         else: ...


#         if line >= 30-1:
#             extracrewcount += 1
#         else:
#             crewMateText += crewmate.info()
#             LIST_FONT.render_to(screen, (SCREEN_WIDTH-560+columnSpace, 440+MAP_START_Y+space), crewMateText, crewmate.shirtColor)
#             space += 15
#             row   += 1
#             if row >= 10:
#                 row = 0
#                 space = 0
#                 columnSpace += 205
#         line  += 1
#     if line > 30: 
#         LIST_FONT.render_to(screen, (SCREEN_WIDTH-560+columnSpace, 440+MAP_START_Y+space), "  + " + str(extracrewcount) + " Additional Crew", GREEN)

#     # SHOW INDIVIUDAL CREW PORTFOLIO -------------------------------------------------------------------------

#     pygame.draw.rect(screen, DARKGREY, pygame.Rect(MAP_START_X+6,MAP_START_Y+190, MAP_WIDTH-10-10, 425))
#     pygame.draw.rect(screen, GREY, pygame.Rect(MAP_START_X+6,MAP_START_Y+190, MAP_WIDTH-10-10, 425),2)

#     pygame.draw.rect(screen, DARKGREY, pygame.Rect(MAP_START_X+8,MAP_START_Y+195, MAP_WIDTH-10-10, 425))
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+8,MAP_START_Y+195, MAP_WIDTH-10-10, 425),2)

#     pygame.draw.rect(screen, DARKGREY, pygame.Rect(MAP_START_X+10,MAP_START_Y+200, MAP_WIDTH-10-10, 425))
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10,MAP_START_Y+200, MAP_WIDTH-10-10, 425),2)

#     crewmate = highlighted_choice
#     SUB_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10), crewmate.fullInfo(), crewmate.shirtColor)

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+275,MAP_START_Y+200+10), "Serial # "       + str(crewmate.getSerialNumber())  , LIGHTGREY)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+375,MAP_START_Y+200+10), "SPECIES: "       + crewmate.species, GREEN)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+375,MAP_START_Y+200+25), "HOMEWORLD: "     + crewmate.homeworld, GREEN)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+500,MAP_START_Y+200+10), "Join Date: "     + crewmate.getEnrollmentDate() + "   -   XP: " + str(crewmate.xp),  WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+25),  "DEPARTMENT: "    + crewmate.department, crewmate.shirtColor)

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+40),  "STRENGTH......... ",       WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+40),str(crewmate.strength),       WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+40-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+40-1, crewmate.strength, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+55),  "HEALTH........... ",         WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+55),str(crewmate.health),         WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+55-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+55-1, crewmate.health, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+70),  "STAMINA.......... ",        WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+70),str(crewmate.stamina),        WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+70-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+70-1, crewmate.stamina, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+85),  "BRAVERY.......... ",        WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+85),str(crewmate.bravery),        WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+85-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+85-1, crewmate.bravery, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+100), "REACTIONS........ ",      WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+100),str(crewmate.reactions),      WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+100-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+100-1, crewmate.reactions, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+115), "ACCURACY......... ",       WHITE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+115),str(crewmate.accuracy),       WHITE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+115-1, 100, 12))
#     pygame.draw.rect(screen, WHITE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+115-1, crewmate.accuracy, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+130), "PSI-STRENGTH..... ",    PURPLE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+130),str(crewmate.psiStrength),    PURPLE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+130-1, 100, 12))
#     pygame.draw.rect(screen, PURPLE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+130-1, crewmate.psiStrength, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+145), "PSI-SKILL........ ",       PURPLE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+145),str(crewmate.psiSkill),       PURPLE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+145-1, 100, 12))
#     pygame.draw.rect(screen, PURPLE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+145-1, crewmate.psiSkill, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+160), "COMMAND.......... ",        RED)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+160),str(crewmate.command),        RED)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+160-1, 100, 12))
#     pygame.draw.rect(screen, RED, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+160-1, crewmate.command, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+175), "PILOTING......... ",       RED)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+175),str(crewmate.piloting),       RED)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+175-1, 100, 12))
#     pygame.draw.rect(screen, RED, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+175-1, crewmate.piloting, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+190), "ENGINEERING...... ",    GOLD)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+190),str(crewmate.engineering),    GOLD)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+190-1, 100, 12))
#     pygame.draw.rect(screen, GOLD, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+190-1, crewmate.engineering, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+205), "TACTICAL........ ",       GOLD)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+205),str(crewmate.tactical),       GOLD)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+205-1, 100, 12))
#     pygame.draw.rect(screen, GOLD, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+205-1, crewmate.tactical, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+220), "SECURITY......... ",       GOLD)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+220),str(crewmate.security),       GOLD)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+220-1, 100, 12))
#     pygame.draw.rect(screen, GOLD, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+220-1, crewmate.security, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+235), "COMMUNICATIONS... ", RED)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+235), str(crewmate.communications), RED)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+235-1, 100, 12))
#     pygame.draw.rect(screen, RED, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+235-1, crewmate.communications, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+250), "PHYSICAL-SCIENCE..",        PURPLE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+250),str(crewmate.physicalScience),        PURPLE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+250-1, 100, 12))
#     pygame.draw.rect(screen, PURPLE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+250-1, crewmate.physicalScience, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+265), "BIO-SCIENCE....... ",        GREEN)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+265),str(crewmate.bioScience),        GREEN)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+265-1, 100, 12))
#     pygame.draw.rect(screen,  GREEN, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+265-1, crewmate.bioScience, 12))

#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+280), "MEDICAL.......... ",        BLUE)
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+150,MAP_START_Y+200+10+280),str(crewmate.medical),        BLUE)
#     pygame.draw.rect(screen, LIGHTGREY, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+280-1, 100, 12))
#     pygame.draw.rect(screen, BLUE, pygame.Rect(MAP_START_X+10+10+175,MAP_START_Y+200+10+280-1, crewmate.medical, 12))



#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+315), "Additional Skills: ",        WHITE)
#     if len(crewmate.extraSkills) > 0:

#         listSkills = ""
#         for skill in crewmate.extraSkills:
#             listSkills += skill
#             if skill != crewmate.extraSkills[-1]:
#                 listSkills += ", "
#         listSkills += "."
#         LIST_FONT.render_to(screen, (MAP_START_X+10+10+15,MAP_START_Y+200+10+330),listSkills.capitalize(),        WHITE)
#     else: LIST_FONT.render_to(screen, (MAP_START_X+10+10+15,MAP_START_Y+200+10+330),"None",        LIGHTGREY)




#     LIST_FONT.render_to(screen, (MAP_START_X+10+10,MAP_START_Y+200+10+360), "NOTES: ",        WHITE)
#     displayTraits = ""
#     traitColor = WHITE

#     traitList = []
#     traitList.extend(crewmate.goodTraits)
#     traitList.extend(crewmate.badTraits)

#     if len(traitList) >= 1:
#         for trait in traitList:
#             displayTraits += trait
#             if trait != traitList[-1]:
#                 displayTraits += ", "
#             elif trait == traitList[-1]:
#                 displayTraits += "."
#         displayTraits = displayTraits.capitalize()
#     else:
#         displayTraits = "None"
#         traitColor = LIGHTGREY
        
#     LIST_FONT.render_to(screen, (MAP_START_X+10+10+15,MAP_START_Y+200+10+375),displayTraits,traitColor)



def showRoster():
    global roster_selected_line

    line         = 0
    space        = 0
    row          = 0
    columnSpace  = 0
    extracrewcount = 0 
    showRosterTitle_surface = FONT24.render(": CREW ROSTER :", True, GREEN)
    SCREEN.blit(showRosterTitle_surface, (CREW_ORIGIN_X, GRID_ORIGIN_Y - SQUARE_SIZE // 3))
    pygame.draw.rect(SCREEN, GREEN, (GRID_ORIGIN_X - 1, GRID_ORIGIN_Y - 1, GRID_SIZE * SQUARE_SIZE + 2, GRID_SIZE * SQUARE_SIZE + 2), 2)

    crewMuster = player.soulsOnBoard.sprites()
    crewMuster.sort(key = getRankforSort, reverse = True)

    for crewmate in crewMuster:
        x_offset = 0
        crewMateText = ""
        if line == roster_selected_line:
            highlighted_choice = crewmate
            crewMateText = "--> "
            x_offset = - 23
        else:
            pass

        if line >= 30-1:
            extracrewcount += 1
        else:
            crewMateText += crewmate.info()
            if line == roster_selected_line:
                highlighted_choice = crewmate
                crewMateText += " <--"
            crewMateText_surface = FONT24.render(crewMateText, True, crewmate.shirtColor)
            SCREEN.blit(crewMateText_surface, (CREW_DETAIL_START_X+columnSpace+x_offset, 440+CREW_DETAIL_START_Y+space))
            space += 15
            row   += 1
            if row >= 10:
                row = 0
                space = 0
                columnSpace += 240
        line  += 1


    if line > 30: 
        additional_crew_text = FONT24.render("  + " + str(extracrewcount) + " Additional Crew", True, GREEN)
        screen.blit(additional_crew_text, (CREW_DETAIL_START_X+columnSpace, 440+CREW_DETAIL_START_Y+space))

    # SHOW INDIVIDUAL CREW PORTFOLIO -------------------------------------------------------------------------

    pygame.draw.rect(SCREEN, NEAR_BLACK, pygame.Rect(CREW_ORIGIN_X,CREW_ORIGIN_Y, CREW_BOX_SIZE_WIDTH, 425))
    pygame.draw.rect(SCREEN, GREEN, pygame.Rect(CREW_ORIGIN_X,CREW_ORIGIN_Y, CREW_BOX_SIZE_WIDTH, 425),2)

    pygame.draw.rect(SCREEN, NEAR_BLACK, pygame.Rect(CREW_ORIGIN_X+5,CREW_ORIGIN_Y+5, CREW_BOX_SIZE_WIDTH, 425))
    pygame.draw.rect(SCREEN, GREEN, pygame.Rect(CREW_ORIGIN_X+5,CREW_ORIGIN_Y+5, CREW_BOX_SIZE_WIDTH, 425),2)

    pygame.draw.rect(SCREEN, NEAR_BLACK, pygame.Rect(CREW_ORIGIN_X+10,CREW_ORIGIN_Y+10, CREW_BOX_SIZE_WIDTH, 425))
    pygame.draw.rect(SCREEN, GREEN, pygame.Rect(CREW_ORIGIN_X+10,CREW_ORIGIN_Y+10, CREW_BOX_SIZE_WIDTH, 425),2)

    crewmate = highlighted_choice
    full_info_surface = FONT24.render(crewmate.fullInfo(), True, crewmate.shirtColor)
    SCREEN.blit(full_info_surface, (CREW_DETAIL_START_X, CREW_DETAIL_START_Y))

    serial_surface = FONT22.render("Serial # " + str(crewmate.getSerialNumber()), True, LIGHT_GREY)
    SCREEN.blit(serial_surface, (CREW_DETAIL_START_X+335, CREW_DETAIL_START_Y+25))

    species_surface = FONT22.render("SPECIES: " + crewmate.species, True, GREEN)
    SCREEN.blit(species_surface, (CREW_DETAIL_START_X+335, CREW_DETAIL_START_Y+50))

    homeworld_surface = FONT22.render("HOMEWORLD: " + crewmate.homeworld, True, GREEN)
    SCREEN.blit(homeworld_surface, (CREW_DETAIL_START_X+335, CREW_DETAIL_START_Y+75))

    join_date_surface = FONT22.render(
        "Join Date: " + str(crewmate.getEnrollmentDate()) + "   -   XP: " + str(round(crewmate.xp)), True, WHITE
    )
    SCREEN.blit(join_date_surface, (CREW_DETAIL_START_X+335, CREW_DETAIL_START_Y+100))

    department_surface = FONT24.render("DEPARTMENT: " + crewmate.department, True, crewmate.shirtColor)
    SCREEN.blit(department_surface, (CREW_DETAIL_START_X, CREW_DETAIL_START_Y+25))

    stats = [
        ("STRENGTH......... ", crewmate.strength, WHITE),
        ("HEALTH........... ", crewmate.health, WHITE),
        ("STAMINA.......... ", crewmate.stamina, WHITE),
        ("BRAVERY.......... ", crewmate.bravery, WHITE),
        ("REACTIONS........ ", crewmate.reactions, WHITE),
        ("ACCURACY......... ", crewmate.accuracy, WHITE),
        ("PSI-STRENGTH..... ", crewmate.psiStrength, PURPLE),
        ("PSI-SKILL........ ", crewmate.psiSkill, PURPLE),
        ("COMMAND.......... ", crewmate.command, RED),
        ("PILOTING......... ", crewmate.piloting, RED),
        ("ENGINEERING...... ", crewmate.engineering, GOLD),
        ("TACTICAL......... ", crewmate.tactical, GOLD),
        ("SECURITY......... ", crewmate.security, GOLD),
        ("COMMUNICATIONS... ", crewmate.communications, RED),
        ("PHYSICAL-SCIENCE..", crewmate.physicalScience, PURPLE),
        ("BIO-SCIENCE.......", crewmate.bioScience, GREEN),
        ("MEDICAL.......... ", crewmate.medical, LIGHT_BLUE),
    ]

    y_offset = 40
    for label, value, color in stats:
        label_surface = FONT24.render(label, True, color)
        value_surface = FONT24.render(str(value), True, color)
        SCREEN.blit(label_surface, (CREW_DETAIL_START_X, CREW_DETAIL_START_Y+y_offset))
        SCREEN.blit(value_surface, (CREW_DETAIL_START_X+175, CREW_DETAIL_START_Y+y_offset))
        pygame.draw.rect(
            SCREEN, DARK_GREY, pygame.Rect(CREW_DETAIL_START_X+200, CREW_DETAIL_START_Y+y_offset, 120, 12)
        )
        pygame.draw.rect(
            SCREEN, color, pygame.Rect(CREW_DETAIL_START_X+200, CREW_DETAIL_START_Y+y_offset, value, 12)
        )
        y_offset += 15

    additional_skills_surface = FONT24.render("Additional Skills: ", True, WHITE)
    SCREEN.blit(additional_skills_surface, (CREW_DETAIL_START_X, CREW_DETAIL_START_Y+315))

    if len(crewmate.extraSkills) > 0:
        listSkills = ", ".join(crewmate.extraSkills) + "."
        listSkills_surface = FONT22.render(listSkills.capitalize(), True, WHITE)
        SCREEN.blit(listSkills_surface, (CREW_DETAIL_START_X+15, CREW_DETAIL_START_Y+330))
    else:
        none_surface = FONT22.render("None", True, LIGHT_GREY)
        SCREEN.blit(none_surface, (CREW_DETAIL_START_X+15, CREW_DETAIL_START_Y+330))

    notes_surface = FONT24.render("NOTES: ", True, WHITE)
    SCREEN.blit(notes_surface, (CREW_DETAIL_START_X, CREW_DETAIL_START_Y+360))

    trait_list = crewmate.goodTraits + crewmate.badTraits
    if trait_list:
        displayTraits = ", ".join(trait_list).capitalize() + "."
        display_traits_surface = FONT22.render(displayTraits, True, WHITE)
    else:
        display_traits_surface = FONT22.render("None", True, LIGHT_GREY)

    SCREEN.blit(display_traits_surface, (CREW_DETAIL_START_X+15, CREW_DETAIL_START_Y+375))

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
                ALARM_CHANNEL.play(NEXT_LINE)
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
                ALARM_CHANNEL.play(NEXT_LINE)
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
                ALARM_CHANNEL.play(NEXT_LINE)
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
                ALARM_CHANNEL.play(NEXT_LINE)
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

    # Add starbase information if present
    # if player.current_quadrant.has_starbase:
    for wormhole in player.current_quadrant.wormholes:
        # starbase_grid_x, starbase_grid_y = base[0], base[1]
        direction, distance = calculate_direction_and_distance(
            player.grid_x, player.grid_y, wormhole.grid_x, wormhole.grid_y
        )
        targets_with_distances.append((wormhole, direction, distance))

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
        displayName = target.name

        if type(target) == Enemy: text_color = RED
        elif type(target) == Planet: 
            text_color = GREEN
            this_font = FONT22
            if player.orbiting_planet == target: 
                direction = "-"
                distance  = "IN ORBIT"
            # if len(player.orbiting_planet.away_team) >= 1:
            #     displayName += "*"


        elif  type(target) == Base: 
            text_color = BLUE
            if player.docked: 
                direction = "-"
                distance  = "DOCKED"
        elif  type(target) == Wormhole:
            text_color = PURPLE 
        




        # Render enemy name
        target_name_text = this_font.render(displayName, True, text_color)
        screen.blit(target_name_text, (SCAN_ORIGIN_X + SCAN_NAME_X -10, SCAN_ORIGIN_Y + y_offset))

        
        if target.cloak_enabled:
            text_color = PURPLE
            direction = "?"
            distance = "?"

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
        if target.cloak_enabled: 
            shield_text = this_font.render(f"?", True, PURPLE)

        shield_x = SCAN_ORIGIN_X + SCAN_SHIELD_X + (100 - shield_text.get_width()) // 2
        screen.blit(shield_text, (shield_x, SCAN_ORIGIN_Y + y_offset))

        # Render enemy hull
        hull_text = this_font.render(f"{target.hull}", True, text_color)
        if target.hull <= 0:
            hull_text = this_font.render(f"--", True, GREY)
        if target.cloak_enabled: 
            hull_text = this_font.render(f"?", True, PURPLE)
        hull_x = SCAN_ORIGIN_X + SCAN_HULL_X + (100 - hull_text.get_width()) // 2
        screen.blit(hull_text, (hull_x, SCAN_ORIGIN_Y + y_offset))


        if type(target) == Planet:

            if target.landers >= 1:
                y_offset += FONT24.get_height()
                target_name_text = this_font.render("  --- Shuttle", True, WHITE)
                screen.blit(target_name_text, (SCAN_ORIGIN_X + SCAN_NAME_X -10, SCAN_ORIGIN_Y + y_offset))



            if len(target.away_team) >= 1:
                y_offset += FONT24.get_height()
                target_name_text = this_font.render("  --- Away Team", True, WHITE)
                screen.blit(target_name_text, (SCAN_ORIGIN_X + SCAN_NAME_X -10, SCAN_ORIGIN_Y + y_offset))


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
                ALARM_CHANNEL.play(NEXT_LINE)
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
    # box_width = 55 * CAPTAIN_BOX_SCALE
    # box_height = 30 * CAPTAIN_BOX_SCALE

    box_width  = CAPTAIN_BOX_WIDTH
    box_height = CAPTAIN_BOX_HEIGHT
    
    # Calculate the position for the box (right of center at the bottom)
    box_x = CAPTAIN_BOX_ORIGIN_X
    # box_x = QUADRANT_ORIGIN_X - box_width - 50  # 10 pixels offset from the right edge
    box_y = SCREEN_HEIGHT - box_height - 25  # 10 pixels offset from the bottom edge

    # Draw the grey outline for the box
    outline_color =  GREEN 
    if   player.condition == "RED":  outline_color =  RED 
    elif player.condition == "BLUE": outline_color =  BLUE 
    pygame.draw.rect(SCREEN, outline_color, (box_x-2, box_y-2, box_width+4, box_height+4), 2)  # 2 is the outline thickness

    
    # Draw the 'CRUISER_CAPTAIN_000' background image inside the box
    SCREEN.blit(CRUISER_CAPTAIN_000, (box_x, box_y))

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
        # overlay_image = pygame.transform.scale(image, (image.get_width()*CAPTAIN_BOX_SCALE, image.get_height()*CAPTAIN_BOX_SCALE))  # Scale to box size
        overlay_image = image
        x_offset, y_offset = abs(x_offset), abs(y_offset)
        SCREEN.blit(overlay_image, (box_x + x_offset*CAPTAIN_BOX_SCALE, box_y + y_offset*CAPTAIN_BOX_SCALE))

def brighten_color(rgb, increase_by):
    """
    Adjusts the brightness of an RGB color by increasing or decreasing each non-zero value.

    :param rgb: Tuple of (R, G, B) values.
    :param increase_by: Amount to adjust each non-zero value (positive or negative).
    :return: New RGB color tuple with modified values.
    """
    def adjust_value(value, increase_by):
        if value == 0:  # Do not adjust if the value is 0
            return 0
        return max(0, min(value + increase_by, 255))  # Clamp between 0 and 255

    return tuple(adjust_value(value, increase_by) for value in rgb)

def log_event(event_string, event_color=GREEN):
    """Add an event to the ship's log with a specified color."""
    global ship_log
    # Add the new event as a tuple (event_string, event_color)
    ship_log.append((event_string, event_color))
    # Trim the log if it exceeds the maximum number of entries
    if len(ship_log) > MAX_LOG_ENTRIES:
        ship_log.pop(0)

def draw_log(screen):
    """Draw the ship's log directly onto the given screen."""
    # Draw a background rectangle for the log
    pygame.draw.rect(
        screen,
        BLACK,
        (LOG_ORIGIN_X, LOG_ORIGIN_Y, LOG_WIDTH, LOG_HEIGHT),
    )

    outline_color = GREEN 

    if player.condition == "RED": outline_color = RED

    elif player.condition == "BLUE": outline_color = BLUE

    # Draw a border around the log
    pygame.draw.rect(
        screen, outline_color, (LOG_ORIGIN_X, LOG_ORIGIN_Y, LOG_WIDTH, LOG_HEIGHT), 2
    )

    # Draw each log entry
    for i, (event, event_color) in enumerate(ship_log):
        # Calculate the Y position for each entry (bottom to top)
        y_pos = (
            LOG_ORIGIN_Y
            + LOG_HEIGHT
            - LOG_PADDING
            - (len(ship_log) - i) * (FONT22.get_height() + 4)
        )
        # Skip if the entry would be above the log area
        if y_pos < LOG_ORIGIN_Y + LOG_PADDING:
            continue

        # Dim older entries (those not in the latest 4)
        dim_amount = 35

        if i < len(ship_log) - 8:
            event_color = brighten_color(event_color, -dim_amount)

        if i < len(ship_log) - 7:
            event_color = brighten_color(event_color, -dim_amount)

        if i < len(ship_log) - 6:
            event_color = brighten_color(event_color, -dim_amount)

        if i < len(ship_log) - 5:
            event_color = brighten_color(event_color, -dim_amount)

        if i < len(ship_log) - 4:
            event_color = brighten_color(event_color, -dim_amount)

        if i < len(ship_log) - 3:
            event_color = brighten_color(event_color, -dim_amount)

        # Render the event with its specific color
        text_surface = FONT22.render(event, True, event_color)
        screen.blit(text_surface, (LOG_ORIGIN_X + LOG_PADDING, y_pos))




def draw_all_to_screen(): # for use when in a prompt.
    global projectile_group
    global key_pressed
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

    draw_log(SCREEN)



### END FUNCTIONS ###########################################################################################################

def main():
    running = True
    global player
    global projectile_group
    global current_index
    global players_turn
    global overlay_images
    global key_pressed

    global showing_roster
    global roster_selected_line
    global ship_log

    roster_selected_line = 0

    ship_log = []
    log_event("Ship launched successfully.")

    player = Player()
    projectile_group = pygame.sprite.Group() 

    current_index = SHIELD_LEVELS.index(player.shield_level)  # Find the current level's index
    players_turn = True
    showing_roster = False

    # List to store overlay images and their offsets
    overlay_images = []

    # The log list to hold recent events
    

    play_delayed_sound(MUSIC_CHANNEL, random.choice(VICTORY_DITTIES), 0.5)
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
        if player.crewQty <= 0:
            ...
            # running = False

        
        key_pressed = False


        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            

            elif event.type == pygame.KEYDOWN:  # Check for key presses

                if players_turn and (len(projectile_group) ==0) and not showing_roster:

                    if event.key == pygame.K_m:
                        player.successive_move()
                        key_pressed = True
                    
                    if event.key == pygame.K_LEFT or event.key ==pygame.K_KP_4:
                        player.move(-1, 0)
                        key_pressed = True
                        

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP_6:
                        player.move(1, 0)
                        key_pressed = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_KP_8:
                        player.move(0, -1)
                        key_pressed = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP_2:
                        player.move(0, 1)
                        key_pressed = True
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_r or event.key == pygame.K_KP_2: # REST
                        player.move(0, 0)
                        key_pressed = True


                    elif event.key == pygame.K_KP_7:
                        player.move(-1, -1)
                        key_pressed = True

                    elif event.key == pygame.K_KP_9:
                        player.move(+1, -1)
                        key_pressed = True

                    elif event.key == pygame.K_KP_1:
                        player.move(-1, +1)
                        key_pressed = True

                    elif event.key == pygame.K_KP_3:
                        player.move(+1, +1)
                        key_pressed = True


                    elif event.key == pygame.K_p:

                        if not player.docked: 
                            ALARM_CHANNEL.play(NEXT_LINE)
                            player.fire_phasers()
                            
                        key_pressed = True


                    elif event.key == pygame.K_t:
                        
                        if not player.docked: 
                            ALARM_CHANNEL.play(NEXT_LINE)
                            player.fire_torpedo()
                            
                        key_pressed = True
                        

                    elif event.key == pygame.K_w:
                        ALARM_CHANNEL.play(NEXT_LINE)
                        if not player.docked:
                            player.activate_warp()
                            ALARM_CHANNEL.play(NEXT_LINE)
                        key_pressed = False
                        

                    elif event.key == pygame.K_s:
                        key_pressed = False
                        # player.shields_toggle()

                        if not player.docked: 
                            prompt_shields_transfer(SCREEN)
                            ALARM_CHANNEL.play(NEXT_LINE)

                    elif event.key == pygame.K_c:
                        if not showing_roster:
                            print("toggle roster on ")
                            # log_event("Viewing Roster")
                            key_pressed = False
                            showing_roster = True
                            # prompt_crew_roster(showing_roster)
                            roster_selected_line = 0
                            ALARM_CHANNEL.play(NEXT_LINE)



                    elif event.key == pygame.K_d:
                        key_pressed =  True
                        if player.inDockingRange is not None:
                            player.toggle_dock(player.inDockingRange)

                    elif event.key == pygame.K_o:
                        key_pressed =  True
                        if player.inOrbitRange is not None:
                            player.toggle_orbit(player.inOrbitRange)

                    elif event.key == pygame.K_l:
                        if player.inOrbit:
                            key_pressed =  True
                            if player.inOrbitRange is not None:
                                ALARM_CHANNEL.play(NEXT_LINE)
                                player.land_away_team()
                                

                    elif event.key == pygame.K_KP_PLUS:

                        key_pressed = False
                        if not player.docked: 
                            # Increase the shield level
                            player.shields_on = True
                            if current_index < len(SHIELD_LEVELS) - 1:
                                current_index += 1
                                player.shield_level = SHIELD_LEVELS[current_index]
                                print(f"Shield level increased to {player.shield_level}%")
                                log_event(f"Shield level increased to {player.shield_level}%", LIGHT_BLUE)
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
                                log_event(f"Shield level decreased to {player.shield_level}%", LIGHT_BLUE)
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

                while showing_roster:
                    prompt_crew_roster()

                    
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

        draw_log(SCREEN)

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
