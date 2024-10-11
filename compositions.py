from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from abc import ABC, abstractmethod

import time

class MovieTitleAndStartDate(ABC): 
    
    # Chrome 옵션 설정
    mobile_emulation = {
        "deviceName": "iPhone X"  # 원하는 기기 이름 (예: 'iPhone X', 'Pixel 2')
    }

    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    def __init__(self, url) : 
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 3)
        
        self.driver.get(url); time.sleep(3)
        
    def quit(self) : 
        self.driver.quit()
    
    @abstractmethod
    def _read_movie_title(self) : 
        """
            이벤트 대상 영화의 제목을 읽어온다
        """
        
        pass
    
    @abstractmethod
    def _read_start_date(self) : 
        """
            특정 영화의 이벤트의 시작시간을 읽어온다
        """
        
        pass
    
    @abstractmethod
    def main(self) -> dict : 
        """
            필요한 모든 작업을 한데 모아 실행한다
            
            만약 제목이 겹친다면 최신 시작시간으로 업데이트한다.
            returns 
                {
                    "영화제목" : 이벤트 시작시간
                }
        """
        pass
    
if __name__ == "__main__" : 
     # Chrome 옵션 설정
    mobile_emulation = {
        "deviceName": "iPhone X"  # 원하는 기기 이름 (예: 'iPhone X', 'Pixel 2')
    }

    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    
    driver = webdriver.Chrome(options= chrome_options)
    wait = WebDriverWait(driver, 3)
    
    driver.get("https://www.lottecinema.co.kr/NLCMW/Event/EventTemplateSpeedMulti?eventId=201210016922014")

    while True : 
        time.sleep(1)