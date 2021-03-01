#Trying to understand how to do this with the low end
#from ../miflora.miflora_poller import MiFloraPoller
#from btlewrap.bluepy import BluepyBackend
import bluepy as bluepy
from bluepy import btle
import binascii as binascii
#This seems to work at least a little

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)
        #print("A notification was received: ")



address="90:03:b7:ca:1b:fe"
print("Address = ", address)
myFlower=bluepy.btle.Peripheral()
print("Device = ", myFlower)
myFlower.connect(address)
upload_service = myFlower.getServiceByUUID("39e1fb00-84a8-11e2-afba-0002a5d5c51b")
print("Upload Service = ", upload_service)
characteristics = upload_service.getCharacteristics()
buffer_handle = characteristics[0]
transmit_status = characteristics[1]
reciever_status = characteristics[2]
#for characteristic in characteristics:
#    print(characteristic, ":", characteristic.getHandle())
    #105 = buffer handle, 109 = transmit status, 113 = reciever status, 116= file selector
#Write idle
print("Reciever Status = ", reciever_status)
reciever_status.write(b"\x00")
print("Idle written")
#Set up notifications
print("Buffer handle = ", buffer_handle)
print("Setting up delegate")
myFlower.setDelegate( MyDelegate() )
#myFlower2.writeCharacteristic(113, 0)
#Write receiving
print("Starting Data")
reciever_status.write(b"\x01")
#myFlower2.writeCharacteristic(113, 1)


