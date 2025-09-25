import ast
from openai import OpenAI

client = OpenAI()


async def get_themes(based_image):
    prompt = """
You are an image classification assistant.
You will be given an image and a fixed set of possible labels. Your task is to carefully analyze the image and return the most relevant labels from the provided list.

Instructions:

Only use labels from the given list. Do not invent new ones.
You can select multiple labels if they apply.
If no label applies, return None.
Return results as a comma-separated list of labels (no extra text).

Labels:
Animals, Fruits, Adventure, Myths, Asian, Gold, Classic (Retro casino theme), Egyptian, Fantasy (Tolkien fantasy only!), Gems, Chinese, Party & Festivals, Magic, Ancient, Misterious, Sea, Wild West, Music, Nature, Cartoons, Christmas, Dragons, Sport, Vegas (Clear sign that action takes place in Vegas), Horror, Latino, Medieval, Space, Fish, History, Cards, Irish, Sweets, Money, Food, Roman, Summer, Native America, Jungle, Fairy Tales, Characters, Bells, Luxury, Nordic, Greek, War, Gods, Winter, Crime, Futuristic, Fire, Bars, Pirates, Ladies, Joker, Monsters, American, Books, Retro, Tropical, Royal, Mining, Japanese, Culture, Alcohol, Dice, Desert, Flowers, Leprechaun, Africa, Celebrities, Easter, Warriors, Safari, Aliens, Arabic, Dinosaurs, Industrial, Cars, Buffalo, Circus, Anime, Explosives, Farming, Vampires, Fighting, Cute, Show, Branded, Romance, Arcade, Indian, Neon, Airplanes, Military, Ships, Ice, Elements, Day Of The Dead, Sexy, Paradise, Night Life, Guns, Zodiac, Hieroglyph, Crypto, Science, Apocalypse, Urban, 3D, Fairy Tale, Slavic, Italian, Hawaii, Europe, Gothic, Spain, Pixel Art, Ukraine, Cyberpunk, French, Britain, Mushrooms, Middle East, German, Desperation, Arctic
"""
    output = send_request(prompt, based_image).output_text
    print(output)
    return output


def get_button_cordinates(based_image):
    prompt = """
You are given a game start screen image. 
Image size: WIDTH = 1920, HEIGHT = 1080 (pixels).

Task:
- Find the single button that would take the player from the start screen into gameplay. 
- This button may contain text such as: start, play, continue, press, tap, click, next, skip, 
  or may be an icon/button without text.
- Determine the center point of this button.

Rules:
- Return only the center coordinates as integers in JSON format:
  [x, y]
- Ensure 0 ≤ x < 1920 and 0 ≤ y < 1080.
- Do not return bounding boxes, text, or explanations.
- If no such button exists, return:
    [null, null]
    """
    output = send_request(prompt, based_image).output_text
    return output


async def get_loading_status(based_image):
    prompt = """
You are an AI that analyzes screenshots of browser-based games to determine their loading status. You have no access to the game’s code, only to the image provided. Your task is to classify the image into one of the following four categories:
1)"loading" — loading screen or progress bar, game logo with a loading animation, text such as "Loading" or "Загрузка".
2)"start_screen" — screen showing "Press Start", "Click to Play", "Press Any Key", or similar instructions.
3)"gameplay" — the game is active: visible game world, characters, battlefield, map, or in-game UI.
4)"error" — empty screen, error message, or game failed to start.
Respond only in JSON format: {"status": "<one of the four categories>"}
"""

    output = send_request(prompt, based_image).output_text
    return ast.literal_eval(output)['status']


def send_request(prompt, based_image):
    return client.responses.create(
        model="gpt-5-mini-2025-08-07",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{based_image}",
                },
            ],
        }],
    )
