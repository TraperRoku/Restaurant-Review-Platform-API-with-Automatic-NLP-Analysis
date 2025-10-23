package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class NlpRequest {

    private String text;
}