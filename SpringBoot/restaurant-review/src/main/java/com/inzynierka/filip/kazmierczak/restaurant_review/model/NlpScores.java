package com.inzynierka.filip.kazmierczak.restaurant_review.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NlpScores {

    private double foodScore;
    private double priceScore;
    private double serviceScore;
    private double atmosphereScore;

}