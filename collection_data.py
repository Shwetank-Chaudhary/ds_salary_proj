import glassdoor_scraper as gp
import pandas as pd

df = gp.get_jobs('data scientist',1050,False,5)
df.to_csv("jobs.csv")