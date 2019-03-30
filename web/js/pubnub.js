var pn_cfg = {
};

var pubnub = {
  pn: new PubNub({
    publishKey: "pub-c-47d6ffe3-6257-4f0e-9315-05d6c206533a",
    subscribeKey: "sub-c-a6951fe8-4f72-11e9-aa90-a6f7447e8d57"
  })
};

pubnub.set_presence = function (channel_name, callback) {

  pubnub.presence_channel_name = channel_name;

  setInterval(function () {
    pubnub.pn.hereNow({
        channels: [channel_name],
        includeState: false,
        includeUUIDS: false
      },
      callback
    );
  }, 5000);
};

window.pubnub = pubnub;
