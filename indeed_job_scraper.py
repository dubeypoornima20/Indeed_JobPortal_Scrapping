
from datetime import datetime
import requests,openpyxl
from collections import defaultdict
import pandas as pd 
import re 
from bs4 import BeautifulSoup
excel=openpyxl.Workbook()
sheet=excel.active
sheet.title='Indeed Jobs'
print(excel.sheetnames)
sheet.append(['Title','Company Name','Company Location','Salary','URl'])


skill=input('Enter your skill:').strip()
place=input('Enter your location:').strip()
no_of_pages=int(input('Enter the number of pages to scrape:'))
def extract(page):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    url=f'https://in.indeed.com/jobs?q={skill}&l={place}&start={page}&pp=gQAPAAABhOjal4MAAAAB8KnljQAYAQEBBwci-xGWZb3eevPDQH5iveyHbMQxAAA&vjk=4d48d3af8347492c'
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    #print(response)
    return soup

def transform(soup):
    try:
        #url = 'https://in.indeed.com/jobs?q='+skill+'&l='+place+'&start='+str(page*10)+'&pp=gQAPAAAAAAAAAAAAAAAB8FvSfgAYAQACCWUjDvXgqCvj9I4nMyC7MaWdoQusAAA&vjk=0ebe7fe75489fdf0'
        outer_most_point=soup.find_all('div',class_="job_seen_beacon")
       # print(len(outer_most_point))
        for div in outer_most_point:
            job_title=div.find('h2',class_='jobTitle').text.strip()
            # print(job_title)
            company_name=div.find('span',class_='companyName').text.strip()
            # print(company_name)
            company_location=div.find('div',class_='companyLocation').text.strip()
            # print(company_location)
            try:
                salary=div.find('div',class_='metadata salary-snippet-container').text.strip()
                #print(salary)
            except:
                salary=''
            URL=div.find('a',class_='jcs-JobTitle')['href']
            #print(URL)
            sheet.append([job_title,company_name,company_location,salary,URL])
                
    except Exception as e:
        print(e)


for i in range(0,no_of_pages):
    print(f'Getting page, {i}')
    c=extract(i*10)
    transform(c)
excel.save('INDEED JOBS.xlsx')