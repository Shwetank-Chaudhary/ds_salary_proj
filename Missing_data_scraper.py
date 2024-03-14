from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import openai
from openai.error import RateLimitError
#from openai import RateLimitError

#API:- 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
# RATE LIMITERROR


#QUITE SLOW
def use_chat_gpt(data,company_name,keyword):
    api_key  = open("API_KEY.txt",'r').read()
    openai.api_key=api_key
    i=0
    for c in company_name:
        if keyword=='Founded':
            try:
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {
                            "role":"user",
                            "content": c+" IS FOUNDED IN WHICH YEAR ONE WORD ANSWER"
                        }
                    ]
                )
                data.loc[company_name.index[i],keyword]=response['choices'][0]['message']['content']
                print(keyword+"Updated")
            except RateLimitError: 
                print(keyword+'failed to update')
                time.sleep(20)
            i+=1
        elif(keyword=='Sector'):
            try:
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {
                            "role":"user",
                            "content": c+" Belongs to which sector ONE WORD ANSWER"
                        }
                    ]
                )
                data.loc[company_name.index[i],keyword]=response['choices'][0]['message']['content']
            except RateLimitError: 
                print(keyword+' failed to update')
                time.sleep(20)
            i+=1

    
        
    '''options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.set_window_size=(1120,1000)
    i=0

    #Intialising ChatGPT
    url = "https://chat.openai.com/auth/login"
    driver.get(url)
    print("WAITING TO AUTHENTICATE")
    #time.sleep(3)
    driver.find_element(By.XPATH,'.//button[@data-testid="login-button"]').click()
    #Loging IN
    try:
        username = driver.find_element(By.ID,"username")
        username.send_keys("jharupa9818@gmail.com")
        try:
            driver.find_element(By.XPATH,'.//button[@type = "submit"]').click()
        except:
            print("SUBMIT Button not found")
        print("USERNAME ENTERED")
        #time.sleep(1)
    except NoSuchElementException:
        print("FAiled to enter login ID")
        time.sleep(10)

    try:
        password = driver.find_element(By.ID,'password')
        password.send_keys("Golden123")
        driver.find_element(By.XPATH,'.//button[@type = "submit"]').click
        print("Login SUCCESSFULL")
        time.sleep(10)
    except NoSuchElementException:
        print("LOGIN FAILED")'''
        

    

    


