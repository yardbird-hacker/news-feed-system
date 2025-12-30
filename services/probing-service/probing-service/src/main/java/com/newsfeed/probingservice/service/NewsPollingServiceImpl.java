package com.newsfeed.probingservice.service;

import com.github.benmanes.caffeine.cache.Cache;
import com.newsfeed.probingservice.client.NewsSourceClient;
import com.newsfeed.probingservice.model.ExternalNewsDto;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;

@Service
class NewsPollingServiceImpl implements NewsPollingService {

    //private final NewsSourceClient newsSourceClient;
    private final Map<String, NewsSourceClient> clients;
    private final Cache<Integer, Boolean> dedupCache;
    private final KafkaTemplate<String, ExternalNewsDto> kafkaTemplate;
    private final ExecutorService executorService;

    //@Value("${news.topic.name:news.events}")
    private String topic = "news.article";

    NewsPollingServiceImpl (Map<String, NewsSourceClient> clients,
                            Cache<Integer, Boolean> cache,
                            KafkaTemplate<String, ExternalNewsDto> kafkaTemplate,
                            ExecutorService executorService) {
        this.clients = clients;
        this.dedupCache = cache;
        this.kafkaTemplate = kafkaTemplate;
        this.executorService = executorService;
    }

    public void poll(String source) {

        System.out.println(clients.size());

        executorService.submit(() -> {
            try {
                System.out.println(
                        "Polling started on thread: " +
                                Thread.currentThread().getName() + " : " + source
                );

                NewsSourceClient newsSourceClient = clients.get(source);

                Thread.sleep(2_000);

                if (newsSourceClient == null)
                    throw new RuntimeException("Not supported news service [" + source + "].");

                List<ExternalNewsDto> externalNews =
                        newsSourceClient.fetchNews();

                externalNews.stream()
                        .forEach(event ->
                                kafkaTemplate.send(
                                        topic,
                                        event.id().toString(),
                                        event
                                )
                        );

                System.out.println(
                        "Finished thread: " +
                                Thread.currentThread().getName()
                        + " : " + source
                );
            } catch (Exception e) {
                System.err.println("Polling failed");
                e.printStackTrace();
            }
        });
    }

    private Boolean isNew(ExternalNewsDto dto) {
        return dedupCache.asMap().putIfAbsent(dto.id(), Boolean.TRUE) == null;
    }

    private void process(ExternalNewsDto news) {
        System.out.println("NEW NEWS: " + news.headline());
    }
}