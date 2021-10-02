#!/bin/env python3
import requests
import discord
from bs4 import BeautifulSoup

bot_token='ODkzMDI3MzI1OTI1NTQ4MDgy.YVVegg.FkVa1Bz6epcYIMbva44uYJT-ah4'

#discord bot info
"""
CLIENT ID: 893027325925548082
PERMS:     68608
URL: https://discord.com/api/oauth2/authorize?client_id=893027325925548082&scope=bot&permissions=68608
"""
date=""
cases=""

print("shitty discord bot V1")
bot = discord.Client()
base_url='https://covidlive.com.au/report/daily-'
state='vic'
#replace the /daily-xxxx/ part in the URL
what='cases'
td_classes={'cases':'COL2 NEW', 'vaccinations':'COL2 DOSES'}


def get_web_table():
    global base_url
    global state
    global what
    url=base_url+what+'/'+state
    print("Fetching url",url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    #<table class="DAILY-CASES"><tr class="TH">

    table_class = 'DAILY-'+what.upper()
    print("Trying to find table with class ",table_class)
    table = soup.find('table', {'class':table_class})
    row=table.find_all('tr')
    return row

print("DATE      CASES")
##row=table.find_all('tr')[i].text.strip()
todays_date=get_web_table()[1].find('td', {'class':'COL1 DATE'})
todays_cases=get_web_table()[1].find('td', {'class':td_classes[what]})
print(todays_date.text,todays_cases.text)

shush_mode=0
@bot.event
async def on_ready():
    print("connected to server ", bot.guilds[0].name ," and my username is ",bot.user.name)
    print("Using VIC numbers by default")

@bot.event
async def on_message(message):
    print("Got message:", message.content, "from channel\x1b[34m", message.channel.name, "\x1b[0mand user\x1b[32m", message.author.name,"\x1b[0m")
    reply=""
    global shush_mode
    global state
    global what
    msg=message.content.lower()

    if(message.channel.name == 'bots'):
        if(msg == 'yo bot'):
            reply='yo human'
        elif(msg.startswith('set state')):
            msg_split=msg.split(' ',2)
            state=msg_split[2].lower()
            reply='State set to '+msg_split[2]
        elif(msg.startswith('set metric')):
            msg_split=msg.split(' ',2)
            what=msg_split[2].lower()
            reply='State metric to '+msg_split[2]
        elif(msg == 'what'):
            reply="Showing " + what + " for " + state
        elif(msg == 'good bot'):
            reply='thank'
        elif(msg.startswith("shush")):
            shush_mode=1
            reply = "ok sorry"
        elif(msg.startswith("unshush")):
            shush_mode=0
            reply = "ok thank"
        elif(msg == 'today'):
            table = get_web_table()
            date=table[1].find('td', {'class':'COL1 DATE'})
            cases=table[1].find('td', {'class':td_classes[what]})
            reply= 'Todays '+what+' in ' + state + ':\n'+ date.text + " cases: " + cases.text
        elif(msg == 'yesterday'):
            table = get_web_table()
            date=table[2].find('td', {'class':'COL1 DATE'})
            cases=table[2].find('td', {'class':td_classes[what]})
            reply= 'Yesterdays '+what+' in ' + state + ':\n'+ date.text + " cases: " + cases.text
        elif(msg == 'week'):
            reply= what+" in "+state+"for the past week:\n"
            table = get_web_table()
            for i in range(7):
                date=table[i+1].find('td', {'class':'COL1 DATE'})
                cases=table[i+1].find('td', {'class':td_classes[what]})
                reply+=date.text + ' ' + what + ' ' + cases.text + "\n"
        elif("dick" in msg or "cock" in msg or "penis" in msg):
            reply = message.author.name + "u gay"
        else:
            if(not bool(shush_mode)):
                reply = "no"
            else:
                reply = ""

        print("reply is [",reply,"]")
        if(message.author.name != bot.user.name and reply):
            await message.channel.send(reply)

bot.run(bot_token)
