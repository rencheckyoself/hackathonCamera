#This class will control servo movements using Pololu micro servo driver

class Servo:
        """A class to interact with the servo board"""

        _bitMask = [127,16256]
        _byteCombo = [0,0]


        def __init__(self, pinNum):
                self.Pin = pinNum
                self._goToPos = 1500
                self.uSecLimits = [992,1900]
                self.servoChn = chr(pinNum)

        def SetPin(self, pinNum):
                self.Pin = pinNum
                self.servoChn = chr(pinNum)
                print("Pin set to " + str(pinNum))

        def Move(self, entry):

                buffer = []

                self._goToPos = self._goToPos + entry

                if self._goToPos < self.uSecLimits[0]:

                        self._goToPos = self.uSecLimits[0]

                elif self._goToPos > self.uSecLimits[1]:

                        self._goToPos = self.uSecLimits[1]

                newPosition = self._goToPos * 4

                self._byteCombo[0] = newPosition & self._bitMask[0]
                self._byteCombo[1] = newPosition & self._bitMask[1]
                self._byteCombo[1] = self._byteCombo[1] >> 7

                buffer = ['\x84',self.servoChn, chr(self._byteCombo[0]), chr(self._byteCombo[1])]

                return buffer
