package main

import (
	"encoding/json"
	"fmt"
	"log"

	"content-processor/model"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "content-processor-test",
		"auto.offset.reset": "earliest",
	})

	if err != nil {
		panic(err)
	}

	c.SubscribeTopics([]string{"news.article"}, nil)

	fmt.Println("Kafka consumer started...")

	for {
		msg, err := c.ReadMessage(-1)
		if err != nil {
			log.Printf("Consumer error: %v\n", err)
			continue
		}

		var event model.ExternalNews
		err = json.Unmarshal(msg.Value, &event)
		if err != nil {
			log.Printf("JSON parse error: %v\n", err)
			continue
		}

		fmt.Printf("✅ Received event: %+v\n", event)
	}
}