[05/06 2:46 am] Vishal Anand
    
try:
    driver.close()
except:
    print("No browsers open")


from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("start-maximized")
options.add_argument('--no-sandbox')



driver = webdriver.Chrome(chrome_options=options, executable_path=r'/Users/visanand2/Downloads/chromedriver')


driver.get("https://www.crunchbase.com/home")



username = 'add username'
password = 'add password'


driver.find_element_by_xpath("//span[contains(text(),'Log In')]").click()


driver.find_element_by_xpath("//input[@id='mat-input-1']").send_keys(username)
driver.find_element_by_xpath("//input[@id='mat-input-2']").send_keys(password)


driver.find_element_by_xpath(
    "//button[@type='submit']//span[@class='mat-button-wrapper'][normalize-space()='Log In']").click()


driver.find_element_by_xpath("//span[contains(text(),'Advanced Search')]").click()
driver.find_element_by_xpath("//span[normalize-space()='Companies']").click()


time.sleep(2)
driver.refresh()




industries =   ['Administrative Services',
                'Advertising',
                'Agriculture Farming',
                'Apps',
                'Artificial Intelligence',
                'Biotechnology',
                'Clothing and Apparel',
                'Commerce and Shopping',
                'Community and Lifestyle',
                'Consumer Electronics',
                'Consumer Goods',
                'Content and Publishing',
                'Data and Analytics',
                'Design',
                'Education',
                'Energy',
                'Events',
                'Financial Services',
                'Food and Beverage',
                'Gaming',
                'Government and Military',
                'Hardware',
                'Health Care',
                'Information Technology', 
                'Internet Services',
                'Lending and Investments',
                'Manufacturing',
                'Media and Entertainment',
                'Messaging and Telecommunications',
                'Mobile',
                'Music and Audio',
                'Natural Resources',
                'Navigation and Mapping',
                'Other',
                'Payments',
                'Platforms',
                'Privacy and Security',
                'Professional Services',
                'Real Estate',
                'Sales and Marketing',
                'Science and Engineering',
                'Software',
                'Sports',
                'Sustainability',
                'Transportation',
                'Travel and Tourism',
                'Video']


years = ["2020","2019"], "2020", "2019", "2018", "2017", "2016", "2015"]
soup_list = []
for industry in industries:
    for year in years:
        duration = driver.find_elements_by_class_name("mat-radio-label")
        duration[4].click()
        time.sleep(1)
        
        driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[1]/div[1]/mat-accordion/mat-expansion-panel[1]/div/div/div[5]/advanced-filter/filter-date-range/div/div[1]/mat-form-field[1]/div/div[1]/div[3]/input").send_keys(year)
        driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[1]/div[1]/mat-accordion/mat-expansion-panel[1]/div/div/div[5]/advanced-filter/filter-date-range/div/div[1]/mat-form-field[2]/div/div[1]/div[3]/input").send_keys(year)
        
        driver.find_element_by_xpath("//input[@id='mat-input-3']").send_keys(industry)
        time.sleep(1)
        
        radio_btn = driver.find_elements_by_class_name('mat-list-item-content')
        
        if len(radio_btn) == 1:   
            driver.find_element_by_xpath("html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[1]/header/button").click()
            time.sleep(1)
            continue
        
        radio_btn[0].click()  
        time.sleep(1)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser") 
        
        results = soup.find_all("h3", {​​​​​​​"class": "component--results-info"}​​​​​​​)[1].text
        results = results.replace(',', '')
        results_num = [int(s) for s in results.split() if s.isdigit()][0]
        
        iterations = int(min(results_num/50,20))
        
        soup_list.append(soup)
        
        for i in range(iterations):
            # click next
            driver.find_element_by_xpath("/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[2]/results/div/div/div[1]/div/results-info/h3/a[2]/span[1]/div/span").click()            
            # extract soup
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, features="html.parser") 
        
            soup_list.append(soup)
            
            
        # next loop 
        
        #TODO: if null in next then still save the soup 
        #clear
        driver.find_element_by_xpath("html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[1]/header/button").click()
        time.sleep(1)



from tqdm import tqdm
df = pd.DataFrame()
for soup in tqdm(soup_list):
    #soup = soup_list[2]
    row_length = len(soup.select('grid-row'))
    
    for i in range(row_length):
        row = soup.select('grid-row')[i]
        company_name = row.find_all('grid-cell')[1].find('div',
                                                         class_='flex-no-grow cb-overflow-ellipsis identifier-label').text
        try:
            website = row.find_all('grid-cell')[7].find(href=True)['href']
        except:
            website = "Na"
        try:
            description = row.find_all('grid-cell')[5].find("span")["title"]
        except:
            description = "Na"
        try:
            funding = row.find_all('grid-cell')[8].find("a").contents[0]
        except:
            funding = "Na"
        
        #print(company_name)
        data = {​​​​​​​'company_name': company_name, 'description': description, "website": website, "funding": funding}​​​​​​​
        temp_df = pd.Series(data).to_frame().T
        df = df.append(temp_df)
        















