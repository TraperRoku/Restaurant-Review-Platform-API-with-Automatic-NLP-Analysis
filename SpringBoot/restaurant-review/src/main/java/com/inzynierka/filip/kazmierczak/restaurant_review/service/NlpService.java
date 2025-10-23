package com.inzynierka.filip.kazmierczak.restaurant_review.service;

import com.inzynierka.filip.kazmierczak.restaurant_review.dto.NlpAnalysisResponse;
import com.inzynierka.filip.kazmierczak.restaurant_review.dto.NlpRequest;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.NlpScores;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * Serwis odpowiedzialny za komunikację z zewnętrznym API NLP (w Pythonie).
 */
@Service
public class NlpService {

    private static final Logger logger = LoggerFactory.getLogger(NlpService.class);

    private final WebClient nlpWebClient;

    public NlpService(WebClient nlpWebClient) {
        this.nlpWebClient = nlpWebClient;
    }

    public NlpScores analyzeReview(String text) {
        logger.info("Wysyłanie recenzji do analizy NLP...");

        NlpRequest request = new NlpRequest(text);

        try {
            NlpAnalysisResponse response = nlpWebClient.post()
                    .uri("/analyze")
                    .body(BodyInserters.fromValue(request))
                    .retrieve()
                    .bodyToMono(NlpAnalysisResponse.class)
                    .block();

            if (response != null) {
                logger.info("Otrzymano analizę NLP: Jedzenie={}, Cena={}", response.getFoodScore(), response.getPriceScore());

                return NlpScores.builder()
                        .foodScore((double) response.getFoodScore())
                        .priceScore((double) response.getPriceScore())
                        .serviceScore((double) response.getServiceScore())
                        .atmosphereScore((double) response.getAtmosphereScore())
                        .build();
            } else {
                logger.warn("Otrzymano pustą odpowiedź z serwera NLP.");
                return createFallbackScores();
            }

        } catch (Exception e) {

            logger.error("Błąd podczas łączenia z API NLP: {}", e.getMessage());

            return createFallbackScores();
        }
    }

    /**
     * Tworzy domyślne, neutralne oceny w przypadku błędu API NLP.
     */
    private NlpScores createFallbackScores() {
        return NlpScores.builder()
                .foodScore(3.0)
                .priceScore(3.0)
                .atmosphereScore(3.0)
                .serviceScore(3.0)
                .build();
    }
}