import asyncio
import os
from urllib.parse import urlparse, parse_qs

import image_processing
from prompt import get_loading_status
from ez import find_button_by_keywords


async def take_screenshots(browser, urls, output_dir: str = "screenshots"):
    os.makedirs(output_dir, exist_ok=True)
    fallback_dir = os.path.join(output_dir, "fallback_screenshots")
    os.makedirs(fallback_dir, exist_ok=True)

    page = await browser.new_page()
    await page.set_viewport_size({
        "width": 1920,
        "height": 1080
    })

    successful_screenshots = []

    for url in urls:
        filename = _extract_filename_from_url(url)
        save_path = os.path.join(output_dir, filename)

        print(f"Capturing {url} -> {save_path}")

        # TODO: keep an eye on this. it might break, then replace:
        # await page.goto(url, wait_until="load")
        await page.goto(url, wait_until="networkidle")
        depth = 0
        prev_status = ""

        while depth < 3:
            await page.screenshot(path=save_path)
            status = get_loading_status(image_processing.encode_image(save_path))
            print(f"Status: {status}")

            match status:
                case "gameplay":
                    successful_screenshots.append(save_path)
                    break

                case "loading":
                    depth = _update_counter(prev_status, "loading", depth)
                    await asyncio.sleep(3)

                case "start_screen":
                    cords = find_button_by_keywords(save_path)
                    print(f"Button coordinates: {cords}")
                    await _click_around(page, cords)

                    depth = _update_counter(prev_status, "start_screen", depth)
                    if depth >= 2:  # fallback if stuck at start screen
                        fallback_path = os.path.join(fallback_dir, filename)
                        await page.screenshot(path=fallback_path)
                        successful_screenshots.append(save_path)

                    await asyncio.sleep(2)

                case "error":
                    print(f"{filename} - failed to load")
                    break

            prev_status = status
            await page.screenshot(path=save_path)

    return successful_screenshots


def _extract_filename_from_url(url: str) -> str:
    """Extracts filename from query parameter 'game_code'."""
    query = parse_qs(urlparse(url).query)
    return f"{query.get('game_code', ['unknown'])[0]}.png"


def _update_counter(status: str, expected_status: str, counter: int) -> int:
    """Resets counter if status changes, otherwise increments."""
    return 0 if status != expected_status else counter + 1


async def _click_around(page, coords: list[tuple[int, int]]):
    """Attempts clicks around given coordinates to handle misaligned buttons."""
    # offsets = [(0, 0), (5, 5), (-5, -5), (-20, -20),
    #            (20, -20), (-20, 0), (20, 0), (0, -20), (0, 20)]

    offsets = [(0, 0), (0, 20)]
    for (x, y) in coords:
        for dx, dy in offsets:
            print(f"click: {x + dx, y + dy}")
            await page.mouse.click(x + dx, y + dy)
