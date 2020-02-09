import React, {useState} from 'react';
import {Button, Form, FormControl, Nav, Navbar, NavDropdown} from "react-bootstrap";
import {SatelliteMap} from "../utils/map";
import axios from 'axios';
import ToggleButtonGroup from "react-bootstrap/ToggleButtonGroup";
import ToggleButton from "react-bootstrap/ToggleButton";
import "react-datepicker/dist/react-datepicker.css";
import './App.css';
import 'rc-slider/assets/index.css';
import {DatePicker} from "../components/DatePicker";
import moment from "moment";


export class MapPage extends React.Component {

    constructor(props) {
        super(props);

        const date = [2015, 11, 1];

        this.state = {
            map: new SatelliteMap(),
            date: moment(date),
            from: moment(date),
            until: moment(date).add(1, "months"),
            layer: "",
            duration: "month",
        };
    }

    componentDidMount() {
        this.state.map.load(10, -160, 3)
            .then(() => this.setState({
                ...this.state,
                map: this.state.map
            }));
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        const {map, from, until, layer} = this.state;
        const dateChanged = from !== prevState.from || until !== prevState.until;
        const layerChanged = layer !== prevState.layer;
        const from_str = from.format('YYYY-MM-DD');
        const until_str = until.format('YYYY-MM-DD');
        if (map.map) {
            if (dateChanged || layerChanged) {
                map.addMapLayer(layer, from_str, until_str);
            }
            if (dateChanged) {
                map.clearMarkers()
                axios.get(`/api/map/fpa_fod/${from_str}/${until_str}/10`)
                    .then((locs) => {
                        locs.data.map((loc) => map.addMarker(loc.lat, loc.lng, "red", 0.5))
                    });
                axios.get(`/api/map/modis_fire/${from_str}/${until_str}/10`)
                    .then((locs) => {
                        locs.data.map((loc) => map.addMarker(loc.lat, loc.lng, "green", 0.5))
                    });
            }
        }
    }

    handleDuration = (duration) => {
        this.setState({
            ...this.state,
            duration,
            until: moment(this.state.from).add(1, `${duration}s`)
        });
    };

    handleDateChange = date => {
        this.setState({
            ...this.state,
            date: date
        });
    };

    handleDateChangeConfirmed = date => {
        this.setState({
            ...this.state,
            from: date,
            until: moment(date).add(1, `${this.state.duration}s`)
        });
    };

    switchMapLayer = (event) => {
        this.setState({
            ...this.state,
            layer: event.target.value
        })
    };

    render() {
        const {duration, date} = this.state;
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
                            <Form.Control as="select" onChange={this.switchMapLayer}>
                                <option value="">No overlay</option>
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
                <div style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "row"
                }}>
                    <div style={{
                        width: 300,
                        color: "white"
                    }}>
                        <div style={{
                            margin: 15
                        }}>
                            <h5>{date.format('YYYY-MM-DD')}</h5>
                            <DatePicker
                                style={{
                                    width: "100%"
                                }}
                                date={date}
                                onChange={this.handleDateChange}
                                onAfterChange={this.handleDateChangeConfirmed}
                            />
                        </div>
                        <h5>Duration</h5>
                        <ToggleButtonGroup
                            type="radio" name="duration" value={duration} onChange={this.handleDuration}
                            style={{
                                width: 270
                            }}
                        >
                            <ToggleButton value={"day"} variant="secondary">1 day</ToggleButton>
                            <ToggleButton value={"week"} variant="secondary">1 week</ToggleButton>
                            <ToggleButton value={"month"} variant="secondary">1 month</ToggleButton>
                        </ToggleButtonGroup>

                    </div>
                    <div id="map" style={{
                        flex: 1
                    }}/>
                </div>
            </div>
        );
    }
}
