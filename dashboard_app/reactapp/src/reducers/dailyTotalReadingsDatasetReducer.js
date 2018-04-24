import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function dailyTotalReadingsDatasetReducer(state = initialState.daily_total_readings_dataset, action) {
    switch(action.type) {
        case types.LOAD_READINGS_GRAPH_TOTAL_DAILY_WATER_CONSUMPTION:
            return action.dataset;
        default:
            return state;
    }
}
