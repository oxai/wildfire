import React, { Component } from 'react';
import './App.css';
import ee from '@google/earthengine'
import { GoogleMap, LoadScript, useGoogleMap } from '@react-google-maps/api'

const googleMapsKey = 'AIzaSyAccl3rn73OcqenWNmTNYM8-7rfBS4xKMM'


function DisplayLayer(props) {
  const map = useGoogleMap();

  const tileSource = new ee.layers.EarthEngineTileSource({
    formatTileUrl: (x, y, z) =>
        `/api/map/tiles/gee/${z}/${x}/${y}`
  });
  const layer = new ee.layers.ImageOverlay(tileSource);

  React.useEffect(() => {
    if (map) map.overlayMapTypes.push(layer);
  }, [map]);
  return <></>
}


export function MapPage(props) {
  return (
      <div className="App">
        <header className="App-header">
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
          >
            Learn React
          </a>
          <LoadScript
              googleMapsApiKey={googleMapsKey}
          >
            <GoogleMap
              id="circle-example"
              mapContainerStyle={{
                height: "400px",
                width: "800px"
              }}
              zoom={7}
              center={{
                lat: -3.745,
                lng: -38.523
              }}
            >
              <DisplayLayer/>
            </GoogleMap>
          </LoadScript>
        </header>
      </div>
  );
}
