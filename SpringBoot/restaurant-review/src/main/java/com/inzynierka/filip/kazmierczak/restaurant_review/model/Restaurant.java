package com.inzynierka.filip.kazmierczak.restaurant_review.model;

import jakarta.validation.constraints.NotBlank;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.geo.GeoJsonPoint;

import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.data.mongodb.core.mapping.FieldType;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "restaurants")
public class Restaurant {

    @Id
    @Field(targetType = FieldType.STRING)
    private String id;

    @Indexed(unique = true)

    private String externalApiId;

    @NotBlank
    private String name;

    private GeoJsonPoint location;

    private double avgStars;

    private NlpScores avgNlpScores;

    private long reviewCount;
}