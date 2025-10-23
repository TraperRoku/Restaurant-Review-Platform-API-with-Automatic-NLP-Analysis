/*
package com.inzynierka.filip.kazmierczak.restaurant_review.service;

import com.inzynierka.filip.kazmierczak.restaurant_review.model.NlpScores;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ZSetOperations;
import org.springframework.stereotype.Service;

@Service
public class RankingService {

    // Definiujemy klucze dla naszych posortowanych zbiorów w Redis
    private static final String RANKING_STARS = "ranking:stars";
    private static final String RANKING_NLP_FOOD = "ranking:nlp:food";
    private static final String RANKING_NLP_PRICE = "ranking:nlp:price";
    private static final String RANKING_NLP_SERVICE = "ranking:nlp:service";
    private static final String RANKING_NLP_ATMOSPHERE = "ranking:nlp:atmosphere";

    private final ZSetOperations<String, String> zSetOps;

    // Wstrzykujemy RedisTemplate i od razu pobieramy z niego operacje na ZSet
    public RankingService(RedisTemplate<String, String> redisTemplate) {
        this.zSetOps = redisTemplate.opsForZSet();
    }

    */
/**
     * Aktualizuje pozycję restauracji we wszystkich rankingach w Redis.
     * Używa ID restauracji jako 'value' i średniej oceny jako 'score'.
     *//*

    public void updateRankings(Restaurant restaurant) {
        String restaurantId = restaurant.getId();
        NlpScores nlpScores = restaurant.getAvgNlpScores();

        // Aktualizuj ranking gwiazdkowy
        zSetOps.add(RANKING_STARS, restaurantId, restaurant.getAvgStars());

        if (nlpScores != null) {
            zSetOps.add(RANKING_NLP_FOOD, restaurantId, nlpScores.getFoodScore());
            zSetOps.add(RANKING_NLP_PRICE, restaurantId, nlpScores.getPriceScore());
            // POPRAWKA:
            zSetOps.add(RANKING_NLP_SERVICE, restaurantId, nlpScores.getServiceScore()); // <-- Poprawione
            zSetOps.add(RANKING_NLP_ATMOSPHERE, restaurantId, nlpScores.getAtmosphereScore());
        }
    }
}*/
