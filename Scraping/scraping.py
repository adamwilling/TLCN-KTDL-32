# khai báo thư viện
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Khai báo biến url gốc
url = 'https://www.nhatot.com'

# Đọc file csv chứa danh sách các url
list_of_urls = pd.read_csv('data/new_url.csv', header=None, names=['url'])
# Tạo list chứa các url mới
new_link = list_of_urls[:]

# Thêm url gốc vào list
new_urls = []
for path in new_link['url']:
    new_url = url + path 
    new_urls.append(new_url)

# Vòng lặp để lấy dữ liệu từ trang web
for links in new_urls:
    driver = webdriver.Chrome()
    driver.get(links)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data_list = []
    house_info = soup.find('div', class_ = 'DetailView_adviewCointainer__rdzwn')
    for data in house_info:
        house_name = house_info.find('h1', class_ = 'AdDecriptionVeh_adTitle__vEuKD')
        if house_name is not None:
            house_name=house_name.text
        else:
            house_name = 'N/A'
        address = house_info.find('span', class_ = "fz13")
        if address is not None:
            address = address.text.replace('Xem bản đồ','')
        else:
            address = 'N/A'
        price = house_info.find('span', itemprop = 'price')
        if price is not None:
            price = price.text.split('-')[0]
        else:
            price = 'N/A'
        house_area = house_info.find('span', class_ = 'AdDecriptionVeh_squareMetre__eG8lb')
        if house_area is not None:
            house_area = house_area.text
        else:
            house_area = 'N/A'
        status = house_info.find('span', itemprop = 'property_status')
        if status is not None:
            status = status.text
        else:
            status = 'N/A'
        price_m2 = house_info.find('span', itemprop = 'price_m2')
        if price_m2 is not None:
            price_m2 = price_m2.text
        else:
            price_m2 = 'N/A'
        bedroom = house_info.find('span', itemprop = 'rooms')
        if bedroom is not None:
            bedroom = bedroom.text
        else:
            bedroom = 'N/A'
        apartment_type = house_info.find('span', itemprop = 'apartment_type')
        if apartment_type is not None:
            apartment_type = apartment_type.text
        else:
            apartment_type = 'N/A'
        project = house_info.find('span', class_ = 'AdParam_adParamValue__IfaYa')
        if project is not None:
            project = project.text.replace("Nhấn để xem thông tin về dự án được sàng lọc uy tín và sát sao nhất thị trường","")
        else:
            project = 'N/A'
        description = house_info.find('p', class_= 'styles_adBody__vGW74')
        if description is not None:
            description = description.text
        else:
            description = 'N/A'
    data_list.append([house_name,address,price,house_area,status,price_m2,bedroom,apartment_type,project,description])
    driver.quit()
    df_house = pd.DataFrame(data_list)
    df_house.to_csv('House_.csv', mode='a', index=False, header=False)
