#!/usr/bin/python
 
"""
	IF you copy/paste 'script.xvbmc.update' please keep the credits -2- EPiC -4- XvBMC-NL, Thx.
"""

#   script.xvbmc.update (XvBMC Update & Development 'Nederland')
#
#   Copyright (C) 2016
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re,base64,urllib,urllib2,uuid
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,shutil,time
import sqlite3
from libs import downloader,extract
from libs import common as Common

from libs import addon_able

################ ProgTitle="XvBMC Update+Development" #################
AddonID        = 'script.xvbmc.update'
addon_id       = 'script.xvbmc.update'
ADDON          = xbmcaddon.Addon(id=addon_id)
addonPath      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.xvbmc.update')
ART            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/media/'))
ICON           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
mediaPath      = os.path.join(addonPath, 'media')
xvbmcfanart    = os.path.join(addonPath, 'fanart.jpg')
FANART         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
dialog         = xbmcgui.Dialog()
base           = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL1h2Qk1DL3JlcG9zaXRvcnkueHZibWMvbWFzdGVyL3ppcHMv'
locate         = 'aHR0cDovL3d3dy5tZWRpYWZpcmUuY29tL2ZpbGUv'
bestand        = '20160906222118'                     # universal recent Pi-build file format voodoo and shit....
pcreset        = 'URL nog te verhuizen'               # zero-fill standalone 
pcrestorefinal = 'URL nog te verhuizen'               # standalone-final 
pcrestoreupgrd = 'ToDo'                               # betas-4-standalone 
pireset        = 'URL nog te verhuizen'               # zero-fill raspberrys 
pirestorefinal = 'ua67cbfa5nf1pvf/20161224210044.tar' # raspberry-final 
pirestoreupgrd = 'ToDO'                               # betas-4-raspberrys 
raspberryPi    = '[COLOR=white]\'Raspberry Pi\'[/COLOR]'
Standalonefork = '[COLOR=white]\'Standalone\'[/COLOR]'
warning        = '[COLOR=red][B]!!!  WARNING  !!![/B][/COLOR]'
readme         = 'if you\'re seeing this message read this first[B]:[/B]'
noservicepack  = 'Sorry the [B]S[/B]ervice[B]P[/B]ack update is [COLOR=red]outdated[/COLOR] at this moment'
notforked      = '[COLOR dimgray](a new XvBMC\'s [B]Pi[/B]-image *fork* is coming soon[B]...[/B])[/COLOR]'
MainTitle      = "XvBMC Nederland"
upgrade40      = 'XvBMC upgrade v4 beta'
upgrade40dl    = 'Download XvBMC v4 beta upgrade -4-'
upgrade31      = 'XvBMC v3.1 *[B]final[/B]* (Jarvis)'
upgrade31dl    = 'Download XvBMC\'s [COLOR=lime]v3.1 *final* 13-10-\'16 (Pi)[/COLOR]'
resetos        = 'XvBMC Reset Kodi'
resetosdl      = 'import XvBMC\'s [COLOR=lime]Kodi defaults[/COLOR]'
resetinfo      = '[COLOR dimgray] (default RPi+Portable) [I]~Jarvis 16.1~[/I][/COLOR]'
comingsoon     = '[B]Coming soon:[/B] onze nieuwste [COLOR=lime]v4 *beta*[/COLOR]'
ingeschakeld   = '[COLOR red]INSTALL: [/COLOR]'
uitgeschakeld  = '[COLOR=red]Disabled: [/COLOR]'
waarschuwing   = '[COLOR red]WARNING: [/COLOR]'
herstart       = 'PRESS OK TO FORCECLOSE AND REBOOT!'
forceersluiten = '[COLOR dimgray]indien forceclose niet werkt, herstart uw systeem handmatig, [/COLOR]if forceclose does not work shutdown manually'
versietxt      = xbmc.translatePath(os.path.join('special://home/userdata','versie.txt'))
currentbldtxt  = base64.b64decode(base)+'update/buildversie.txt'
uwspversietxt  = xbmc.translatePath(os.path.join('special://home/userdata','versiesp.txt'))
currentsptxt   = base64.b64decode(base)+'update/sp/versiesp.txt'
USER_AGENT     = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
U              = ADDON.getSetting('User')


