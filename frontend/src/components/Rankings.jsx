import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import restaurantService from '../services/restaurant.service';
import { Award, TrendingUp, Star } from 'lucide-react'; 

const Rankings = () => {
  const [traditionalRanking, setTraditionalRanking] = useState([]);
  const [nlpRanking, setNlpRanking] = useState([]);
  const [restaurantDetails, setRestaurantDetails] = useState({}); 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRankingsAndDetails = async () => {
      setLoading(true);
      setError('');
      try {

        const [tradData, nlpData, allRestaurants] = await Promise.all([
          restaurantService.getTopRankings('traditional', 10), 
          restaurantService.getTopRankings('nlp', 10),       
          restaurantService.getAllRestaurants(),             
        ]);

        const detailsMap = allRestaurants.reduce((map, restaurant) => {
          map[restaurant.id] = { name: restaurant.name, address: restaurant.address };
          return map;
        }, {});
        setRestaurantDetails(detailsMap);

        const formatRanking = (rankingData) => {
          return Object.entries(rankingData).map(([id, score], index) => ({
            id,
            score,
            rank: index + 1, 
          }));
        };

        setTraditionalRanking(formatRanking(tradData));
        setNlpRanking(formatRanking(nlpData));

      } catch (err) {
        console.error("Błąd ładowania rankingów:", err);
        setError("Nie udało się załadować rankingów.");
      } finally {
        setLoading(false);
      }
    };

    fetchRankingsAndDetails();
  }, []); 


  const RankingList = ({ title, ranking, icon: Icon, colorClass }) => (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className={`text-xl font-bold text-gray-800 mb-4 flex items-center gap-2 ${colorClass}`}>
        <Icon size={24} /> {title} (TOP 10)
      </h2>
      {ranking.length > 0 ? (
        <ol className="list-decimal list-inside space-y-3">
          {ranking.map((item) => (
            <li key={item.id} className="border-b border-gray-100 pb-2 last:border-0">
              <Link
                to={`/restaurants/${item.id}`}
                className="hover:text-indigo-600 transition-colors"
              >
                <span className="font-semibold text-lg mr-2">{item.rank}.</span>
                <span className="font-medium">{restaurantDetails[item.id]?.name || `Restauracja ID: ${item.id}`}</span>
              </Link>
              <span className={`float-right font-bold text-lg ${colorClass}`}>
                {item.score?.toFixed(2)} 
              </span>
         
               <p className="text-xs text-gray-500 ml-6">{restaurantDetails[item.id]?.address || ''}</p>
            </li>
          ))}
        </ol>
      ) : (
        <p className="text-gray-500">Brak danych w rankingu.</p>
      )}
    </div>
  );


  if (loading) return <div className="text-center p-10">Ładowanie rankingów...</div>;
  if (error) return <div className="text-center p-10 text-red-600">{error}</div>;

  return (
    <div className="space-y-6">
       <h1 className="text-3xl font-bold text-gray-800 mb-6">Rankingi Restauracji</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
   
        <RankingList
          title="Ranking Tradycyjny"
          ranking={traditionalRanking}
          icon={Star}
          colorClass="text-yellow-600" 
        />

         <RankingList
          title="Ranking NLP"
          ranking={nlpRanking}
          icon={TrendingUp}
          colorClass="text-purple-600" 
        />
      </div>
    </div>
  );
};

export default Rankings;