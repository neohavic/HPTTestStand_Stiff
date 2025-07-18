"""

@author: Attocube Systems

------------------------------------------------------------------------------------------------
(c) COPYRIGHT 2019 by attocube systems AG, Germany. All rights reserved.

This module shall be a starting point for everyone working with LUA and wanting
to integrate an IDS3010 to their setup. For any suggestions on code optimization
or already modified code please contact Daniel Schiessl:
daniel.schiessl@attocube.com

------------------------------------------------------------------------------------------------

"""

import ACS
import System

import time

class Device(ACS.Device, System.Device):

    ############################ Convenience functions IDS specific ############
    ############################################################################

    def waitUntilInMode(self, desired_mode='system idle', timeout=30):
        """
            Blocks for a maximum of timeout seconds until in the desired_mode
            Parameters
            ----------
            desired_mode : str
                Desired Mode
            timeout : int
                Timeout in seconds
            Returns
            -------
            errorNumber : int
               No error = 0
            """

        count = 0
        while not self.getCurrentMode() == desired_mode and count < timeout:
            count += 1
            time.sleep(1)
        if count >= timeout:
            return False
        else:
            return True



    ############################ System functions IDS specific ################################
    ###############################################################################

    def uploadFirmwareImageBase64(self, content):
        """
            Uploads a Firmwage Image to the device.
        Parameters
        ----------
        contents : str
            Base64 encoded image file
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.system.uploadFirmwareImageBase64", [content])
        return response['result'][0]

    def firmwareUpdate(self):
        """
            Installs a previously uploaded Firmware Image.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.system.firmwareUpdateBase64")
        return response['result'][0]

    def getFwUpdateProgress(self):
        """
            Reads out the current progress in percentage of a running firmware update procedure.
        Parameters
        ----------
        Returns
        -------
        progress : int
           Firmware update progress in %
        """
        response = self.request("com.attocube.system.getFwUpdateProgress")
        return response['result'][0]


    def licenseUpdate(self):
        """
            Installs an uploaded License.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.system.licenseUpdateBase64")
        return response['result'][0]

    def uploadLicenseBase64(self, contents):
        """
            Uploads a license file to the IDS.

        Parameters
        ----------
        contents : str
            base64 encoded license file

        Returns
        -------
        errorNumber : int
           No error = 0
        """
        response = self.request("com.attocube.system.uploadLicenseBase64", [contents])
        return response['result'][0]

    def getNumberOfActivatedFeatures(self):
        """
            Reads out the number of activated features activated on the IDS.
        Parameters
        ----------
        Returns
        -------
        numberofactivatedfeatures : int
           Gives the number of activated features
        """
        response = self.request("com.attocube.ids.system.getNbrFeaturesActivated")
        return response['result'][0]

    def getFeatureName(self, feature):
        """
            Reads out the name of a feature activated on the IDS.
        Parameters
        ----------
        feature : int
            Number of feature
        Returns
        -------
        featurename : str
           The name of the corresponding feature
        """
        response = self.request("com.attocube.ids.system.getFeaturesName", [feature])
        self.handleError(response)
        return response['result'][0], response['result'][1]


    def getFpgaVersion(self):
        """
            Function specific parameters
        Parameters
        ----------
        Returns
        -------
        version : str
           Version in the form X.Y.Z
        """
        response = self.request("com.attocube.ids.system.getFpgaVersion")
        return response['result'][0]

    def getDeviceType(self):
        """
            Reads out the IDS device type.
        Parameters
        ----------
        Returns
        -------
        type : str
           Type of IDS
        """
        response = self.request("com.attocube.ids.system.getDeviceType")
        return response['result'][0]

    def getCurrentMode(self):
        """
            Function specific parameters
        Parameters
        ----------
        Returns
        -------
        mode : str
           Values: 'system idle', 'measurement starting','measurement running',
           'optics alignment starting', 'optics alignment running',
           'pilot laser enabled', 'test channels enabled'
        """
        response = self.request("com.attocube.ids.system.getCurrentMode")
        return response['result'][0]

    def enableTestChannel(self):
        """
            Enables the Test Channel.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.enableTestChannel", [0])
        #self.handleError(response)
        return response#['result'][0]

    def getTestChannelEnabled(self):
        """
            Checks if the Test Channel is enabled.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        enabled : bool
            true = enabled, false = disabled
        """
        response = self.request("com.attocube.ids.realtime.isTestChannelEnabled")
        return response['result'][0]

    def disableTestChannel(self):
        """
            Disables the Test Channel.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.disableTestChannel")
        self.handleError(response)
        return response['result'][0]

    ############################# Quick Initialization ############################
    ###############################################################################

    def setInitMode(self, mode):
        """
            sets the Initialization mode.
        Parameters
        ----------
        mode : int
            0 = High Accuracy Initialization
            1 = Quick Initialization
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.setInitMode", [mode])
        self.handleError(response)
        applyResponse = self.request("com.attocube.ids.system.applyInitMode")
        self.handleError(applyResponse)

        return response['result'][0]

    def getInitMode(self):
        """
            Returns the Initialization mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        mode : int
            0 = High Accuracy Initialization
            1 = Quick Initialization
        """
        response = self.request("com.attocube.ids.system.getInitMode")
        self.handleError(response)
        return response['result'][1]

    ############################# Optical Alignment ###############################
    ###############################################################################

    def getPassMode(self):
        """
            Reads out the current pass mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        mode : int
            0 = single pass
            1 = dual pass
        """
        response = self.request("com.attocube.ids.axis.getPassMode")
        return response['result'][0]

    def setPassMode(self, mode):
        """
            sets the desired pass mode.
        Parameters
        ----------
        mode : int
            0 = single pass;
            1 = dual pass;
            3 = xs sensor single pass;
            3= customized sensor head
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.axis.setPassMode", [mode])
        self.handleError(response)
        return response['result'][0]

    def setMasterAxis(self, axisNumber):
        """
            sets the master axis
        Parameters
        ----------
        axisNumber : int
            Axis which is operating as masteraxis [0..2]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.axis.setMasterAxis", [axisNumber])
        self.handleError(response)
        return response['result'][0]

    def getMasterAxis(self):
        """
            Returns the master axis
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        masteraxis : int
            Axis which is operating as masteraxis [0..2]
        """
        response = self.request("com.attocube.ids.axis.getMasterAxis")
        return response['result'][0]

    def getPilotLaserEnabled(self):
        """
            Reads out whether the pilot laser is enabled or not.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        enabled : bool
            true = enabled; false = disabled
        """
        response = self.request("com.attocube.ids.pilotlaser.isEnabled")
        return response['result'][0]

    def setPilotLaserEnable(self):
        """
            Enables the pilot laser.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.pilotlaser.enable")
        self.handleError(response)
        return response['result'][0]

    def setPilotLaserDisable(self):
        """
            Disables the pilot laser.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.pilotlaser.disable")
        self.handleError(response)
        return response['result'][0]

    def startOpticsAlignment(self):
        """
            Starts the optical alignment mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.startOpticsAlignment")
        self.handleError(response)
        return response['result'][0]

    def stopOpticsAlignment(self):
        """
            Stops the optical alignment mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.stopOpticsAlignment")
        self.handleError(response)
        return response['result'][0]

    def getContrastInPermille(self, axisNumber):
        """
            Reads out the optical contrast in permill during running alignment.
        Parameters
        ----------
        axisNumber : int
            Axis to get the value from [0..2]
        Returns
        -------
        errorNumber : int
            No error = 0
        contrast : int
            in permille
        baseline : int
            Offset of the contrast measurement
        mixContrast : int
            lower contrast measurment when measuring a mix contrast (indicated by error code)
        """
        response = self.request("com.attocube.ids.adjustment.getContrastInPermille", [axisNumber])
        self.handleError(response)
        return response['result'][0], response['result'][1], \
               response['result'][2], response['result'][3]

    def getAxisSignalQuality(self, axisNumber):
        """
            Reads out the optical contrast in permill during running measurement.
        Parameters
        ----------
        axisNumber : int
            Axis to get the value from [0..2]

        Returns
        -------
        errorNumber : int
            No error = 0
        constrast : int
            contrast of the base band signal in permille
        baseline : int
            offset of the contrast measurement in permille
        """
        response = self.request("com.attocube.ids.displacement.getSignalQuality", [axisNumber])
        self.handleError(response)
        return response['result'][1], response['result'][2]

    ############################# Real-Time Interfaces ############################
    ###############################################################################

    def getRtOutputMode(self):
        """ Reads out the current realtime output mode.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        rtOutMode : int
            0=HSSL (TTL), 1=HSSL (LVDS),
            2=AquadB (TTL), 3=AquadB (LVDS),
            4=SinCos (TTL Error Signal), 5=SinCos (LVDS Error Signal),
            6 Linear (TTL), 7 Linear (LVDS), 8 BiSS-C
        """
        response = self.request("com.attocube.ids.realtime.getRtOutMode", [0])
        if (response['result'][0] != 0 and response['result'][0] != 'null'):
            Mode = 'Error'
            self.printError(response['result'][0])
        elif response['result'][1] == 0:
            Mode = 'HSSL (LVTTL)'
        elif response['result'][1] == 1:
            Mode = 'HSSL (LVDS)'
        elif response['result'][1] == 2:
            Mode = 'AquadB (LVTTL)'
        elif response['result'][1] == 3:
            Mode = 'AquadB (LVDS)'
        elif response['result'][1] == 4:
            Mode = 'SinCos(LVTTL Error Signal)'
        elif response['result'][1] == 5:
            Mode = 'SinCos (LVDS Error Signal)'
        elif response['result'][1] == 6:
            Mode = 'Linear (TTL)'
        elif response['result'][1] == 7:
            Mode = 'Linear (LVDS)'
        return Mode

    def setRtOutputMode(self, rtOutMode):
        """
            sets the real time output mode.
        Parameters
        ----------
        Mode : int
            0=HSSL (TTL), 1=HSSL (LVDS),
            2=AquadB (TTL), 3=AquadB (LVDS),
            4=SinCos (TTL Error Signal), 5=SinCos (LVDS Error Signal),
            6 Linear (TTL),7 Linear (LVDS), 8 BiSS-C
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setRtOutMode", [rtOutMode])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getResolutionHsslLow(self):
        """
            Reads out the HSSL resolution low bit.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        resolution : int
            Resolution in the range of [0..46]
        """
        response = self.request("com.attocube.ids.realtime.getResolutionHsslLow", [0])
        self.handleError(response)
        return response['result'][1]

    def setResolutionHsslLow(self, resolution):
        """
            sets the HSSL resolution low bit.
        Parameters
        ----------
        resolution : int
            Resolution in the range of [0..46]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setResolutionHsslLow", [resolution])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getResolutionHssHigh(self):
        """
            Reads out the HSSL resolution high bit.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        resolution : int
            Resolution in the range of [0..46]
        """
        response = self.request("com.attocube.ids.realtime.getResolutionHsslHigh", [0])
        self.handleError(response)
        self.rtApply()
        return response['result'][1]

    def setResolutionHssHigh(self, resolution):
        """
            sets the HSSL resolution high bit.
        Parameters
        ----------
        resolution : int
            Resolution in the range of [0..46]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setResolutionHsslHigh", [resolution])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getPeriodHssClk(self):
        """
            Reads out the HSSL period clock.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        period : int
            Period in the range of [40ns..10200ns]
        """
        response = self.request("com.attocube.ids.realtime.getPeriodHsslClk", [0])
        self.handleError(response)
        return response['result'][1]

    def setPeriodHsslClock(self, clock):
        """
            set the HSSL period clock.
        Parameters
        ----------
        clock : int
            Period in the range of [40ns..10200ns]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setPeriodHsslClk", [clock])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getPeriodHsslGap(self):
        """
            Reads out the HSSL period gap.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        gap : int
            Gap in the range of [40ns..10200ns]
        """
        response = self.request("com.attocube.ids.realtime.getPeriodHsslGap", [0])
        self.handleError(response)
        return response['result'][1]

    def setPeriodHsslGap(self, gap):
        """
            set the HSSL period clock.set the HSSL period gap.
        Parameters
        ----------
        gap : int
            Gap in the range of [40ns..10200ns]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setPeriodHsslGap", [gap])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getRtLinearRangeNumber(self):
        """
            Reads out the range number of Linear/Analog output mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        rangenumber : int
            N, Linear Analog range is +-2N+11 pm, with N from [0, 34]
        """
        response = self.request("com.attocube.ids.realtime.getLinearRange", [0])
        self.handleError(response)
        return response['result'][1]

    def setRtLinearRangeNumber(self, rangenumber):
        """
            sets the range number of Linear/Analog output mode.
        Parameters
        ----------
        range : int
            N, Linear Analog Range is +-2N+11 pm,with N from [0,34]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setLinearRange", [rangenumber])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getRtLinearHighPassFilterNumber(self):
        """
            Reads out the high pass filter number of Linear/Analog output mode.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        filternumber : int
            N, Linear Analog High Pass Cut-Off frequency is 1600/2N kHz, with N
            from [1,24]
        """
        response = self.request("com.attocube.ids.realtime.getHighPassCutOffFreq", [0])
        self.handleError(response)
        return response['result'][1]

    def setRtLinearHighPassFilterNumber(self, filternumber):
        """
            sets the high pass filter number of Linear/Analog output mode.
        Parameters
        ----------
        number : int
            N, Linear Analog High Pass Cut-Off frequency is 1600/2N kHz, with N
            from [1,24]
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setHighPassCutOffFreq", [filternumber])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getDistanceMode(self):
        """
            Reads out the distance mode. Depending on the realtime output mode,
            the mode can be Displacement (returns 1), Absolute Distance (returns 2)
            or Vibrometry (returns 3).
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        linearmode : int
            1 = Displacement (Available in HSSL mode and Linear Mode)
            2 = Absolute Distance (Available in HSSL mode only)
            3 = Vibrometry (Available in Linear mode)
        """
        response = self.request("com.attocube.ids.realtime.getRtDistanceMode", [0])
        self.handleError(response)
        return response['result'][1]

    def setDistanceMode(self, distancemode):
        """
            sets the distance mode. Depending on the configuration of the
            IDS the mode can be Displacement (returns 1), Absolute Distance
            (returns 2) or Vibrometry (returns 3).
        Parameters
        ----------
        mode : int
            1 = Displacement (HSSL mode and Linear Mode)
            2 = Absolute Distance (HSSL mode only)
            3 = Vibrometry (Linear mode)
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setRtDistanceMode", [distancemode])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getPeriodSinCosClk(self):
        """
            Reads out the Sine-Cosine period clock.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        period : int
            40ns - 10200ns
        """
        response = self.request("com.attocube.ids.realtime.getPeriodSinCosClk", [0])
        self.handleError(response)
        return response['result'][1]

    def setPeriodSinCosClk(self, period):
        """
            sets the Sine-Cosine period clock.
        Parameters
        ----------
        period : int
            40ns- 10200ns
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setPeriodSinCosClk", [period])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getResolutionSinCos(self):
        """
            Reads out the Sine-Cosine resolution.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        resolution : int
            1pm to 65535pm
        """
        response = self.request("com.attocube.ids.realtime.getResolutionSinCos", [0])
        self.handleError(response)
        return response['result'][1]

    def setResolutionSinCos(self, resolution):
        """
            sets the Sine-Cosine period clock.
        Parameters
        ----------
        resolution : int
            1pm to 65535pm
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setResolutionSinCos", [resolution])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getResolutionBissC(self):
        """
            Reads out the BissC resolution.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        resolution : int
            1pm to 65535pm
        """
        response = self.request("com.attocube.ids.realtime.getResolutionBissC", [0])
        self.handleError(response)
        return response['result'][1]

    def setResolutionBissC(self, resolution):
        """
            sets the BissC resolution.
        Parameters
        ----------
        resolution : int
            1pm to 65535pm
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setResolutionBissC", [resolution])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def setAaf(self, Set, attenuation, window):
        """
            sets the Anti-Aliasing Unit with assigned Filter Window.
        Parameters
        ----------
        set : int
            0 - disables the Anti-Aliasing Filter
            1 - enables the Anti-Aliasing Filter
        attenuation :
            [3-30] dB m f_nyquist
        window :
            0 = Rectangular ,
            1 = Cosine,
            2 = Cosine^2,
            3 = Hamming,
            4 = Raised Cosine
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.realtime.setAaf", [Set, attenuation, window])
        self.handleError(response)
        self.rtApply()
        return response['result'][0]

    def getAafEnabled(self):
        """
            Checks if the Anti-Aliasing Unit is enabled.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        enabled : bool
            true = AAF is enabled , false = AAF is disabled
        """
        response = self.request("com.attocube.ids.realtime.AafIsEnabled", [0])
        self.handleError(response)
        return response['result'][1]

    def getAafAttenuation(self):
        """
            Returns the current Attenuation at f_nyquist of the Anti-Aliasing Unit.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        attenuation : int
            [0-33] dB at f_nyquist
        """
        response = self.request("com.attocube.ids.realtime.getAafAttenuation", [0])
        self.handleError(response)
        return response['result'][1]

    def getAafWindow(self):
        """
            Returns the current Filter Window of the Anti-Aliasing Unit.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        FilterWindow : int
            0 = Rectangular ,
            1 = Cosine,
            2 = Cosine^2, 3 = Hamming,
            4 Raised Cosine
        """
        response = self.request("com.attocube.ids.realtime.getAafWindow", [0])
        self.handleError(response)
        return response['result'][1]

    ############################ Position Measurement #############################
    ###############################################################################

    def startMeasurement(self):
        """
            Starts the position measurement.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.startMeasurement")
        self.handleError(response)
        return response['result'][0]

    def stopMeasurement(self):
        """
            Stops the position measurement.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.stopMeasurement")
        self.handleError(response)
        return response['result'][0]

    def getAverageN(self):
        """
           Reads-out the averaging (lowpass) parameter N. The averaging time is
           calculated by (2^N)*40ns, where N is the averaging value. Table 1 indicates
           when the stopband starts (column: 'bandwidth') and where we have to assume
           the 3dB cut-off frequency in accordance to the set averaging parameter N.
        Parameters
        ----------
        Returns
        -------
        averageN : int
            A value from 0 to 24
        """
        response = self.request("com.attocube.ids.displacement.getAverageN")
        return response['result'][0]

    def setAverageN(self, averageN):
        """
            sets the averaging (lowpass) parameter N. The averaging time is
            calculated by (2^N)*40ns, where N is the averaging value.
        Parameters
        ----------
        averageN : int
            A value from 0 to 24
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.displacement.setAverageN", [averageN])
        self.handleError(response)
        return response['result'][0]

    def getAxisDisplacement(self, axisNumber):
        """
            Reads out the displacement value of a specific measurement axis.
        Parameters
        ----------
        axisNumber : int
            Axis to get the relative displacement from {0-2}
        Returns
        -------
        errorNumber : int
            No error = 0
        displacement : int
            Displacement of the axis in pm
        """
        response = self.request("com.attocube.ids.displacement.getAxisDisplacement", [axisNumber])
        self.handleError(response)
        return response['result'][1]

    def getAxesDisplacement(self):
        """
            Reads out the displacement values of all measurement axes.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        Displacement0 : int
            displacement of the axis 0 in pm
        Displacement1 : int
            displacement of the axis 1 in pm
        Displacement2 : int
            displacement of the axis 2 in pm
        """
        response = self.request("com.attocube.ids.displacement.getAxesDisplacement")
        self.handleError(response)
        return response['result'][1], response['result'][2], response['result'][3]

    def linProc(self, axisNumber, fringesnbr, samplesperfringe, setlinProg):
        """
            Starts linearization procedure.
        Parameters
        ----------
        axisNumber : int
            Axis to get the relative displacement from {0-2}
        fringesnbr : int
            Number of fringes to be acquired
        samplesperfringe : int
            Number of samples per fringe
        setlinProg : int
            0 = evaluate current nonlinear amplitude
            1 = perform linearization and upload look up table
            2 = Clear look up table
        Returns
        -------
        errorNumber : int
            No error = 0
        lintable : str
            String, which contains all 512 phase related correction values
        nonlinearamp : str
            String which contains the residual positive and negative maximal
            nonlinear amplitude
        """
        response = self.request("com.attocube.ids.displacement.linProc",
                                [axisNumber, fringesnbr, samplesperfringe, setlinProg])
        self.handleError(response)
        return response['result'][0], response['result'][1], response['result'][2]

    def getAbsolutePosition(self, axisNumber):
        """
            Get the absolute position of an axis taken upon measurement start.
            The absolute position is not updated during system operation.
            A dynamic absolute position can be obtained by adding the
            displacement value to the absolute position.
        Parameters
        ----------
        axisNumber : int
            number of the axis to get the position from(0-2)
        Returns
        -------
        errorNumber : int
            No error = 0
        position : int
            position of the axis in pm
        """
        response = self.request("com.attocube.ids.displacement.getAbsolutePosition", [axisNumber])
        self.handleError(response, True)
        return response['result'][0], response['result'][1]

    def getAbsolutePositions(self):
        """
            Get the absolute position of an axis taken upon measurement start.
            The absolute position is not updated during system operation.
            A dynamic absolute position can be obtained by adding the displacement value to the absolute position.
        Parameters
        ----------
        Returns
        -------
        position0 : int
            position of the axis0 in pm
        position1 : int
            position of the axis1 in pm
        position2 : int
            position of the axis2 in pm
        """
        response = self.request("com.attocube.ids.displacement.getAbsolutePositions")
        self.handleError(response)
        return response['result'][1], response['result'][2], response['result'][3]

    def resetAxis(self, axisnumber):
        """
            Resets the position value to zero of a specific measurement axis.
        Parameters
        ----------
        axisNumber : int
            number of the axis to reset (0-2)
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.resetAxis", [axisnumber])
        self.handleError(response)
        return response['result'][0]

    def resetAxes(self):
        """
            Resets the position value to zero of a specific measurement axis.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.resetAxes")
        self.handleError(response)
        return response['result'][0]

    ################################### ECU #######################################
    ###############################################################################

    def ECUisEnabled(self):
        """
            Reads out whether the ECU interface is enabled or not.
        Parameters
        ----------
        Returns
        -------
        enabled : bool
            True if enabled, false if not
        """
        response = self.request("com.attocube.ecu.isEnabled")
        return response['result'][0]

    def ECUisConnected(self):
        """
            Reads out whether the ECU interface is physically connected or not.
            Checking if the ECU is connected can only
            be done on an enabled ECU interface.
        Parameters
        ----------
        Returns
        -------
        connected : bool
            true if connected, false if not
        """
        response = self.request("com.attocube.ecu.isConnected")
        return response['result'][0]

    def ECUenable(self):
        """
            Enables the ECU interface.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ecu.enable")
        return response['result'][0]

    def ECUdisable(self):
        """
            Disables the ECU interface.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ecu.disable")
        return response['result'][0]

    def ECUgetTemperatureInDegrees(self):
        """
            Reads out the ECU measured air temperature in degrees Celsius.
        Parameters
        ----------
        Returns
        -------
        temp : int
            temperature in degrees C
        """
        response = self.request("com.attocube.ecu.getTemperatureInDegrees")
        return response['result'][0]

    def ECUgetPressureInHPa(self):
        """
            Reads out the ECU measured air pressure in HPa.
        Parameters
        ----------
        Returns
        -------
        pressure : int
            pressure in HPa
        """
        response = self.request("com.attocube.ecu.getPressureInHPa")
        return response['result'][0]

    def ECUgetHumidityInPercent(self):
        """
            Reads out the ECU measured air humidity in percent.
        Parameters
        ----------
        Returns
        -------
        humidity : int
            humidity in %
        """
        response = self.request("com.attocube.ecu.getHumidityInPercent")
        return response['result'][0]

    def ECUgetRefractiveIndex(self):
        """
            Reads out the ECU estimated refractive index.
        Parameters
        ----------
        Returns
        -------
        rIndex : int
            refractive index
        """
        response = self.request("com.attocube.ecu.getRefractiveIndex")
        return response['result'][0]

    ############################# Error Handling ##################################
    ###############################################################################

    def resetError(self, renormalisation):
        """
            Resets a measurement error that can have occurred with the aim to
            continue the interrupted measurement. It is configurable if an additional
            renormalization process (please refer to the IDS User Manual) should be performed or not.
        Parameters
        ----------
        renormalisation : int
            Indicates if an additional renormalization has to be done in case of beam interruption or signal loss
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.resetError", [renormalisation])
        self.handleError(response)
        return response['result'][0]

    def getSystemError(self):
        """
             Reads out the system error. The function returns an integer number which represents
             the error. The number can be converted into a string using the errorNumberToString
             function, which is described below.
        Parameters
        ----------
        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.ids.system.getSystemError")
        self.handleError(response)
        return response['result'][0]

    ############################ Apply functions ##################################
    ###############################################################################

    def rtApply(self): # used in setRtOutputMode:
        response = self.request("com.attocube.ids.realtime.apply")
        self.handleError(response)
        return response['result'][0]

    def axisApply(self): # used in setPassMode:
        response = self.request("com.attocube.ids.axis.apply")
        self.handleError(response)
        return response['result'][0]

    def displacementApply(self): # used in setAverageN:
        response = self.request("com.attocube.ids.displacement.apply")
        self.handleError(response)
        return response['result'][0]

    def systemApply(self): # used in setdevicename:
        response = self.request("com.attocube.system.apply")
        self.handleError(response)
        return response['result'][0]

    ############################### JSON Handler ##################################
    ###############################################################################
