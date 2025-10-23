package com.inzynierka.filip.kazmierczak.restaurant_review.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ReviewCreateRequest {

    @NotBlank(message = "Tekst recenzji nie może być pusty")
    private String text;

    @Min(value = 1, message = "Ocena musi być między 1 a 5")
    @Max(value = 5, message = "Ocena musi być między 1 a 5")
    private int starRating;

    // UWAGA: Na razie dodajemy tu userId dla testów.
    // Docelowo, w Etapie 4, będziemy to pole pobierać automatycznie
    // z zalogowanego użytkownika (z tokenu JWT).
    @NotBlank(message = "UserId jest tymczasowo wymagany do testów")
    private String userId;
}