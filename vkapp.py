import json
import requests
from pprint import pprint  
import time  
from tqdm import tqdm

with open("requirements.txt","r", encoding="utf-8") as f:
    file = f.read().split("\n")
vk_token = file[0]
vk_url = file[1]
yandex_token = file[2]
ya_url = file[3]
my_id = file[4]


class VkUserPhoto():       
    def __init__(self, token, version, owner_id):
        self.params = {
            "access_token" : token,
            "v" : version,
            "album_id" : "profile",
            "extended" : "1",
            "owner_id" : owner_id
        }
    def get_photos(self, vk_url):
        url_get_photos = vk_url + "photos.get?"
        req = requests.get(url_get_photos, params=self.params).json()
        return req

    def create_inf_file(self):
        photo_dict = self.get_photos(vk_url)
        photo_information = []
        for ind, i in enumerate(tqdm(photo_dict["response"]["items"])):
            photos = {"file_name" : str(photo_dict["response"]["items"][ind]['likes']["count"]) + '.jpg'}  
            for key, value in photo_dict["response"]["items"][ind]['sizes'][-1].items():
                if key == "type":
                    photos.update(type = value)
                    photo_information.append(photos)
                    time.sleep(0.4)        
        with open("photo_information.json", 'w') as outfile:
            json.dump(photo_information, outfile)   
            
    def get_url_photo(self):
        photo_dict = self.get_photos(vk_url)
        photo_url = []
        for ind, i in enumerate(tqdm(photo_dict["response"]["items"])):            
            photos = photo_dict["response"]["items"][ind]['sizes'][-1]["url"]
            photo_url.append(photos) 
            time.sleep(0.4)
        return ", ".join(photo_url)

    def get_name_folder(self):
        photo_dict = self.get_photos(vk_url)
        return photo_dict["response"]["items"][0]["owner_id"]  

    def get_zip_name_url(self):
        photo_dict = self.get_photos(vk_url)
        photo_information = []
        for ind, i in enumerate(tqdm(photo_dict["response"]["items"])):
            url = []
            name = []  
            for key, value in photo_dict["response"]["items"][ind]['sizes'][-1].items():                
                    if key == "url":
                        url.append(value)
                        name.append(str(photo_dict["response"]["items"][ind]['likes']["count"]) + '.jpg')
                        photo_information.append(*list(zip(name, url)))
                        time.sleep(0.4)
        return photo_information

class YandexUploader():
    def __init__(self, token, url):
        self.token = token
        self.url = url

    def create_new_folder(self):
        headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {
            "path" : f"/{my_vk_page.get_name_folder()}"
        }
        req = requests.put(ya_url, headers = headers, params = params)
        return req.json

    def upload_from_vk(self, path_to_file, url):
        headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {
            'url' : url,
            'path' : path_to_file, 
            "overwrite": "true",
        }
        response = requests.post(self.url, headers = headers, params = params)
        # response.raise_for_status()

# my_vk_page.create_inf_file() #имя загружаемого файла
# my_vk_page.get_zip_name_url() #URL загружаемого файла 
# my_vk_page.get_name_folder() # название папки для яндекс диска

my_vk_page = VkUserPhoto(vk_token, 5.131, my_id)
ya_upload = YandexUploader(yandex_token , ya_url + "/upload")  
ya_create_folder = YandexUploader(yandex_token , ya_url)
ya_create_folder.create_new_folder()
for name_, url_ in tqdm(my_vk_page.get_zip_name_url()):   
    count_ = 0
    if count_ < 5:
        ya_upload.upload_from_vk(f"{my_vk_page.get_name_folder()}/{name_}" , url_)
        time.sleep(1)
        count_ += 1