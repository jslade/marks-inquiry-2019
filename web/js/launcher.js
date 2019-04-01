var showJoinCode = function() {
  //$('#instructions h1').text('Scan the QR code to join the next game');

  var link =
    window.location.protocol + "//" +
    window.location.hostname;
  if (window.location.port) {
    link += ":" + window.location.port;
  }
  link += "/controller.html"

  $('#link').text(link);
  new QRCode($('#qrcode')[0], link);
};


$(document).ready(function () {
  showJoinCode();

  var pubnub = window.pubnub;
  pubnub.set_presence("launcher", function(status, response) {
    $("#presence.span").text(response);
  })
});
