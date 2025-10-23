package com.inzynierka.filip.kazmierczak.restaurant_review.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Value("${nlp.api.baseurl}")
    private String nlpApiBaseUrl;

    @Bean
    public WebClient nlpWebClient() {
        return WebClient.builder()
                .baseUrl(nlpApiBaseUrl)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
}