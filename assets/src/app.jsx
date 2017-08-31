import '../css/app.css';

import React from 'react';
import { Provider } from 'react-redux';
import Login from './pages/Login';
import Map from './pages/Map';
import store from './store';
import ReactDOM from 'react-dom';
import {getTokenFromStorage} from './actions/'
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
if (getTokenFromStorage() === null) {
    render_login()
} else{
    render_map()
}

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var socket = new WebSocket(ws_scheme+'://' + window.location.host + '/posts/?token='+localStorage.getItem('id_token'));
socket.onopen = function open() {
    console.log('WebSockets connection created.');
    socket.send(JSON.stringify('{"message":"This is a message."}'));
    socket.close();
};
socket.onclose = function open() {
    console.log('WebSockets connection closed.');
};


