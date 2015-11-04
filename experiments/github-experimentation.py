import time
import grequests

#curl https://api.github.com/users/decker108/repos

# response = grequests.get('https://api.github.com/users/decker108/repos')
# responseJson = response.json()

startTime = time.time()
# languageUrls = [entry['languages_url'] for entry in response]
# print languageUrls

languageUrls = ['http://www.google.com', 'http://www.example.com', 'http://www.python.org']
# jobs = [spawn(grequests.get, url) for url in urls]
# joinall(jobs, timeout=2)
# print [job.value for job in jobs]
rs = [grequests.get(u) for u in languageUrls]
print [r.status_code for r in (grequests.map(rs))]
print 'endtime ', time.time()-startTime

#TODO use OAuTH2 auth to increase rate limit
