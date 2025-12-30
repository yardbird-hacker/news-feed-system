package com.newsfeed.probingservice.client;


import com.newsfeed.probingservice.model.ExternalNewsDto;
import com.newsfeed.probingservice.model.FinnhubResponseDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;


public class FinnHubClientImpl implements NewsSourceClient {
    private final WebClient webClient;
    private final String apiKey;

    public FinnHubClientImpl(
            WebClient.Builder  webClientBuilder,
            @Value("${finnhub.api.key}") String key
    ) {
        this.webClient = webClientBuilder
                .baseUrl("https://finnhub.io/api/v1")
                .build();
        this.apiKey = key;
    }

    @Override
    public List<ExternalNewsDto> fetchNews() {

        List<FinnhubResponseDto> response = webClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/news")
                        .queryParam("category", "general")
                        .queryParam("token", apiKey)
                        .build())
                .retrieve()
                .bodyToFlux(FinnhubResponseDto.class)
                .timeout(Duration.ofSeconds(5))
                .collectList()
                .block();


        if (response == null) return List.of();

        return response.stream()
                .map(r -> new ExternalNewsDto(
                        r.id(),
                        r.category(),
                        Instant.ofEpochSecond(r.datetime()),
                        r.headline(),
                        r.related(),
                        r.source(),
                        r.summary(),
                        r.url()
                ))
                .toList();
    }
}