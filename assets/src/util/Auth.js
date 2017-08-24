import axios from 'axios';
import _ from 'lodash';
import { login_success, logout_success } from '../actions'
import { URL, LOGIN } from '../config/Api';

export function InvalidCredentialsException(message) {
    this.message = message;
    this.name = 'InvalidCredentialsException';
}

export function login(userData) {
  return axios
    .post(URL + LOGIN, {
      username: userData.username,
      password: userData.password
    })
    .then(function (response) {
      dispatch(login_success(userData.username,response.data.token));
    })
    .catch(function (error) {
      // raise different exception if due to invalid credentials
      dispatch(logout_success());
      if (_.get(error, 'response.status') === 400) {
        throw new InvalidCredentialsException(JSON.stringify(_.get(error, 'response.data')));
      }
      throw error;
    });
}
