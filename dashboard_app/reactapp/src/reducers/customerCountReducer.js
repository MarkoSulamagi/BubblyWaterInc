import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function customerCountReducer(state = initialState.customer_count, action) {
    switch(action.type) {
        case types.LOAD_CUSTOMER_COUNT_SUCCESS:
            return action.customer_count;
        default:
            return state;
    }
}
