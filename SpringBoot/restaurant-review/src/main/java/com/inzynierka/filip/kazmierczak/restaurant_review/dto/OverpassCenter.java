package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class OverpassCenter {
    private Double lat;
    private Double lon;
}