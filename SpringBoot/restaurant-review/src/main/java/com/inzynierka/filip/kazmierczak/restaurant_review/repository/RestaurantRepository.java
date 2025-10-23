package com.inzynierka.filip.kazmierczak.restaurant_review.repository;

import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface RestaurantRepository extends MongoRepository<Restaurant,String> {
    Optional<Restaurant> findByExternalApiId(String externalApiId);
}
