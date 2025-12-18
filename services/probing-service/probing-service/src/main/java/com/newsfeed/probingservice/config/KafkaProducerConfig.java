package com.newsfeed.probingservice.config;


import com.newsfeed.probingservice.model.ExternalNewsDto;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, ExternalNewsDto> producerFactory(
            KafkaProperties properties
    ) {
        Map<String, Object> props = new HashMap<>(properties.buildProducerProperties());

        return new DefaultKafkaProducerFactory<>(props);
    }

    @Bean
    public KafkaTemplate<String, ExternalNewsDto> kafkaTemplate(
            ProducerFactory<String, ExternalNewsDto> producerFactory
    ) {
        return new KafkaTemplate<>(producerFactory);
    }
}