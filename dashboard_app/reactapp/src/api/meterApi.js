class MeterApi {

    static getMeterCount() {
        return fetch('http://localhost:8444/api/meters/count').then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default MeterApi;