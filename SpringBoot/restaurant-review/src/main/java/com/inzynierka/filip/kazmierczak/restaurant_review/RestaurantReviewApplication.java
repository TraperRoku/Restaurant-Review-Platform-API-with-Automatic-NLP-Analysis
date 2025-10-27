package com.inzynierka.filip.kazmierczak.restaurant_review;

import com.inzynierka.filip.kazmierczak.restaurant_review.service.OverpassService;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@SpringBootApplication
public class RestaurantReviewApplication {

    @Autowired
    private OverpassService overpassService; // Wstrzyknij serwis

    public static void main(String[] args) {
        SpringApplication.run(RestaurantReviewApplication.class, args);
    }

    // Metoda uruchamiana raz po starcie aplikacji
    @PostConstruct
    public void init() {
        // Pobierz i zapisz restauracje dla Goleniowa
       // overpassService.fetchAndSaveRestaurants("Goleniów")
         //       .subscribe(); // Uruchom asynchroniczne zadanie

        // Możesz dodać inne miasta
        // overpassService.fetchAndSaveRestaurants("Szczecin").subscribe();
    }
}