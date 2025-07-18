# -*- coding: utf-8 -*-

class Device:

    def printError(self, errorNumber):
        """ Converts the errorNumber into an error string an prints it to the
        console.

        Parameters
        ----------
        errorNumber : int
        """
        print("Error! " + str(self.errorNumberToString(errorNumber)))

    def errorNumberToRecommendation(self, errorNumber):
        """ This function “translates” the error code into an error
        recommendation

        Parameters
        ----------
        errorNumber : int
            error code to translate

        Returns
        -------
        error : str
           error message
        """
        response = self.request("com.attocube.system.errorNumberToRecommendation", [self.language, errorNumber])
        return response['result'][0]
        
    def errorNumberToString(self, errorNumber):
        """ This function “translates” the error code into an error text and
        adds it to the error out cluster.

        Parameters
        ----------
        language : int
            value corresponding to language in which the error should return
            0 – System language
            1 – English (not implemented yet!)
        errorNumber : int
            error code to translate

        Returns
        -------
        error : str
           error message
        """
        response = self.request("com.attocube.system.errorNumberToString", [self.language, errorNumber])
        return response['result'][0]
    
    def getLockStatus(self):
        """ This function gets information whether the device is locked and if
        access is authorized.

        Parameters
        ----------

        Returns
        -------
        locked : bool
            indicates if locked
        authorized : bool
            indicates if access is granted
        """
        response = self.request("getLockStatus")
        return response['result'][0], response['result'][1]

    def lock(self, password):
        """ This function locks the device, so the calling of functions is
        only possible with valid password.

        Parameters
        ----------
        password : str
            password for locking the Device

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("lock", [password])
        return response['result'][0]

    def grantAccess(self, password):
        """ This function requests access to a locked device, so all functions
        can be called after entering the correct password. Otherwise, each
        function creates an error.

        Parameters
        ----------
        password : str
            password for locking the Device

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("grantAccess", [password])
        return response['result'][0]

    def unlock(self):
        """ This function unlocks the device, so it will not be necessary to
        execute the grantAccess function to run any VI.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("unlock")
        return response['result'][0]

    def getFirmwareVersion(self):
        """ This function gets the version number of the controller’s firmware.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        version : str
            firmware version number
        """
        response = self.request("com.attocube.system.getFirmwareVersion")
        return 0,response['result'][0]

    def rebootSystem(self):
        """ This function reboots the device.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.system.rebootSystem")
        return response['result'][0]


    def factoryReset(self):
        """ This function resets the device to the factory settings when it's
        booted the next time.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.system.factoryReset")
        return response['result'][0]

    def getMacAddress(self):
        """ This function gets the MAC address of the device.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        mac : str
            MAC address
        """
        response = self.request("com.attocube.system.getMacAddress")
        return  response['result'][0]

    def getIPAddress(self):
        """ This function gets the IP address of the device.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        mac : str
            MAC address
        """
        response = self.request("com.attocube.system.network.getIpAddress")
        return  response['result'][0]

    def getSerialNumber(self):
        """ This function gets the device’s serial number.

        Parameters
        ----------

        Returns
        -------
        SN : str
            Serial number
        """
        response = self.request("com.attocube.system.getSerialNumber")
        return  response['result'][0]

    def getDeviceName(self):
        """ This function gets the device's name.

        Parameters
        ----------

        Returns
        -------
        errorNumber : int
            No error = 0
        Devicename : str
            get device name
        """
        response = self.request("com.attocube.system.getDeviceName")
        return  response['result'][0]

    def setDeviceName(self, devicename):
        """ This function sets the device’s name.

        Parameters
        ----------
        Devicename : str
            set device name

        Returns
        -------
        errorNumber : int
            No error = 0
        """
        response = self.request("com.attocube.system.setDeviceName", [devicename])
        return response['result'][0]
