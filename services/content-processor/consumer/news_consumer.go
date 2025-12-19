package consumer

import (
	"encoding/json"
	"log"

	"content-processor/model"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

type NewsConsumer struct {
	consumer *kafka.Consumer
}

func NewNewsConsumer() (*NewsConsumer, error) {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "content-processor",
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		return nil, err
	}

	c.SubscribeTopics([]string{"news.article"}, nil)

	return &NewsConsumer{
		consumer: c,
	}, nil
}

func (n *NewsConsumer) Start() {
	log.Println("Kafka consumer started...")

	for {
		msg, err := n.consumer.ReadMessage(-1)
		if err != nil {
			log.Printf("Consumer error: %v\n", err)
			continue
		}

		var event model.ExternalNews
		if err := json.Unmarshal(msg.Value, &event); err != nil {
			log.Printf("JSON parse error: %v\n", err)
			continue
		}

		log.Printf("✅ Received event: %+v\n", event)
	}
}
