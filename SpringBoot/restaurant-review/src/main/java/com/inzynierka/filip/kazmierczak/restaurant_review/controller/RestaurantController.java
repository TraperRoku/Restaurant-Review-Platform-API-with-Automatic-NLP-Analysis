package com.inzynierka.filip.kazmierczak.restaurant_review.controller;

import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import com.inzynierka.filip.kazmierczak.restaurant_review.repository.RestaurantRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/restaurants")
public class RestaurantController {

    private final RestaurantRepository restaurantRepository;

    public RestaurantController(RestaurantRepository restaurantRepository) {
        this.restaurantRepository = restaurantRepository;
    }

    /**
     * Endpoint do pobierania listy wszystkich restauracji.
     * Dostępny publicznie (skonfigurowane w WebSecurityConfig).
     *
     * @return Lista wszystkich restauracji.
     */
    @GetMapping
    public ResponseEntity<List<Restaurant>> getAllRestaurants() {
        List<Restaurant> restaurants = restaurantRepository.findAll();
        return ResponseEntity.ok(restaurants);
    }


    @GetMapping("/{id}")
    public ResponseEntity<Restaurant> getRestaurantById(@PathVariable String id) {
        Optional<Restaurant> byId = restaurantRepository.findById(id);
        return ResponseEntity.ok(byId.get());
    }
}