from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, traceback, re

from compositions import MovieTitleAndStartDate

class LotteCinema(MovieTitleAndStartDate) : 

    # Chrome 옵션 설정
    mobile_emulation = {
        "deviceName": "iPhone X"  # 원하는 기기 이름 (예: 'iPhone X', 'Pixel 2')
    }

    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
        
    def __init__(self, url, site) : 

        super().__init__(site)
        
        self.driver.get(url); time.sleep(3)

    def quit(self) : 
        self.driver.quit()
    
    def _read_movie_title(self) : 
        try:
            elements  = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "wordcut2"))
            )        

        except Exception as e:
            print(f"영화 제목을 읽어오는 중 오류 발생: {e}")
            print(traceback.format_exc())
            
        return [element.get_attribute("textContent") for element in elements]
    
    def _read_start_date(self) : 
        try:
            # 주어진 클래스에서 요소를 찾기
            info_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.info_top.type2 span.roboto'))
            )
            
            # 찾은 요소들의 텍스트값 읽어오기
            texts = [element.text for element in info_elements]
            full_text = ' '.join(texts)
            
            full_text = full_text.strip()
            
            match = re.search(r'(\d{2})/(\d{2}) (\d{2})', full_text)
            
            if match:
                month = match.group(1)
                day = match.group(2)
                hour = match.group(3)
                
                # 원하는 형식으로 변환 (예: 10-08 16시)
                formatted_str = f"{month}-{day} {hour}시"
                return formatted_str
            else:
                return "형식에 맞는 날짜와 시간이 없습니다."

        except Exception as e:
            print(f"영화 제목을 읽어오는 중 오류 발생: {e}")
            print(traceback.format_exc())
            
    def _click_left_arrow(self) : 
        try:
            # 이전 슬라이드 버튼을 찾고 클릭하기
            prev_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "swiper-button-prev"))
            )
            # 자바스크립트로 클릭
            self.driver.execute_script("arguments[0].click();", prev_button)
        except Exception as e:
            raise Exception("버튼 클릭 오류:", e)
            
    def _click_right_arrow(self) : 
        try:
            # 다음 슬라이드 버튼을 찾고 클릭하기
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "swiper-button-next"))
            )
            # 자바스크립트로 클릭
            self.driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            raise Exception("버튼 클릭 오류:", e)
            
    def main(self) :
        
        # 1. 영화 제목을 읽어온다.
        movie_titles = self._read_movie_title()
        
        # 2. 영화의 시작 시간을 읽어온다.
        # 왼쪽 화살표 비활성화될 때까지 클릭
        for _ in range(len(movie_titles)) :
            
            try : 
                self._click_left_arrow()
                time.sleep(1)
                
            except Exception : 
                break
        
        print("왼쪽 화살표 클릭 완료")
        
        # 시작 시간 읽어오기
        start_date = []
        
        
        for _ in range(len(movie_titles)) :
            
            # 시작 시간 읽어오기
            start_date.append(self._read_start_date())
            
            # 오른쪽 화살표가 비활성화될 때까지 클릭
            try : 
                self._click_right_arrow()
                time.sleep(1)
                
            except Exception : 
                break
        
        return dict(zip(movie_titles, start_date))
    
class MegaBox(MovieTitleAndStartDate) : 

    chrome_options = Options()

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 3)

    def __init__(self, url, site) : 

        super().__init__(site)
        
        self.driver.get(url); time.sleep(3)

        self.event_list = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-list"))
        )

    def quit(self) : 
        self.driver.quit()

    def _read_movie_title(self):

        titles = self.event_list.find_elements(By.CLASS_NAME, 'tit')

        return [title for title in titles]

    def _read_start_date(self):
        
        dates = self.event_list.find_elements(By.CLASS_NAME, 'date')

        return [(date.text).split('~')[0].strip() for date in dates]

    def main(self) -> dict : 
        
        movie_titles = self._read_movie_title()

        start_dates = self._read_start_date()

        _dict = dict(zip(movie_titles, start_dates))

        result = {e.text.split(']')[0].strip('[') : _dict.get(e) for e in _dict if '빵원티켓' in e.text}

        return result
                
if __name__ == "__main__" :
    lottecinma = LotteCinema(url = "https://www.lottecinema.co.kr/NLCMW/Event/EventTemplateSpeedMulti?eventId=201210016922014", 
                             site = "LotteCinema")

    print(lottecinma.main())

    # megabox = MegaBox(url = "https://megabox.co.kr/event/movie", 
    #                   site = "MegaBox")
    
    # print(megabox.main())
    
    
    


    
# 화면을 보면 
# 1. 왼쪽 화살표가 비활성화될 때까지 왼쪽 화살표를 클릭한다.
# 2. 해당 화면에서 시작 시간을 읽어온다.
# 3. 오른쪽 화살표를 클릭한다.
# 4. 2-3번 과정을 오른쪽 화살표가 비활성화될 때까지 반복한다.
                     

