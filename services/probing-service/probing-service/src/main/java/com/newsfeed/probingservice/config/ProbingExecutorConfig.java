package com.newsfeed.probingservice.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

@Configuration
public class ProbingExecutorConfig {

    @Bean(destroyMethod = "shutdown")
    public ExecutorService probingExecutor() {
        return new ThreadPoolExecutor(
                5,
                5,
                0L,
                TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<>(50),
                new ThreadPoolExecutor.CallerRunsPolicy()
        );
    }
}
