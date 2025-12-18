package com.newsfeed.probingservice.service;

import com.github.benmanes.caffeine.cache.Cache;
import com.newsfeed.probingservice.client.NewsSourceClient;
import com.newsfeed.probingservice.model.ExternalNewsDto;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
class NewsPollingServiceImpl implements NewsPollingService {

    private final NewsSourceClient newsSourceClient;
    private final Cache<Integer, Boolean> dedupCache;
    private final KafkaTemplate<String, ExternalNewsDto> kafkaTemplate;
    //@Value("${news.topic.name:news.events}")
    private String topic = "news.article";



    NewsPollingServiceImpl (NewsSourceClient newsSourceClient,
                            Cache<Integer, Boolean> cache,
                            KafkaTemplate<String, ExternalNewsDto> kafkaTemplate) {
        this.newsSourceClient = newsSourceClient;
        this.dedupCache = cache;
        this.kafkaTemplate = kafkaTemplate;
    }

    public void poll() {
        System.out.println("Send event to Kafka!!");
        List<ExternalNewsDto> externalNews = newsSourceClient.fetchNews();

        externalNews.stream()
                .filter(this::isNew)
                .forEach(event -> kafkaTemplate.send(topic, event.id().toString(), event));

        return;
    }

    private Boolean isNew(ExternalNewsDto dto) {
        return dedupCache.asMap().putIfAbsent(dto.id(), Boolean.TRUE) == null;
    }

    private void process(ExternalNewsDto news) {
        System.out.println("NEW NEWS: " + news.headline());
    }
}