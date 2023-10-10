import glassdoor_scraper as gp
import pandas as pd

df = gp.get_jobs('data scientist',2000,True,5)
df.to_csv("jobs.csv")