/**
 * Initialize the Google Map and add our custom layer overlay.
 * @param {string} mapid
 * @param {string} token
 * @param {string} mapurl
 */
const initialize = () => {
  // Create an ImageOverlay using the MapID and token we got from Node.js.
  const tileSource = new ee.layers.EarthEngineTileSource({
    formatTileUrl: (x, y, z) =>
        `/api/map/tiles/gee/${z}/${x}/${y}`
  });
  const layer = new ee.layers.ImageOverlay(tileSource);

  const myLatLng = new google.maps.LatLng(45.340833, -116.466667);
  const mapOptions = {
    center: myLatLng,
    zoom: 8,
    maxZoom: 10,
    streetViewControl: false,
  };

  // Create the base Google Map.
  const map = new google.maps.Map(document.getElementById('map'), mapOptions);

  // Add the EE layer to the map.
  map.overlayMapTypes.push(layer);
};