if 1==0 :
    #GATT specifies
    # pair
    # getState
    # setDelegate
    # withDelegate
    # setMTU
    # status
    # parseResp

    # waitForNotifications
    #services        -- collections of characteristics and "relationships to other services"
    # getServices
    # discoverServices
    # getServiceByUUID
    #characteristics  -- by standard defined attribute that contains a single value
    # getCharacteristics
    # readCharacteristic
    # writeCharacteristic
    #descriptors      -- defined attributes that describe a characteristic value
    # getDescriptors
    #declaritions     -- read only reveal parts of the device
    #  ?
    #This form also seems to work
    address="90:03:b7:ca:1b:fe"
    myFlower2=bluepy.btle.Peripheral()
    myFlower2.connect(address)
    #This is by characteristic, what about by service
    #Let's check the battery first, this should be standard, but I couldn't find a way not, so let's just hack it in
    battery = myFlower2.readCharacteristic(0x18)[0]
    print("Current Battery Level ", battery)
    #I'd imagine services return a more complex structure
    #The manual 3.3 refers to this as a custom time profile
    #So this doesn't work, that's kind of a bummer, do we have to form the UUID differently?
    myFlower2.connect(address)
    #This doesn't work either
    profileTime=myFlower2.readCharacteristic(0xFD00)



    #Now let's read history
    charHistoryEntry=myFlower2.readCharacteristic(0xFC01)

    bat = getServiceByUUID("0x2A19")

    charBat=int.from_bytes("0x2A19", "big")
    myFlower2.readCharacteristic()
    #This (list before + 1 matches the device description)
    myFlower2.readCharacteristic(3)
    #This should help make sure I'm decoding this properly
    myFlower2.readCharacteristic(5)
    #This reads 07, 00
    #Hoping this matches soil temp
    #Little endian u16, least first, actually thought seems like most first 
    #From page 7
    # xFA03Soil    Temp(characteristic_value    *    3.3)        /    (211-­‐1
    #   Read as characteristic 45
    #   0xFA04 is air temp characteristic from manual
    # 39e1fa04-84a8-11e2-afba-0002a5d5c51b
    t=myFlower2.readCharacteristic(45)
    val = int.from_bytes(t, "big") 
    print(val)
    val = (int.from_bytes(t, "big") * 3.3 )/(2**11 - 1)
    #When this succeeds it does provide a list that looks like UUID services
    serviceList=myFlower2.getServices()
    myFlower2.connect(address)
    descriptors=myFlower2.getDescriptors()
    characteristics=myFlower2.getCharacteristics()
    #Descriptors match characteristics, descriptors are descriptive
    #read_handle = read_characteristic

    desc_iterator = iter(descriptors)
    d1 = next(desc_iterator)
    print(d1.__str__)
    char_iter = iter(characteristics)
    c1 = next(char_iter)
    c1.getDescriptors()
    c1.getHandle()
    c1.propertiesToString()
    c1.read()

    #Let's grab the first service and first characteristics
    #We'd expect this to be the generic access
    myFlower2.connect(address)
    #services=myFlower2.getServices()
    #temp_itr = iter(services)
    #next(temp_itr)
    #next(temp_itr)
    #next(temp_itr)
    #cur_service = next(temp_itr)
    #An alternative is 
    cur_service = myFlower2.getServiceByUUID("39e1fa00-84a8-11e2-afba-0002a5d5c51b")
    #Get the descriptors
    descriptors = cur_service.getDescriptors()
    #Look at all descriptors
    for descriptor in descriptors:
        #Printing these as is isn't that exciting
        print(" ", descriptor, "-", descriptor.read())
        #Might need to read it
    characteristics = cur_service.getCharacteristics()
    for characteristic in characteristics:
        #Printing these as is isn't that exciting
        print(" ", characteristic, "-", characteristic.read())
        #Might need to read it



    #Should be on
    #Service <uuid=39e1fa00-84a8-11e2-afba-0002a5d5c51b handleStart=35 handleEnd=73>
    # 39e1fa01-84a8-11e2-afba-0002a5d5c51b  --light
    # 39e1fa02-84a8-11e2-afba-0002a5d5c51b  --Soil EC
    # 39e1fa03-84a8-11e2-afba-0002a5d5c51b  --Soil temp
    # 39e1fa04-84a8-11e2-afba-0002a5d5c51b  --Air temp
    # 39e1fa05-84a8-11e2-afba-0002a5d5c51b  --Soil VWC
    # 39e1fa07-84a8-11e2-afba-0002a5d5c51b  --Light On/Off
    # 39e1fa07-84a8-11e2-afba-0002a5d5c51b  --Move detected time

    print(cur_service)
    characteristics = cur_service.getCharacteristics()
    temp_itr = iter(characteristics)
    cur_char = next(temp_itr)
    descriptors = cur_service.getDescriptors()
    temp_itr = iter(descriptors)
    cur_desc = next(temp_itr)
    print(cur_desc)
    handle = cur_char.getHandle()
    #We get handle 37
    print(myFlower2.readCharacteristic(handle))

    temp_itr = iter(handles)
    cur_hand = next(temp_itr)
    print(cur_hand)
    print(cur_char.propertiesToString())
    print(cur_char.read())


    for service in services:
        print(service)
        characteristics = service.getCharacteristics()
        #for characteristic in characteristics:
        #    print(" ", characteristic)
        #get a single characteristic
        char_iter = iter(characteristics)
        characteristic = next(char_iter)
        print(characteristic.getDescriptors())
        print(characteristic.getHandle())
        characteristic.propertiesToString()
        characteristic.read()
        characteristic.supportsRead()
        characteristic.write()

        descriptors = service.getDescriptors()
        for descriptor in descriptors:
            print(" ", descriptor)


    #Let's try reading the history
    #Would need to reference this to get the correct information to do the read correctly, will defer and just poke around with
    myFlower2.connect(address)
    history_service = myFlower2.getServiceByUUID("39e1fc00-84a8-11e2-afba-0002a5d5c51b")
    characteristics = history_service.getCharacteristics()
    for characteristic in characteristics:
        print(characteristic, "-", characteristic.read(), ":", characteristic.getHandle())



    #try:
    #     myval=characteristic.read()
    #     break
    #except:
    #    myval="N/A"
    #print("   ", myval,  ":", characteristic.getHandle())


    #This is the file upload protocol
    #Service <uuid=39e1fb00-84a8-11e2-afba-0002a5d5c51b handleStart=103 handleEnd=117>
    # 39e1fb01-84a8-11e2-afba-0002a5d5c51b Tx Buffer 20 bytes
    # 39e1fb02-84a8-11e2-afba-0002a5d5c51b Tx Status U8
    # 39e1fb03-84a8-11e2-afba-0002a5d5c51b Rx Status U8 Read/Write



    #<uuid=39e1fc00-84a8-11e2-afba-0002a5d5c51b handleStart=78 handleEnd=102>

    #The following 3 are standard sevices    
    #Service <uuid=Generic Access handleStart=1 handleEnd=11>
    #
    #Service <uuid=Generic Attribute handleStart=12 handleEnd=15>
    #
    #Service <uuid=Device Information handleStart=16 handleEnd=34>
    #
    #Service <uuid=39e1fa00-84a8-11e2-afba-0002a5d5c51b handleStart=35 handleEnd=73>
    # 39e1fa01-84a8-11e2-afba-0002a5d5c51b  --light
    # 39e1fa02-84a8-11e2-afba-0002a5d5c51b  --Soil EC
    # 39e1fa03-84a8-11e2-afba-0002a5d5c51b  --Soil temp
    # 39e1fa04-84a8-11e2-afba-0002a5d5c51b  --Air temp
    # 39e1fa05-84a8-11e2-afba-0002a5d5c51b  --Soil VWC
    # 39e1fa07-84a8-11e2-afba-0002a5d5c51b  --Light On/Off
    # 39e1fa07-84a8-11e2-afba-0002a5d5c51b  --Move detected time
    #
    #A standard service for the battery also 0x2A19
    #Service <uuid=Battery Service handleStart=74 handleEnd=77>
    #
    #This is the history service
    #Service <uuid=39e1fc00-84a8-11e2-afba-0002a5d5c51b handleStart=78 handleEnd=102>
    # 39e1fc01-84a8-11e2-afba-0002a5d5c51b number of entries
    # 39e1fc02-84a8-11e2-afba-0002a5d5c51b last index entry
    # 39e1fc03-84a8-11e2-afba-0002a5d5c51b transfer star idx
    #
    #This is the file upload protocol
    #Service <uuid=39e1fb00-84a8-11e2-afba-0002a5d5c51b handleStart=103 handleEnd=117>
    # 39e1fb01-84a8-11e2-afba-0002a5d5c51b Tx Buffer 20 bytes
    # 39e1fb02-84a8-11e2-afba-0002a5d5c51b Tx Status U8
    # 39e1fb03-84a8-11e2-afba-0002a5d5c51b Rx Status U8 Read/Write


    #Time service
    #Service <uuid=39e1fd00-84a8-11e2-afba-0002a5d5c51b handleStart=118 handleEnd=121>
    #Service <uuid=39e1fe00-84a8-11e2-afba-0002a5d5c51b handleStart=122 handleEnd=136>
    #Service <uuid=39e1fd80-84a8-11e2-afba-0002a5d5c51b handleStart=137 handleEnd=150>
    #Service <uuid=f000ffc0-0451-4000-b000-000000000000 handleStart=151 handleEnd=65535>


    myFlower2.connect(address)
    descriptors=myFlower2.getDescriptors()
    show1=0
    for descriptor in descriptors:
        if show1 == 1:
            show1 = 0
            help(descriptor)
        print(descriptor)
        print(descriptor.__dict__)
        

    #This has all the descritions, except for the actual readings
    myFlower2.connect(address)
    characteristics=myFlower2.getCharacteristics()
    for characteristic in characteristics:
        print(characteristic)


    #Room was 3075  70c=21.11
    #Outside is 2307 36c=2
    #That gives 40 counts per degree
    #Now room is giving me 6658

    #In window for a while 2307
    #Looks to me more like 2**9

    #actualy temperature is ~21.111
    #So 3076/146 get's us there.   
    #x0c, x03 -> 12 3 - 780 or 3075
    binascii.hexlify(t)

    binascii.hexlify("\x12")


    myFlower2.readCharacteristic(4)
    myFlower2.readCharacteristic(5)
    #x02, x05, x00, x01
    #  2    5    0    1
    #b'\x12-\x00\x1b\xc5\xd5\xa5\x02\x00\xba\xaf\xe2\x11\xa8\x84\x03\xfa\xe19'
    #    18    0  27  197 213 165  2   0  186   
    serviceList=myFlower.getServices()
    values = list(serviceList.values())
    #This should be Appearance
    myFlower2.readCharacteristic(4)

    myFlower2.readCharacteristic(44)
    myFlower2.readCharacteristic(36)

    #Hmm this doesn't error out not sure what it does
    t=myFlower.getServiceByUUID("39e1fa00-84a8-11e2-afba-0002a5d5c51b")


    #poller = MiFloraPoller("90:03:b7:ca:1b:fe", BluepyBackend)

    myFlower2.connect(address)
    #Page 18
    #Number entries (readings)
    charNumEnt  =myFlower2.readCharacteristic(79+1)
    #Last idx
    charLastIdx =myFlower2.readCharacteristic(83+1)
    #Calculated first idx
    firstIdx    = charLastIdx - charNumEnt + 1
    #Write first idd
    myFlower2.writeCharacteristic(87+1, firstIdx)

