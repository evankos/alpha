import * as actionType from './types';
import querystring from 'querystring';
import browserHistory from '../history'
import {render_map,render_login} from '../app'

export function getTokenFromStorage(){
    return localStorage.getItem('id_token')
}

export const login = (username, password) => {
    return {
        type: actionType.LOGIN,
        username: username,
        payload: {
            request:{
                method: 'post',
                url:'/auth/',
                data: querystring.stringify({
                    username: username, //gave the values directly for testing
                    password: password
                }),
            // headers: {
            //     "Accept": "application/json"
            // }
        }
    }
};
};

export const logout = () => {
    return {
        type: actionType.LOGOUT,
        username: '',
        token: ''
    };
};

export const signup = (username, password) => {
    return (dispatch) => {
    };
};

const defaultState = {
    isLoggedIn: getTokenFromStorage() !== null,
    username: '',
    token: getTokenFromStorage()
};



export function reducer(state = defaultState, action) {
    switch (action.type) {
        case actionType.LOGIN:
            return Object.assign({}, state, {
                username: action.username
            });
        case actionType.LOGIN_SUCCESS:
            localStorage.setItem('id_token', action.response.data.token);
            render_map();
            return Object.assign({}, state, {
                isLoggedIn: true,
                token: action.response.data.token
            });
        case actionType.LOGIN_FAIL:
            return Object.assign({}, state, {
                isLoggedIn: false,
                username: '',
                token: '',
                errorMessage: JSON.stringify(action.error.response.data)
            });
        default:
            return state;
    }
}