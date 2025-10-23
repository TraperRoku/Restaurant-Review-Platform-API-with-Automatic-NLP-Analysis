package com.inzynierka.filip.kazmierczak.restaurant_review;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@SpringBootApplication
@EnableMongoRepositories(basePackages = "com.inzynierka.filip.kazmierczak.restaurant_review.repository")
public class RestaurantReviewApplication {

	public static void main(String[] args) {
		SpringApplication.run(RestaurantReviewApplication.class, args);
	}

}
