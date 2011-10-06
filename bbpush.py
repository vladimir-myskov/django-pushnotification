from basic import Push
from django.template import Context, Template
from django.template.loader import get_template
from datetime import datetime
from time import time
from random import random
import httplib
from base64 import b64encode
import settings



class BBPush(Push):
    BOUNDARY = "8d5588928a90afd3009d"
    def __init__(self,device_token,message=""):
        Push.__init__(self,device_token,message)

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
        addresses = (device or [self.device_token])
        deliver_before_timestamp = (datetime.now() + (5 * 60))
        push_id = int(round(int(time.time()) * random()) + int(time.time())) # simplify
        t = get_template("bbpush.post")
        c = Context({'addresses':addresses,'deliver_before_timestamp':deliver_before_timestamp ,'push_id':push_id,'app_id':settings.BB_APP_ID})
        content = t.render(c)

    def _send(self,device=None):
        msg = self._pack_message(device)
        #try:
            c = httplib.HTTPSConnection(settings.BB_PUSH_URL)
            headers = {"User-Agent":"BBPush Python Library",
		       "Authorization":"Basic %s" % b64encode(settings.BB_APP_ID+':'+settings.BB_APP_PASS),
                  	"Content-Type":"multipart/related; boundary=%s; type=application/xml" % BBPush.BOUNDARY}                  
            c.request("POST", "", msg, headers)
            response = c.getresponse()
            data = response.read()
            c.close()
            return response.status, response.reason
        #except:
        #    raise

        


