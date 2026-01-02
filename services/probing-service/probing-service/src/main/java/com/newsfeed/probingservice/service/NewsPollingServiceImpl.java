package com.newsfeed.probingservice.service;

import com.github.benmanes.caffeine.cache.Cache;
import com.newsfeed.probingservice.client.NewsSourceClient;
import com.newsfeed.probingservice.model.ExternalNewsDto;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

@Service
class NewsPollingServiceImpl implements NewsPollingService {

    //private final NewsSourceClient newsSourceClient;
    private final Map<String, NewsSourceClient> clients;
    private final Cache<Integer, Boolean> dedupCache;
    private final KafkaTemplate<String, ExternalNewsDto> kafkaTemplate;
    private final ExecutorService executorService;

    private final Map<String, AtomicBoolean> running;

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

        this.running = new ConcurrentHashMap<>();
    }

    public void poll(String source) {

        if (!running
                .computeIfAbsent(source, x -> new AtomicBoolean(false))
                .compareAndSet(false, true)) {
            System.out.println("Polling already running for " + source);
            return;
        }

        CompletableFuture
                .supplyAsync(() -> {
                    System.out.println(
                            "Polling started on thread: " +
                                    Thread.currentThread().getName() + " : " + source
                    );

                    NewsSourceClient newsSourceClient = clients.get(source);
                    if (newsSourceClient == null) {
                        throw new RuntimeException(
                                "Not supported news service [" + source + "]"
                        );
                    }
                    return newsSourceClient;
                }, executorService)
                .thenCompose(sourceClient ->
                        CompletableFuture
                                .supplyAsync(sourceClient::fetchNews, executorService)
                                .orTimeout(5, TimeUnit.SECONDS)
                )
                .thenApplyAsync(
                        news -> news,
                        CompletableFuture.delayedExecutor(2, TimeUnit.SECONDS)
                )
                .thenCompose(newsList -> {
                    if (newsList.isEmpty()) {
                        return CompletableFuture.completedFuture(null);
                    }

                    List<CompletableFuture<Void>> sendFutures =
                            newsList.stream()
                                    .map(event ->
                                            kafkaTemplate
                                                    .send(topic, event.id().toString(), event)
                                                    .thenAccept(result -> {
                                                        ;
                                                    })
                                    )
                                    .toList();

                    return CompletableFuture
                            .allOf(sendFutures.toArray(CompletableFuture[]::new))
                            .orTimeout(5, TimeUnit.SECONDS);
                })
                .exceptionally(ex -> {
                    System.err.println(
                            "Polling failed for " + source + " : " + ex.getMessage()
                    );
                    return null;
                })
                .whenComplete((r, ex) -> {
                    running.get(source).set(false);

                    System.out.println(
                            "Polling finished on thread: " +
                                    Thread.currentThread().getName() + " : " + source
                    );
                });

        return;
    }

    private Boolean isNew(ExternalNewsDto dto) {
        return dedupCache.asMap().putIfAbsent(dto.id(), Boolean.TRUE) == null;
    }

    private void process(ExternalNewsDto news) {
        System.out.println("NEW NEWS: " + news.headline());
    }
}