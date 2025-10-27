package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class OverpassElement {
    private String type;
    private long id;
    private Double lat;
    private Double lon;
    private Map<String, String> tags;
    private OverpassCenter center;
}

