package com.inzynierka.filip.kazmierczak.restaurant_review.controller;

import com.inzynierka.filip.kazmierczak.restaurant_review.service.RankingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/rankings")
public class RankingController {

    private final RankingService rankingService;

    @Autowired
    public RankingController(RankingService rankingService) {
        this.rankingService = rankingService;
    }

    /**
     * Pobiera TOP N restauracji dla danego typu rankingu.
     * Dostępny publicznie (zakładając, że WebSecurityConfig pozwala na GET /api/**).
     *
     * @param type Typ rankingu ("traditional" lub "nlp").
     * @param limit Liczba restauracji do pobrania (domyślnie 10).
     * @return Mapa <ID_Restauracji, Wynik> posortowana malejąco.
     */
    @GetMapping("/top/{type}")
    public ResponseEntity<Map<String, Double>> getTopRanked(
            @PathVariable String type,
            @RequestParam(defaultValue = "10") int limit) {

        Map<String, Double> topRanked = rankingService.getTopRankedRestaurants(type, limit);
        return ResponseEntity.ok(topRanked);
    }
}