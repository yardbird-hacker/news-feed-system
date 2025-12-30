package com.newsfeed.probingservice.config;

import com.newsfeed.probingservice.client.FinnHubClientImpl;
import com.newsfeed.probingservice.client.NewsSourceClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class NewsSourceAliasConfig {


    @Bean("finnhub")
    public NewsSourceClient finnhub(
            WebClient.Builder builder,
            @Value("${finnhub.api.key}") String key
    ) {
        return new FinnHubClientImpl(builder, key);
    }

    @Bean("finnhub1")
    public NewsSourceClient finnhub1(
            WebClient.Builder builder,
            @Value("${finnhub.api.key}") String key
    ) {
        return new FinnHubClientImpl(builder, key);
    }

    @Bean("finnhub2")
    public NewsSourceClient finnhub2(
            WebClient.Builder builder,
            @Value("${finnhub.api.key}") String key
    ) {
        return new FinnHubClientImpl(builder, key);
    }
}
