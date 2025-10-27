import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; 
import { Star, TrendingUp, MapPin, Search, Filter, Award, MessageSquare } from 'lucide-react';
import RestaurantService from '../services/restaurant.service';

const Dashboard = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('traditional');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchRestaurants = () => {
      RestaurantService.getAllRestaurants()
        .then(
          (data) => {
            const mappedData = data.map(restaurant => ({
              ...restaurant,
              avgTraditionalRating: restaurant.avgStars, 
              avgNlpRating: restaurant.avgNlpScores ? (restaurant.avgNlpScores.foodScore + restaurant.avgNlpScores.priceScore + restaurant.avgNlpScores.serviceScore + restaurant.avgNlpScores.atmosphereScore) / 4 : 0,
              nlpScores: restaurant.avgNlpScores || { food: 0, price: 0, service: 0, atmosphere: 0 }
            }));
            setRestaurants(mappedData); 
          },
          (error) => {
            console.error("Nie udało się pobrać restauracji:", error);
            setErrorMessage("Nie można załadować danych restauracji.");
          }
        );
    };
    fetchRestaurants();
  }, []);

  const sortedRestaurants = [...restaurants].sort((a, b) => {
    if (sortBy === 'traditional') return b.avgTraditionalRating - a.avgTraditionalRating;
    if (sortBy === 'nlp') return b.avgNlpRating - a.avgNlpRating;
    return b.reviewCount - a.reviewCount;
  });

  const filteredRestaurants = sortedRestaurants.filter(r =>
    (r.name && r.name.toLowerCase().includes(searchQuery.toLowerCase())) ||
    (r.address && r.address.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const getDiscrepancy = (traditional, nlp) => {
    const diff = Math.abs(traditional - nlp);
    if (diff > 0.5) return 'high';
    if (diff > 0.3) return 'medium';
    return 'low';
  };

  const getAverage = (arr, key) => {
    if (arr.length === 0) return 0;
    const total = arr.reduce((sum, r) => sum + r[key], 0);
    return (total / arr.length);
  };

  const avgTraditional = getAverage(restaurants, 'avgTraditionalRating');
  const avgNlp = getAverage(restaurants, 'avgNlpRating');

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-indigo-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Restauracje</p>
              <p className="text-3xl font-bold text-gray-800">{restaurants.length}</p>
            </div>
            <MapPin className="text-indigo-600" size={32} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Recenzje</p>
              <p className="text-3xl font-bold text-gray-800">
                {restaurants.reduce((sum, r) => sum + r.reviewCount, 0)}
              </p>
            </div>
            <MessageSquare className="text-green-600" size={32} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-yellow-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Śr. Tradycyjna</p>
              <p className="text-3xl font-bold text-gray-800">
                {avgTraditional.toFixed(2)}
              </p>
            </div>
            <Star className="text-yellow-600" size={32} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-purple-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Śr. NLP</p>
              <p className="text-3xl font-bold text-gray-800">
                {avgNlp.toFixed(2)}
              </p>
            </div>
            <TrendingUp className="text-purple-600" size={32} />
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-md">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Szukaj restauracji..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter size={20} className="text-gray-600" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="traditional">Ocena tradycyjna</option>
              <option value="nlp">Ocena NLP</option>
              <option value="reviews">Liczba recenzji</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredRestaurants.map((restaurant) => {
          const discrepancy = getDiscrepancy(restaurant.avgTraditionalRating, restaurant.avgNlpRating);
          return (
          
            <Link
              to={`/restaurants/${restaurant.id}`} 
              key={restaurant.id}
              className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow cursor-pointer block" 
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-800">{restaurant.name}</h3>
                  <p className="text-gray-600 text-sm flex items-center gap-1 mt-1">
                    <MapPin size={14} />
                    {restaurant.address || 'Brak adresu'}
                  </p>
                </div>
                {discrepancy === 'high' && (
                  <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-semibold">
                    Wysoka rozbieżność
                  </span>
                )}
              </div>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-yellow-50 p-3 rounded-lg">
                  <p className="text-xs text-gray-600 mb-1">Ocena Tradycyjna</p>
                  <div className="flex items-center gap-2">
                    <Star className="text-yellow-500 fill-yellow-500" size={20} />
                    <span className="text-2xl font-bold text-gray-800">
                      {restaurant.avgTraditionalRating.toFixed(1)}
                    </span>
                  </div>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="text-xs text-gray-600 mb-1">Ocena NLP</p>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="text-purple-600" size={20} />
                    <span className="text-2xl font-bold text-gray-800">
                      {restaurant.avgNlpRating.toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">
                  {restaurant.reviewCount} recenzji
                </span>
                <span className="text-indigo-600 font-semibold text-sm hover:text-indigo-700">
                  Zobacz szczegóły →
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default Dashboard;