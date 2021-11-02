from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup
import requests


# Create your views here.

def homepage(request):
    html_text = None
    if request.method == "POST":
        language = request.POST.get('language')
        fam_skill = request.POST.get('skill')
        print(language, fam_skill)
        url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={}&txtLocation='.format(
            language)
        html_text = requests.get(url)
        html_text = html_text.text
        # print(html_text)
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find('span', id="totolResultCountsId").text

        if not jobs == "0":
            print(jobs, " inside jobs---------------")
            jobs = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")
            dict_data = {}
            list_data = []
            for job in jobs:
                post_time = job.find('span', class_="sim-posted").span.text
                if 'few' in post_time:
                    company_name = job.find('h3', class_='joblist-comp-name').text.strip()
                    job_role = job.find('strong', class_='blkclor')
                    skills = job.find('span', class_='srp-skills').text.replace('  ,  ', ', ').strip()
                    more_info = job.header.h2.a['href']
                    if fam_skill in skills:
                        dict_data = {'search_for': job_role.text, 'company': company_name, 'skills': skills, 'more_info': more_info}

                        list_data.append(dict_data)
            # print("start----", list_data, " end------")
            if list_data:
                context = {
                    "list_data": list_data
                }
                return render(request, 'app/homepage.html', context)
            else:
                return HttpResponse("<h1>No '{}' skill found in '{}'</h1>".format(fam_skill, language))
        else:
            return HttpResponse("<h1>NO JOBS FOUND</h1>")
    return render(request, 'app/homepage.html')


# print("Enter Skill to find job:")
# familiar_skill = input('>')
# print(f"Looking for jobs with skill {familiar_skill}...")


# html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from'
#                          '=submit&txtKeywords=Python&txtLocation=').text
# soup = BeautifulSoup(html_text, 'lxml')
# jobs = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")
# for job in jobs:
#     post_time = job.find('span', class_="sim-posted").span.text
#     if 'few' in post_time:
#         company_name = job.find('h3', class_='joblist-comp-name').text.strip()
#         job_role = job.find('strong', class_='blkclor').text
#         skills = job.find('span', class_='srp-skills').text.replace('  ,  ', ', ').strip()
#         more_info = job.header.h2.a['href']
#         if familiar_skill in skills:
#             print(f"{job_role}")
#             print(f"Company: {company_name}")
#             print(f"Skills Needed: {skills}")
#             print(f"More Info: {more_info}")
#
#             print("---*---*---*---*---*---*---")
