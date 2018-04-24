import {combineReducers} from 'redux';
import customer from './customerReducer';
import customers from './customersReducer';
import customer_count from './customerCountReducer';
import meter_count from './meterCountReducer';
import daily_total_readings_dataset from './dailyTotalReadingsDatasetReducer';

const rootReducer = combineReducers({
    customer,
    customers,
    customer_count,
    meter_count,
    daily_total_readings_dataset
});

export default rootReducer;