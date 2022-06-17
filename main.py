import os
import time
import csv
import urllib.request
import numpy as np
import argparse
from datetime import datetime
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def save_data_images(dict_images_info, path_file_save, columns_name):
    try:
        with open(path_file_save, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns_name)
            writer.writeheader()
            for data in dict_images_info:
                writer.writerow(data)
    except IOError:
        print("Error save data info images")


class DownloadImagesGoogle:
    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        # options.add_argument("--start-maximized");
        self.driver = webdriver.Chrome(options=options)
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.SLEEPS = [2, 1, 1.5, 1.2]
        self.SLEEPS_2 = [5.7, 6.1, 5.8, 6.2, 5.7, 6.1, 6.2, 6.3]

    def _scroll_down_page(self):
        page_scroll_sleep = 2
        # get height page
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        print("-" * 50)
        print("Scrolling dynamic ...")
        print("-" * 50)
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # wait to load page
            time.sleep(page_scroll_sleep)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                try:
                    button_more_show_results = self.driver.find_elements_by_class_name("r0zKGf")
                    WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                        (By.CLASS_NAME,
                         "r0zKGf")))
                    button_more_show_results[0].click()
                except:
                    try:
                        button_more_show_results = self.driver.find_elements_by_class_name("mye4qd")
                        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                            (By.CLASS_NAME,
                             "mye4qd")))
                        button_more_show_results[0].click()
                    except:
                        break
            last_height = new_height
        print("-" * 50)
        print("Finish scrolling dynamic ...")
        print("-" * 50)

    def routine_simple(self, page, search_text, path=".", limit=0, copyright=False):

        print("-" * 50)
        print("Go to the page ...")
        print(f"Searching {search_text} ...")
        print(f"Max quantity: {limit} images")
        print("-" * 50)

        self.driver.get(page)

        # get element html input search
        input_search = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/input")
        button_search = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/button")
        # send text to input
        input_search.send_keys(search_text)
        button_search.click()

        if not copyright:
            print("No copyright images")
            # get element html tab tools
            tab_tools = self.driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div/div")
            tab_tools.click()

            # get element html tab copy right
            tab_copy_right = self.driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[1]/div/div[5]")
            # wait while is clickable tab_copy_right
            state = True
            while state:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[1]/div/div[5]")))
                    tab_copy_right.click()
                    state = False
                except:
                    pass

            # get element html option licenses creative commons
            option_licenses_creative_commons = self.driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[3]/div/a[1]")
            option_licenses_creative_commons.click()
        else:
            print("With copyright images")

        self._scroll_down_page()

        # get element div items images
        list_items_images = self.driver.find_elements_by_class_name("wXeWr")
        list_items_images_references = self.driver.find_elements_by_class_name("VFACy")

        list_info_image = []

        print("-" * 50)
        print("Routine scrapping ...")
        count = 0
        number_bad_url = 0
        self.driver.execute_script("window.scrollTo(0, 0);")
        if limit != 0:
            try:
                list_items_images = list_items_images[:limit]
                list_items_images_references = list_items_images_references[:limit]
            except:
                print(f"Max number images is: {len(list_items_images)}")
        for child_item_image, child_item_image_reference in tqdm(zip(list_items_images, list_items_images_references
                                                                     )):

            image_element = child_item_image.find_element_by_class_name("rg_i")

            description = image_element.get_attribute("alt").replace("|", '')
            url_reference = child_item_image_reference.get_attribute("href").replace("|", '')
            location = child_item_image.location
            x_position = location['x']
            y_position = location['y']
            self.driver.execute_script(f"window.scrollTo({x_position}, {y_position});")
            try:
                child_item_image.click()
            except:
                continue
            image_container = self.driver.find_elements_by_class_name("v4dQwb")

            # Google image web site logic
            try:
                if count == 0:
                    image = image_container[0].find_element_by_class_name('n3VNCb')
                else:
                    image = image_container[1].find_element_by_class_name('n3VNCb')
            except:
                continue

            count += 1

            time.sleep(np.random.choice(self.SLEEPS_2))

            url_image = image.get_attribute('src').replace('|', '')


            # verification about image link
            if not ((url_image.find("encrypted-tbn0") < 0) and (url_image.find("http") >= 0)):
                number_bad_url += 1
                #print("bad url")
                url_image = None
                """child_item_image.click()
                image_container = self.driver.find_elements_by_class_name("v4dQwb")

                # Google image web site logic
                try:
                    image = image_container[1].find_element_by_class_name('n3VNCb')
                except:
                    image = image_container[0].find_element_by_class_name('n3VNCb')

                count += 1
                time.sleep(np.random.choice(self.SLEEPS_2))
                url_image = image.get_attribute('src').replace('|', '')
                cont_aux -= 1"""

            if url_image is not None:
                list_info_image.append(
                    {"url_image": url_image,
                     "url_ref": url_reference,
                     "description": description})

        print(f"Number bad urls: {number_bad_url}")
        print(f"Number ok urls: {len(list_info_image)}")

        print("Finish Routine scrapping ...")
        print("-" * 50)

        print("-" * 50)

        path = f"{path}/{search_text}"
        print(f"Creating folder {search_text}")
        print("-" * 50)
        os.mkdir(path)
        print("-" * 50)
        print(f"Created folder {search_text}")
        print("-" * 50)

        print("-" * 50)
        print("Saving info images")
        print("-" * 50)

        today = datetime.now()
        today_string = today.strftime("_%d_%m_%Y-%H_%M_%S")
        save_data_images(dict_images_info=list_info_image,
                         path_file_save=f"{path}/info_images_{search_text}_{today_string}.csv",
                         columns_name=['url_image', 'url_ref', 'description'])

        print("-" * 50)
        print("Saved info images correctly")
        print("-" * 50)

        print("-" * 50)
        print("Downloading images ...")
        number_download_bad = 0

        for i, image in enumerate(tqdm(list_info_image)):
            state = False
            count_aux = 5
            while not state:
                if count_aux <= 0:
                    number_download_bad += 1
                    break
                time.sleep(np.random.choice(self.SLEEPS))
                state = self._download_image(image['url_image'], f"{path}/{i}. {image['description'].replace('.', '')[:50]}.jpeg")
                #print(f"entra {count_aux}")
                count_aux -= 1

        print(f"Images download bad: {number_download_bad}")
        print(f"Images download ok: {len(list_info_image) - number_download_bad}")
        print("Images download correctly")
        print("-" * 50)

    def _download_image(self, url_image, path_image):
        try:
            request_help = urllib.request.Request(url=url_image, headers={'User-Agent': 'Mozilla/5.0'})
            request = urllib.request.urlopen(request_help, timeout=5)
            with open(path_image, 'wb') as f:
                try:
                    f.write(request.read())
                    time.sleep(np.random.choice(self.SLEEPS))
                    return True
                except:
                    return False
            # urllib.request.urlretrieve(url_image, path_image)
        except:
            return False

    def routine_multiple(self, page, list_search_texts, path=".", limit=0, copyright=False):
        for search_text in list_search_texts:
            self.routine_simple(page, search_text, path=path, limit=limit, copyright=copyright)

    def __del__(self):
        self.driver.close()


parser = argparse.ArgumentParser()
parser.add_argument("-page", "-p", type=str, help="page google images in where to search")
parser.add_argument("-path_saved", "-d", type=str, help="page google images in where to search")
parser.add_argument("-list_searching_texts", "-s", nargs="+", help="texts to search in google images")
parser.add_argument("-limit", "-l", type=int, help="limit download images", default=0)
parser.add_argument("-copyright", "-c", help="With this option the images has copyright", action="store_true", default=True)

args = parser.parse_args()

page_google = args.page
list_searching_texts = args.list_searching_texts
copyright_option = args.copyright
path_saved = args.path_saved
limit_images = args.limit


download_google_images = DownloadImagesGoogle()
download_google_images.routine_multiple(page=page_google, list_search_texts=list_searching_texts, path=path_saved, limit=limit_images, copyright=copyright_option)


#download_google_images.routine(page="https://www.google.com.co/imghp?hl=es-419&authuser=0&ogbl",
#                                   search_text="conflicto armado", path="./images")

#  python main.py -p "https://www.google.com.co/imghp?hl=es-419&authuser=0&ogbl" -d ./images -s "conflicto armado en colombia" -l 5 -c

