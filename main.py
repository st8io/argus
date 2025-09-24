from typing import List, Optional
from playwright.async_api import async_playwright

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import cleaner
import image_processing
import prompt
from screenshotter import take_screenshots

app = FastAPI()

class GameCodesRequest(BaseModel):
    game_codes: List[str]
    generate_themes: Optional[bool] = False


class GameScreenshotRequest(BaseModel):
    game_code: str
    screenshot: str


@app.post("/process/butch")
async def process_game_codes(request: GameCodesRequest):
    urls = [
        f"https://megaplays.net/launch?operator_code=test002&game_code={code}&fun_mode=true"
        for code in request.game_codes
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        screenshots = await take_screenshots(browser, urls)
        await browser.close()

    if request.generate_themes:
        themes_dict = {}
        for filename in screenshots:
            based_image = image_processing.encode_image(filename)
            themes_dict[filename.split("/")[-1].split(".")[0]] = prompt.get_themes(based_image)

        print(themes_dict)
        data = cleaner.format(themes_dict)
        # TODO: save screenshots in the bucket
        return {"screenshots": screenshots, "data": data}

    return {"screenshots": screenshots}


@app.post("/process/screenshot")
async def process_screenshot(request: GameScreenshotRequest):
    themes_dict = {request.game_code: prompt.get_themes(request.screenshot)}
    data = cleaner.format(themes_dict)
    return {"themes": data}

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*pin_memory.*")
    uvicorn.run(app, host="0.0.0.0", port=8000)