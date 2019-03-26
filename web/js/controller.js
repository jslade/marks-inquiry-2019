var knob = {};
var rim = {};

var pubnum = window.pubnub;


var relative_location = function(elem, evt) {
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

  knob.el.attr("cx", knob.center_x + x);
  knob.el.attr("cy", knob.center_y + y);

  pubnub.publish({
    channel: 'launcher',
    message: { knob: { x: x, y: y } }
  });
};

var resetKnob = function() {
  knob.el.attr("cx", knob.center_x);
  knob.el.attr("cy", knob.center_y);
};

var makeKnobDraggable = function() {
  knob.el = $('#knob');
  knob.center_x = parseFloat(knob.el.attr("cx"));
  knob.center_y = parseFloat(knob.el.attr("cy"));
  knob.radius = knob.el.attr("r");

  rim.el = $('#rim');
  rim.radius = rim.el.attr("r");


  knob.el.mousedown(function (evt) {
    knob.touch_down = true;
  });

  knob.el.mouseup(function (evt) {
    knob.touch_down = false;
    resetKnob();
  });

  knob.el.mousemove(function (evt) {
    var loc = relative_location(rim.el, evt);
    dragKnob(loc);
  });

  knob.el.on("touchstart", function (evt) {
    knob.touch_down = true;
  });

  knob.el.on("touchend", function (evt) {
    knob.touch_down = false;
  });

  knob.el.on("touchmove", function (evt) {
    var loc = relative_location(rim.el, evt);
    dragKnob(loc);
  });
};


$(document).ready(function () {
  makeKnobDraggable();
});
