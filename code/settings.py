
#game value
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#ui
BAR_HEIGHT = 30
HP_BAR_WIDTH = 200
MP_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = '../assets/github/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

#general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#ffffff'
TEXT_COLOR = '#EEEEEE'

#upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

#UI colors
HP_COLOR = 'red'
MP_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

#weapon
weaponData = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../assets/github/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 300, 'damage': 30, 'graphic': '../assets/github/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 200, 'damage': 25, 'graphic': '../assets/github/graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 10, 'damage': 9, 'graphic': '../assets/github/graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 15, 'graphic': '../assets/github/graphics/weapons/sai/full.png'}
}

#magic
magicData = {
    'heal' : {'strength': 5, 'cost': 20, 'graphic': '../assets/github/graphics/particles/heal/heal.png'},
    'flame': {'strength': 10, 'cost': 20, 'graphic': '../assets/github/graphics/particles/flame/fire.png'},
}

#enemy
monsterData = {
    'squid' : {'HP': 200, 'exp': 70, 'damage': 15, 'attackType': 'slash', 'attackSound': '../assets/github/audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attackRadius': 80, 'noticeRadius': 380},
    'raccoon' : {'HP': 300, 'exp': 250, 'damage': 40, 'attackType': 'claw', 'attackSound': '../assets/github/audio/attack/claw.wav', 'speed': 1, 'resistance': 1.5, 'attackRadius': 80, 'noticeRadius': 300},
    'specialRaccoon' : {'HP': 2000, 'exp': 1, 'damage': 96, 'attackType': 'claw', 'attackSound': '../assets/github/audio/attack/claw.wav', 'speed': 2, 'resistance': 1, 'attackRadius': 70, 'noticeRadius': 400},
    'spirit' : {'HP': 300, 'exp': 120, 'damage': 20, 'attackType': 'thunder', 'attackSound': '../assets/github/audio/attack/fireball.wav', 'speed': 2, 'resistance': 3, 'attackRadius': 60, 'noticeRadius': 360},
    'bamboo' : {'HP': 150, 'exp': 25, 'damage': 8, 'attackType': 'leaf_attack', 'attackSound': '../assets/github/audio/attack/slash.wav', 'speed': 1.5, 'resistance': 3, 'attackRadius': 50, 'noticeRadius': 380},

}

avatarPath = '../assets/graphics/player/Faceset.png'
