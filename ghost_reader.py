from mkw_ghosts import CTGPGhosts, MkwGhosts
import hashlib
import requests
hasher = hashlib.sha1()
from mii import Mii
import io
import sys
import binascii
import crcmod
import struct

color_dict = {0:'Red', 1:'Orange', 2:'Yellow', 3:'Light Green', 4:'Dark Green', 5:'Dark Blue', 6:'Cyan', 7:'Pink', 8:'Purple', 9:'Brown', 10:'White', 11:'Black'}
controller_dict = {'Controllers.wii_remote':'Nunchuck', 'Controllers.wii_wheel':'Wii Wheel', 'Controllers.gamecube_controller':'GCN Controller', 'Controllers.classic_controller':'Classic Controller'}
drift_dict = {False:'Manual', True:'Automatic'}
track_dict = {8:'Luigi Circuit', 1:'Moo Moo Meadows', 2:'Mushroom Gorge', 4:"Toad's Factory", 0:'Mario Circuit', 5:'Coconut Mall', 6:'DK Summit', 7:"Wario's Gold Mine", 9:'Daisy Circuit', 15:'Koopa Cape', 11:'Maple Treeway', 3:'Grumble Volcano', 14:'Dry Dry Ruins', 10:'Moonview Highway', 12:"Bowser's Castle", 13:'Rainbow Road', 16:'GCN Peach Beach', 20:'DS Yoshi Falls', 25:'SNES Ghost Valley 2', 26:'N64 Mario Raceway', 27:'N64 Sherbet Land', 31:'GBA Shy Guy Beach', 23:'DS Delfino Square', 18:'GCN Waluigi Stadium', 21:'DS Desert Hills', 30:'GBA Bowser Castle 3', 29:"N64 DK's Jungle Parkway", 17:'GCN Mario Circuit', 24:'SNES Mario Circuit 3', 22:'DS Peach Gardens', 19:'GCN DK Mountain', 28:"N64 Bowser's Castle"}
country_dict = {49: 'US', 76: 'FI', 82: 'IE', 24: 'DO', 88: 'LU', 95: 'NZ', 1: 'JP', 79: 'GR', 110: 'GB', 105: 'ES', 65: 'AU', 18: 'CA', 96: 'NO', 94: 'NL', 107: 'SE', 74: 'DK', 78: 'DE', 108: 'CH', 136: 'KR', 67: 'BE', 52: 'VE', 77: 'FR', 16: 'BR'}
type_dict = {1:'Personal Record', 2:'World Record', 3:'Continental Record', 4:'Challenge Ghost', 6:'Ghost Race', 37:'Easy Staff Ghost', 38:'Expert Staff Ghost', range(7, 36):'Friend Ghost'}

def crc16(data):
	crc = crcmod.predefined.Crc('xmodem')
	crc.update(data)
	return crc.hexdigest()

def hex_string(data):
	return str(binascii.hexlify(data).upper())[2:-1]

def ctgp_check(ghost):
	return ghost[:-4] == b'CKGD'

def birthday(month, day):
	if day == 0:
		return 'Not Set'
	else:
		return str(month) + '/' + str(day)

def parse_shroomstrat(laps_driven, shrooms = []):
	strategy = [0] * laps_driven
	for shroom in shrooms:
		strategy[shroom - 1] += 1

	return '-'.join(str(x) for x in strategy)

def clean_mii_name(name):
	name, sep, garbgae = name.partition('\x00')
	return name.lstrip()
try:
	filename = sys.argv[1]
except IndexError:
	filename = 'ghost.rkg'

