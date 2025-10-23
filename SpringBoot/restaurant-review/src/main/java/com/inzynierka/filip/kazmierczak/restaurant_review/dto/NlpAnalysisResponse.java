package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.Map;

/**
 * DTO reprezentujący odpowiedź z endpointu /analyze.
 * Mapuje pola JSON z Pythona (np. "food_score") na pola Javy.
 */
@Data
@NoArgsConstructor
public class NlpAnalysisResponse {

    @JsonProperty("food_score")
    private int foodScore;

    @JsonProperty("price_score")
    private int priceScore;

    @JsonProperty("service_score")
    private int serviceScore;

    @JsonProperty("atmosphere_score")
    private int atmosphereScore;

    @JsonProperty("overall_sentiment_label")
    private String overallSentimentLabel;

    @JsonProperty("confidence_scores")
    private Map<String, Double> confidenceScores;

    @JsonProperty("model_type")
    private String modelType;
}