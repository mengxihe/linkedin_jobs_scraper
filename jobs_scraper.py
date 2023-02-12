#Import Packages
from selenium import webdriver
import time
import pandas as pd
import os
#Import Packages
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#go to linkedin log in page
url1 = 'https://www.linkedin.com/login'
service = Service(executable_path='path/to/chromdriver')
driver = webdriver.Chrome(service=service)
driver.get(url1)
time.sleep(2)


#accept the terms 
driver.find_element(By.XPATH, '//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]').click()
#login with your user_credentials
with open('user_credentials.txt', 'r',encoding="utf-8") as file:
    user_credentials = file.readlines()
    user_credentials = [line.rstrip() for line in user_credentials]
user_name = user_credentials[0] # First line
password = user_credentials[1] # Second line
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user_name)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
time.sleep(1)

# click Login button
driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Access to the Jobs button and click it
driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a/span').click()
time.sleep(3)
# Go to search results directly via link
executable_link = "Link to your linkedin job search result"
driver.get(executable_link)
time.sleep(3)

#start empty list to collect all the jobs links: scroll down and click the next page, this clicks through 2-14 
links = []
print('Links are being collected now.')
try:
    for page in range(2, 14):
        time.sleep(2)
        jobs_block = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME, 'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        print(f'Collecting the links in the page: {page-1}')
        #go to next page:
        driver.find_element(By.XPATH, f"//button[@aria-label='Page {page}']").click()
        time.sleep(3)
except:
    pass

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []

i = 0 
j = 1
#Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i = i+1
        time.sleep(4)
        # Click the See more button.
        driver.find_element(By.CLASS_NAME, "artdeco-card__actions").click()
        time.sleep(2)
    except:
        pass

    contents = driver.find_elements(By.CLASS_NAME, 'p5')
    for content in contents:
        try:
            job_titles.append(content.find_element(By.TAG_NAME, "h1").text)
            company_names.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/li[1]").text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+= 1
        except:
            pass
        time.sleep(2)
    job_description = driver.find_elements(By.CLASS_NAME, "jobs-description__content")
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME, "jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(2)


# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names, company_locations,work_methods,post_dates,work_times)),
columns =['job_title', 'company_name','company_location','work_method','post_date','work_time'])
# Storing the data to csv file
df.to_csv('job_offers.csv', index=False)
# Output job descriptions to txt file
with open('job_descriptions.txt', 'w',encoding="utf-8") as f:
    for line in job_desc:
        f.write(line)
        f.write('\n')