with open(filename, 'rb') as file:

	ghostbytes = file.read()
	if ghostbytes[:4] == b'RKGD':
		hasher.update(ghostbytes)
		ctgpid = (hasher.hexdigest()).upper()
		chadsoft_link = (f'http://chadsoft.co.uk/time-trials/rkgd/{ctgpid[0:2]}/{ctgpid[2:4]}/{ctgpid[4:]}')
		is_ctgp = ctgp_check(ghostbytes[-8:]) 

		if is_ctgp:
			ghost = CTGPGhosts.from_bytes(ghostbytes)
		else:
			ghost = MkwGhosts.from_bytes(ghostbytes)
		miidata = ghost.driver_mii_data
		mii = Mii.from_bytes(miidata)
		encode = binascii.hexlify(miidata)
		print(f'Name: {clean_mii_name(mii.mii_name).lstrip()}')
		print(f'Track Slot: {track_dict.get(int(ghost.track_id))}')
		print(f'Finishing Time: {ghost.finishing_time_minutes}:{str(ghost.finishing_time_seconds).zfill(2)}.{str(ghost.finishing_time_milliseconds).zfill(3)}')
		for i in range(ghost.lap_count):
			print(f'Lap {i+1}: {str(ghost.lap_split_time[i].finishing_time_seconds)}.{str(ghost.lap_split_time[i].finishing_time_milliseconds).zfill(3)}')
		print(f'Controller: {controller_dict.get(str(ghost.controller_id))}')
		print(f'Country: {country_dict.get(ghost.country_code)}')
		print(f'Date Set: 20{str(ghost.ghost_sent_year).zfill(2)}-{str(ghost.ghost_sent_month).zfill(2)}-{str(ghost.ghost_sent_day).zfill(2)}')
		print(f'Drift Mode: {drift_dict.get(ghost.drift_type)}')
		if is_ctgp:
			print(f'Shroom Strategy: {parse_shroomstrat(ghost.lap_count, [ghost.shroom1, ghost.shroom2, ghost.shroom3])}')
		
		if not is_ctgp:
			print(f'Ghost Type: {type_dict.get(ghost.ghost_type, "Unknown")}')
		if is_ctgp:
			print('')
			ghost_to_check = requests.get(chadsoft_link + '.rkg')
			if ghost_to_check.status_code == 200:
				if ghostbytes == ghost_to_check.content:
					print(f'This ghost was downloaded from the CTGP Ghost Database, meaning that it is highly likely a legitimate ghost.')
			print(f'CTGP Player Page: http://chadsoft.co.uk/time-trials/players/{ghost.ctgp_pid[0:2]}/{ghost.ctgp_pid[2:]}.html')
			print(f'CTGP Ghost Link: {chadsoft_link}.html')
			#ok so the way you have to make this is a mess. to get the slot id you need to read the track id of the ghost then convert it to bytes then hexlify it THEN make it a string and slice the b'' off of it. then you need to add the track sha1 and then also at the end before the html read the category from the ghost and add a leading 0
			print(f'CTGP Leaderboard Link: http://chadsoft.co.uk/time-trials/leaderboard/{hex_string(ghost.track_id.to_bytes(1, "big"))}/{ghost.track_sha1}/{str(ghost.category).zfill(2)}.html')
			#print(f'CTGP Version: {ghost.ctgp_ver_1}.{str(ghost.ctgp_ver_2).zfill(2)}.{(ghost.ctgp_ver_3)}') This is incorrect
			
			if ghost.my_stuff_enabled:
				print(f'My Stuff Enabled: {ghost.my_stuff_enabled}')
			if ghost.my_stuff_used:
				print(f'My Stuff Used: {ghost.my_stuff_used}')
			if ghost.usb_gcn:
				print(f'USB GameCube Enabled: {ghost.usb_gcn}')
			if ghost.oob:
				print(f'Went Out of Bounds: {ghost.oob}')
			if ghost.respawns:
				print(f'Respawns: {ghost.respawns}')
			if ghost.cannoned:	
				print(f'Used Cannon: {ghost.cannoned}')
			if ghost.rapid_fire:
				print(f'Potential Rapidfire: {ghost.rapid_fire}')
			if ghost.mii_data_replaced:
				print(f'Has Mii Replaced: {ghost.mii_data_replaced}')
			if ghost.has_name_replaced:	
				print(f'Has Name Replaced: {ghost.has_name_replaced}')
			
		else:
			print('This ghost does not appear to have any CTGP Metadata associated with it. Some extra information cannot be displayed.')
		print('\nMii Extended Info:')
		print(f'Name: {clean_mii_name(mii.mii_name).lstrip()}')
		print(f'Creator Name: {clean_mii_name(mii.creator_name).lstrip() }')
		print(f'Gender: {mii.gender}')
		print(f'Birthday: {birthday(mii.birth_month, mii.birth_day)}')
		print(f'Shirt Color: {color_dict.get(mii.favorite_color)}')
		print('View Mii: https://miicontestp.wii.rc24.xyz/cgi-bin/render.cgi?data=' + str(encode)[2:-1])
		
		print('\nAdvanced Info:')
		print(f'Mii CRC16 (CCITT-XModem): {crc16(miidata)}')
		print(f'Ghost CRC32: {hex_string(binascii.crc32(ghostbytes[:-4]).to_bytes(4, "big"))}')
		if not crc16(miidata) == hex_string(ghost.crc16_mii):
			print(f'Mii CRC is not correct! {crc16(miidata)} - {hex_string(ghost.crc16_mii)}')
		if not binascii.crc32(ghostbytes[:-4]) == ghost.crc32:
			print(f'Ghost CRC is not correct!: {binascii.crc32(ghostbytes[:-4])} - {ghost.crc32}')
		if is_ctgp:
			print(f'CTGP Footer Version: v{ghost.footer_version}')
