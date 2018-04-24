import * as types from './actionTypes';
import customerApi from '../api/customerApi';

export function loadCustomer(customer_id) {
    return function(dispatch) {
        return customerApi.getCustomer(customer_id).then(customer => {
            dispatch(loadCustomerSuccess(customer));
        }).catch(error => {
            throw(error);
        });
    };
}


export function loadCustomers() {
    return function(dispatch) {
        return customerApi.getAllCustomers().then(customers => {
            dispatch(loadCustomersSuccess(customers));
        }).catch(error => {
            throw(error);
        });
    };
}

export function loadCustomerCount() {
    return function(dispatch) {
        return customerApi.getCustomerCount().then(customer_count => {
            dispatch(loadCustomerCountSuccess(customer_count.count));
        }).catch(error => {
            throw(error);
        });
    };
}

export function loadCustomersSuccess(customers) {
    return {type: types.LOAD_CUSTOMERS_SUCCESS, customers};
}

export function loadCustomerSuccess(customer) {
    return {type: types.LOAD_CUSTOMER_DATA_SUCCESS, customer};
}

export function loadCustomerCountSuccess(customer_count) {
    return {type: types.LOAD_CUSTOMER_COUNT_SUCCESS, customer_count};
}