import '../css/app.css';

import React from 'react';
import { Provider } from 'react-redux';
import Login from './pages/Login';
import Map from './pages/Map';
import store from './store';
import ReactDOM from 'react-dom';
import {getTokenFromStorage} from './actions/'

if (getTokenFromStorage() === null) {
    render_login()
} else{
    render_map()
}

export function render_map(){
    ReactDOM.render(
    <Provider store={store}>
        <Map />
    </Provider>,
    document.getElementById('app-container')
);
}
export function render_login(){
    ReactDOM.render(
    <Provider store={store}>
        <Login />
    </Provider>,
    document.getElementById('app-container')
);
}

