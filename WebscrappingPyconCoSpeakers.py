#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract pycon.co speakers information
using web scrapping
https://www.pycon.co/speakers/

Created on Tue Mar 27 07:26:42 2018

@author: Jose R. Zapata
@contact: https://joserzapata.github.io/
"""
import requests
from bs4 import BeautifulSoup
import csv   #para manipular archivos csv

#%% Download webpage
URL = 'https://www.pycon.co'
page = requests.get(URL+'/speakers/')
contents = page.content

#%% Reading web info
Info = BeautifulSoup(contents, 'html.parser')
speakers = Info.find_all("div", "speaker")
file2write=open("Pycon2018SpeakersInfo.md",'w')
file2write.write("# Pycon 2018 Colombia Speakers Info"+'\n\n')
file2write.write("List of speakers and  workshops in pycon 2018"+'\n\n')
file2write.write("| Name | Github | Presentation |"+'\n')
file2write.write("| --- | --- | ---"+ '\n')
for data in speakers:
    name = data.find("div","speaker-name").getText()
    links = data.find_all("a","social-hover",href=True)
    if len(links)!=0:
        github_link = [x['href'] for x in links if 'www.github' in x['href']]
        
    # get the talk or workshop name
    per = data.find("a","",href=True)
    personal_info = requests.get(URL+per['href'])
    content_personal = personal_info.content
    per_info = BeautifulSoup(content_personal, 'html.parser')
    talk = per_info.select('ul > li > a')[-1].getText()
    talk = talk.replace('(Spanish)', '').replace('(English)', '').replace('Español', '')
    if len(github_link) >= 1 :
        file2write.write(f'{name} | [{github_link[0][23:]}]({github_link[0]}) | {talk}'+ '\n')
    else:
        file2write.write(f'{name} |  | {talk}'+ '\n')
    github_link = []
file2write.close()   
print("Have a Nice day :)")        
        