var GP = GP || {};

var Mapper = (function() {

  function init() {
    GP.map = new google.maps.Map(document.getElementById('map-canvas'), {
      center: {lat: 36.3955, lng: -97.8783},
      zoom: 5
    });
  }

  return {
    init: init
  };
})();

$(document).ready(function () {
  GP.mapper = Mapper;
});
