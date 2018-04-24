import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function customerReducer(state = initialState.customer, action) {
    switch(action.type) {
        case types.LOAD_CUSTOMER_DATA_SUCCESS:
            return action.customer;
        default:
            return state;
    }
}
