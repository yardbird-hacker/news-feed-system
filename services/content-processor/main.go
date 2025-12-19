package main

import (
	"content-processor/config"
	"content-processor/consumer"
	"content-processor/producer"
	"log"
)

func main() {

	cfg := config.Load()

    processedProducer, err := producer.NewKafkaProcessedProducer(
        cfg.KafkaBrokers,
        cfg.KeywordTopic,
    )
    if err != nil {
        log.Fatal(err)
    }
	
    defer processedProducer.Close()

	newsConsumer, err := consumer.NewNewsConsumer(processedProducer)
	if err != nil {
		log.Fatal(err)
	}

	newsConsumer.Start()
}
