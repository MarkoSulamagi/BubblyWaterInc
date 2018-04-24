import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function meterCountReducer(state = initialState.meter_count, action) {
    switch(action.type) {
        case types.LOAD_METER_COUNT_SUCCESS:
            return action.meter_count;
        default:
            return state;
    }
}
