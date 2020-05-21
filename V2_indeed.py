import requests #pip install requests
from bs4 import BeautifulSoup#pip install BeautifulSoup4#html에서 data추출에 용이한 library
LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=Python&limit={LIMIT}&radius=25"

    
def get_last_page() :
    result= requests.get(URL)
    #print(result)#200 mean okay
    soup = BeautifulSoup(result.text,"html.parser")
    #print(soup)
    pagination = soup.find("div",{"class":"pagination"})
    #print(pagination)
    links = pagination.find_all('a')
    #print(links)
    pages = []
    for link in links[:-1] :#0부터해서 마지막 전까지 마지막은 "다음" 이라 숫자가 아니다
        #print(link.find("span"))#list의 find모듈
        pages.append(int(link.find("span").string))
    max_page = pages[-1]#다음으로 넘어가기 전 까지 총페이지의 수를 파악 앞으로는 각각페이지에 들릴 예정 즉 max_page만큼 requests를 해줘야함
    return max_page


def extract_job(html) :
    title = html.find("h2",{"class":"title"}).find("a")["title"]#title 속성의 속성값 가져오기 
    company = html.find("span",{"class":"company"})
    company_anchor = company.find("a") # html보니 anchor내에 있는 것도 있고 아닌것도 있네?
    if company_anchor is not None :
        company = (str(company_anchor.string))
    else :
        company = (str(company.string))
        company = company.strip()
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    apply_link = f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?&jk={job_id}"
    return{'title':title ,'company':company, 'location':location, 'apply_link':apply_link}


def extract_jobs(last_page):
    
    jobs = []
    for page in range(last_page):
        print(f"Scrapping INDEED :page = {page}..")
        result = requests.get(f"{URL}&start={page*LIMIT}")
         #print(result.status_code)
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        #find_all() : 해당 조건에 맞는 모든 태그들을 가져온다.
        for result in results :
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs() :
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs