#!/bin/env python3
import requests
import discord
from bs4 import BeautifulSoup

bot_token=''
if(not bot_token):
    print("need token, ask me on discord")

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

def get_help():
    help_msg="""some shit I can do
    yo bot - bot will return a greeting
    set state <state code> - will set the state to get metrics for. State codes are vic,qld,nsw,sa,act,nt,tas,wa
    set metric <metric type> - will change the metric to search. So far only supports 'cases' and 'vaccinations'
    help - show this
    what - returns what its searching from what state
    good bot - raises centience level, dangerous do not use
    shush - stops automatic replies to unknown commands
    unshush - unshuses
    today - gets todays numbers for the metric and state set
    yesterday - you can figure it out
    week - yup thats it
    \n
    The numbers are from covidlive.com.au

    """
    return help_msg

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
todays_date=get_web_table()[1].find('td', {'class':'COL1 DATE'}).text
todays_cases=get_web_table()[1].find('td', {'class':td_classes[what]}).text
print('|'+todays_date+'|'+todays_cases+'|')

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
        elif(msg == 'help'):
            reply=get_help()
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
            date=table[1].find('td', {'class':'COL1 DATE'}).text
            cases=table[1].find('td', {'class':td_classes[what]}).text
            if(cases == '-'):
                cases='NO DATA'
            reply= 'Todays '+what+' in ' + state + ':\n'+ date + " cases: " + cases
        elif(msg == 'yesterday'):
            table = get_web_table()
            date=table[2].find('td', {'class':'COL1 DATE'}).text
            cases=table[2].find('td', {'class':td_classes[what]}).text
            if(cases == '-'):
                cases='NO DATA'
            reply= 'Yesterdays '+what+' in ' + state + ':\n'+ date + " cases: " + cases
        elif(msg == 'week'):
            reply= what+" in "+state+" for the past week:\n"
            table = get_web_table()
            for i in range(7):
                date=table[i+1].find('td', {'class':'COL1 DATE'}).text
                cases=table[i+1].find('td', {'class':td_classes[what]}).text
                if(cases == '-'):
                    cases='NO DATA'
                reply+=date + ' ' + what + ' ' + cases + "\n"
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
