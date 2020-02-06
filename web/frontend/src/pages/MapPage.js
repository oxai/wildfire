import React from 'react';
import './App.css';
import ee from '@google/earthengine'
import {Loader} from 'google-maps';
import {Button, Form, FormControl, Nav, Navbar, NavDropdown} from "react-bootstrap";

let map;
const googleMapsKey = 'AIzaSyAccl3rn73OcqenWNmTNYM8-7rfBS4xKMM'
const loader = new Loader(googleMapsKey, {});
loader.load().then((google) => {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8,
    });

    addMapLayer("landsat/8/raw/default");
});


const addMapLayer = (product) => {
    const tileSource = new ee.layers.EarthEngineTileSource({
        formatTileUrl: (x, y, z) =>
            `/api/map/tiles/${product}/${z}/${x}/${y}`
    });
    const layer = new ee.layers.ImageOverlay(tileSource);

    map.overlayMapTypes.clear();
    map.overlayMapTypes.push(layer);
};

const handleChange = (event) => {
    addMapLayer(event.target.value)
};


export function MapPage() {
    return (
        <div className="App">
            <Navbar bg="dark" variant="dark" expand="lg">
                <Navbar.Brand href="/">OxAI Earth</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mr-auto">
                        <Nav.Link href="/">Home</Nav.Link>
                        <Nav.Link href="https://oxai.org">Society</Nav.Link>
                    </Nav>
                    <Form inline>
                        <FormControl type="text" placeholder="Enter location" className="mr-sm-2"/>
                        <Button variant="dark">Search</Button>
                    </Form>
                    <Form inline className="ml-5">
                        <Form.Control as="select" onChange={handleChange}>
                            <option value="landsat/8/raw/default">Landsat 8 Raw Scenes</option>
                            <option value="landsat/8/raw/nbr">Landsat 8 NBR (Raw)</option>
                            <option value="landsat/8/surface/default">Landsat 8 Surface</option>
                            <option value="landsat/8/surface/nbr">Landsat 8 NBR (Surface)</option>
                            <option value="landsat/8/ndvi/default">Landsat 8 NDVI</option>
                            <option value="modis/terra/fire/default">MODIS Active Fire</option>
                            <option value="modis/terra/snow/default">MODIS Terra Snow</option>
                            <option value="modis/terra/temperature/default">MODIS Terra Temperature</option>
                            <option value="sentinel/2/l1c/default">Sentinel 2 Level-1C</option>
                            <option value="sentinel/2/l1c/vis_fire">Sentinel 2 Level-1C Visualise fire</option>
                            <option value="sentinel/2/l1c/nbr">Sentinel 2 Level-1C NBR</option>
                        </Form.Control>
                    </Form>
                </Navbar.Collapse>
            </Navbar>
            <div id="map" style={{
                flex: 1
            }}/>
        </div>
    );
}
