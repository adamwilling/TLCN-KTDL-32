# Khai báo thư viện
from selenium import webdriver
from bs4 import BeautifulSoup
from csv import writer
import time

# Khai báo biến start và end để lấy dữ liệu từ phạm vi xác định
start = 1 
end = 457

# Khai báo biến base_url với tham số trang 
base_url = "https://www.nhatot.com/mua-ban-can-ho-chung-cu-tp-ho-chi-minh?fbclid=IwAR0SgwuK99ZxStbKCt3PmFqY5UisKvatRsu2JEnu5c5y2GvQhhzH7KBGqLI&page=*"

# Vòng lặp để lấy dữ liệu từ trang web
for i in range(start,end+1):

    # Thay thế tham số trang vào base_url
    url = base_url.replace("*",str(i))

    # Khai báo biến driver để mở trình duyệt Chrome
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # Scroll tới cuối trang để lấy dữ liệu 
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    
        time.sleep(3) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    href_web = soup.find("div", class_ = 'container pty-container ct-listing')

    # Lưu dữ liệu vào file csv
    with open('new_url.csv', 'a', encoding='utf-8', newline='') as f:
        csv_writer = writer(f)
        for link in href_web.find_all('a', class_ = 'AdItem_adItem__gDDQT'): 
            href = link.get('href')
            if href:
                csv_writer.writerow([href])

    # Đóng trình duyệt Chrome
    driver.quit()