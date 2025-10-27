
package com.inzynierka.filip.kazmierczak.restaurant_review.service;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.NlpScores;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ZSetOperations;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.LinkedHashMap; // Aby zachować kolejność
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Service
public class RankingService {

    private static final Logger logger = LoggerFactory.getLogger(RankingService.class);


    private static final String RANKING_KEY_TRADITIONAL = "ranking:traditional";
    private static final String RANKING_KEY_NLP = "ranking:nlp";

    private final RedisTemplate<String, Object> redisTemplate;

    @Autowired
    public RankingService(RedisTemplate<String, Object> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }


public void updateRankings(Restaurant restaurant) {
    if (restaurant == null || restaurant.getId() == null) {
        logger.warn("Próba aktualizacji rankingu dla nieprawidłowej restauracji.");
        return;
    }

    String restaurantId = restaurant.getId();

    double traditionalScore = restaurant.getAvgStars();

    redisTemplate.opsForZSet().add(RANKING_KEY_TRADITIONAL, restaurantId, traditionalScore);
    logger.debug("Zaktualizowano ranking tradycyjny dla {}: {}", restaurantId, traditionalScore);


    NlpScores nlpScores = restaurant.getAvgNlpScores();
    double nlpScore = 0.0;
    if (nlpScores != null) {

        nlpScore = (nlpScores.getFoodScore() + nlpScores.getPriceScore() +
                nlpScores.getServiceScore() + nlpScores.getAtmosphereScore()) / 4.0;
    }

    redisTemplate.opsForZSet().add(RANKING_KEY_NLP, restaurantId, nlpScore);
    logger.debug("Zaktualizowano ranking NLP dla {}: {}", restaurantId, nlpScore);
}

/**
 * Pobiera TOP N restauracji z rankingu (tradycyjnego lub NLP).
 *
 * @param type Typ rankingu ("traditional" lub "nlp").
 * @param topN Liczba restauracji do pobrania (np. 10).
 * @return Mapa, gdzie kluczem jest ID restauracji, a wartością jej wynik w rankingu.
 * Mapa jest posortowana od najwyższego wyniku.
 */
public Map<String, Double> getTopRankedRestaurants(String type, int topN) {
    String key;
    if ("nlp".equalsIgnoreCase(type)) {
        key = RANKING_KEY_NLP;
    } else {
        key = RANKING_KEY_TRADITIONAL; // Domyślnie tradycyjny
    }

    // ZREVRANGE key 0 (topN - 1) WITHSCORES
    // Pobieramy ID restauracji (member) i ich wyniki (score)
    // reverseRangeWithScores zwraca od najwyższego do najniższego wyniku
    Set<ZSetOperations.TypedTuple<Object>> results = redisTemplate.opsForZSet()
            .reverseRangeWithScores(key, 0, topN - 1);

    if (results == null || results.isEmpty()) {
        return Collections.emptyMap(); // Zwróć pustą mapę, jeśli ranking jest pusty
    }

    // Konwertujemy wyniki na mapę <ID, Wynik> zachowującą kolejność
    return results.stream()
            .collect(Collectors.toMap(
                    tuple -> (String) tuple.getValue(), // ID restauracji
                    ZSetOperations.TypedTuple::getScore, // Wynik
                    (oldValue, newValue) -> oldValue, // W razie duplikatów (nie powinno być)
                    LinkedHashMap::new // Używamy LinkedHashMap, aby zachować kolejność
            ));
}

/**
 * Usuwa restaurację z rankingów (np. gdy restauracja jest usuwana).
 *
 * @param restaurantId ID restauracji do usunięcia.
 */
public void removeRestaurantFromRankings(String restaurantId) {
    if (restaurantId == null) return;
    // ZREM key member
    redisTemplate.opsForZSet().remove(RANKING_KEY_TRADITIONAL, restaurantId);
    redisTemplate.opsForZSet().remove(RANKING_KEY_NLP, restaurantId);
    logger.info("Usunięto restaurację {} z rankingów Redis.", restaurantId);
}
}