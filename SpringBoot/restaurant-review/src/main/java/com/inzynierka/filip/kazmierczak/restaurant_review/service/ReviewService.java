package com.inzynierka.filip.kazmierczak.restaurant_review.service;

import com.inzynierka.filip.kazmierczak.restaurant_review.dto.ReviewCreateRequest;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.NlpScores;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Review;
import com.inzynierka.filip.kazmierczak.restaurant_review.repository.RestaurantRepository;
import com.inzynierka.filip.kazmierczak.restaurant_review.repository.ReviewRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ReviewService {

    private static final Logger logger = LoggerFactory.getLogger(ReviewService.class);

    private final ReviewRepository reviewRepository;
    private final RestaurantRepository restaurantRepository;
    private final NlpService nlpService;
  //  private final RankingService rankingService;

    // Wstrzykujemy wszystkie 4 zależności
    public ReviewService(ReviewRepository reviewRepository,
                         RestaurantRepository restaurantRepository,
                         NlpService nlpService
                         //RankingService rankingService
                         ) {
        this.reviewRepository = reviewRepository;
        this.restaurantRepository = restaurantRepository;
        this.nlpService = nlpService;
      //  this.rankingService = rankingService;
    }

    /**
     * Główna metoda biznesowa: tworzy recenzję, analizuje ją
     * i aktualizuje średnie oceny restauracji.
     */
    public Review createReview(String restaurantId, ReviewCreateRequest request) {


        logger.info("==================== DEBUG START ====================");
        logger.info("Próba dodania recenzji dla restaurantId: '{}'", restaurantId);

        List<Restaurant> allRestaurants = restaurantRepository.findAll();

        if (allRestaurants.isEmpty()) {
            logger.warn("!!! BAZA DANYCH (kolekcja 'restaurants') JEST PUSTA !!!");
        } else {
            logger.info("Znaleziono {} restauracji w bazie:", allRestaurants.size());
            for (Restaurant r : allRestaurants) {
                // Logujemy ID i nazwę każdej restauracji
                logger.info(" -> ID: '{}', Nazwa: '{}'", r.getId(), r.getName());

                // Sprawdzamy, czy ID się zgadza (i dlaczego)
                if (r.getId().equals(restaurantId)) {
                    logger.info("    ^ DOBRE ID! ZNALEZIONO DOPASOWANIE!");
                } else {
                    logger.warn("    ^ ZŁE ID! Stringi nie są równe.");
                }
            }
        }
        logger.info("==================== DEBUG KONIEC ====================");
        // ==================================================================

        // 1. Sprawdź, czy restauracja istnieje
        // (Jeśli nie, rzuci wyjątek, co jest dobrym zachowaniem)
        Restaurant restaurant = restaurantRepository.findById(restaurantId)
                .orElseThrow(() -> new RuntimeException("Restauracja nie znaleziona: " + restaurantId));

        // 2. Wywołaj serwis NLP (Pythona), aby przeanalizować tekst
        logger.info("Rozpoczynam analizę NLP dla recenzji restauracji: {}", restaurantId);
        NlpScores scores = nlpService.analyzeReview(request.getText());
        logger.info("Analiza NLP zakończona.");

        // 3. Stwórz i zapisz nową recenzję w MongoDB
        Review newReview = Review.builder()
                .restaurantId(restaurantId)
                .userId(request.getUserId()) // Tymczasowo z DTO
                .text(request.getText())
                .starRating(request.getStarRating())
                .nlpScores(scores) // Zapisz wyniki z NLP
                .createdAt(LocalDateTime.now())
                .build();

        reviewRepository.save(newReview);
        logger.info("Nowa recenzja zapisana w MongoDB: {}", newReview.getId());

        // 4. Zaktualizuj średnie oceny dla restauracji
        updateRestaurantAverages(restaurant);

        // 5. Zwróć nowo utworzoną recenzję
        return newReview;
    }

    /**
     * Przelicza i zapisuje nowe średnie oceny dla danej restauracji.
     */
    private void updateRestaurantAverages(Restaurant restaurant) {
        // Pobierz WSZYSTKIE recenzje dla tej restauracji
        List<Review> reviews = reviewRepository.findByRestaurantId(restaurant.getId());

        if (reviews.isEmpty()) {
            return; // Nic do roboty
        }

        int count = reviews.size();

        // Oblicz średnią gwiazdkową
        double avgStars = reviews.stream()
                .mapToDouble(Review::getStarRating)
                .average()
                .orElse(0.0);

        // Oblicz średnie oceny NLP
        double avgFood = reviews.stream().mapToDouble(r -> r.getNlpScores().getFoodScore()).average().orElse(0.0);
        double avgPrice = reviews.stream().mapToDouble(r -> r.getNlpScores().getPriceScore()).average().orElse(0.0);
        double avgService = reviews.stream().mapToDouble(r -> r.getNlpScores().getServiceScore()).average().orElse(0.0);
        double avgAtmosphere = reviews.stream().mapToDouble(r -> r.getNlpScores().getAtmosphereScore()).average().orElse(0.0);

        NlpScores newNlpScores = new NlpScores(avgFood, avgPrice, avgService, avgAtmosphere);

        // 5. Zaktualizuj i zapisz restaurację w MongoDB
        restaurant.setAvgStars(avgStars);
        restaurant.setAvgNlpScores(newNlpScores);
        restaurant.setReviewCount(count);
        restaurantRepository.save(restaurant);
        logger.info("Zaktualizowano średnie oceny dla restauracji: {}", restaurant.getId());

        // 6. Zaktualizuj rankingi w Redis
       // rankingService.updateRankings(restaurant);
        logger.info("Zaktualizowano rankingi w Redis dla restauracji: {}", restaurant.getId());
    }
}