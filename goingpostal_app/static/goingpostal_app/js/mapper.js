var GP = GP || {};

var Mapper = (function() {

  function addMap() {
    GP.map = new google.maps.Map(document.getElementById("map-canvas"), {
      center: {lat: 36.3955, lng: -97.8783},
      scrollwheel: false,
      zoom: 5
    });
  }

  function drawFeatures() {
    var $shipmentsTable = $(".table");
    
    if ($shipmentsTable.length > 0) {
      GP.map.data.loadGeoJson("/load_geojson/");
    }
  }

  function init() {
    addMap();
    drawFeatures();
  }

  return {
    init: init
  };
})();

$(document).ready(function () {
  GP.mapper = Mapper;
});
