var showJoinCode = function() {
  $('#instructions h1').text('Scan the QR code to join the next game');

  var link =
    window.location.protocol + "//" +
    window.location.hostname + ":" +
    window.location.port +
    "/controller.html"

  new QRCode($('#qrcode')[0], link);
};


$(document).ready(function () {
  showJoinCode();
});
