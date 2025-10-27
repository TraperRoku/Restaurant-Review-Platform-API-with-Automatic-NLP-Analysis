import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; 
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Star, TrendingUp, MapPin, Plus, MessageSquare } from 'lucide-react';

import RestaurantService from '../services/restaurant.service';
import AuthService from '../services/auth.service'; 


const RestaurantDetails = () => {
  const { id } = useParams(); 
  const [restaurant, setRestaurant] = useState(null);
  const [reviews, setReviews] = useState([]); 
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState('');

  const [newReview, setNewReview] = useState({ text: '', starRating: 5 });
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const currentUser = AuthService.getCurrentUser();

  useEffect(() => {
    const fetchDetailsAndReviews = async () => { 
      setLoading(true);
      setErrorMessage(''); 
      try {
        const restaurantData = await RestaurantService.getRestaurantDetails(id);
        const mappedRestaurantData = {
          ...restaurantData,
          avgTraditionalRating: restaurantData.avgStars,
          avgNlpRating: restaurantData.avgNlpScores ? (restaurantData.avgNlpScores.foodScore + restaurantData.avgNlpScores.priceScore + restaurantData.avgNlpScores.serviceScore + restaurantData.avgNlpScores.atmosphereScore) / 4 : 0,
          nlpScores: restaurantData.avgNlpScores || { food: 0, price: 0, service: 0, atmosphere: 0 }
        };
        setRestaurant(mappedRestaurantData);

        const reviewsData = await RestaurantService.getRestaurantReviews(id);
        reviewsData.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
        setReviews(reviewsData);

      } catch (error) {
        console.error("Błąd podczas ładowania danych:", error);
        setErrorMessage("Nie można załadować danych dla tej restauracji.");
      } finally {
        setLoading(false); 
      }
    };

    fetchDetailsAndReviews();
  }, [id]);

  const handleSubmitReview = (e) => {
    e.preventDefault(); 
    setIsSubmitting(true);
    setErrorMessage(''); 
    setSubmitSuccess(''); 
 
    const reviewData = {
      text: newReview.text,
      starRating: newReview.starRating,
      userId: currentUser?.id || 'nieznany-uzytkownik', 
    };

    RestaurantService.postRestaurantReview(id, reviewData) 
      .then((newlyAddedReview) => {
        setReviews([newlyAddedReview, ...reviews]);
        setNewReview({ text: '', starRating: 5 });
        setSubmitSuccess('Recenzja została dodana!'); 
        setIsSubmitting(false);

        setRestaurant(prev => ({...prev, reviewCount: prev.reviewCount + 1}));

      })
      .catch((err) => {

        console.error('Błąd dodawania recenzji:', err);
        const errorMsg = err.response?.data?.message || err.message || 'Nie udało się dodać recenzji.';
        setErrorMessage(errorMsg); 
        setIsSubmitting(false);
      });
  };

  if (loading) {
    return <div className="text-center p-10">Ładowanie danych restauracji...</div>;
  }

  if (errorMessage) {
    return <div className="text-center p-10 text-red-600">{errorMessage}</div>;
  }
  
  if (!restaurant) {
    return <div className="text-center p-10">Nie znaleziono restauracji.</div>;
  }

  return (
    <div className="space-y-6">
      <Link
        to="/" 
        className="text-indigo-600 font-semibold hover:text-indigo-700 flex items-center gap-2"
      >
        ← Powrót do listy
      </Link>

      <div className="bg-white p-8 rounded-xl shadow-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">{restaurant.name}</h1>
        <p className="text-gray-600 flex items-center gap-2 mb-6">
          <MapPin size={18} />
          {restaurant.address || 'Brak adresu'}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-lg">
            <p className="text-sm text-gray-700 mb-2 font-semibold">Ocena Tradycyjna</p>
            <div className="flex items-center gap-3">
              <Star className="text-yellow-500 fill-yellow-500" size={32} />
              <span className="text-4xl font-bold text-gray-800">
                {restaurant.avgTraditionalRating.toFixed(1)}
              </span>
            </div>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg">
            <p className="text-sm text-gray-700 mb-2 font-semibold">Ocena NLP</p>
            <div className="flex items-center gap-3">
              <TrendingUp className="text-purple-600" size={32} />
              <span className="text-4xl font-bold text-gray-800">
                {restaurant.avgNlpRating.toFixed(1)}
              </span>
            </div>
          </div>
          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-6 rounded-lg">
            <p className="text-sm text-gray-700 mb-2 font-semibold">Recenzje</p>
            <div className="flex items-center gap-3">
              <MessageSquare className="text-indigo-600" size={32} />
              <span className="text-4xl font-bold text-gray-800">
                {restaurant.reviewCount}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Analiza Aspektowa NLP</h3>
          <ResponsiveContainer width="100%" height={500}>
            <RadarChart data ={[
              { aspect: 'Jedzenie', value: restaurant.nlpScores.foodScore || restaurant.nlpScores.food },
              { aspect: 'Cena', value: restaurant.nlpScores.priceScore || restaurant.nlpScores.price },
              { aspect: 'Obsługa', value: restaurant.nlpScores.serviceScore || restaurant.nlpScores.service },
              { aspect: 'Atmosfera', value: restaurant.nlpScores.atmosphereScore || restaurant.nlpScores.atmosphere }
            ]}>
              <PolarGrid />
              <PolarAngleAxis 
        dataKey="aspect"
        fontSize={14} 
        fontWeight="bold" 
        stroke="#374151" 
      />
              <PolarRadiusAxis 
        domain={[0, 5]}
        fontSize={14}
        fontWeight="medium"
          stroke="#374151"
      />
              <Radar name="Ocena NLP" dataKey="value" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Porównanie Ocen</h3>
          <ResponsiveContainer width="100%" height={500}>
             <BarChart data={[
                { name: 'Jedzenie', NLP: restaurant.nlpScores.foodScore || restaurant.nlpScores.food, Tradycyjna: restaurant.avgTraditionalRating },
                { name: 'Cena', NLP: restaurant.nlpScores.priceScore || restaurant.nlpScores.price, Tradycyjna: restaurant.avgTraditionalRating },
                { name: 'Obsługa', NLP: restaurant.nlpScores.serviceScore || restaurant.nlpScores.service, Tradycyjna: restaurant.avgTraditionalRating },
                { name: 'Atmosfera', NLP: restaurant.nlpScores.atmosphereScore || restaurant.nlpScores.atmosphere, Tradycyjna: restaurant.avgTraditionalRating }
              ]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 5]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="NLP" fill="#8b5cf6" />
              <Bar dataKey="Tradycyjna" fill="#eab308" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

     {currentUser && (
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Plus size={20} />
            Dodaj Recenzję
          </h3>

          {errorMessage && (
            <div className="mb-4 text-red-600 bg-red-100 p-3 rounded-lg text-sm font-medium">
              {errorMessage}
            </div>
          )}
          {submitSuccess && (
            <div className="mb-4 text-green-600 bg-green-100 p-3 rounded-lg text-sm font-medium">
              {submitSuccess}
            </div>
          )}

          <form onSubmit={handleSubmitReview} className="space-y-4">
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Twoja opinia</label>
              <textarea
                value={newReview.text}
                onChange={(e) => setNewReview({ ...newReview, text: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                rows="4"
                placeholder="Opisz swoje doświadczenie..."
                required
                disabled={isSubmitting} 
              />
            </div>
            <div>
              <label className="block text-gray-700 font-semibold mb-2">
                Ocena: {newReview.starRating} <Star className="inline text-yellow-500 fill-yellow-500" size={16} />
              </label>
              <input
                type="range"
                min="1"
                max="5"
                step="1"
                value={newReview.starRating}
                onChange={(e) => setNewReview({ ...newReview, starRating: parseInt(e.target.value) })}
                className="w-full accent-indigo-600" // Dodajemy kolor suwaka
                disabled={isSubmitting} // Wyłącz podczas wysyłania
              />
            </div>
            <button
              type="submit"
              disabled={isSubmitting || !newReview.text} // Wyłącz, jeśli pole tekstowe jest puste
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? "Wysyłanie..." : "Wyślij Recenzję"}
            </button>
          </form>
        </div>
      )}

      <div className="bg-white p-6 rounded-xl shadow-md">
        <h3 className="text-lg font-bold text-gray-800 mb-4">
          Recenzje ({reviews.length})
        </h3>
        {reviews.length > 0 ? (
          <div className="space-y-4">
            {reviews.map((review) => (
              <div key={review.id} className="border-b border-gray-200 pb-4 last:border-0">
                <div className="flex justify-between items-start mb-2">
                  {/* Ocena gwiazdkowa */}
                  <div className="flex items-center gap-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        size={16}
                        className={i < review.starRating ? "text-yellow-500 fill-yellow-500" : "text-gray-300"}
                      />
                    ))}
                    <span className="font-semibold ml-2">{review.starRating}/5</span>
                  </div>
                  {/* Data dodania */}
                  <span className="text-sm text-gray-500">
                    {new Date(review.createdAt).toLocaleDateString('pl-PL', { year: 'numeric', month: 'long', day: 'numeric' })}
                  </span>
                </div>
                {/* Tekst recenzji */}
                <p className="text-gray-700 mb-3">{review.text}</p>
                {/* Oceny NLP (jeśli istnieją) */}
                {review.nlpScores && (
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                    <div className="bg-green-50 p-2 rounded text-center">
                      <p className="text-gray-600">Jedzenie</p>
                      <p className="font-bold text-green-700">{review.nlpScores.foodScore?.toFixed(1) ?? 'N/A'}</p>
                    </div>
                    <div className="bg-blue-50 p-2 rounded text-center">
                      <p className="text-gray-600">Cena</p>
                      <p className="font-bold text-blue-700">{review.nlpScores.priceScore?.toFixed(1) ?? 'N/A'}</p>
                    </div>
                    <div className="bg-purple-50 p-2 rounded text-center">
                      <p className="text-gray-600">Obsługa</p>
                      <p className="font-bold text-purple-700">{review.nlpScores.serviceScore?.toFixed(1) ?? 'N/A'}</p>
                    </div>
                    <div className="bg-yellow-50 p-2 rounded text-center">
                      <p className="text-gray-600">Atmosfera</p>
                      <p className="font-bold text-yellow-700">{review.nlpScores.atmosphereScore?.toFixed(1) ?? 'N/A'}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          // Komunikat, jeśli nie ma recenzji
          <p className="text-gray-500">Brak recenzji dla tej restauracji.</p>
        )}
      </div>
    </div>
  );
};

export default RestaurantDetails;