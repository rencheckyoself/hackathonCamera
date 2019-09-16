#This program will prompt a user for an input and move the respective servo(s)


import serial

askUser = 1
goodInput = 0

userInput = [-1,-1]

inputLimits = [0,100]
uSecLimits = [950,1850]

servoChn = ['\x00','\x01']

byteCombo = [0,0]

b = uSecLimits[0]
m = (uSecLimits[1] - uSecLimits[0])/inputLimits[1]

target = [0,0] #[base motor target, head motor target]

ser = serial.Serial('/dev/ttyACM0',9600)

if ser.is_open:

        print(ser.name)

        while askUser == 1:

                print("Enter the desired target to move each motor to. \n Range is " + str(inputLimits[0]) +" to " + str(inputLimits[1]) + " or -1 to exit")

                while goodInput == 0:
                        try:
                                userInput[0] = raw_input("Base Servo: ")
                                userInput[1] = raw_input("Head Servo: ")

                                target[0] = int(userInput[0])
                                target[1] = int(userInput[1])

                                if target[0] > inputLimits[1] or target[1] > inputLimits[1]:

                                        print("Input values must be " + str(inputLimits[0]) +" to " + str(inputLimits[1]) + ", or -1 to exit")
                                else:

                                        goodInput = 1

                        except (ValueError):

                                print("except")
                                print("Input values must be " + str(inputLimits[0]) +" to " + str(inputLimits[1]) + ", or -1 to exit")

                if target[1] == -1 or target[0] == -1:
                        askUser = 0
                        print("Program Done")
                else:
                        for i in range(len(target)):
                                target[i] = (m * target[i] + b) * 4 #calc 4 * quarter micro second position

                                print(target[i])

                                target[i] = bin(target[i])

                                print(target[i])

                                byteCombo[0] = target[i][9:]
                                byteCombo[1] = target[i][2:9]

                                for j in range(len(byteCombo)):
                                        while len(byteCombo[j]) < 8:
                                                byteCombo[j] = '0' + byteCombo[j]

                                        byteCombo[j] = '0b' + byteCombo[j]
                                        print(byteCombo[j])

                                        byteCombo[j] = int(byteCombo[j],2)

                                        print(byteCombo[j])

                                        byteCombo[j] = chr(byteCombo[j])

                                        print(byteCombo[j])

                                #buffer = '\x84' + servoChn[i] + byteCombo[0] + byteCombo[1]

                                # ser.write(buffer)
                        goodInput = 0
else:
        print("Serial port not open or not found")
