package com.newsfeed.probingservice.config;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import jakarta.annotation.PostConstruct;
import org.springframework.boot.autoconfigure.cache.CacheProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

@Configuration
public class CacheConfig {
    @Bean(name = "newsDedupCache")
    public Cache<Integer, Boolean> newsDedupCache() {
        return Caffeine.newBuilder()
                .expireAfterAccess(Duration.ofHours(1))
                .maximumSize(1000)
                .build();

    }

    @PostConstruct
    public void check() {
        System.out.println("✅ CacheConfig loaded");
    }
}