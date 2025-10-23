package com.inzynierka.filip.kazmierczak.restaurant_review.repository;

import com.inzynierka.filip.kazmierczak.restaurant_review.model.Review;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface ReviewRepository extends MongoRepository<Review, String> {


    List<Review> findByRestaurantId(String restaurantId);


    List<Review> findByUserId(String userId);
}