#github: mid0aria
import requests
import os
import json
import concurrent.futures

media_type = input("Enter the download type (e.g. waifu, neko, etc.): ")

api_url = f"https://nekos.best/api/v2/{media_type}?amount=21"

downloaded_medias_file = f"{media_type}.json"

medias_folder = media_type

if os.path.exists(downloaded_medias_file):
    with open(downloaded_medias_file, "r") as file:
        downloaded_medias = json.load(file)
else:
    downloaded_medias = []

#github: mid0aria
def download_media(media_url, media_name):
    response = requests.get(media_url)
    if response.status_code == 200:
        with open(f"{medias_folder}/{media_name}", "wb") as file:
            file.write(response.content)
        print(f"[{media_type}] media downloaded: {media_name}")
    else:
        print(f"[{media_type}] media failed to download: {media_url}")


if not os.path.exists(medias_folder):
    os.makedirs(medias_folder)

#github: mid0aria
while True:
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        media_urls = [
            (item["url"], item["url"].split("/")[-1]) for item in data["results"]
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for media_url, media_name in media_urls:
                if media_url not in downloaded_medias:
                    futures.append(
                        executor.submit(download_media, media_url, media_name)
                    )
                    downloaded_medias.append(media_url)

            concurrent.futures.wait(futures)

        with open(downloaded_medias_file, "w") as file:
            json.dump(downloaded_medias, file)
    else:
        print("API could not be accessed")

print("The download is complete.")
#github: mid0aria