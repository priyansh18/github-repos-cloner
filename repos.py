from bs4 import BeautifulSoup
import requests
import os

username = 'priyansh18'
url = "https://github.com/{}?tab=repositories".format(username)
allLinks = []
isLastPage = False

while True:
    if isLastPage:
        break
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data,'html.parser')
    signup = soup.find('a',{'data-target':'nux-signup-candidates.signupAction'})
    if signup.text == 'Sign up':
        all_repos = soup.find_all('h3',{'class':'wb-break-all'})
        for repos in all_repos:
            link = repos.find('a',{'itemprop':'name codeRepository'})
            itemlink = "https://github.com" + link.get('href')
            allLinks.append(itemlink)
    else:
        all_repos = soup.find_all('div',{'class':'private source'})
        for repos in all_repos:
            link = repos.find('a',{'itemprop':'name codeRepository'})
            itemlink = "https://github.com" + link.get('href')
            allLinks.append(itemlink)

        
    buttonDiv = soup.find_all('a',{'class':'BtnGroup-item'})
    for divs in buttonDiv:
        if (divs.text == 'Next'):
            url = divs.get('href')
        else:
            isLastPage = True
            break
    
