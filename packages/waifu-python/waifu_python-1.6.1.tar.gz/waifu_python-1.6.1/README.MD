# WAIFU-PYTHON

A project born out of boredom, designed to simplify and reduce the code related to the Waifu API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **waifu-python**.

```bash
pip install waifu-python
```

## API Included

- [Waifu.im](https://www.waifu.im/)
- [Waifu.pics](https://waifu.pics/)  
- [Nekos.best](https://nekos.best/) 
- [Pic.re](https://pic.re/)  
- [Purrbot.site](https://purrbot.site/)  
- [N-sfw.com](https://n-sfw.com/)

## Usage

```python
import asyncio
from waifu_python import WaifuIm

async def main():

    image_data1 = await WaifuIm.fetch_sfw_images()
    #support for tags in args 
    image_data2 = await WaifuIm.fetch_sfw_images('raiden-shogun')
    #retrive tags for the API
    tags = await WaifuIm.get_tags()

    print(f"Random Image{image_data1}\n\nRaiden Shogun{image_data2}\n\nTags{tags}")

asyncio.run(main())
```

## Example 1

```python
import asyncio
from waifu_python import WaifuIm
from waifu_python import NekosBest
from waifu_python import WaifuPics
from waifu_python import PicRe
from waifu_python import PurrBot
from waifu_python import NSFWBot


async def main():

#-----------------SFW-----------------


    image_data1 = await WaifuIm.fetch_sfw_images()
    image_data2 = await NekosBest.fetch_sfw_images()
    image_data3 = await WaifuPics.fetch_sfw_images()
    image_data4 = await PicRe.fetch_sfw_images()
    image_data5 = await NSFWBot.fetch_sfw_images()
    image_data6 = await PurrBot.fetch_sfw_images()


#-----------------NSFW -----------------


    image_data11 = await WaifuIm.fetch_nsfw_images()
    image_data33 = await WaifuPics.fetch_nsfw_images()
    image_data55 = await NSFWBot.fetch_nsfw_images()
    image_data66 = await PurrBot.fetch_nsfw_gif()


#-------------------TAGS-----------------

    image_data111 = await WaifuIm.get_tags()
    image_data222 = await NekosBest.get_tags()
    image_data333 = await WaifuPics.get_tags()
    image_data444 = await PicRe.get_tags()
    image_data555 = await NSFWBot.get_tags()
    image_data666 = await PurrBot.get_tags()


#-------------------GIF------------- ----


# WAIFU.PICS
# NEKO.BEST
# PURRBOT

    print(f"SFW\n\n{image_data1}\n{image_data2}\n{image_data3}\n{image_data4}\n{image_data5}\n{image_data6}\n\nNSFW\n\n{image_data11}\n{image_data33}\n{image_data55}\n{image_data66}")
    #\n\nTAGS\n\n{image_data111}\n\n{image_data222}\n\n{image_data333}\n\n{image_data444}\n\n{image_data555}\n\n{image_data666}") 

#---TAGs mightbe overwhelming....

asyncio.run(main())
```

## Example 2 (TELEGRAM BOT)

```python
from pyrogram import Client, filters
from waifu_python import WaifuIm

app = Client("Raiden", api_id="API_ID", api_hash="API_HASH", bot_token="BOT_TOKEN")

@app.on_message(filters.command("sfw"))
async def send_sfw_image(client, message):
    
    command = message.text.split()
    tag = command[1] if len(command) > 1 else None
    try:
        image_url = await WaifuIm.fetch_sfw_images(tag)
        if image_url:
            await message.reply_photo(image_url)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@app.on_message(filters.command("nsfw"))
async def send_nsfw_image(client, message):
    command = message.text.split()
    tag = command[1] if len(command) > 1 else None
    try:
        image_url = await WaifuIm.fetch_nsfw_images(tag)
        if image_url:
            await message.reply_photo(image_url)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    app.run()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
