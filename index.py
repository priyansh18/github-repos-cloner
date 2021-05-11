from bs4 import BeautifulSoup
import requests
import os
import sys

def scrapCurrentPageReposLink(url):
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')

    reposLinks = []
    reposAnchors = soup.find_all('a', {'itemprop': 'name codeRepository'})
    for anchor in reposAnchors:
        reposLinks.append("https://github.com" + anchor.get('href'))

    nextpageURL = ""
    buttonDiv = soup.find_all('a', {'class': 'BtnGroup-item'})
    for divs in buttonDiv:
        if (divs.text.title() == 'Next'):
            nextpageURL = divs.get('href')
        elif(divs.text.title() == 'Previous'):
            continue
        else:
            break

    return (reposLinks, nextpageURL)


def scrapGithubReposLink(username):
    repos = []
    url = "https://github.com/{}?tab=repositories".format(username)

    while True:
        (currentPageRepos, nextPageURL) = scrapCurrentPageReposLink(url)

        repos.extend(currentPageRepos)
        url = nextPageURL

        if not url:
            break

    return repos


def cloneRepos(reposLinks):
    os.chdir('../')
    for repoLink in reposLinks:
        print("========\nCloning the {}\n==============".format(repoLink))
        os.system("git clone {}".format(repoLink))


if(__name__ == "__main__"):
    username = sys.argv[1]
    reposLinks = scrapGithubReposLink(username)
    print("Total Repos Found are {}".format(len(reposLinks)))
    print("Repos To be cloned :")
    for repoLink in reposLinks:
        print(repoLink)
    cloneRepos(reposLinks)
