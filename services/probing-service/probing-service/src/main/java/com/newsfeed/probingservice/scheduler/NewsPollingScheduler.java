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

    @Scheduled(fixedDelay = 1_000)
    public void run() {
        newsPollingService.poll("finnhub");
    }

    @Scheduled(fixedDelay = 2_000)
    public void runWith2Min() {
        newsPollingService.poll("finnhub1");
    }

    @Scheduled(fixedDelay = 3_000)
    public void runWith3Min() {
        newsPollingService.poll("finnhub2");
    }
}