import axios from "axios";

export class SaloonService {

    apiUrl = "http://localhost:8080/api/movie/saloons/"

    getSaloonsByCityId(cityId) {
        return axios.get(this.apiUrl + "getSaloonsByCityId/" + cityId);
    }

    getall() {
        return axios.get(this.apiUrl + "getall");
    }
}