import re


def format(themes_dict):
    whitelist = ["Animals", "Fruits", "Adventure", "Myths", "Asian", "Gold", "Classic", "Egyptian", "Fantasy", "Gems",
                 "Chinese", "Party & Festivals", "Magic", "Ancient", "Misterious", "Sea", "Wild West", "Music",
                 "Nature", "Cartoons", "Christmas", "Dragons", "Sport", "Vegas", "Horror", "Latino", "Medieval",
                 "Space", "Fish", "History", "Cards", "Irish", "Sweets", "Money", "Food", "Roman", "Summer",
                 "Native America", "Jungle", "Fairy Tales", "Characters", "Bells", "Luxury", "Nordic", "Greek", "War",
                 "Gods", "Winter", "Crime", "Futuristic", "Fire", "Bars", "Pirates", "Ladies", "Joker", "Monsters",
                 "American", "Books", "Retro", "Tropical", "Royal", "Mining", "Japanese", "Culture", "Alcohol", "Dice",
                 "Desert", "Flowers", "Leprechaun", "Africa", "Celebrities", "Easter", "Warriors", "Safari", "Aliens",
                 "Arabic", "Dinosaurs", "Industrial", "Cars", "Buffalo", "Circus", "Anime", "Explosives", "Farming",
                 "Vampires", "Fighting", "Cute", "Show", "Branded", "Romance", "Arcade", "Indian", "Neon", "Airplanes",
                 "Military", "Ships", "Ice", "Elements", "Day Of The Dead", "Sexy", "Paradise", "Night Life", "Guns",
                 "Zodiac", "Hieroglyph", "Crypto", "Science", "Apocalypse", "Urban", "3D", "Fairy Tale", "Slavic",
                 "Italian", "Hawaii", "Europe", "Gothic", "Spain", "Pixel Art", "Ukraine", "Cyberpunk", "French",
                 "Britain", "Mushrooms", "Middle East", "German", "Desperation", "Arctic"]
    data = []
    for game_code, themes in themes_dict.items():
        game_object = {"code": game_code, "game_meta": {"themes": []}}
        for theme in themes.split(","):
            theme = re.sub(r"\[[^]]*\]", "", theme).strip()
            if theme in whitelist:
                game_object["game_meta"]["themes"].append(theme)
        data.append(game_object)
    return data
