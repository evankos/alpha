// import { combineReducers } from 'redux';
// import * as actionType from '../actions/types';
//
// const tokenInitialState = null;
// const token = (state = tokenInitialState, action) => {
//   switch(action.type) {
//     case actionType.SET_TOKEN:
//       return action.data;
//     default:
//       return state;
//   }
// }
//
// const appReducer = combineReducers({
//   token,
// })
//
// const rootReducer = (state, action) => {
//   return appReducer(state, action);
// }
//
// export default rootReducer;
import { combineReducers } from 'redux';
import {reducer} from '../actions';

const rootReducer = combineReducers({
    auth:reducer
});

export default rootReducer;
