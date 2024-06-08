
#game value
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

#ui
BAR_HEIGHT = 20
HP_BAR_WIDTH = 200
MP_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../assets/github/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

#general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#ffffff'
TEXT_COLOR = '#EEEEEE'

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
    'squid' : {'HP': 100, 'exp': 100, 'damage': 20, 'attackType': 'slash', 'attackSound': '../assets/github/audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attackRadius': 80, 'noticeRadius': 360},
    'raccoon' : {'HP': 300, 'exp': 250, 'damage': 40, 'attackType': 'claw', 'attackSound': '../assets/github/audio/attack/claw.wav', 'speed': 1, 'resistance': 3, 'attackRadius': 80, 'noticeRadius': 280},
    'spirit' : {'HP': 100, 'exp': 110, 'damage': 8, 'attackType': 'thunder', 'attackSound': '../assets/github/audio/attack/fireball.wav', 'speed': 2, 'resistance': 3, 'attackRadius': 60, 'noticeRadius': 300},
    'bamboo' : {'HP': 140, 'exp': 120, 'damage': 6, 'attackType': 'leaf_attack', 'attackSound': '../assets/github/audio/attack/slash.wav', 'speed': 1.5, 'resistance': 3, 'attackRadius': 50, 'noticeRadius': 260},

}
