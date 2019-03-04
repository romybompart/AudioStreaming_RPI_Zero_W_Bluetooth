#!/usr/bin/env python
##mixertest.py
##This is an example of using the ALSA mixer API
##Romy Bompart

import alsaaudio

def list_cards():
	print("Available sound cards:")
	for i in alsaaudio.card_indexes():
		(name, longname) = alsaaudio.card_name(i)
		print("%d:, %s (%s)" % (i, name, longname))

def list_mixers():
	print ("Available mixer controls:")
	for m in alsaaudio.mixers():
		print ( " '%s' " % m)

def show_mixer(MixerName):
	mixer = alsaaudio.Mixer(MixerName)
	print ("Mixer name: '%s" % mixer.mixer())
	print ( "Capabilities: %s %s" % (' '.join(mixer.volumecap()), ' '.join(mixer.switchcap())))
	volumes = mixer.getvolume()
	for i in range(len(volumes)):
		print ("Channel %i volume: %i%%" % (i, volumes[i]))

	try:
		mutes = mixer.getmute()
		for i in range (len(mutes)):
			if mutes[i]:
				print( "channel %i is muted" % i)
	except alsaaudio.ALSAAudioError:
		print ("No mute supported")
		pass

	try:
		recs = mixer.getrec()
		for i in range(len(recs)):
			if recs[i]:
				print ( "Channel %i is recording" % i)
	except alsaaudio.ALSAAudioError:
		print ( "No recording supported")
		pass

if __name__ == '__main__':

	print ( "_____________________________________________ ")
	list_cards()
	
	print ( "_____________________________________________ ")
	list_mixers()
	
	print ( "______________________________________________ ")
	MixerName = input ("Enter the Mixer Name: ")
	print ( " You entered: {} ".format( MixerName ))

	print ( "______________________________________________ ")
	show_mixer(MixerName)

	print ( "______________________________________________ ")
	MixerName = 'Digital'
	m = alsaaudio.Mixer(MixerName)

	exit = 'n'
	while ( exit == 'n' ) : 
		print ( "______________________________________________ ")
		vol = m.getvolume()
		print ( "Current volume at: {}".format(vol))
		setvol = input("Enter a new volume: ")
		try:
			vol = int(setvol)
			if vol <= 100 and vol >= 0: 
				m.setvolume(vol , alsaaudio.MIXER_CHANNEL_ALL)
			else:
				vol = 50
				m.setvolume(vol, alsaaudio.MIXER_CHANNEL_ALL)
			print ( " New volume is : {}".format( vol ) )
		except ValueError:
			print ( "Enter a integer number please")
			pass
		exit = input ("Do you wanna exit y/n?:" )
			
