from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# CGV는 다른 사이트와 달리 영화 제목들이 전부 image로 표현되어 있다.
# 텍스트로 저장되어 있지 않다는 것이다. 

# Tesseract라는 도구를 사용해야 할 것 같다. 
# 이미지에서 텍스트를 읽어오기
