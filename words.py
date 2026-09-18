# words.py

# 5-letter words for Wordle-style mode
FIVE_LETTER_WORDS = [
    "apple", "brave", "crane", "dream", "eagle", "flame", "grape", "house",
    "input", "joker", "knife", "lemon", "money", "noble", "ocean", "piano",
    "queen", "robot", "stone", "tiger", "uncle", "voice", "water", "xenon",
    "yield", "zebra", "baker", "charm", "dance", "earth", "fable", "ghost",
    "happy", "ivory", "jelly", "karma", "light", "magic", "night", "olive",
    "peace", "quiet", "river", "smile", "table", "urban", "vivid", "wheat",
    "young", "zesty"
]

# Words for scramble mode (longer, more letters)
SCRAMBLE_WORDS = [
    "elephant", "mountain", "computer", "keyboard", "sunflower", "umbrella",
    "treasure", "festival", "chocolate", "adventure", "butterfly", "harmony",
    "pineapple", "strawberry", "waterfall", "telephone", "crocodile", "universe",
    "knowledge", "beautiful"
]

# Words for hangman mode
HANGMAN_WORDS = [
    "python", "telegram", "guitar", "planet", "rocket", "diamond", "whistle",
    "pyramid", "dolphin", "volcano", "library", "glacier", "compass", "harvest",
    "phantom", "crystal", "journey", "mystery", "fountain", "lighthouse"
]

# Riddle-style hints for scramble mode (keyed by word)
SCRAMBLE_HINTS = {
    "elephant": "A large mammal with a trunk.",
    "mountain": "A very tall natural landform.",
    "computer": "An electronic device for processing data.",
    "keyboard": "You type on it.",
    "sunflower": "A tall yellow flower that follows the sun.",
    "umbrella": "You use it when it rains.",
    "treasure": "Hidden riches, often buried.",
    "festival": "A celebration or carnival.",
    "chocolate": "A sweet treat made from cocoa.",
    "adventure": "An exciting or unusual experience.",
    "butterfly": "An insect with colorful wings.",
    "harmony": "Peaceful agreement or balance.",
    "pineapple": "A tropical fruit with a spiky top.",
    "strawberry": "A small red fruit with seeds on the outside.",
    "waterfall": "Water falling from a height.",
    "telephone": "A device for voice communication.",
    "crocodile": "A large reptile with a long snout.",
    "universe": "All of space and everything in it.",
    "knowledge": "Information and understanding.",
    "beautiful": "Pleasing to the senses."
}

# Riddle-style hints for hangman mode
HANGMAN_HINTS = {
    "python": "A programming language — or a snake.",
    "telegram": "A messaging app — or a written message.",
    "guitar": "A stringed musical instrument.",
    "planet": "A celestial body orbiting a star.",
    "rocket": "A vehicle that launches into space.",
    "diamond": "A precious gemstone, or a baseball field.",
    "whistle": "A high-pitched sound, or a device to make one.",
    "pyramid": "An ancient triangular structure.",
    "dolphin": "A smart marine mammal.",
    "volcano": "A mountain that erupts lava.",
    "library": "A place full of books.",
    "glacier": "A slow-moving mass of ice.",
    "compass": "A tool for finding direction.",
    "harvest": "The season of gathering crops.",
    "phantom": "A ghost or illusion.",
    "crystal": "A clear, solid material with a lattice structure.",
    "journey": "A long trip from one place to another.",
    "mystery": "Something difficult to explain.",
    "fountain": "A structure that shoots water.",
    "lighthouse": "A tower with a beacon for ships."
}
