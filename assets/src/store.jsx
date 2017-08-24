import { compose, createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import { persistStore, autoRehydrate } from 'redux-persist';
import rootReducer from './reducers';
import axiosMiddleware from 'redux-axios-middleware';
import {getActionTypes} from 'redux-axios-middleware';
import axios from 'axios';



const client = axios.create({ //all axios can be used, shown in axios documentation
    baseURL:'http://35.189.101.64:80/api/', //TODO remove hardcoded IP
    responseType: 'json'
});
const options = {
    // not required, but use-full configuration option
    returnRejectedPromiseOnError: true,
    onSuccess : ({ action, next, response }, options) => {
        const nextAction = {
            type: getActionTypes(action, options)[1],
            response: response,
            meta: {
                previousAction: action
            }
        };
        // next(nextAction);
        store.dispatch(nextAction);
        return nextAction;
    },
    onError : ({ action, next, error }, options) => {
        let errorObject;
        if (!error.response) {
            errorObject = {
                data: error.message,
                status: 0
            };
            if (process.env.NODE_ENV !== 'production') {
                console.log('HTTP Failure in Axios', error);
            }
        } else {
            errorObject = error;
        }
        const nextAction = {
            type: getActionTypes(action, options)[2],
            error: errorObject,
            meta: {
                previousAction: action
            }
        };
        // next(nextAction);
        store.dispatch(nextAction);
        return nextAction;
    }
};
const store = createStore(
    rootReducer,
    compose(
        applyMiddleware(
            createLogger(),
            axiosMiddleware(client,options)
        ),
        // autoRehydrate()
    )
);
persistStore(store);
export default store;