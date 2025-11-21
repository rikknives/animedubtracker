import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url='https://myanimelist.net/forum/?topicid=1692966'
r=requests.get(url)
soup=BeautifulSoup(r.text,'html.parser')
post=soup.select_one('[id^="msg"]')
text=post.get_text(separator='\n') if post else ''
lines=[l.strip() for l in text.split('\n') if l.strip()]

html_parts=[]
start=False
for line in lines:
    if 'Currently Streaming' in line:
        start=True
        html_parts.append(f'<div class="section"><h2>{line}</h2>')
    elif start:
        if line.strip() in['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            html_parts.append(f'<div class="day">{line}</div>')
        elif '(Episode' in line or '(Episode' in line:
            html_parts.append(f'<div class="anime"><span>{line.split("(Episode")[0].strip()}</span><span class="ep">{"(Episode"+line.split("(Episode")[1]}</span></div>')
        elif not line.startswith('**') and line not in ['Last Updated:']:
            html_parts.append(f'<div class="anime"><span>{line}</span></div>')
        if 'Upcoming' in line or 'Winter' in line or 'Fall' in line:
            html_parts.append('</div>')

html_parts.append('</div>')
data={'updated':datetime.now().strftime("%b %d, %Y at %I:%M %p"),'html':''.join(html_parts)}
with open('docs/data.json','w') as f:
    json.dump(data,f)
