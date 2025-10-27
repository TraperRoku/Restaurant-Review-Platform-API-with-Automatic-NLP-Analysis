package com.inzynierka.filip.kazmierczak.restaurant_review.controller;

import com.inzynierka.filip.kazmierczak.restaurant_review.dto.ReviewCreateRequest;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Review;
import com.inzynierka.filip.kazmierczak.restaurant_review.repository.ReviewRepository;
import com.inzynierka.filip.kazmierczak.restaurant_review.service.ReviewService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/restaurants") // Bazowy URL dla tego kontrolera
public class ReviewController {

    private final ReviewService reviewService;
    private final ReviewRepository reviewRepository;

    public ReviewController(ReviewService reviewService, ReviewRepository reviewRepository) {
        this.reviewService = reviewService;
        this.reviewRepository = reviewRepository;
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

        Review createdReview = reviewService.createReview(restaurantId, request);

        return new ResponseEntity<>(createdReview, HttpStatus.CREATED);
    }
    @GetMapping("/{restaurantId}/reviews")
    public ResponseEntity<List<Review>> getAllReviews(@PathVariable String restaurantId) {
        List<Review> byRestaurantId = reviewRepository.findByRestaurantId(restaurantId);
        return new ResponseEntity<>(byRestaurantId, HttpStatus.OK);
    }
}