#pip install paho-mqtt

import time
import paho.mqtt.client as mqtt
import configparser
#import tomllib

class Publish:
  def on_connect(self, client, userdata, flags, rc):
    if rc==0:
      #print("Connected successfully", flush=True)
      pass
    else:
      print("Connection problem code {}".format(rc), flush=True)

  def on_disconnect(self, client, userdata, rc):
    #print("Disconnection code {}".format(rc), flush=True)
    pass

  def on_publish(self, client, userdata, mid):
    #print("Published msg number {}".format(mid), flush=True)
    pass

  def __init__(self, name="publish"):
    self.client = mqtt.Client(name)
    self.client.on_connect = self.on_connect
    self.client.on_disconnect = self.on_disconnect
    self.client.on_publish = self.on_publish
    self.msgPattern=("[{{ "
            "\"bn\": \"test/\""
            ",\"bt\": {}"
            "}}]")
    self.config = configparser.ConfigParser()
    self.config.read('publish.ini')
    #with open("publish.toml", "rb") as f:
    #  self.config = tomllib.load(f)

  def publish(self, *args):
    unix = int(time.time())//60*60
    msg = self.msgPattern.format(unix, *args)
    #print("msg: {}".format(msg))
    self.client.username_pw_set("sensors", "sensors")
    r=self.client.connect("192.168.1.200", 1883)
    #r=self.client.connect("127.0.0.1", 1883)
    print("connect result: {}".format(r), flush=True)
    self.client.loop(timeout=1.0)
    r=self.client.publish("myhome", msg, qos=2)
    print("publish result: {} result: {} mid: {}".format(r, r.rc, r.mid), flush=True)
    #r.wait_for_publish()
    for i in range(5):
      y = r.is_published()
      print("is published: {}".format(y), flush=True)
      if (y):
        break
      self.client.loop(timeout=1.0)
    self.client.disconnect()
    self.client.loop(timeout=1.0)


