import React from 'react';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import moment from "moment";


const date2value = (date) =>
    (date.year() - 2000) * 12 + date.month();

const value2date = (value) => {
    const year = Math.floor(value / 12) + 2000;
    const month = value % 12;
    return moment({year, month, day: 1});
};

const curr = moment();
const max = date2value(curr);

export function DatePicker(props) {

    const {date, onChange, onAfterChange} = props;
    const value = date2value(date);

    return (
        <Slider
            min={0}
            max={max}
            value={value}
            onChange={(val) => onChange(value2date(val))}
            onAfterChange={(val) => onAfterChange(value2date(val))}
        />
    )
}