#######################################################################
#						Define Menus
#######################################################################

def mainMenu():
	xbmc.executebuiltin("Container.SetViewMode(51)")
	versie = checkxvbmcversie()
	addItem('[COLOR dimgray][B]----------[/B] INSTALLED BUILD[B]:[/B] %s [/COLOR]' % versie,'url','',os.path.join(mediaPath, "wtf.png"))
	buildversion = OPEN_URL(currentbldtxt).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(buildversion)
	for name,url,iconimage,fanart,description in match:
		addDir('[COLOR darkgreen]XvBMC v[B]3[/B].1 *final* Jarvis[/COLOR] [COLOR dimgray] (RPi+Portable) ~released[B]:[/B] %s[/COLOR]' % name,url, 2,ART+'dev.png',FANART,description)
		addDir('[COLOR red]XvBMC v[B]4[/B].0 beta upgrade[/COLOR] [COLOR dimgray] (RPi+Portable) ~released[B]:[/B] %s[/COLOR]' % name,url, 1,ART+'dev.png',FANART,description)
	addItem('XvBMC Reset Kodi' +resetinfo, 'url', 3,os.path.join(mediaPath, "dev.png"))
	spversie = checkSPversie()
	addItem('[COLOR dimgray][B]----------[/B] INSTALLED SERVICEPACK[B]:[/B] %s[/COLOR]' % spversie,'url','',os.path.join(mediaPath, "wtf.png"))
	spversion = OPEN_URL(currentsptxt).replace('\n','').replace('\r','')  #http://bit.ly/2lStxyU
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(spversion)
	for name,url,iconimage,fanart,description in match:
		addDir('XvBMC [B]S[/B]ervice[B]P[/B]ack (v3.1[B]+[/B]) [COLOR dimgray]~released[B]:[/B] %s[/COLOR]' % name,url, 4,ART+'dev.png',FANART,description)
		addDir('XvBMC [B]B[/B]ulk[B]P[/B]ack \'all-in-1\' (v3.1[B]+[/B]) [COLOR dimgray]~released[B]:[/B] %s[/COLOR]' % name,url, 5,ART+'dev.png',FANART,description)
	addItem('XvBMC [COLOR white]#DEV#[/COLOR] Corner [COLOR dimgray](firmware, OS, etc.)[/COLOR]', 'url', 8,os.path.join(mediaPath, "dev.png"))
	addItem('XvBMC [B]A[/B]dvancedsettings Unlocker [COLOR dimgray](reset)[/COLOR]', 'url', 12,os.path.join(mediaPath, "dev.png"))
	addItem('XvBMC [B]E[/B]nable Kodi [COLOR white]Addons[/COLOR] [COLOR dimgray](v[COLOR white]17[/COLOR] Krypton)[/COLOR]', 'url', 14,os.path.join(mediaPath, "dev.png"))
	addItem('XvBMC [B]E[/B]nable Kodi [COLOR white]RTMP[/COLOR] [COLOR dimgray](v[COLOR white]17[/COLOR] Krypton)[/COLOR]', 'url', 15,os.path.join(mediaPath, "dev.png"))
	addItem('XvBMC [COLOR white]O[/COLOR]ver[COLOR white]C[/COLOR]lock [COLOR dimgray] (raspberry pi **only**)[/COLOR]', 'url', 7,os.path.join(mediaPath, "dev.png"))
	addItem('XvBMC [B]S[/B]choonmaak/[B]M[/B]aintenance [COLOR darkgreen][I](kodi schoonmaak)[/I][/COLOR]', 'url', 11,os.path.join(mediaPath, "xvbmc.png"))
	addItem('XvBMC [B]W[/B]hois & about [COLOR dimgray](over xvbmc & [COLOR dodgerblue][B]i[/B][/COLOR]nfo)[/COLOR]', 'url', 9,os.path.join(mediaPath, "xvbmc.png"))
	addItem('[COLOR white][B]Back[/B][/COLOR]', 'url', 13,os.path.join(mediaPath, "dev.png"))


#######################################################################
#						Add to menus
#######################################################################

