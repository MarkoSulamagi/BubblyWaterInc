class meterReadingsApi {

    static getReadingsGraphTotalDailyWaterConsumption(customer_id=null) {
        let customer_filter = '';
        if (customer_id) {
            customer_filter += '&customer_id=' + customer_id
        }
        return fetch('http://localhost:8444/api/meters/readings?dataset=daily-total' + customer_filter).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default meterReadingsApi;