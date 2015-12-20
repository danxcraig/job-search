# -*- coding: utf-8 -*-

#import necessary libraries
import re
import urllib2
import json
import os

#ask the user to set their initial search parameters
location_criteria = raw_input("Which location would you like to search within?: ") 
distance_criteria = raw_input("How big should the radius be (in miles, min 5)?: ") #in miles
salary_criteria = raw_input("What minimum salary are you looking for (e.g. £55k-£120k)?: ") 

#ask the user to set their keywords or phrases and write each line to job_list.txt
with open('job_list.txt', 'wb') as job_list:
    while True:
        keywords = raw_input("Add some keywords to search for. If you're done, just key 'd': ")
        if keywords == "d":
            break
        else:
            keywords = keywords + "\n"
            job_list.write(keywords)

#ask the user to set their exclusion phrases and write each line to exclusion_list.txt
with open('exclusion_list.txt', 'wb') as exclusion_list:
    while True:
        keywords = raw_input("Add some words or phrases to exclude. If you're done, just key 'd': ")
        if keywords == "d":
            break
        else:
            keywords = keywords + "\n"
            exclusion_list.write(keywords)

#set the Indeed publisher ID
publisher_id = "7317619313909945"

#setup regex to remove annoying bold tags from item descriptions
regex = re.compile(r'(?=(.))(?:<b>|</b>)', flags=re.IGNORECASE)

#make an API call for each line in job_list.txt. 
#write jobs to job_results.txt, but ignore any job which has words or phrases from exclusion_list.txt in the job title.
with open('job_list.txt') as job_list_criteria, open('job_results.txt', 'wb') as job_list_results, open('exclusion_list.txt', 'r') as exclusions:
    job_phrases = job_list_criteria.read().splitlines()
    exclusion_phrases = exclusions.read().splitlines()
    print exclusion_phrases
    for job in job_phrases:
        search_criteria1 = str(job)
        search_criteria2 = search_criteria1.replace(' ', '+')
        api_query = "http://api.indeed.com/ads/apisearch?publisher=" + publisher_id + "&v=2&format=json&q=%22" + search_criteria2 + "%22&l=" + location_criteria + "&fromage=14&radius=" + distance_criteria + "&salary=" + salary_criteria + "&limit=50&sort=date&co=gb&ip=188.221.151.22&useragent=Mozilla/%2F4.0%28Firefox%29"
        #fetch the response and assign json parsed data to a variable 
        json_data = json.loads(urllib2.urlopen(api_query).read())
        #parse through json, strip out bold tags and then write relevant items from the job search to job_results.txt
        for item in json_data["results"]:
            if any(exclusion in item["jobtitle"] for exclusion in exclusion_phrases):
                continue
            else:
                company = regex.sub(r"", item["company"]) + "\n"
                job_title = regex.sub(r"", item["jobtitle"]) + "\n"
                job_snippet = regex.sub(r"", item["snippet"]) + "\n"
                job_url = regex.sub(r"", item["url"]) + "\n"
                job_list_results.write("COMPANY\n")
                job_list_results.write(company.encode('utf-8', 'replace'))
                job_list_results.write("JOB TITLE\n")
                job_list_results.write(job_title.encode('utf-8', 'replace'))
                job_list_results.write("JOB DESCRIPTION\n")
                job_list_results.write(job_snippet.encode('utf-8', 'replace'))    
                job_list_results.write("LINK\n")
                job_list_results.write(job_url.encode('utf-8', 'replace'))    
                job_list_results.write("\n")

#open the list of jobs for review, so that job title keywords can be excluded
os.system('open job_results.txt')

