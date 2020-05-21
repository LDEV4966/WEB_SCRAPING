from V2_indeed import get_jobs as get_indeed_jobs
from V2_so import get_jobs as get_so_jobs
so_jobs = get_so_jobs()
indeed_jobs = get_indeed_jobs()
jobs = indeed_jobs + so_jobs
print(jobs)