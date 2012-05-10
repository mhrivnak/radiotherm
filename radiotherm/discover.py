import socket
import struct

IP_ADDRESS = '239.255.255.250'
PORT = 1900
MESSAGE = """TYPE: WM-DISCOVER\r\nVERSION: 1.0\r\n\r\nservices: com.marvell.wm.system*\r\n\r\n""".encode('utf-8')

def discover_address():
    """
    The example discovery program provided by Radio Thermostat sets the IP packet's
    TTL to 3. I'm not sure why that would be a good idea, because the default value
    of 1 (in the case of multicast) seems reasonable. I'm content to say that this
    method will discover a thermostat on your local network ONLY, and in any more
    complicated case, you should supply a FQDN or IP address.
    """

    with ExitingSocket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        # set the receive timeout to 1 second
        sock.settimeout(1)
        # make the address reuseable
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(MESSAGE, (IP_ADDRESS, PORT))

        ip_mreq = struct.pack("=4sl", socket.inet_aton(IP_ADDRESS), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, ip_mreq)
        thermostats = []

        while True:
            try:
                data, thermostat = sock.recvfrom(4096)
                # append IP address only
                thermostats.append(thermostat[0])
            except socket.timeout:
                break

        if len(thermostats) == 0:
            raise IOError('No thermostats were found')
        if len(thermostats) > 1:
            raise IOError("Found %d thermostats and I don't know which to pick." % len(thermostats))
        return thermostats[0]

class ExitingSocket(socket.socket):
    """
    This is a socket subclass that can be used with the "with" statement. It
    will attempt to clean up and close itself on exit.
    """
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        try:
            self.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(IP_ADDRESS) + socket.inet_aton('0.0.0.0'))
        except socket.error:
            pass
        self.close()
