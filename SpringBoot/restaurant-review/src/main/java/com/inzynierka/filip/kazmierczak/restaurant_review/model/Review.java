package com.inzynierka.filip.kazmierczak.restaurant_review.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "reviews")
public class Review {

    @Id
    private String id;

    @NotBlank
    @Indexed
    private String restaurantId;

    @NotBlank
    @Indexed
    private String userId;

    @NotBlank
    private String text;

    @Min(1)
    @Max(5)
    private int starRating;

    private NlpScores nlpScores;

    private LocalDateTime createdAt;
}