package com.inzynierka.filip.kazmierczak.restaurant_review.controller;

import com.inzynierka.filip.kazmierczak.restaurant_review.dto.ReviewCreateRequest;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Review;
import com.inzynierka.filip.kazmierczak.restaurant_review.service.ReviewService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/restaurants") // Bazowy URL dla tego kontrolera
public class ReviewController {

    private final ReviewService reviewService;

    public ReviewController(ReviewService reviewService) {
        this.reviewService = reviewService;
    }

    /**
     * Endpoint do dodawania nowej recenzji dla konkretnej restauracji.
     *
     * @param restaurantId ID restauracji pobrane ze ścieżki URL.
     * @param request      Dane recenzji (text, starRating) z ciała JSON.
     * @return Zwraca nowo utworzoną recenzję ze statusem 201 (Created).
     */
    @PostMapping("/{restaurantId}/reviews")
    public ResponseEntity<Review> addReview(
            @PathVariable String restaurantId,
            @RequestBody ReviewCreateRequest request) {

        // Wywołaj nasz serwis, który robi całą magię
        Review createdReview = reviewService.createReview(restaurantId, request);

        // Zwróć odpowiedź 201 Created
        return new ResponseEntity<>(createdReview, HttpStatus.CREATED);
    }
}