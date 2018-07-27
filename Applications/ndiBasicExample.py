from ndicapy import (
    ndiDeviceName, ndiProbe, NDI_OKAY,
    ndiOpen, ndiClose, ndiCommand, ndiGetError,
    ndiErrorString, NDI_115200,
    NDI_8N1, NDI_NOHANDSHAKE,
)


MAX_SERIAL_PORTS = 20
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        result = ndiProbe(name)
    else:
        name = ""
        for port_no in range(MAX_SERIAL_PORTS):
            name = ndiDeviceName(port_no)
            if not name:
                continue
            result = ndiProbe(name)
            if result == NDI_OKAY:
                break
    if result != NDI_OKAY:
        raise IOError(
            'Could not find any NDI device in '
            '{} serial port candidates checked. '
            'Please check the following:\n'
            '\t1) Is an NDI device connected to your computer?\n'
            '\t2) Is the NDI device switched on?\n'
            '\t3) Do you have sufficient privilege to connect to '
            'the device? (e.g. on Linux are you part of the "dialout" '
            'group?)'.format(MAX_SERIAL_PORTS)
        
        )
    print ("probed ok")
    print ("opening",name)
    device = ndiOpen(name)
    if not device:
        raise IOError(
            'Could not connect to NDI device found on '
            '{}'.format(name)
        )
    print(ndiGetDeviceName(device))

    reply = ndiCommand(device, 'INIT:')
    error = ndiGetError(device)
    if reply.startswith('ERROR') or error != NDI_OKAY:
        raise IOError(
            'Error when sending command: '
            '{}'.format(ndiErrorString(error))
        )

    reply = ndiCommand(
        device,
        'COMM:{:d}{:03d}{:d}'.format(NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)
    )
    ndiCommand("TSTART:")

    # TODO activate GX
    # time
    ndiCommand("BX: 1")
    for i in range(1,10):
        # port
        for j in range(0,2):
            print(ndiGetGXTransform(i,j))
    # Add your own commands here!!!
    ndiCommand("TSTOP:")

    ndiClose(device)
