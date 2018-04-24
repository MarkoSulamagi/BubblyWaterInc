import * as types from './actionTypes';
import meterApi from '../api/meterApi';

export function loadMeterCount() {
    return function(dispatch) {
        return meterApi.getMeterCount().then(meter_count => {
            dispatch(loadMeterCountSuccess(meter_count.count));
        }).catch(error => {
            throw(error);
        });
    };
}

export function loadMeterCountSuccess(meter_count) {
    return {type: types.LOAD_METER_COUNT_SUCCESS, meter_count};
}