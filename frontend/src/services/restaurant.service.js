import axios from 'axios';
import AuthService from './auth.service';

const API_BASE_URL = 'http://localhost:8080/api'; 

class RestaurantService {
  getAllRestaurants() {
    return axios.get(`${API_BASE_URL}/restaurants`).then((response) => response.data);
  }

  getRestaurantDetails(id) {
    return axios.get(`${API_BASE_URL}/restaurants/${id}`).then((response) => response.data);
  }

  getRestaurantReviews(restaurantId) {
    return axios
      .get(`${API_BASE_URL}/restaurants/${restaurantId}/reviews`)
      .then((response) => response.data);
  }

  addReview(restaurantId, reviewData) {
    const user = AuthService.getCurrentUser();
    if (!user || !user.token) {
      return Promise.reject('Brak autoryzacji do dodania recenzji.');
    }
    const headers = { Authorization: 'Bearer ' + user.token };
    return axios
      .post(`${API_BASE_URL}/restaurants/${restaurantId}/reviews`, reviewData, { headers })
      .then((response) => response.data);
  }

  getTopRankings(type = 'traditional', limit = 10) {
    return axios
      .get(`${API_BASE_URL}/rankings/top/${type}?limit=${limit}`)
      .then((response) => response.data);
  }
}

export default new RestaurantService();