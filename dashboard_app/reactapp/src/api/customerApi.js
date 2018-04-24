class CustomerApi {
    static getAllCustomers() {
        return fetch('http://localhost:8444/api/customers').then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }

    static getCustomerCount() {
        return fetch('http://localhost:8444/api/customers/count').then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }

    static getCustomer(customer_id) {
        return fetch('http://localhost:8444/api/customers/' + customer_id).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default CustomerApi;