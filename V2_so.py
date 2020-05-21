import requests #pip install requests
from bs4 import BeautifulSoup#pip install BeautifulSoup4#html에서 data추출에 용이한 library

URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page() :
    result= requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("span")
    #print(pages)
    last_page= pages[-2].string.strip()
    return int(last_page)

def extrcat_job(html) :
    title = html.find("div", {"class":"fl1"}).find("h2").find("a")["title"]#title값을 포함하는 최 하위의 클래스 부터 찾아갔다
    company , location = html.find("div", {"class":"fl1"}).find("h3").find_all("span",recursive=False)
    
    company = company.get_text(strip=True)
    location = location.get_text(strip=True) 
    job_id = html["data-jobid"]
    apply_link = f"https://stackoverflow.com/jobs/{job_id}/"
    #비어있을 시 string은 Nonetype 반환 , get_text 는 빈 문자열 반환 
    #-> 정확한건 html 태그 공부한 다음 다시 검색해 보기
    return {
        'title' : title,
        'company' : company,
        'location' : location,
        'link' : apply_link
    }

def extrcat_jobs(last_page) :
    jobs = []
    for page in range(1,last_page+1) :
        print(f"Scrapping SO :page = {page-1}..")
        result= requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results :
            job = extrcat_job(result)
            jobs.append(job)
    return jobs
    
def get_jobs() :
    last_page = get_last_page()
    jobs = extrcat_jobs(last_page)
    return []