def mising_data(data,company_name,keyword):
    #Initializing webDriver
    options = webdriver.ChromeOptions()
    driver  = webdriver.Chrome(options=options)
    driver.set_window_size=(1120,1000)
    i=j=k=l=0

    for c in company_name:
        #RATINGS
        if keyword=='Rating':
            url = 'https://www.google.com/search?q='+c+'+company+rating+according+to+glassdoor&oq='+c+'+company+rating+according+to+glassdoor&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTEzNTU3ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'
            driver.get(url)
            #print("RATINGS PAGE OPENED")
            time.sleep(1)

            try:
                rating = driver.find_element(By.XPATH,'.//div[@class="VwiC3b yXK7lf yDYNvb W8l4ac lyLwlc lEBKkf"]//following-sibling::span//following-sibling::em').text
                print(rating)
                try:
                    data.loc[company_name.index[i],keyword] = float(rating[:3])
                except ValueError:
                    data.loc[company_name.index[i],keyword] = np.nan
            except NoSuchElementException:
                print("FAILED")
                data.loc[company_name.index[i],keyword] = np.nan
            i+=1


        #SECTORS
        elif keyword == 'Sector':
            url = 'https://www.google.com/search?q='+c+'+which+sector&sca_esv=567819863&sxsrf=AM9HkKl7k6P1PcmFBus8IK3yWH-maR6KHA%3A1695461536763&ei=oLAOZemULu2Y4-EP0fW3oAw&ved=0ahUKEwjp5IO1tsCBAxVtzDgGHdH6DcQQ4dUDCBA&uact=5&oq='+c+'+which+sector&gs_lp=Egxnd3Mtd2l6LXNlcnAiHkZ1bGNydW0gQW5hbHl0aWNzIHdoaWNoIHNlY3RvcjIFECEYoAFIgSZQtAdYpCBwAXgAkAEAmAHPAaAB-hCqAQYwLjEyLjG4AQPIAQD4AQHCAgQQIxgnwgIFEAAYgATCAggQABiKBRiGA8ICBxAhGKABGArCAgQQIRgVwgIIECEYFhgeGB3iAwQYASBBiAYB&sclient=gws-wiz-serp#ip=1'
            driver.get(url)
            try:
                sector = driver.find_element(By.XPATH,'.//span[@class="hgKElc"]//following-sibling::b').text
                print("Sector successfully extracted")
                data.loc[company_name.index[j],keyword] = sector
                    
            except NoSuchElementException:
                print("FAILED")
                data.loc[company_name.index[j],keyword] = np.nan
            j+=1
        
        #FOUNDED
        elif keyword == 'Founded':
            url = 'https://www.google.com/search?q='+c+'+founded+in+which+year&sca_esv=567819863&sxsrf=AM9HkKm24J0wXuGu3Ll_m9vXf1npGZ73xw%3A1695461551599&ei=r7AOZfKJJNCZ4-EP0bC74AM&ved=0ahUKEwiynY28tsCBAxXQzDgGHVHYDjwQ4dUDCBA&uact=5&oq='+c+'+founded+in+which+year&gs_lp=Egxnd3Mtd2l6LXNlcnAiJ0Z1bGNydW0gQW5hbHl0aWNzIGZvdW5kZWQgaW4gd2hpY2ggeWVhcjIFEAAYogQyBRAAGKIEMgUQABiiBDIIEAAYiQUYogRI1zVQqwVY_CxwAXgAkAEAmAHJAaABiB2qAQYwLjIyLjG4AQPIAQD4AQHCAggQABiiBBiwA8ICBxAjGK4CGCfCAgQQIxgnwgIFEAAYgATCAggQABiKBRiGA8ICBRAhGKABwgIHECEYoAEYCsICCBAhGBYYHhgdwgIEECEYFeIDBBgBIEGIBgGQBgM&sclient=gws-wiz-serp#ip=1'
            driver.get(url)
            try:
                founded = driver.find_element(By.XPATH,'.//span[@class="hgKElc"]//following-sibling::b').text
                if(len(founded)<4):
                    raise NoSuchElementException
                print(k,founded)
                data.loc[company_name.index[k],keyword] = founded
                    
            except NoSuchElementException:
                try:
                    founded = driver.find_element(By.XPATH,'.//div[@class="Z0LcW t2b5Cf"]').text
                    if(len(founded)<4):
                        raise NoSuchElementException
                    print(k,founded)
                    data.loc[company_name.index[k],keyword] = founded

                except NoSuchElementException:
                    try:
                        txt=driver.find_element(By.ID,'recaptcha-anchor-label').text
                        if(txt=="I'm not a robot"):
                            time.sleep(5)
                    except NoSuchElementException:
                        print("FAILED")
                        data.loc[company_name.index[k],keyword] = np.nan
            k+=1
        elif keyword == 'Industry':
            url = 'https://www.google.com/search?q=Industry+of+'+c+'&oq=Industry+of+'+c+'&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTI0MTg0ajBqMagCALACAA&sourceid=chrome&ie=UTF-8#ip=1'
            driver.get(url)
            try:
                industry = driver.find_element(By.XPATH,'.//span[@class = "hgKElc"]//following-sibling::b').text
                data.loc[company_name.index[l],keyword] = industry
            except NoSuchElementException:
                print("Industry FAILED")
                data.loc[company_name.index[l],keyword] = np.nan
            l+=1





#mising_data('Tech brothers infoservices','Rating')

