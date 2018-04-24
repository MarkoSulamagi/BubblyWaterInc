import * as types from './actionTypes';
import meterReadingsApi from '../api/meterReadingsApi';

export function loadReadingsGraphTotalDailyWaterConsumption(customer_id=null) {
    return function(dispatch) {
        return meterReadingsApi.getReadingsGraphTotalDailyWaterConsumption(customer_id).then(dataset => {
            dispatch(loadReadingsGraphTotalDailyWaterConsumptionSuccess(dataset));
        }).catch(error => {
            throw(error);
        });
    };
}

export function loadReadingsGraphTotalDailyWaterConsumptionSuccess(dataset) {
    return {type: types.LOAD_READINGS_GRAPH_TOTAL_DAILY_WATER_CONSUMPTION, dataset};
}