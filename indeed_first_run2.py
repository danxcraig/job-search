# -*- coding: utf-8 -*-

#import necessary libraries
import re
import urllib2
import json
import os

#ask the user to set their initial search parameters
location_criteria = "London" 
distance_criteria = "50"
salary_criteria = "£55k-£150k"

#set the Indeed publisher ID
publisher_id = "7317619313909945"

#setup regex to remove annoying bold tags from item descriptions
regex = re.compile(r'(?=(.))(?:<b>|</b>)', flags=re.IGNORECASE)

snippets = []

#make an API call for each line in job_list.txt. 
#write jobs to job_results.txt, but ignore any job which has words or phrases from exclusion_list.txt in the job title.
with open('job_list.txt') as job_list_criteria, open('job_results.html', 'wb') as job_list_results, open('exclusion_list.txt', 'r') as exclusions:
    job_phrases = job_list_criteria.read().splitlines()
    exclusion_phrases = exclusions.read().splitlines()
    job_list_results.write('<html>\n<head><link rel="stylesheet" type="text/css" href="mystyle.css"></head>\n<body>\n')
    for job in job_phrases:
        search_criteria1 = str(job)
        search_criteria2 = search_criteria1.replace(' ', '+')
        api_query = "http://api.indeed.com/ads/apisearch?publisher=" + publisher_id + "&v=2&format=json&q=%22" + search_criteria2 + "%22&l=" + location_criteria + "&fromage=21&radius=" + distance_criteria + "&salary=" + salary_criteria + "&limit=500&sort=date&co=gb&ip=188.221.151.22&useragent=Mozilla/%2F4.0%28Firefox%29"
        #fetch the response and assign json parsed data to a variable 
        json_data = json.loads(urllib2.urlopen(api_query).read())
        #parse through json, strip out bold tags and then write relevant items from the job search to job_results.txt
        for item in json_data["results"]:
            if any(exclusion in item["jobtitle"] for exclusion in exclusion_phrases):
                continue
            else:
                if item["snippet"] not in snippets:
                    snippets.append(item["snippet"])
                    job_list_results.write('<div id="job">\n')
                    company = '<h2>' + regex.sub(r"", item["company"]) + '</h2>' + "\n"
                    job_title = '<h1>' + regex.sub(r"", item["jobtitle"]) + '</h1>' + "\n"
                    job_snippet = '<p>' + regex.sub(r"", item["snippet"]) + '</h3>' + "\n" + "<br /><br />"
                    job_url = '<a href="' + regex.sub(r"", item["url"]) + '">Link to full description</a>'
                    job_list_results.write(job_title.encode('utf-8', 'replace'))
                    job_list_results.write(company.encode('utf-8', 'replace'))
                    job_list_results.write(job_snippet.encode('utf-8', 'replace'))    
                    job_list_results.write(job_url.encode('utf-8', 'replace'))    
                    job_list_results.write("\n")
                    job_list_results.write('</div>\n')
                else:
                    continue
    job_list_results.write("</body>\n</html>")
#open the list of jobs for review, so that job title keywords can be excluded
os.system('open job_results.html')