def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setArt({'fanart': xvbmcfanart})
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==1 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        elif mode==2 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        elif mode==4 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        elif mode==5 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#######################################################################
#						Parses Choice
#######################################################################
      
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
							
	return param   


#######################################################################
#						Work Functions
#######################################################################

def checkxvbmcversie():
    if os.path.isfile(versietxt):
        file = open(versietxt, 'r')
        versie = file.read()
        file.close()
        return '[COLOR lime]' +versie +'[/COLOR]'
    else:
        return 'XvBMC Version Unknown'

def XvbmcPiUpgrade(url):
    if dialog.yesno(upgrade40 +' [B]- Pi[/B] image', upgrade40dl +' [B]Raspberry [COLOR=white]Pi?[/COLOR][/B]',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pirestoreupgrd #upgrade40
        path = xbmc.translatePath(os.path.join('/storage/.restore/',''))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.tar')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        time.sleep(3)
        dialog.ok(MainTitle +'[B]-  Pi[/B]', upgrade40 +' done.', herstart,  forceersluiten)
        Common.killKodi()

def XvbmcUpgradePortable(url):
    if dialog.yesno(upgrade40 +' - Portable build', upgrade40dl +' [COLOR=white]Portable?[/COLOR]','','(...enig [B]geduld[/B] is vereist, please be patient...)',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pcrestoreupgrd #upgrade40
        path = xbmc.translatePath(os.path.join('special://home/','temp'))
        addonpath = xbmc.translatePath(os.path.join('special://home/','addons'))
        userpath = xbmc.translatePath(os.path.join('special://home/','userdata'))
        mediapath = xbmc.translatePath(os.path.join('special://home/','media'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland (dutch)","XvBMC-NL: doing some crazy ass VOODOO...",'', '[COLOR dimgray](format C:[B] ;-p [/B]*please wait*)[/COLOR]')
            Common.removefolder(addonpath, 'script.xvbmc.update')
            Common.removefolder(userpath, 'script.xvbmc.update')
            Common.removefolder(mediapath, 'script.xvbmc.update')
            dp.update(0,"", "now really going medieval on your ass")
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - UPGRADER","XvBMC-NL: doing some upgrading VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            for root, dirs, files in os.walk(xbmc.translatePath('special://thumbnails')):
                file_count = 0
                file_count += len(files)
                if file_count > 0:                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
            dialog.ok(MainTitle +' - Portable', upgrade40 +' done.', herstart,  forceersluiten)
            Common.killKodi()


def XvbmcPiFinal(url):
    if dialog.yesno(upgrade31 +' [B]- Pi[/B] image', upgrade31dl +' [COLOR=white]image?[/COLOR]',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pirestorefinal #upgrade31
        path = xbmc.translatePath(os.path.join('/storage/.restore/',''))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.tar')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        time.sleep(3)
        dialog.ok(MainTitle +'[B]-  Pi[/B]', upgrade31 +' done.', herstart,  forceersluiten)
        Common.killKodi()

def XvbmcPortableFinal(url):
    if dialog.yesno(upgrade31 +' - Portable', upgrade31dl +' [COLOR=white]fork?[/COLOR]','','(...enig [B]geduld[/B] is vereist, please be patient...)',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pcrestorefinal #upgrade31
        path = xbmc.translatePath(os.path.join('special://home/','temp'))
        addonpath = xbmc.translatePath(os.path.join('special://home/','addons'))
        userpath = xbmc.translatePath(os.path.join('special://home/','userdata'))
        mediapath = xbmc.translatePath(os.path.join('special://home/','media'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland (dutch)","XvBMC-NL: doing some crazy ass VOODOO...",'', '[COLOR dimgray](format C:[B] ;-p [/B]*please wait*)[/COLOR]')
            Common.removefolder(addonpath, 'script.xvbmc.update')
            Common.removefolder(userpath, 'script.xvbmc.update')
            Common.removefolder(mediapath, 'script.xvbmc.update')
            dp.update(0,"", "now really going medieval on your ass")
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - UPGRADER","XvBMC-NL: doing some upgrading VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            for root, dirs, files in os.walk(xbmc.translatePath('special://thumbnails')):
                file_count = 0
                file_count += len(files)
                if file_count > 0:                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
            dialog.ok(MainTitle +' - Portable', upgrade31 +' done.', herstart,  forceersluiten)
            Common.killKodi()


def XvbmcPiReset(url):
    if dialog.yesno(resetos +' [B]- Pi[/B] image', resetosdl +'; reset to Jarvis v[B]16.1[/B]?','','(...enig [B]geduld[/B] is vereist, please be patient...)',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pireset #factorypresets
        path = xbmc.translatePath(os.path.join('/storage/.restore/',''))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.tar')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        time.sleep(3)
        dialog.ok(MainTitle +'[B]-  Pi[/B]', resetos +' done.', herstart,  forceersluiten)
        Common.killKodi()

def XvbmcResetPortable(url):
    if dialog.yesno(resetos +' - Portable', resetosdl +'; reset to default[B]?[/B]','','(...enig [B]geduld[/B] is vereist, please be patient...)',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(locate)+pcreset #factorypresets
        path = xbmc.translatePath(os.path.join('special://home/','temp'))
        addonpath = xbmc.translatePath(os.path.join('special://home/','addons'))
        userpath = xbmc.translatePath(os.path.join('special://home/','userdata'))
        mediapath = xbmc.translatePath(os.path.join('special://home/','media'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, bestand+'.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland (dutch)","XvBMC-NL: doing some crazy ass VOODOO...",'', '[COLOR dimgray](format C:[B] ;-p [/B]*please wait*)[/COLOR]')
            Common.removefolder(addonpath, 'script.xvbmc.update')
            Common.removefolder(userpath, 'script.xvbmc.update')
            Common.removefolder(mediapath, 'script.xvbmc.update')
            dp.update(0,"", "now really going medieval on your ass")
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - UPGRADER","XvBMC-NL: doing some upgrading VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            for root, dirs, files in os.walk(xbmc.translatePath('special://thumbnails')):
                file_count = 0
                file_count += len(files)
                if file_count > 0:                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
            dialog.ok(MainTitle +' - Portable', resetos +' done.', herstart,  forceersluiten)
            Common.killKodi()


def checkSPversie():
    if os.path.isfile(uwspversietxt):
        file = open(uwspversietxt, 'r')
        spversie = file.read()
        file.close()
        return '[COLOR lime]' +spversie +'[/COLOR]'
    else:
        return 'ServicePack Unknown'
		
def ServicePack(url):
    Common.verifyplatform()
    if dialog.yesno('XvBMC NL most recent ServicePack','Download de laatste XvBMC [COLOR=white][B]S[/B]ervice[B]P[/B]ack?[/COLOR]',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(base)+'update/sp/03-servicepack.zip' # servicepacks
        path = xbmc.translatePath(os.path.join('special://home','addons','packages'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, 'update.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - Updater","XvBMC-NL: doing some updating VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            dialog.ok('XvBMC-NL ServicePack - Update finished', 'een REBOOT van uw systeem is SOMS wenselijk...','', '(if add-ons do NOT work you probably should reboot first)')
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            xbmc.executebuiltin('XBMC.RunScript(special://home/addons/script.schoonmaak/purge.py)')

def UpdateRollup(url):
    Common.verifyplatform()
    if dialog.yesno('XvBMC NL ServicePack Update Rollup','Download ALLE XvBMC [COLOR=white][B]SP[/B][/COLOR]-updates [COLOR=white]([B]all-in-1[/B])?[/COLOR]',nolabel='Nee, No',yeslabel='Ja, Yes'):
        url=base64.b64decode(base)+'update/sp/03-sp-rollup.zip' # roll-ups
        path = xbmc.translatePath(os.path.join('special://home','addons','packages'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, 'update.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - Updater","XvBMC-NL: doing some updating VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            dialog.ok('XvBMC-NL ServicePack - RollUp finished', 'een REBOOT van uw systeem is SOMS wenselijk...','', '(if add-ons do NOT work you probably should reboot first)')
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            xbmc.executebuiltin('XBMC.RunScript(special://home/addons/script.schoonmaak/purge.py)')


def xvbmcOverclock(url):
    pluginpath=os.path.exists(xbmc.translatePath(os.path.join('special://home','addons','script.xvbmc.oc')))
    if pluginpath: xbmc.executebuiltin("XBMC.RunAddon(script.xvbmc.oc)")
    else:
        myplatform = Common.platform()
        print "Platform: " + str(myplatform)
        if myplatform == 'linux': # Open-/LibreELEC #linux
            url=base64.b64decode(base)+'script.xvbmc.oc/script.xvbmc.oc-4.0.0.zip'
            path = xbmc.translatePath(os.path.join('special://home','addons','packages'))
            if not os.path.exists(path):
                os.makedirs(path)
            lib=os.path.join(path, 'script.xvbmc.oc-4.0.0.zip')
            try:
                os.remove(lib)
            except:
                pass
            downloader.download(url, lib)
            if os.path.exists(lib):
                addonfolder = xbmc.translatePath(os.path.join('special://','home','addons',''))
                time.sleep(3)
                dp = xbmcgui.DialogProgress()
                dp.create("XvBMC Nederland - Updater","XvBMC-#OC: doing some VOODOO...",'', 'Please Wait')
                dp.update(0,"", "*Extracting ZiP Please Wait*")
                extract.all(lib,addonfolder,dp)
                dp.close()
                try: os.remove(lib)
                except: pass
                print '=== Kodi.#OC XvBMC Nederland ==='
                xbmc.executebuiltin("UpdateLocalAddons")
               #xbmc.executebuiltin("RunAddon(script.xvbmc.oc)")

                xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
                version=float(xbmc_version[:4])
                if version >= 17.0 and version <= 17.9:
                    codename = 'Krypton'
                else:
                    codename = 'Pass'
                if codename == "Krypton": #Krypton
                    xbmc.executebuiltin("RunAddon(script.xvbmc.oc)")
                    dialog.ok(warning, '[B]...if[/B] #OC#-Addon isn\'t enabled after reboot,', 'please enable add-ons with our \'addon-enabler\' yourself.', '[COLOR dimgray](geen #OC#-Addon; gebruik handmatige \'addon-enabbler\')[/COLOR]')
                    AddonsEnable()
                else:
                   #dialog.ok(MainTitle +' : add-ons enabler', '[COLOR=red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re not running Kodi v17 Krypton.','[NL] dit is geen Kodi v17 Krypton.')
                    xbmc.executebuiltin("RunAddon(script.xvbmc.oc)")

        else: #rest
            dialog.ok(warning, '[COLOR=red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re running a \'none linux os\' ie. Open-/LibreELEC','[NL] dit is geen Raspberry Pi met Open-/LibreELEC OS...')
            print "none linux os"
#           xbmc.executebuiltin("UpdateLocalAddons")
#           xbmc.executebuiltin("RunAddon(script.xvbmc.oc)")


def subDEVmenu(url):
    pluginpath=os.path.exists(xbmc.translatePath(os.path.join('special://home','addons','script.xvbmc.dev')))
    if pluginpath: xbmc.executebuiltin("XBMC.RunAddon(script.xvbmc.dev)")
    else:
        myplatform = Common.platform()
        print "Platform: " + str(myplatform)
        if myplatform == 'linux': # Open-/LibreELEC #linux
            url=base64.b64decode(base)+'script.xvbmc.dev/script.xvbmc.dev-4.0.0.zip'
            path = xbmc.translatePath(os.path.join('special://home','addons','packages'))
            if not os.path.exists(path):
                os.makedirs(path)
            lib=os.path.join(path, 'script.xvbmc.dev-4.0.0.zip')
            try:
                os.remove(lib)
            except:
                pass
            downloader.download(url, lib)
            if os.path.exists(lib):
                addonfolder = xbmc.translatePath(os.path.join('special://','home','addons',''))
                time.sleep(3)
                dp = xbmcgui.DialogProgress()
                dp.create("XvBMC Nederland - Updater","XvBMC-#DEV: doing some VOODOO...",'', 'Please Wait')
                dp.update(0,"", "*Extracting ZiP Please Wait*")
                extract.all(lib,addonfolder,dp)
                dp.close()
                try: os.remove(lib)
                except: pass
                print '=== Kodi.#DEV XvBMC Nederland ==='
                xbmc.executebuiltin("UpdateLocalAddons")
               #xbmc.executebuiltin("RunAddon(script.xvbmc.dev)")

                xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
                version=float(xbmc_version[:4])
                if version >= 17.0 and version <= 17.9:
                    codename = 'Krypton'
                else:
                    codename = 'Pass'
                if codename == "Krypton": #Krypton
                    xbmc.executebuiltin("RunAddon(script.xvbmc.dev)")
                    dialog.ok(warning, '[B]...if[/B] #DEV#-Addon isn\'t enabled after reboot,', 'please enable add-ons with our \'addon-enabler\' yourself.', '[COLOR dimgray](geen #DEV#-Addon; gebruik handmatige \'addon-enabbler\')[/COLOR]')
                    AddonsEnable()
                else:
                   #dialog.ok(MainTitle +' : add-ons enabler', '[COLOR=red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re not running Kodi v17 Krypton.','[NL] dit is geen Kodi v17 Krypton.')
                    xbmc.executebuiltin("RunAddon(script.xvbmc.dev)")

        else: #rest
            dialog.ok(warning, '[COLOR=red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re running a \'none linux os\' ie. Open-/LibreELEC','[NL] dit is geen Raspberry Pi met Open-/LibreELEC OS...')
            print "none linux os"
#           xbmc.executebuiltin("UpdateLocalAddons")
#           xbmc.executebuiltin("RunAddon(script.xvbmc.dev)")


def unlocker():
#	EPiC XvBMC user preferences and tweaking
    dialog.ok(MainTitle +' - unlocker',' ' , 'unlock advancedsettings for this build', '[COLOR dimgray](+reset \'advancedsettings.xml\' -use at your own risk)[/COLOR]')
    addonmappie=xbmc.translatePath(os.path.join('special://home/userdata/'))
    advancedunlock=base64.b64decode('YWR2YW5jZWRzZXR0aW5ncy54bWw=')
    removed = True
    try:
        os.unlink(addonmappie+advancedunlock)
    except:
        removed = False

    if removed:
        dialog.ok(MainTitle +' - [B]UNLOCKED[/B]', '[COLOR=green][B]!!!  FINISHED  !!![/B][/COLOR]', '[B]Herstart[/B] Kodi ter afronding \'unlocker\' (force close)', '[B]Reboot[/B] Kodi to complete \'unlocker\' (force close)')
        os._exit(1)
    else:
        dialog.ok(MainTitle +' - [B]OOOOOOPS[/B]', '[COLOR=red][B]!!!  Failed  !!![/B][/COLOR]', '[B]Nope![/B] helaas geen succes (niks te \'unlocken\')', '[B]Nope![/B] close but no cigar  (nothing to \'unlock\')')


def xvbmcMaintenance(url):
    pluginpath=os.path.exists(xbmc.translatePath(os.path.join('special://home','addons','script.schoonmaak')))
    if pluginpath: xbmc.executebuiltin("RunAddon(script.schoonmaak)")
    else:
        url=base64.b64decode(base)+'script.schoonmaak/script.schoonmaak-1.10.22.zip'
        path = xbmc.translatePath(os.path.join('special://home','addons','packages'))
        if not os.path.exists(path):
            os.makedirs(path)
        lib=os.path.join(path, 'script.schoonmaak-1.10.22.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        if os.path.exists(lib):
            addonfolder = xbmc.translatePath(os.path.join('special://','home','addons',''))
            time.sleep(3)
            dp = xbmcgui.DialogProgress()
            dp.create("XvBMC Nederland - Updater","XvBMC-#Maintenance: doing some of our VOODOO...",'', 'Please Wait')
            dp.update(0,"", "*Extracting ZiP Please Wait*")
            extract.all(lib,addonfolder,dp)
            dp.close()
            try: os.remove(lib)
            except: pass
            print '=== Kodi.#CrapClean XvBMC Nederland ==='
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("RunAddon(script.schoonmaak)")


def AddonsEnable():
    databasePath   = xbmc.translatePath('special://database')
    adb27 = os.path.join(databasePath,"Addons27.db") #krypton
    if os.path.exists(adb27):
        #Thx. Patrick (en Wilfred)#
        conn = sqlite3.connect(xbmc.translatePath("special://database/Addons27.db"))
        c = conn.cursor()
        c.execute("UPDATE installed SET enabled = 1 WHERE addonID NOT LIKE '%audiodecoder.%' AND addonID NOT LIKE '%inputstream.%' AND addonID NOT LIKE '%pvr.%' AND addonID NOT LIKE '%screensaver.%' AND addonID NOT LIKE '%visualization.%';")
        conn.commit()
        conn.close()
        #dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno(MainTitle +' : add-ons [B]enabled[/B]', '[COLOR=green][B]!!!  FINISHED  !!![/B][/COLOR]', '[B]Herstart[/B] Kodi ter afronding \'enable\' (force close)', '[B]Reboot[/B] Kodi to complete \'enable\' (force close)',yeslabel='[COLOR lime]Ja/Yes[/COLOR]',nolabel='[COLOR red]Nee/No[/COLOR]')
        if choice == 1:
            os._exit(1)
        else: pass
    else:
        dialog.ok(MainTitle +' : add-ons enabler', '[COLOR=red][B]!!!  NOPE  !!![/B][/COLOR]','[US] you\'re not running Kodi v17 Krypton.','[NL] dit is geen Kodi v17 Krypton.')

def EnableRTMP():
		dialog = xbmcgui.Dialog()
		try: addon_able.set_enabled("inputstream.adaptive")
		except: pass
		time.sleep(0.5)
		try: addon_able.set_enabled("inputstream.rtmp")
		except: pass
		time.sleep(0.5)
		xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
		#xbmc.executebuiltin("UpdateLocalAddons")
		dialog.ok("Operation Complete!", "Live Streaming has been Enabled!",
		"    Brought To You By %s " % MainTitle)


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def closeandexit():
#	http://kodi.wiki/view/Keyboard.xml
	xbmc.executebuiltin('Action(back)')


#######################################################################
#						ABOUT
#######################################################################

def AboutXvBMC():
	text = ''
	twit = 'https://raw.githubusercontent.com/XvBMC/repository.xvbmc/master/readme.xml'
	req = urllib2.Request(twit)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("<title>(.+?)</title><pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)
	for status, dte in match:
	    try:
			    status = status.decode('ascii', 'ignore')
	    except:
			    status = status.decode('utf-8','ignore')
	    dte = dte[:-15]
	    status = status.replace('&amp;','')
	    dte = '[COLOR lime][B]'+dte+'[/B][/COLOR]'
	    text = text+dte+'\n'+status+'\n'+'\n'
	infoTXT('[COLOR lime]Over XvBMC Nederland[/COLOR]', text)	

def infoTXT(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass


#######################################################################
#						START MAIN
#######################################################################              

params=get_params()
url=None
name=None
mode=None
fanart=None
iconimage=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:    
		fanart=urllib.unquote_plus(params["fanart"])
except: 
		pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Base: "+str(base)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Fanart: "+str(fanart)
print "IconImage: "+str(iconimage)

if mode==None or url==None or len(url)<1:
	mainMenu()

elif mode==1:
#	Upgrade(v40)
    myplatform = Common.platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': # Open-/LibreELEC
        dialog.ok(upgrade40 +' [B]- Pi[/B]', uitgeschakeld +upgrade40 +' '+raspberryPi,'', comingsoon +' image [COLOR dimgray] [B]([/B]Pi 2+3[B])[/B][/COLOR]') # DiSABLE indien v4.0 *online* #
        #XvbmcPiUpgrade(url) # BLOCKED-4-NOW (v4.0) # 
    else: #rest
        print "none linux os"
        dialog.ok(upgrade40 +' - Portable', uitgeschakeld +upgrade40 +' '+Standalonefork,'', comingsoon +' build [COLOR dimgray] [B]([/B]Pi fork[B])[/B][/COLOR]') # DiSABLE indien v4.0 *online* #
        #XvbmcUpgradePortable(url) # BLOCKED-4-NOW (v4.0) # 

elif mode==2:
#	Upgrade(v31)
    myplatform = Common.platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': # Open-/LibreELEC
        dialog.ok(upgrade31 +' [B]- Pi[/B]', ingeschakeld +upgrade31 +' '+raspberryPi +' !!!','', comingsoon +' image [COLOR dimgray] [B]([/B]Pi 2+3[B])[/B][/COLOR]') # AANPASSEN in Tip! indien v4.0 *online* #
        XvbmcPiFinal(url)
    else: #rest
        print "none linux os"
       #dialog.ok(upgrade31 +' - Portable', ingeschakeld +upgrade31 +' '+Standalonefork +' !!!','', comingsoon +' build [COLOR dimgray] [B]([/B]Pi fork[B])[/B][/COLOR]') # AANPASSEN in Tip! indien v4.0 *online* #
        dialog.ok(upgrade31 +' - Portable', uitgeschakeld +upgrade31 +' '+Standalonefork +' !!!','', comingsoon +' build [COLOR dimgray] [B]([/B]Pi fork[B])[/B][/COLOR]') # AANPASSEN in Tip! indien v4.0 *online* #
        #XvbmcPortableFinal(url)

elif mode==3:
#	Reset(null-"upgrade")
    myplatform = Common.platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': # Open-/LibreELEC
       #dialog.ok(resetos +' [B]- Pi[/B]', waarschuwing +resetos +' '+raspberryPi +' -2- [B]Jarvis[/B]','', '[COLOR dimgray][B]NOTE: [/B][/COLOR]' +resetinfo +'   [B]!!![/B]')
        dialog.ok(resetos +' [B]- Pi[/B]', uitgeschakeld +resetos +' '+raspberryPi +' -2- [B]Jarvis[/B]','', '[COLOR dimgray][B]NOTE: [/B][/COLOR]' +resetinfo +'   [B]!!![/B]')
        #XvbmcPiReset(url)
    else: #rest
        print "none linux os"
       #dialog.ok(resetos +' - Portable', waarschuwing +resetos +' '+Standalonefork +' -2- default','', '[COLOR dimgray][B]NOTE: [/B][/COLOR]' +resetinfo +'   [B]!!![/B]')
        dialog.ok(resetos +' - Portable', uitgeschakeld +resetos +' '+Standalonefork +' -2- default','', '[COLOR dimgray][B]NOTE: [/B][/COLOR]' +resetinfo +'   [B]!!![/B]')
        #XvbmcResetPortable(url)

elif mode==4:
#	ServicePack(url)
    myplatform = Common.platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': # Open-/LibreELEC
        dialog.ok('XvBMC-NL most recent ServicePack', uitgeschakeld +' download laatste XvBMC [COLOR=white]ServicePack[/COLOR]','', upgrade31dl +' image') # DiSABLE indien SP *online* #
        #ServicePack(url) # BLOCKED-4-NOW (v4.0) # 
    else: #rest
        print "none linux os"
        dialog.ok(warning,  readme, noservicepack, notforked) # DiSABLE indien SP *online* #
        #ServicePack(url) # BLOCKED-4-NOW (v4.0) # 

elif mode==5:
#	UpdateRollup(url)
    myplatform = Common.platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': # Open-/LibreELEC
        dialog.ok('XvBMC-NL ServicePack Update Rollup', uitgeschakeld +' download alle XvBMC SP-updates [COLOR=white](all-in-1)[/COLOR]','', upgrade31dl +' image') # DiSABLE indien SP *online* #
        #ServicePack(url) # BLOCKED-4-NOW (v4.0) # 
    else: #rest
        print "none linux os"
        dialog.ok(warning,  readme, noservicepack, notforked) # DiSABLE indien SP *online* #
        #UpdateRollup(url) # BLOCKED-4-NOW (v4.0) # 

#elif mode==6:
#	forceRefresh()

elif mode==7:
	xvbmcOverclock(url)

elif mode==8:
    subDEVmenu(url)

elif mode==9:	
	AboutXvBMC()

#elif mode==10:	
#	xvbmcLog()

elif mode==11:
	xvbmcMaintenance(url)

elif mode==12:
    unlocker()

elif mode==13:
	closeandexit()

elif mode==14:
	AddonsEnable()

elif mode==15:
	EnableRTMP()


xbmcplugin.endOfDirectory(int(sys.argv[1]))

