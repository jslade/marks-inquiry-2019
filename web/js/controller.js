var knob = {};
var rim = {};

var resizeControls = function() {
  var svg = $('#svg');
  var w = parseInt($(window).width()) - 100;
  var h = parseInt($(window).height()) - 100;
  console.log(`w=${w} h=${h}`);

  svg.attr('width', w);
  svg.attr('height', h);

  knob.el = $('#knob');
  knob.center_x = w/2;
  knob.center_y = h/2;
  knob.radius = (w < h) ? w/6 : h/6;
  knob.el.attr("cx", knob.center_x);
  knob.el.attr("cy", knob.center_y);
  knob.el.attr("r", knob.radius);

  rim.el = $('#rim');
  rim.radius = (w < h) ? w / 3 : h / 3;
  rim.radius_2 = rim.radius * rim.radius;
  rim.el.attr("cx", knob.center_x);
  rim.el.attr("cy", knob.center_y);
  rim.el.attr("r", rim.radius);
};


var pubnub = window.pubnub;

pubnub.connect = function () {
  pubnub.playerID = Math.floor(Math.random() * 10000);
  pubnub.playerChannel = 'player.' + pubnub.playerID;
  pubnub.gameChannel = 'game';

  console.log(`playerID=${pubnub.playerID}`);

  pubnub.pn.subscribe({
    channels: [pubnub.gameChannel, pubnub.playerChannel + '.back'],
    state: {
      name: pubnub.playerID
    }
  });

  var listener = {
    status: function (status) {
      console.log("PN status: ", status);
    },
    message: function (m) {
      //console.log("PN message received: ", m);
      if (m.message.action) {
        var cb = pubnub.callbacks[m.message.action]
        if (cb) {
          cb(m.message);
        }
      }
    },
    presence: function (m) {
      console.log("PN presence received: ", m);
    }
  };
  pubnub.pn.addListener(listener);

  pubnub.callbacks = {}

  pubnub.pn.publish({
    channel: 'launcher',
    message: { player: pubnub.playerID }
  })
};


pubnub.publish = function (msg) {
  pubnub.pn.publish({
    channel: pubnub.playerChannel,
    message: msg
  })
}


var on_set_snake = function (msg) {
  $('#svg').css({'background-color': `rgb(${msg.color.r},${msg.color.g},${msg.color.b})`})
  $('#score').css({ 'background-color': `rgb(${msg.color.r},${msg.color.g},${msg.color.b})` })
  $('#score').text(msg.length)
}

var on_growth = function (msg) {
  $('#score').text(msg.length)
}


var relativeLocation = function(elem, evt) {
  var offs = elem.offset();
  return {
    x: evt.pageX - offs.left,
    y: evt.pageY - offs.top
  };
}

var dragKnob = function(loc) {
  if (!knob.touch_down) {
    return;
  }

  var x = loc.x - rim.radius;
  var y = loc.y - rim.radius;

  dist_2 = x*x + y*y;
  if (dist_2 > rim.radius_2) {
    var angle = Math.atan2(y, x);
    x = rim.radius * Math.cos(angle);
    y = rim.radius * Math.sin(angle);
  }

  knob.el.attr("cx", knob.center_x + x);
  knob.el.attr("cy", knob.center_y + y);
  //$('#debug').text(`x=${x} y=${y}`)

  pubnub.publish({ knob: { x: x, y: y } })
};

var resetKnob = function() {
  knob.el.attr("cx", knob.center_x);
  knob.el.attr("cy", knob.center_y);
  pubnub.publish({ knob: { x: 0, y: 0 } })
};

var makeKnobDraggable = function() {
  document.ontouchstart = function (e) {
    e.preventDefault();
  }

  knob.el.mousedown(function (evt) {
    knob.touch_down = true;
  });

  knob.el.mouseup(function (evt) {
    knob.touch_down = false;
    resetKnob();
  });

  knob.el.mouseleave(function (evt) {
    knob.touch_down = false;
    resetKnob();
  });

  knob.el.mousemove(function (evt) {
    var loc = relativeLocation(rim.el, evt);
    dragKnob(loc);
  });

  knob.el.on("touchstart", function (evt) {
    knob.touch_down = true;
  });

  knob.el.on("touchend", function (evt) {
    knob.touch_down = false;
    resetKnob();
  });

  knob.el.on("touchcancel", function (evt) {
    knob.touch_down = false;
    resetKnob();
  });

  knob.el.on("touchmove", function (evt) {
    var loc = relativeLocation(rim.el, evt.touches[0]);
    dragKnob(loc);
  });
};


$(document).ready(function () {
  resizeControls();
  makeKnobDraggable();
  pubnub.connect();

  pubnub.callbacks.set_snake = on_set_snake
  pubnub.callbacks.growth = on_growth
});
