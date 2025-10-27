package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class OverpassResponse {
    private List<OverpassElement> elements;
}