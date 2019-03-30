from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from .engine.game_object import GameObject


class PubNubManager(GameObject, SubscribeCallback):
    def __init__(self):
        GameObject.__init__(self, 'PubNub')
        SubscribeCallback.__init__(self)

        self.pnconfig = PNConfiguration()
        self.pnconfig.publish_key = 'pub-c-47d6ffe3-6257-4f0e-9315-05d6c206533a'
        self.pnconfig.subscribe_key = 'sub-c-a6951fe8-4f72-11e9-aa90-a6f7447e8d57'
        self.pubnub = PubNub(self.pnconfig)

        self.pubnub.add_listener(self)
        self.pubnub.subscribe().channels(
            'launcher'
        ).execute()

        self.subscriptions = {}


    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()


    def subscribe(self, channel, callback):
        self.subscriptions[channel] = callback
        self.pubnub.subscribe().channels(channel).execute()


    def shutdown(self):
        self.pubnub.publish().channel('lauuncher').message({'msg': "bye"}).sync()

        self.pubnub.unsubscribe_all()

    def publish_callback(self, envelope, status):
        # Check whether request successfully completed or not
        if status.is_error():
            self.log("PubNub: publish failed: %s" % (status))


    # SubscribeCallback.presence:
    def presence(self, pubnub, presence):
        self.log("PubNub: presence: %s" % (presence))

    # SubscribeCallback.status:
    def status(self, pubnub, status):
        self.log("PubNub: satus = %s" % (status))
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            self.log("PubNub: unexpected disconnect")

        elif status.category == PNStatusCategory.PNConnectedCategory:
            self.log("PubNub: connected!")

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            self.log("PubNub: reconnected")

    # SubscribeCallback.message:
    def message(self, pubnub, message):
        #self.log("PubNub: incoming = %s" % (message.message))

        channel = message.channel
        callback = self.subscriptions.get(channel)
        if callback is not None:
            callback(message.message)

