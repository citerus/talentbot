import json

#curl https://api.github.com/users/decker108/repos

data = ''
with open('repos.json', 'r') as myfile:
    data = myfile.readlines()
    
#jsonData = json.loads(data)
