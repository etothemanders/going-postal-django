var GP = GP || {};

var Mapper = (function() {
  var defaultStrokeColor = "gray";
  var defaultStrokeWeight = 5;
  var activeColor = "#FF6633";

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
      GP.map.data.setStyle({
        strokeColor: defaultStrokeColor,
        strokeWeight: defaultStrokeWeight
      });
    }
  }

  function listenForPathHover() {
    GP.map.data.addListener('mouseover', function(event) {
      var id = event.feature.getProperty("shipmentID");
      var row = $("#table_row_" + id);

      row.addClass("active-row");
      GP.map.data.revertStyle();
      GP.map.data.overrideStyle(event.feature, {
        strokeColor: activeColor
      });
    });

    GP.map.data.addListener('mouseout', function(event) {
      var id = event.feature.getProperty("shipmentID");
      var row = $("#table_row_" + id);

      row.removeClass("active-row");
      GP.map.data.revertStyle();
    })
  }

  function listenForTableHover() {
    $(".table tbody tr").hover(tableHoverIn, tableHoverOut);
  }

  function tableHoverIn(event) {
    var $tableRowID = parseInt($(this).attr("id").substring(10));

    $(this).addClass("active-row");
    GP.map.data.setStyle(function(feature) {
      if (feature.getProperty("shipmentID") === $tableRowID) {
        GP.map.data.overrideStyle(feature, {
          strokeColor: activeColor,
          strokeWeight: defaultStrokeWeight
        });
      } else {
        return {
          strokeColor: defaultStrokeColor,
          strokeWeight: defaultStrokeWeight
        };
      }
    });
  }

  function tableHoverOut(event) {
    $(this).removeClass("active-row");
    GP.map.data.revertStyle();
    GP.map.data.setStyle(function(feature) {
      return {
        strokeColor: defaultStrokeColor,
        strokeWeight: defaultStrokeWeight
      };
    });
  }

  function init() {
    addMap();
    drawFeatures();
    listenForPathHover();
    listenForTableHover();
  }

  return {
    init: init
  };
})();

$(document).ready(function () {
  GP.mapper = Mapper;
});
