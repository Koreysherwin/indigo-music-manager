#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music Manager Plugin for Indigo
Provides unified control over Spotify, Apple Music, VLC, and Airfoil Satellite with automatic mutual exclusion
"""

import indigo
import time


class Plugin(indigo.PluginBase):
    """Main plugin class for Music Manager"""
    
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get("showDebugInfo", False)
        self.deviceDict = {}
        
    def startup(self):
        """Called when plugin starts"""
        self.debugLog(u"Music Manager Plugin startup called")
        
    def shutdown(self):
        """Called when plugin shuts down"""
        self.debugLog(u"Music Manager Plugin shutdown called")
    
    ########################################
    # ConfigUI Methods
    ########################################
    
    def getSpotifyDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of Spotify devices"""
        self.debugLog(u"getSpotifyDeviceList called")
        deviceList = [(0, "-- None --")]
        for dev in indigo.devices.iter():
            self.debugLog(u"Checking device: {} with pluginId: {}".format(dev.name, dev.pluginId))
            if dev.pluginId == "com.sherwinsound.spotifycontrol":
                self.debugLog(u"Found Spotify device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} Spotify devices".format(len(deviceList)))
        return deviceList
    
    def getAppleMusicDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of Apple Music devices.

        v1.2.7: be tolerant of Apple Music plugin id/name variants so
        existing installs show up in the ConfigUI even if the bundle id was
        changed or rebuilt locally.
        """
        self.debugLog(u"getAppleMusicDeviceList called")
        deviceList = [(0, "-- None --")]
        applePluginIds = (
            "com.indigodomo.applemusic",
            "com.sherwinsound.applemusic",
            "com.sherwinsound.applemusiccontrol",
            "com.indigodomo.applemusiccontrol",
        )
        for dev in indigo.devices.iter():
            pluginId = getattr(dev, "pluginId", "") or ""
            name = getattr(dev, "name", "") or ""
            deviceTypeId = getattr(dev, "deviceTypeId", "") or ""
            stateKeys = set(getattr(dev, "states", {}).keys())

            looksLikeAppleMusic = (
                pluginId in applePluginIds or
                "applemusic" in pluginId.lower().replace(" ", "") or
                "apple music" in name.lower() or
                deviceTypeId == "appleMusicPlayer" or
                ({"isPlaying", "trackName", "artist", "album"}.issubset(stateKeys) and "spotify" not in pluginId.lower())
            )

            if looksLikeAppleMusic:
                self.debugLog(u"Found Apple Music device: {} ({})".format(dev.name, pluginId))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} Apple Music devices".format(len(deviceList)))
        return deviceList
    
    def getVLCDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of VLC devices"""
        self.debugLog(u"getVLCDeviceList called")
        deviceList = [(0, "-- None --")]
        for dev in indigo.devices.iter():
            if dev.pluginId == "com.indigodomo.vlc":
                self.debugLog(u"Found VLC device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} VLC devices".format(len(deviceList)))
        return deviceList
        
    def getAirfoilDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of Airfoil Satellite devices"""
        self.debugLog(u"getAirfoilDeviceList called")
        deviceList = [(0, "-- None --")]
        for dev in indigo.devices.iter():
            if dev.pluginId == "com.sherwinsound.airfoilsatellite":
                self.debugLog(u"Found Airfoil Satellite device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} Airfoil Satellite devices".format(len(deviceList)))
        return deviceList

    def deviceStartComm(self, dev):
        """Called when device communication starts"""
        self.debugLog(u"Starting device: " + dev.name)
        
        # Store device info
        self.deviceDict[dev.id] = {
            'device': dev,
            'lastActiveService': None,
            'lastSpotifyState': False,
            'lastAppleMusicState': False,
            'lastVLCState': False,
            'lastAirfoilState': False
        }
        
        # Do initial update
        self.updateMusicStatus(dev)
        
    def deviceStopComm(self, dev):
        """Called when device communication stops"""
        self.debugLog(u"Stopping device: " + dev.name)
        if dev.id in self.deviceDict:
            del self.deviceDict[dev.id]
            
    def runConcurrentThread(self):
        """Main plugin loop - monitors music players and enforces exclusivity"""
        try:
            while True:
                for devId, devInfo in list(self.deviceDict.items()):
                    dev = devInfo['device']
                    self.updateMusicStatus(dev)
                
                self.sleep(0.5)  # Update every 0.5 seconds
                
        except self.StopThread:
            pass
            
    def _toDeviceId(self, value):
        """Safely convert a ConfigUI menu value to an Indigo device id."""
        try:
            return int(value) if value not in (None, "") else 0
        except Exception:
            return 0

    def updateMusicStatus(self, dev):
        """Update unified music status from all services."""
        try:
            spotifyDeviceId = self._toDeviceId(dev.pluginProps.get('spotifyDeviceId', ''))
            appleMusicDeviceId = self._toDeviceId(dev.pluginProps.get('appleMusicDeviceId', ''))
            vlcDeviceId = self._toDeviceId(dev.pluginProps.get('vlcDeviceId', ''))
            airfoilDeviceId = self._toDeviceId(dev.pluginProps.get('airfoilDeviceId', ''))

            if not spotifyDeviceId and not appleMusicDeviceId and not vlcDeviceId and not airfoilDeviceId:
                self.debugLog(u"No devices configured for Music Manager")
                return

            spotifyDev = indigo.devices.get(spotifyDeviceId) if spotifyDeviceId else None
            appleMusicDev = indigo.devices.get(appleMusicDeviceId) if appleMusicDeviceId else None
            vlcDev = indigo.devices.get(vlcDeviceId) if vlcDeviceId else None
            airfoilDev = indigo.devices.get(airfoilDeviceId) if airfoilDeviceId else None

            spotifyPlaying = bool(spotifyDev.states.get('isPlaying', False)) if spotifyDev else False
            appleMusicPlaying = bool(appleMusicDev.states.get('isPlaying', False)) if appleMusicDev else False
            vlcPlaying = bool(vlcDev.states.get('isPlaying', False)) if vlcDev else False
            # Airfoil Satellite v0.1.4+ exposes 'streaming'. Fall back to connected+metadata for older builds.
            if airfoilDev:
                airfoilPlaying = bool(airfoilDev.states.get('streaming', False))
                if not airfoilPlaying:
                    connected = bool(airfoilDev.states.get('connected', False))
                    has_meta = bool(airfoilDev.states.get('trackTitle', '') or airfoilDev.states.get('artist', '') or airfoilDev.states.get('nowPlaying', ''))
                    airfoilPlaying = connected and has_meta
            else:
                airfoilPlaying = False

            devInfo = self.deviceDict.get(dev.id)
            if not devInfo:
                return

            spotifyJustStarted = spotifyPlaying and not devInfo.get('lastSpotifyState', False)
            appleMusicJustStarted = appleMusicPlaying and not devInfo.get('lastAppleMusicState', False)
            vlcJustStarted = vlcPlaying and not devInfo.get('lastVLCState', False)
            airfoilJustStarted = airfoilPlaying and not devInfo.get('lastAirfoilState', False)

            if dev.pluginProps.get('autoExclusive', True):
                if spotifyJustStarted:
                    if appleMusicPlaying and appleMusicDev:
                        self.debugLog(u"Spotify started - pausing Apple Music")
                        self.executeDeviceAction(appleMusicDev, 'pause')
                        appleMusicPlaying = False
                    if vlcPlaying and vlcDev:
                        self.debugLog(u"Spotify started - pausing VLC")
                        self.executeDeviceAction(vlcDev, 'pause')
                        vlcPlaying = False
                    if airfoilPlaying and airfoilDev:
                        self.debugLog(u"Spotify started - toggling Airfoil Satellite play/pause")
                        self.executeDeviceAction(airfoilDev, 'pause')
                        airfoilPlaying = False

                elif appleMusicJustStarted:
                    if spotifyPlaying and spotifyDev:
                        self.debugLog(u"Apple Music started - pausing Spotify")
                        self.executeDeviceAction(spotifyDev, 'pause')
                        spotifyPlaying = False
                    if vlcPlaying and vlcDev:
                        self.debugLog(u"Apple Music started - pausing VLC")
                        self.executeDeviceAction(vlcDev, 'pause')
                        vlcPlaying = False
                    if airfoilPlaying and airfoilDev:
                        self.debugLog(u"Apple Music started - toggling Airfoil Satellite play/pause")
                        self.executeDeviceAction(airfoilDev, 'pause')
                        airfoilPlaying = False

                elif vlcJustStarted:
                    if spotifyPlaying and spotifyDev:
                        self.debugLog(u"VLC started - pausing Spotify")
                        self.executeDeviceAction(spotifyDev, 'pause')
                        spotifyPlaying = False
                    if appleMusicPlaying and appleMusicDev:
                        self.debugLog(u"VLC started - pausing Apple Music")
                        self.executeDeviceAction(appleMusicDev, 'pause')
                        appleMusicPlaying = False
                    if airfoilPlaying and airfoilDev:
                        self.debugLog(u"VLC started - toggling Airfoil Satellite play/pause")
                        self.executeDeviceAction(airfoilDev, 'pause')
                        airfoilPlaying = False

                elif airfoilJustStarted:
                    if spotifyPlaying and spotifyDev:
                        self.debugLog(u"Airfoil Satellite started - pausing Spotify")
                        self.executeDeviceAction(spotifyDev, 'pause')
                        spotifyPlaying = False
                    if appleMusicPlaying and appleMusicDev:
                        self.debugLog(u"Airfoil Satellite started - pausing Apple Music")
                        self.executeDeviceAction(appleMusicDev, 'pause')
                        appleMusicPlaying = False
                    if vlcPlaying and vlcDev:
                        self.debugLog(u"Airfoil Satellite started - pausing VLC")
                        self.executeDeviceAction(vlcDev, 'pause')
                        vlcPlaying = False

            devInfo['lastSpotifyState'] = spotifyPlaying
            devInfo['lastAppleMusicState'] = appleMusicPlaying
            devInfo['lastVLCState'] = vlcPlaying
            devInfo['lastAirfoilState'] = airfoilPlaying

            activeService = "none"
            activeDevice = None

            if spotifyPlaying:
                activeService = "spotify"
                activeDevice = spotifyDev
                devInfo['lastActiveService'] = 'spotify'
            elif appleMusicPlaying:
                activeService = "applemusic"
                activeDevice = appleMusicDev
                devInfo['lastActiveService'] = 'applemusic'
            elif vlcPlaying:
                activeService = "vlc"
                activeDevice = vlcDev
                devInfo['lastActiveService'] = 'vlc'
            elif airfoilPlaying:
                activeService = "airfoil"
                activeDevice = airfoilDev
                devInfo['lastActiveService'] = 'airfoil'
            else:
                preferredService = dev.pluginProps.get('preferredService', 'last')
                if preferredService == 'spotify' and spotifyDev:
                    activeService = "spotify"; activeDevice = spotifyDev
                elif preferredService == 'applemusic' and appleMusicDev:
                    activeService = "applemusic"; activeDevice = appleMusicDev
                elif preferredService == 'vlc' and vlcDev:
                    activeService = "vlc"; activeDevice = vlcDev
                elif preferredService == 'airfoil' and airfoilDev:
                    activeService = "airfoil"; activeDevice = airfoilDev
                elif preferredService == 'last' and devInfo.get('lastActiveService'):
                    activeService = devInfo['lastActiveService']
                    if activeService == 'spotify' and spotifyDev:
                        activeDevice = spotifyDev
                    elif activeService == 'applemusic' and appleMusicDev:
                        activeDevice = appleMusicDev
                    elif activeService == 'vlc' and vlcDev:
                        activeDevice = vlcDev
                    elif activeService == 'airfoil' and airfoilDev:
                        activeDevice = airfoilDev
                    else:
                        activeService = 'none'
                else:
                    if spotifyDev:
                        activeService = "spotify"; activeDevice = spotifyDev
                    elif appleMusicDev:
                        activeService = "applemusic"; activeDevice = appleMusicDev
                    elif vlcDev:
                        activeService = "vlc"; activeDevice = vlcDev
                    elif airfoilDev:
                        activeService = "airfoil"; activeDevice = airfoilDev

            stateList = []
            stateList.append({'key': 'activeService', 'value': activeService})
            stateList.append({'key': 'spotifyPlaying', 'value': spotifyPlaying})
            stateList.append({'key': 'appleMusicPlaying', 'value': appleMusicPlaying})
            stateList.append({'key': 'vlcPlaying', 'value': vlcPlaying})
            stateList.append({'key': 'airfoilPlaying', 'value': airfoilPlaying})

            if activeDevice:
                if activeService == 'airfoil':
                    isPlaying = airfoilPlaying
                    isPaused = bool(activeDevice.states.get('connected', False)) and not airfoilPlaying
                    isStopped = not bool(activeDevice.states.get('connected', False))
                    trackName = activeDevice.states.get('trackTitle', '')
                    artist = activeDevice.states.get('artist', '')
                    album = activeDevice.states.get('album', '')
                    playerPosition = 0
                    playerPositionFormatted = '0:00'
                    duration = activeDevice.states.get('streamingDurationSeconds', 0) or 0
                    durationFormatted = activeDevice.states.get('streamingDuration', '0:00') or '0:00'
                    progressPercent = 0
                    volume = 0
                else:
                    isPlaying = activeDevice.states.get('isPlaying', False)
                    isPaused = activeDevice.states.get('isPaused', False)
                    isStopped = activeDevice.states.get('isStopped', True)
                    if activeService == 'vlc':
                        trackName = activeDevice.states.get('mediaName', '')
                        playerPosition = activeDevice.states.get('currentTime', 0)
                        playerPositionFormatted = activeDevice.states.get('currentTimeFormatted', '0:00')
                        volume = activeDevice.states.get('audioVolume', 50)
                    else:
                        trackName = activeDevice.states.get('trackName', '')
                        playerPosition = activeDevice.states.get('playerPosition', 0)
                        playerPositionFormatted = activeDevice.states.get('playerPositionFormatted', '0:00')
                        volume = activeDevice.states.get('soundVolume', 50)
                    artist = activeDevice.states.get('artist', '')
                    album = activeDevice.states.get('album', '')
                    duration = activeDevice.states.get('duration', 0)
                    durationFormatted = activeDevice.states.get('durationFormatted', '0:00')
                    progressPercent = activeDevice.states.get('progressPercent', 0)

                stateList.append({'key': 'isPlaying', 'value': bool(isPlaying)})
                stateList.append({'key': 'isPaused', 'value': bool(isPaused)})
                stateList.append({'key': 'isStopped', 'value': bool(isStopped)})
                stateList.append({'key': 'trackName', 'value': trackName})
                stateList.append({'key': 'artist', 'value': artist})
                stateList.append({'key': 'album', 'value': album})
                stateList.append({'key': 'playerPosition', 'value': playerPosition})
                stateList.append({'key': 'playerPositionFormatted', 'value': playerPositionFormatted})
                stateList.append({'key': 'duration', 'value': duration})
                stateList.append({'key': 'durationFormatted', 'value': durationFormatted})
                stateList.append({'key': 'progressPercent', 'value': progressPercent})
                stateList.append({'key': 'soundVolume', 'value': volume})

                if activeService == "spotify":
                    serviceIcon = "🎵"
                elif activeService == "applemusic":
                    serviceIcon = "🍎"
                elif activeService == "vlc":
                    serviceIcon = "🎬"
                elif activeService == "airfoil":
                    serviceIcon = "🛰"
                else:
                    serviceIcon = "🎶"

                if isPlaying:
                    statusIcon = u"▶"
                elif isPaused:
                    statusIcon = u"⏸"
                else:
                    statusIcon = u"⏹"

                if trackName and artist:
                    status = u"{} {} {} - {}".format(serviceIcon, statusIcon, artist, trackName)
                elif trackName:
                    status = u"{} {} {}".format(serviceIcon, statusIcon, trackName)
                else:
                    status = u"{} {} Not Playing".format(serviceIcon, statusIcon)
                stateList.append({'key': 'status', 'value': status})
            else:
                stateList.append({'key': 'isPlaying', 'value': False})
                stateList.append({'key': 'isPaused', 'value': False})
                stateList.append({'key': 'isStopped', 'value': True})
                stateList.append({'key': 'trackName', 'value': ''})
                stateList.append({'key': 'artist', 'value': ''})
                stateList.append({'key': 'album', 'value': ''})
                stateList.append({'key': 'playerPosition', 'value': 0})
                stateList.append({'key': 'playerPositionFormatted', 'value': '0:00'})
                stateList.append({'key': 'duration', 'value': 0})
                stateList.append({'key': 'durationFormatted', 'value': '0:00'})
                stateList.append({'key': 'progressPercent', 'value': 0})
                stateList.append({'key': 'soundVolume', 'value': 0})
                stateList.append({'key': 'status', 'value': u'🎶 ⏹ Not Playing'})

            # Indigo can keep an existing device's state table until the device definition is refreshed.
            # Filter unknown keys so upgraded installs do not spam the Event Log if a newly-added state
            # such as airfoilPlaying is not registered yet on the existing Music Manager device.
            validStateKeys = set(dev.states.keys())
            filteredStateList = [state for state in stateList if state.get('key') in validStateKeys]
            skippedStateKeys = [state.get('key') for state in stateList if state.get('key') not in validStateKeys]
            if skippedStateKeys and not devInfo.get('loggedMissingStateKeys', False):
                self.debugLog(u"Skipping unregistered Music Manager state keys: {}. Edit/save the Music Manager device or recreate it if you want those new states visible.".format(', '.join(skippedStateKeys)))
                devInfo['loggedMissingStateKeys'] = True

            dev.updateStatesOnServer(filteredStateList)

            if dev.pluginProps.get('updateVariables', False):
                self.updateVariables(dev, filteredStateList)

        except Exception as e:
            self.errorLog(u"Exception in updateMusicStatus: {}".format(str(e)))

    def updateVariables(self, dev, stateList):
        """Update Indigo variables with current states"""
        try:
            prefix = dev.pluginProps.get('variablePrefix', 'Music')
            
            for state in stateList:
                varName = prefix + state['key'][0].upper() + state['key'][1:]
                
                # Create variable if it doesn't exist
                if varName not in indigo.variables:
                    indigo.variable.create(varName, value=str(state['value']), folder=0)
                else:
                    indigo.variable.updateValue(varName, value=str(state['value']))
                    
        except Exception as e:
            self.errorLog(u"Exception in updateVariables: {}".format(str(e)))
    
    def getActiveDevice(self, dev):
        """Get the currently active music device."""
        activeService = dev.states.get('activeService', 'none')
        propMap = {
            'spotify': 'spotifyDeviceId',
            'applemusic': 'appleMusicDeviceId',
            'vlc': 'vlcDeviceId',
            'airfoil': 'airfoilDeviceId',
        }

        deviceId = self._toDeviceId(dev.pluginProps.get(propMap.get(activeService, ''), '')) if activeService in propMap else 0

        if not deviceId:
            for prop in ('spotifyDeviceId', 'appleMusicDeviceId', 'vlcDeviceId', 'airfoilDeviceId'):
                deviceId = self._toDeviceId(dev.pluginProps.get(prop, ''))
                if deviceId:
                    break

        return indigo.devices.get(deviceId) if deviceId else None

    def executeDeviceAction(self, targetDevice, actionName, props=None):
        """Execute an action on a target plugin device."""
        try:
            if not targetDevice:
                return False

            plugin = indigo.server.getPlugin(targetDevice.pluginId)
            if not plugin or not plugin.isEnabled():
                self.errorLog(u"Target plugin not available or disabled for {}".format(targetDevice.name))
                return False

            # Indigo plugin-defined device actions are executed through the owning
            # plugin's executeAction() API, not indigo.device.execute().
            action_aliases = {
                'play': ['play'],
                'pause': ['pause', 'playPause', 'playpause'],
                'playpause': ['playPause', 'playpause'],
                'stop': ['stop'],
                'nextTrack': ['nextTrack'],
                'previousTrack': ['prevTrack', 'previousTrack', 'previousTrack'],
                'setVolume': ['setVolume'],
                'volumeUp': ['increaseVolume', 'volumeUp'],
                'volumeDown': ['decreaseVolume', 'volumeDown'],
                'mute': ['mute'],
                'unmute': ['unmute'],
                'setShuffle': ['setShuffle'],
                'setRepeat': ['setRepeat'],
                'skipForward': ['skipForward'],
                'skipBackward': ['skipBackward'],
            }

            normalized_props = None
            if props:
                normalized_props = indigo.Dict(props)
                if actionName == 'volumeUp':
                    amount = props.get('amount', props.get('volume', '10'))
                    normalized_props = indigo.Dict({'volume': amount})
                elif actionName == 'volumeDown':
                    amount = props.get('amount', props.get('volume', '10'))
                    normalized_props = indigo.Dict({'volume': amount})
                elif actionName == 'setShuffle' and 'shuffleState' in props:
                    shuffle_state = props.get('shuffleState', 'toggle')
                    normalized_props = indigo.Dict({'shuffle': shuffle_state})
                elif actionName == 'setRepeat' and 'repeatState' in props:
                    repeat_state = props.get('repeatState', 'toggle')
                    normalized_props = indigo.Dict({'repeat': repeat_state})

            last_error = None
            for action_id in action_aliases.get(actionName, [actionName]):
                try:
                    kwargs = {
                        'deviceId': targetDevice.id,
                        'waitUntilDone': True,
                    }
                    if normalized_props is not None:
                        kwargs['props'] = normalized_props
                    plugin.executeAction(action_id, **kwargs)
                    self.debugLog(u"Executed action '{}' on {} via plugin {}".format(action_id, targetDevice.name, targetDevice.pluginId))
                    return True
                except Exception as inner_error:
                    last_error = inner_error
                    self.debugLog(u"Action '{}' failed on {}: {}".format(action_id, targetDevice.name, str(inner_error)))

            if last_error is not None:
                raise last_error
            return False
        except Exception as e:
            self.errorLog(u"Exception executing action on {}: {}".format(targetDevice.name, str(e)))
            return False
            
    ########################################
    # Action Handlers
    ########################################
    
    def actionPlay(self, pluginAction, dev):
        """Play action - plays on active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'play')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionPause(self, pluginAction, dev):
        """Pause action - pauses active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'pause')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionPlayPause(self, pluginAction, dev):
        """Play/Pause toggle - toggles active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'playpause')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionStop(self, pluginAction, dev):
        """Stop action - stops all services"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        airfoilDeviceIdStr = dev.pluginProps.get('airfoilDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        airfoilDeviceId = int(airfoilDeviceIdStr) if airfoilDeviceIdStr else 0
        
        if spotifyDeviceId:
            spotifyDev = indigo.devices.get(spotifyDeviceId)
            if spotifyDev:
                self.executeDeviceAction(spotifyDev, 'stop')
        
        if appleMusicDeviceId:
            appleMusicDev = indigo.devices.get(appleMusicDeviceId)
            if appleMusicDev:
                self.executeDeviceAction(appleMusicDev, 'stop')
        
        if vlcDeviceId:
            vlcDev = indigo.devices.get(vlcDeviceId)
            if vlcDev:
                self.executeDeviceAction(vlcDev, 'stop')
        
        if airfoilDeviceId:
            airfoilDev = indigo.devices.get(airfoilDeviceId)
            if airfoilDev and airfoilDev.states.get('streaming', False):
                self.executeDeviceAction(airfoilDev, 'pause')
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionNextTrack(self, pluginAction, dev):
        """Next track action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'nextTrack')
            time.sleep(0.5)
            self.updateMusicStatus(dev)
        
    def actionPreviousTrack(self, pluginAction, dev):
        """Previous track action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'previousTrack')
            time.sleep(0.5)
            self.updateMusicStatus(dev)
        
    def actionSetVolume(self, pluginAction, dev):
        """Set volume action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setVolume', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionVolumeUp(self, pluginAction, dev):
        """Volume up action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'volumeUp', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionVolumeDown(self, pluginAction, dev):
        """Volume down action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'volumeDown', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionMute(self, pluginAction, dev):
        """Mute action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'mute')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionUnmute(self, pluginAction, dev):
        """Unmute action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'unmute')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSwitchToSpotify(self, pluginAction, dev):
        """Switch to Spotify"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        airfoilDeviceIdStr = dev.pluginProps.get('airfoilDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if appleMusicDeviceId:
                appleMusicDev = indigo.devices.get(appleMusicDeviceId)
                if appleMusicDev:
                    self.executeDeviceAction(appleMusicDev, 'pause')
            if vlcDeviceId:
                vlcDev = indigo.devices.get(vlcDeviceId)
                if vlcDev:
                    self.executeDeviceAction(vlcDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'spotify'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionSwitchToAppleMusic(self, pluginAction, dev):
        """Switch to Apple Music"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        airfoilDeviceIdStr = dev.pluginProps.get('airfoilDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if spotifyDeviceId:
                spotifyDev = indigo.devices.get(spotifyDeviceId)
                if spotifyDev:
                    self.executeDeviceAction(spotifyDev, 'pause')
            if vlcDeviceId:
                vlcDev = indigo.devices.get(vlcDeviceId)
                if vlcDev:
                    self.executeDeviceAction(vlcDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'applemusic'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
    
    def actionSwitchToVLC(self, pluginAction, dev):
        """Switch to VLC"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        airfoilDeviceIdStr = dev.pluginProps.get('airfoilDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if spotifyDeviceId:
                spotifyDev = indigo.devices.get(spotifyDeviceId)
                if spotifyDev:
                    self.executeDeviceAction(spotifyDev, 'pause')
            if appleMusicDeviceId:
                appleMusicDev = indigo.devices.get(appleMusicDeviceId)
                if appleMusicDev:
                    self.executeDeviceAction(appleMusicDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'vlc'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionSwitchToAirfoil(self, pluginAction, dev):
        """Switch to Airfoil Satellite."""
        spotifyDeviceId = self._toDeviceId(dev.pluginProps.get('spotifyDeviceId', ''))
        appleMusicDeviceId = self._toDeviceId(dev.pluginProps.get('appleMusicDeviceId', ''))
        vlcDeviceId = self._toDeviceId(dev.pluginProps.get('vlcDeviceId', ''))

        if pluginAction.props.get('pauseOther', True):
            if spotifyDeviceId:
                spotifyDev = indigo.devices.get(spotifyDeviceId)
                if spotifyDev:
                    self.executeDeviceAction(spotifyDev, 'pause')
            if appleMusicDeviceId:
                appleMusicDev = indigo.devices.get(appleMusicDeviceId)
                if appleMusicDev:
                    self.executeDeviceAction(appleMusicDev, 'pause')
            if vlcDeviceId:
                vlcDev = indigo.devices.get(vlcDeviceId)
                if vlcDev:
                    self.executeDeviceAction(vlcDev, 'pause')

        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'airfoil'

        time.sleep(0.2)
        self.updateMusicStatus(dev)

    def actionSetShuffle(self, pluginAction, dev):
        """Set shuffle action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setShuffle', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSetRepeat(self, pluginAction, dev):
        """Set repeat action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setRepeat', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSkipForward(self, pluginAction, dev):
        """Skip forward action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'skipForward', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSkipBackward(self, pluginAction, dev):
        """Skip backward action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'skipBackward', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionUpdateNow(self, pluginAction, dev):
        """Force immediate update"""
        self.updateMusicStatus(dev)
