from mkw_ghosts import MkwGhosts
import hashlib
import requests
from mii import Mii
import io
import binascii
import pid2fc



#dictionaries that are useful for presesnting information to the user
controller_dict = {'Controllers.wii_remote':'Nunchuck', 'Controllers.wii_wheel':'Wii Wheel', 'Controllers.gamecube_controller':'GCN Controller', 'Controllers.classic_controller':'Classic Controller'}
drift_dict = {False:'Manual', True:'Automatic'}
track_dict = {8:'Luigi Circuit', 1:'Moo Moo Meadows', 2:'Mushroom Gorge', 4:"Toad's Factory", 0:'Mario Circuit', 5:'Coconut Mall', 6:'DK Summit', 7:"Wario's Gold Mine", 9:'Daisy Circuit', 15:'Koopa Cape', 11:'Maple Treeway', 3:'Grumble Volcano', 14:'Dry Dry Ruins', 10:'Moonview Highway', 12:"Bowser's Castle", 13:'Rainbow Road', 16:'GCN Peach Beach', 20:'DS Yoshi Falls', 25:'SNES Ghost Valley 2', 26:'N64 Mario Raceway', 27:'N64 Sherbet Land', 31:'GBA Shy Guy Beach', 23:'DS Delfino Square', 18:'GCN Waluigi Stadium', 21:'DS Desert Hills', 30:'GBA Bowser Castle 3', 29:"N64 DK's Jungle Parkway", 17:'GCN Mario Circuit', 24:'SNES Mario Circuit 3', 22:'DS Peach Gardens', 19:'GCN DK Mountain', 28:"N64 Bowser's Castle"}
country_dict = {49: 'US', 76: 'FI', 82: 'IE', 24: 'DO', 88: 'LU', 95: 'NZ', 1: 'JP', 79: 'GR', 110: 'GB', 105: 'ES', 65: 'AU', 18: 'CA', 96: 'NO', 94: 'NL', 107: 'SE', 74: 'DK', 78: 'DE', 108: 'CH', 136: 'KR', 67: 'BE', 52: 'VE', 77: 'FR', 16: 'BR'}

#parsing the data from the ghost
ghost = open('ghost.rkg', 'rb+')
ghostbytes = ghost.read()
hasher = hashlib.sha1()
hasher.update(ghostbytes) #gettingt the sha1 hash of the ghost
ctgpid = (hasher.hexdigest()).upper()
chadsoft_link = (f'http://chadsoft.co.uk/time-trials/rkgd/{ctgpid[0:2]}/{ctgpid[2:4]}/{ctgpid[4:]}') #creating a chadsoft link based off the hash, if the ghost here matches then it will tell user that the ghost is on chadsoft
ghostkaitai = MkwGhosts.from_bytes(ghostbytes) #using the ghost kaitai class
miidata = ghostkaitai.driver_mii_data
miikaitai = Mii.from_bytes(miidata) #using mii kaitai class
miiname = miikaitai.mii_name
miiname, sep, garbgae = miiname.partition('\x00')#removes null bytes from mii name to prevent this: 'Oofer<0x00>OOOF'

#printing the information
print(f'Name: {miiname}')
print(f'Track: {track_dict.get(int(ghostkaitai.track_id))}')
print(f'Finishing Time: {ghostkaitai.finishing_time_minutes}:{str(ghostkaitai.finishing_time_seconds).zfill(2)}.{str(ghostkaitai.finishing_time_milliseconds).zfill(3)}')
print('Lap 1: ' + str(ghostkaitai.lap_split_time[0].finishing_time_seconds) + '.' + str(ghostkaitai.lap_split_time[0].finishing_time_milliseconds).zfill(3))
print('Lap 2: ' + str(ghostkaitai.lap_split_time[1].finishing_time_seconds) + '.' + str(ghostkaitai.lap_split_time[1].finishing_time_milliseconds).zfill(3))
print('Lap 3: ' + str(ghostkaitai.lap_split_time[2].finishing_time_seconds) + '.' + str(ghostkaitai.lap_split_time[2].finishing_time_milliseconds).zfill(3))
print(f'Controller: {controller_dict.get(str(ghostkaitai.controller_id))}')
print(f'Country: {country_dict.get(ghostkaitai.country_code)}')
print(f'Date Set: 20{ghostkaitai.ghost_sent_year}-{ghostkaitai.ghost_sent_month}-{ghostkaitai.ghost_sent_day}')
print(f'Drift Type: {drift_dict.get(ghostkaitai.drift_type)}')
miidata = ghostkaitai.driver_mii_data
miikaitai = Mii.from_bytes(miidata)
encode = binascii.hexlify(miidata)
print('View the mii used in this ghost data at: https://miicontestp.wii.rc24.xyz/cgi-bin/render.cgi?data=' + str(encode)[2:-1])
ghost_to_check = requests.get(chadsoft_link + '.rkg')

if ghostbytes == ghost_to_check.content:
	print(f'This ghost is on the CTGP Ghost Database, meaning that it is likely legitimate. View it at {chadsoft_link}.html')
else:
	print('This ghost is not on the CTGP Ghost Database. If you believe this is in error, It may not have originated from the Ghost Database or has had some of the data altered / removed.')

