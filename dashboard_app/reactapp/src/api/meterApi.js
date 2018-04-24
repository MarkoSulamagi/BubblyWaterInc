import { API_URL } from '../const';

class MeterApi {

    static getMeterCount() {
        return fetch(`${API_URL}/api/meters/count`).then(response => {
            return response.json();
        }).catch(error => {
            return error;
        });
    }
}

export default MeterApi;