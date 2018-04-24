import { API_URL } from '../const';

console.log(API_URL)
class CustomerApi {
    static getAllCustomers() {
        return fetch(`${API_URL}/api/customers`).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }

    static getCustomerCount() {
        return fetch(`${API_URL}/api/customers/count`).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }

    static getCustomer(customer_id) {
        return fetch(`${API_URL}/api/customers/${customer_id}`).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default CustomerApi;