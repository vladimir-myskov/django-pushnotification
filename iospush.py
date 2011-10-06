import datetime
import struct
import ssl
import binascii
from socket import socket
import ssl
from basic import Push
import settings
try:
    import json
except ImportError:
    import simplejson as json

class IosPush(Push):
    def __init__(self,device_token,message="",badge=None,sound=None):
        Push.__init__(self,device_token,message)
        self.badge = badge
        self.sound = sound

    @property
    def badge(self):
        return self.badge

    @badge.setter
    def badge(self,badge):
        self.badge = badge

    @property
    def sound(self):
        return self.sound

    @sound.setter
    def sound(self,sound):
        self.sound = sound

    def _pack_message(self,device = None):
        aps_payload = {'alert':self.message}
        if self.badge:
            aps_payload['badge'] = self.badge 
        if self.sound:
            aps_payload['sound'] = self.sound 
        payload = {'aps':aps_payload}
        s_payload = json.dumps(payload, separators=(',',':'))
        if len(s_payload) > 256:
            raise OverflowError, 'The JSON generated is too big at %d - *** "%s" ***' % (len(s_payload), s_payload)        
        fmt = "!cH32sH%ds" % len(s_payload)
        command = '\x00'      
        msg = struct.pack(fmt, command, 32, binascii.unhexlify(device or self.device_token), len(s_payload), s_payload) 
        return msg

    def _send(self,device=None):
        msg = self._pack_message(device)
        try:
            s = socket()
            c = ssl.wrap_socket(s,
                                ssl_version=ssl.PROTOCOL_SSLv3,
                                certfile=settings.IOS_PUSH_CERT)
            c.connect((settings.IOS_PUSH_URL, 2195))
            c.write(msg)
            c.close()
        except:
            raise

def send_ios(message, device_token, badge=None,sound=None):
    IosPush(device_token,message, badge, sound).send()
