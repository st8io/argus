import os
import easyocr
import json
import image_processing
import prompt

keywords = ['start', 'play', 'continue', 'press', 'tap', 'click', 'next', 'skip']
reader = easyocr.Reader(['en'])


def find_button_by_keywords(image_path):
    coordinates = find_words(image_path)

    if not coordinates:
        image = image_processing.preprocess_for_white_text(image_path)
        coordinates = find_words(image)

    if not coordinates:
        print("Trying to use OpenAI")
        result = prompt.get_button_cordinates(image_processing.encode_image(image_path))
        lst = json.loads(result)
        if lst[0] is not None and lst[1] is not None:
            coordinates = [tuple(lst)]

    return coordinates


def find_words(image_path):
    coordinates = []
    results = reader.readtext(image_path)

    for bbox, text, conf in results:
        if text.strip().lower() in keywords:
            print(f"Detected text: {text}")
            print(f"Bounding box coordinates: {bbox}\n")
            coordinates.append(get_center(bbox))
    return coordinates



def get_center(bbox):
    # [
    # [top-left-x, top-left-y],
    # [top-right-x, top-right-y],
    # [bottom-right-x, bottom-right-y],
    # [bottom-left-x, bottom-left-y]
    #  ]

    x_coords = [pt[0] for pt in bbox]
    y_coords = [pt[1] for pt in bbox]

    scale_factor = int(os.environ['SCALE_FACTOR'])
    center_x = int(sum(x_coords) / 4 / scale_factor)
    center_y = int(sum(y_coords) / 4 / scale_factor)

    return (center_x, center_y)
