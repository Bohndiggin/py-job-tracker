import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('C:/Users/bohnd\Documents/_codingProjects/chromedriver_win32/chromedriver.exe')



def job_hunter():
    pass

def indeed_api_boi(client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }
    acces_token = requests.request(method="POST", url='https://apis.indeed.com/oauth/v2/tokens', headers=headers, data=body).json()
    return acces_token

async def indeed_spider():
    driver.get('https://indeed.com/')
    search_bar = driver.find_element_by_xpath("//html/body/div/div[1]/div/span/div[4]/div[1]/div/div/div/div/form/div/div[1]/div/div[1]/div/div[2]/input")
    search_bar.send_keys('')
    search_bar.send_keys(Keys.ENTER)
    result_count = 0
    descriptions = []
    for j  in range(3):
        for i in range(20):
            try:
                first_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[{i + 1}]'))
                )
                # need better way to locate jobs
                result = driver.find_elements_by_class_name("jobTitle")[i]
            except:
                break
            try:
                await asyncio.sleep(2)
                result.click()
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'jobDescriptionText'))
                )
                job_description = driver.find_element(By.ID, 'jobDescriptionText')
                
                salary_info_job_type = driver.find_element(By.ID, 'salaryInfoAndJobType')
                try:
                    job_title = driver.find_element(By.XPATH, '//html/body/main/div/div[1]/div/div/div[5]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/h1')
                    descriptions.append([job_title.text.replace('\n', '').replace(',', '').encode('ascii', 'ignore'), salary_info_job_type.text.replace('\n', '').replace(',', '').encode('ascii', 'ignore'), job_description.text.replace('\n', '').replace(',', '').encode('ascii', 'ignore')])
                except:
                    job_title = 'empty'
                    print('unable to locate job_title')
                    descriptions.append([job_title, salary_info_job_type.text.replace('\n', '').replace(',', '').encode('ascii', 'ignore'), job_description.text.replace('\n', '').replace(',', '').encode('ascii', 'ignore')])
                driver.execute_script('window.scrollTo(0, 3000)')
                result_count += 1
            except Exception as e:
                print(e)
                continue
            print(result_count)
        await asyncio.sleep(10)
        driver.find_element(By.XPATH, '//a[@aria-label="Next Page"]').click()

    with open('results.csv', 'w', newline='') as results_csv:
        result_file = csv.writer(results_csv, delimiter=',')
        for i in descriptions:
            result_file.writerow(i)
    # result = driver.find_element_by_xpath(f"//html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul/li[1]")
    # result.click()
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, 'jobDescriptionText'))
    # )
    # description = driver.find_element_by_xpath('//html/body/main/div/div[1]/div/div/div[5]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div[6]')
    # print(description.text)

asyncio.run(indeed_spider())


