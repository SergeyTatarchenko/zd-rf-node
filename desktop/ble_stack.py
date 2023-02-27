# -*- coding: utf-8 -*-
import bleak

defaultSearchTimeout  = 5
defaultConnectTimeout = 5

AvailableServers      = list()
ConnectedServers      = dict()

async def ble_scan_for_devices(AdvNameTemplate="Any"):
    """
    scan for available devices, AvailableServers will be filled up 
    with actual advertising data
    """
    global AvailableServers
    
    AvailableServers.clear()
    AllDevices = await bleak.BleakScanner.discover(timeout=defaultSearchTimeout)
    
    for item in AllDevices:
        if AdvNameTemplate != "Any":    
            try:
                if AdvNameTemplate in item.name:
                    AvailableServers.append(item)
            except(TypeError):
                #empty item passed (without name), skip it
                continue
        else:
            # add all available devices  
            AvailableServers.append(item)

async def ble_connect_to_device(name : str):
    """
    connect to device by passed name
    name : device name
    """
    global AvailableServers
    global ConnectedServers
    
    state = False
    for item in AvailableServers:
        if item.name == name:
            session =  bleak.BleakClient(item.address)
            await session.connect(timeout=defaultConnectTimeout)

            if session.is_connected:
                print("<info> connected to " + item.name + " " + str(item.address))
                ConnectedServers.update({item : session})
                AvailableServers.remove(item)
                state = True
            else:
                print("<error> failed to connect to " + str(item.address))
            break

    return state

async def ble_enable_notifications(name : str, NotificationCallback, 
                                   IncomingDataCharacteristic : str):
    """
    enable notifications in connected device
    name                       : device name
    NotificationCallback       : handler that will be called on each notification event
    IncomingDataCharacteristic : characteristic first part
    """
    global ConnectedServers
    
    session = None
    for item in ConnectedServers.keys():
        if item.name == name:
            session = ConnectedServers[item]
            break
    
    state = False
    if session != None and session.is_connected:
        for service in session.services:
                for char in service.characteristics:
                    service_uuid = char.uuid.split('-')[0]
                    if service_uuid == IncomingDataCharacteristic and "notify" in char.properties:
                        await session.start_notify(char, NotificationCallback)
                        print("<info> enable notifications...")
                        state = True
                        break
    return state

async def ble_disconnect_from_device(name : str):
    """
    disconnect from device by passed name
    name : device name
    """    
    session = None
    key     = None
    state   = False
    
    for item in ConnectedServers.keys():
        if item.name == name:
            key     = item
            session = ConnectedServers[item]
            break

    if session != None and session.is_connected:
        await session.disconnect()
        
    if session.is_connected:
        print("<error> failed to disconnect from " + name)
    else:
        print("<error> disconnected from " + item.name + " " + str(item.address))
        ConnectedServers.pop(key)  
        state = True

    return state

async def ble_send_data(name : str, messages : list, OutgoingDataCharacteristic : str):
    """
    send data to connected device
    name     : device name
    messages : list with messages to send
    """
    state   = False
    session = None
    for item in ConnectedServers.keys():
        if item.name == name:
            session = ConnectedServers[item]
            break
            
    if session != None:
        for service in session.services:
            for char in service.characteristics:
                service_str = char.uuid.split('-')[0]
                if service_str == OutgoingDataCharacteristic:
                    for message in messages:
                        await session.write_gatt_char(char_specifier=char, 
                                                      data=bytes(message, encoding='ascii'))
                    state   = True
                    break     
    else:
        print("<error> device with selected name is not connected")

    return state
