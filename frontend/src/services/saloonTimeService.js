import axios from "axios";

export class SaloonTimeService {

    apiUrl = "http://localhost:8080/api/movie/saloonTimes/"

    getMovieSaloonTimeSaloonAndMovieId(saloonId, movieId) {
        return axios.get(this.apiUrl + "getMovieSaloonTimeSaloonAndMovieId/" + saloonId + "/" + movieId);
    }

    getSaloonTimesByMovieId(movieId) {
        return axios.get(this.apiUrl + "getSaloonTimesByMovieId/" + movieId);
    }

}