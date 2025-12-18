package com.newsfeed.probingservice.scheduler;

import com.newsfeed.probingservice.service.NewsPollingService;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class NewsPollingScheduler {
    private final NewsPollingService newsPollingService;

    NewsPollingScheduler(NewsPollingService service) {
        this.newsPollingService = service;
    }

    @Scheduled(fixedDelay = 10_000)
    public void run() {
        newsPollingService.poll();
    }
}