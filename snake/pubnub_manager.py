from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from .engine.game_object import GameObject

from multiprocessing import Pipe, Process
import sys


class PubNubManager(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'PubNub')

        self.subscriptions = {}
        self.subprocess = self.Subprocess()

    def publish(self, channel, message):
        self.subprocess.publish(channel, message)

    def subscribe(self, channel, callback):
        self.subscriptions[channel] = callback
        self.subprocess.subscribe(channel)

    def tick(self, millis):
        while True:
            incoming = self.subprocess.receive()
            if incoming is None: break
            self.process_incoming(incoming)

    def process_incoming(self, message):
        channel = message.channel
        callback = self.subscriptions.get(channel)
        if callback is not None:
            callback(message.message)


    # Because of the performance of the pubnub processing, it is done in
    # a separate subprocess using multiprocessing.Process, with messages
    # exchanged between the main process and the subprocess using a
    # multiprocessing.Pipe. This prevents the thread locking and such
    # that PubNub does from interfering with the game loop.
    class Subprocess(object):
        def __init__(self):
            self.parent_conn, child_conn = Pipe()

            self.mp = Process(target=self.main, args=(child_conn,))
            self.mp.start()

        def log(self, msg):
            print(msg)
            sys.stdout.flush()

        # This is the entry point for the subprocess, basically just needs
        # to proxy pubnum traffic between the parent.
        def main(self, child_conn):
            self.setup_pubnub()
            self.loop(child_conn)

        def setup_pubnub(self):
            self.pnconfig = PNConfiguration()
            self.pnconfig.publish_key = 'pub-c-47d6ffe3-6257-4f0e-9315-05d6c206533a'
            self.pnconfig.subscribe_key = 'sub-c-a6951fe8-4f72-11e9-aa90-a6f7447e8d57'
            self.pubnub = PubNub(self.pnconfig)

            self.listener = self.Listener(self)
            self.pubnub.add_listener(self.listener)
            self.pubnub.subscribe().channels('launcher').execute()

        def loop(self, conn):
            self.child_conn = conn
            try:
                while True:
                    msg = conn.recv()
                    if msg.get('publish', None):
                        self.publish_now(*msg['publish'])
                    elif msg.get('subscribe', None):
                        self.subscribe_now(msg['subscribe'])
            except EOFError:
                self.shutdown()


        def shutdown(self):
            self.pubnub.publish().channel('lauuncher').message({'msg': "bye"}).sync()
            self.pubnub.unsubscribe_all()


        # On the parent side, this just pushes the message into the pipe
        # to be published on the child side
        def publish(self, channel, message):
            self.parent_conn.send({ 'publish': (channel, message) })

        # This is done on the child side
        def publish_now(self, channel, message):
            self.pubnub.publish().channel(channel).message(message).sync()


        # On the parent side, this just pushed the message into the pipe
        # to be handled on the child side
        def subscribe(self, channel):
            self.parent_conn.send({ 'subscribe': channel })

        # This is done on the child side
        def subscribe_now(self, channel):
            self.log("subscribing to %s" % (channel))
            self.pubnub.subscribe().channels(channel).execute()


        def receive(self):
            ready = self.parent_conn.poll()
            if not ready: return None
            try:
                return self.parent_conn.recv()
            except EOFError:
                return None


        class Listener(SubscribeCallback):
            def __init__(self, subprocess):
                self.subprocess = subprocess

            def log(self, msg):
                self.subprocess.log(msg)

            def presence(self, pubnub, presence):
                self.log("PubNub: presence: %s" % (presence))

            def status(self, pubnub, status):
                self.log("PubNub: satus = %s" % (status))
                if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                    self.log("PubNub: unexpected disconnect")

                elif status.category == PNStatusCategory.PNConnectedCategory:
                    self.log("PubNub: connected!")

                elif status.category == PNStatusCategory.PNReconnectedCategory:
                    self.log("PubNub: reconnected")

            def message(self, pubnub, message):
                #self.log("PubNub: incoming = %s" % (message.message))
                self.subprocess.child_conn.send(message)





