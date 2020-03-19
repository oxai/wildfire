import {Loader} from "google-maps";
import ee from "@google/earthengine";

export class SatelliteMap {
    map;
    google;
    markers = [];

    constructor() {
        const googleMapsKey = 'AIzaSyD9rdeB16ByYofOMRAaTZcB60QVHP-_iAs';
        this.loader = new Loader(googleMapsKey, {});
    }

    load = (lat, lng, zoom) => {
        return this.loader.load().then((g) => {
            this.google = g;
            this.map = new this.google.maps.Map(document.getElementById('map'), {
                center: {lat, lng},
                zoom: zoom,
            });
        });
    };

    addMapLayer = (product, from_date, until_date) => {
        this.map.overlayMapTypes.clear();
        if (product === "") return;
        const tileSource = new ee.layers.EarthEngineTileSource({
            formatTileUrl: (x, y, z) =>
                `/api/map/tiles/${product}/${z}/${x}/${y}/${from_date}/${until_date}`
        });
        const layer = new ee.layers.ImageOverlay(tileSource);
        this.map.overlayMapTypes.push(layer);
    };

    addMarker = (lat, lng, color, opacity=1.0) => {
        const marker = new this.google.maps.Marker({
            position: {lat, lng},
            map: this.map,
            icon: {
              url: `/static/${color}_dot.png`
            },
            opacity
        });
        this.markers.push(marker)
    };

    clearMarkers = () => {
        this.markers.map((marker) => marker.setMap(null));
    }
}
