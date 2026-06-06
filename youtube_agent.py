import os, json, time, random, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
from moviepy import ImageClip

COOKIES = os.getenv("YOUTUBE_COOKIES")

def sanitize_cookies(raw):
    valid = {"Strict","Lax","None"}
    cleaned = []
    for c in raw:
        new = {"name":c.get("name",""),"value":c.get("value",""),"domain":c.get("domain",""),
               "path":c.get("path","/"),"secure":c.get("secure",False),"httpOnly":c.get("httpOnly",False)}
        s = c.get("sameSite","Lax")
        new["sameSite"] = s if s in valid else "Lax"
        if not c.get("session") and "expirationDate" in c:
            new["expires"] = float(c["expirationDate"])
        cleaned.append(new)
    return cleaned

def create_video():
    img = Image.new("RGB",(1920,1080),(random.randint(0,255),)*3)
    d = ImageDraw.Draw(img)
    for _ in range(100):
        x1,x2 = sorted([random.randint(0,1920),random.randint(0,1920)])
        y1,y2 = sorted([random.randint(0,1080),random.randint(0,1080)])
        d.rectangle([x1,y1,x2,y2],fill=(random.randint(0,255),)*3)
    img_path = os.path.join(tempfile.gettempdir(),"yt_thumb.png")
    img.save(img_path)
    clip = ImageClip(img_path, duration=10)
    video_path = os.path.join(tempfile.gettempdir(),"yt_video.mp4")
    clip.write_videofile(video_path, fps=24, logger=None)
    return video_path

def main():
    if not COOKIES:
        return
    cookies = sanitize_cookies(json.loads(COOKIES))
    topics = ["crypto news","Bitcoin update","Ethereum trends","AI technology","passive income"]
    topic = random.choice(topics)
    title = f"Today's {topic.title()} – Quick Update"
    description = f"{topic} continues to evolve. Stay updated!\n\n#crypto #passiveincome #ai"
    video_path = create_video()

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(cookies)
        pg = ctx.new_page()
        pg.goto("https://studio.youtube.com", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector("ytcp-button#create-icon", timeout=30000)
        pg.click("ytcp-button#create-icon")
        pg.click("tp-yt-paper-item:has-text('Upload video')")
        pg.set_input_files("input[type='file']", video_path)
        time.sleep(3)
        pg.fill("div#title-textarea", title)
        pg.fill("div#description-container #description-textarea", description)
        pg.click("tp-yt-paper-radio-button:has-text('No, it's not made for kids')")
        time.sleep(1)
        for _ in range(3):
            pg.click("ytcp-button#next-button")
            time.sleep(1)
        pg.click("tp-yt-paper-radio-button:has-text('Public')")
        pg.click("ytcp-button#done-button")
        time.sleep(5)
        b.close()

if __name__ == "__main__":
    main()
