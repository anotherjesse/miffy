#import web
#web.serve()

mqtt_server = '192.168.86.98'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'miffy'

def sub_cb(topic, msg):
    global bunny
    try:
        r = int(msg[0:2], 16)
        g = int(msg[3:4], 16)
        b = int(msg[4:5], 16)
        bunny.setColor((r,g,b))
        bunny.draw()
    except Exception as e:
        print(e)
    print((topic, msg))


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()


while True:
  try:
    client.wait_msg()
  except OSError as e:
    restart_and_reconnect()