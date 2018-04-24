import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function customersReducer(state = initialState.customers, action) {
    switch(action.type) {
        case types.LOAD_CUSTOMERS_SUCCESS:
            return action.customers;
        default:
            return state;
    }
}
