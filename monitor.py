import os
2
import requests
3
 
4
BOT_TOKEN = os.environ["BOT_TOKEN"]
5
CHAT_ID = os.environ["CHAT_ID"]
6
 
7
message = """
8
✅ Festool/Makita Monitor virker!
9
 
10
Denne besked er sendt automatisk fra GitHub.
11
"""
12
 
13
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
14
 
15
response = requests.post(
16
url,
17
data={
18
"chat_id": CHAT_ID,
19
"text": message
20
}
21
)
22
 
23
print(response.text)
