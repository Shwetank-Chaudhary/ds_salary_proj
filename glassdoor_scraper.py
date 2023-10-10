
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
from playsound import playsound


def get_jobs(keyword, num_jobs, verbose,slp_time):
    print("GETTING JOB INFO")
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    #driver = webdriver.Chrome(executable_path="D:/Microsoft Downloads/chromedriver-win64/chromedriver-win64/chromedriver", options=options)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(3)

        #Test for the "Sign Up" prompt and get rid of it.
        # link: https://www.selenium.dev/documentation/webdriver/elements/finders/
        try:
            #driver.find_element(By.CLASS_NAME,"selected").click()
            driver.find_element(By.XPATH,'.//div[@id = "LoginModal"]')
            print("Found SELECTED")
        except ElementClickInterceptedException:
            print("FAILED TO FIND SELECTED")
            pass

        time.sleep(1)

        try:
            driver.find_element(By.XPATH,".//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()  #clicking to the X.
            #https://stackoverflow.com/questions/54939227/how-to-click-the-close-button-within-a-modal-window-through-selenium-and-python
            #WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']"))).click()
            print("FOUND X")
        except NoSuchElementException:
            print("FAILED to find X")

        
        #Going through each job in this page
        #job_buttons = driver.find_elements(By.XPATH,'//div[@class="job-search-193lseq"]')  #jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.XPATH,'//li[@class="JobsList_jobListItem__JBBUV"]')
        print("Jobs FOund: ",len(job_buttons))
        #print(job_buttons)
        for job_button in job_buttons:  
            
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(2)
            collected_successfully = False
            flag=0
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH,'.//div[@class="css-8wag7x"]').text
                    #print(rating)
                    #print("Compant NAme: " , company_name)
                    location = driver.find_element(By.XPATH,'.//div[@data-test="location"]').text
                    #print("Location: ",location)
                    job_title = driver.find_element(By.XPATH,'.//div[@class="JobDetails_jobTitle__Rw_gn"]').text
                    #print("job title",job_title)
                    job_description = driver.find_element(By.XPATH,'.//div[@class="JobDetails_jobDescription__6VeBn JobDetails_blurDescription__fRQYh"]//following-sibling::*').text
                    #print(job_description[:50])
                    collected_successfully = True
                    #print("COLLECTED SUCCUESSFULLY: ",collected_successfully)
                except:
                    print("Failed to collect")
                    playsound('05.mp3')
                    print("please click on next job profile")
                    time.sleep(2)

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//div[@class="SalaryEstimate_averageEstimate__xF_7h"]').text
                print(salary_estimate)
            except NoSuchElementException:
                salary_estimate = np.NAN #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.XPATH,'.//div[@class="css-8wag7x"]//span[@class = "ml-xsm"]//following-sibling::*').text
                print(rating)
            except NoSuchElementException:
                rating = np.NAN #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:2]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                #driver.find_element(By.XPATH,'.//div[@class="tab" and @data-tab-type="overview"]').click()
                driver.find_element(By.XPATH,'.//div[@class ="JobDetails_companyOverviewGrid__CV62w"]')
                print("Overview Found")

                """try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    headquarters = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Headquarters"]//next-sibling::*').text
                except NoSuchElementException:
                    headquarters = np.NAN"""

                try:
                    size = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text() = "Size"]//following-sibling::*').text
                    #print("Size: ",size)
                except NoSuchElementException:
                    print("SIZE NOT FOUND")
                    size = np.NAN

                try:
                    founded = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text()="Founded"]//following-sibling::*').text
                    #print("FOUNDED BY: ", founded)
                except NoSuchElementException:
                    print("Founded Not Found")
                    founded = np.NAN

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text()="Type"]//following-sibling::*').text
                    #print("OWNERSHIP: ",type_of_ownership)
                except NoSuchElementException:
                    print("Ownership not found")
                    type_of_ownership = np.NAN

                try:
                    industry = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text() = "Industry" ]//following-sibling::*').text
                    #print("Industry: ",industry)
                except NoSuchElementException:
                    print("Industry not found")
                    industry = np.NAN

                try:
                    sector = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text() = "Sector"]//following-sibling::*').text
                    #print("Sector: ",sector)
                except NoSuchElementException:
                    print("sector not found")
                    sector = np.NAN

                try:
                    revenue = driver.find_element(By.XPATH,'.//span[@class="JobDetails_overviewItemLabel__5vi0o" and text() = "Revenue"]//following-sibling::div').text
                    #print("Revenue: ",revenue)
                except NoSuchElementException:
                    print("Revenue not found")
                    revenue = np.NAN

                '''try:
                    competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = np.NAN'''

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                print("FAILED TO FIND OVERVIEW")
                #headquarters = np.NAN
                size = np.NAN
                founded = np.NAN
                type_of_ownership = np.NAN
                industry = np.NAN
                sector = np.NAN
                revenue = np.NAN
                #competitors = np.NAN

                
            if verbose:
                #print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                #print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            #"Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            #"Competitors" : competitors
            })
            
            #add job to jobs

        #Clicking on the "Show More" button
        try:
            driver.find_element(By.XPATH,'.//button[@class=""]').click()
        except NoSuchElementException:
            print("FAiled to push show more")
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
        #Clicking on the "next page" button
        """try:
            #driver.find_element(By.XPATH,'.//li[@class="react-job-listing css-108gl9c eigr9kq3"]//a').click()
            driver.find_element(By.XPATH,'.//button[@class="nextButton job-search-opoz2d e13qs2072"]').click()
            print("NExt Page")
        except NoSuchElementException:
            print("FAiled")
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break"""

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.