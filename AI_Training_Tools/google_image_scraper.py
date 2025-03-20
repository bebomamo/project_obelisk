from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import requests 
import io 
from PIL import Image 
import time  
import os

options = Options()
options.add_argument("--window-size=1920,1080")
wd = webdriver.Chrome(options=options)

def get_images_from_google(wd, delay, max_images): 
    def scroll_down(wd, go_to): 
        ActionChains(wd).move_to_element(go_to).perform()
        # scroll_origin = ScrollOrigin.from_element(go_to,0,-50)
        # ActionChains(turvo_driver).scroll_from_origin(scroll_origin, 0, 800).perform() #Scroll in Widget window
        time.sleep(delay)
    # url = "https://www.google.com/search?sca_esv=8e300a61fb8ea468&rlz=1C1NDCM_enUS754US754&sxsrf=ADLYWIKtzZKOUV5MAQr3nK3erCtWC8gbzA:1731999615121&q=pictures+with+a+white+background&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3J03RPjGV0MznOJ6Likin94qgEKgZsTg4PX84JG3F-btD6HZ96SO26gpHdhe184a4g8SIySIaQxlkbf_9LYdgWhpzG2HznnjoXADuLb0NM_e6Xen2HcRK3rGETQyb9srtJ4jI89f-5cZ59x9f6pQub1F3cWqFOZXe7vUnVGcGRvTWEMXo4g&sa=X&ved=2ahUKEwig0L2u6eeJAxV1j4kEHQgFJHsQtKgLegQIQhAB&biw=1080&bih=1759&dpr=1" 
    # url = "https://www.google.com/search?q=hot+blonde+girl&sca_esv=8e300a61fb8ea468&rlz=1C1NDCM_enUS754US754&udm=2&biw=1080&bih=1759&sxsrf=ADLYWILfmHBLru664ZIx5nxgej21HNAvtA%3A1731999617071&ei=gTc8Z-CBBL_sptQP-eyb8QI&oq=hot+&gs_lp=EgNpbWciBGhvdCAqAggAMgQQIxgnMgQQIxgnMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgsQABiABBixAxiDATIKEAAYgAQYQxiKBUifEFAAWNsBcAB4AJABAJgBWaAB_wGqAQE0uAEByAEA-AEBmAIEoAKOAsICCBAAGIAEGLEDwgIFEAAYgASYAwCSBwE0oAe6Hg&sclient=img"
    url = "https://www.google.com/search?sca_esv=03e995a0e07cb544&rlz=1C1UEAD_enUS961US961&sxsrf=ADLYWIKz5hKA3RvVoCRLUSJ6T3DgNBtJUg:1732061906777&q=cats&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3J7pRxUp2pI1mXV9fBsfh39Jw_Y7pXPv6W9UjIXzt09-YEIs5ATTcnTjDJVNBp4RbjWfOwdDigA7cgGTMAUqYq-XHEDvQBj6Tl1QS1iTN88pVlmn091C3m1whg-P_znMBPc134Mo5pdLl6dOdpk_DVU2P2jhAuxqhhJeiHOdPxH_lV-0F7w&sa=X&ved=2ahUKEwjgprq10emJAxVIv4kEHcHiCxQQtKgLegQIEhAB&biw=1280&bih=598&dpr=1.5"
    wd.get(url) 

    image_urls = set() 
    thumbnails = wd.find_elements(By.CLASS_NAME, "ob5Hkd") 
    skips = 0 
    all_images_found_test = 50
    time.sleep(10) # give a clean amount of time to load the page

    while len(image_urls) + skips < max_images and all_images_found_test > 0: 
        prev_image_urls_count = len(image_urls)
        prev_thumbnails_count = len(thumbnails)
        thumbnails = wd.find_elements(By.CLASS_NAME, "ob5Hkd") 
        if(prev_image_urls_count == len(image_urls) and prev_thumbnails_count == len(thumbnails)):
            all_images_found_test -= 1
            print("Shutting down image search in ", all_images_found_test)
        else:
            print("Thumbnails found: ", len(thumbnails))

        for img in thumbnails[len(image_urls) + skips:max_images]: 
            try: 
                img.click() 
                time.sleep(delay) 
            except: 
                continue 

            images = wd.find_elements(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img') 
            for image in images: #just in case we get multiple zoomed image elements from google for some reason
                if image.get_attribute('src') in image_urls: 
                    max_images += 1 
                    skips += 1 
                    break 
                if image.get_attribute('src') and 'http' in image.get_attribute('src'): 
                    image_urls.add(image.get_attribute('src')) 
                    print(f"Found {len(image_urls)}") 
        scroll_down(wd,thumbnails[-1]) 
    
    if all_images_found_test <= 0:
        print(max_images, " images not found, saving ", len(image_urls), " instead...")
                    
    return image_urls 
            
def download_image(download_path, url, file_name): 
    try: 
        image_content = requests.get(url).content 
        image_file = io.BytesIO(image_content) 
        image = Image.open(image_file)
        file_path = download_path + file_name 
        with open(file_path, "wb") as f: 
            image.save(f, "JPEG") 
        print("Success", end=' ') 
        return True
    except Exception as e: 
        print('FAILED -', e) 
        return False
    
def remove_image(file_path, file_name):
    try:
        os.remove(file_path + file_name)
        print("bad image removed")
    except:
        print("failed to remove bad image")
        
urls = get_images_from_google(wd, .5, 1000) 
        
for i, url in enumerate(urls): 
    success = download_image("cats/", url, str(i) + ".jpg")
    if not success:
        remove_image("cats/", str(i) + ".jpg")
    print(i, end='')
    
wd.quit()