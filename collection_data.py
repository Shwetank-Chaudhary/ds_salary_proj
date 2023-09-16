import glassdoor_scraper as gp
import pandas as pd

df = gp.get_jobs('data scientist',15,False,15)
df.to_excel("file.xlsx")