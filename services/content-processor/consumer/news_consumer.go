package consumer

import (
	"content-processor/fetcher"
	"content-processor/model"
	"content-processor/processor"
	"content-processor/producer"
	"encoding/json"
	"log"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

type NewsConsumer struct {
	consumer *kafka.Consumer
	processedProducer producer.ProcessedProducer
}

func NewNewsConsumer(
    processedProducer producer.ProcessedProducer,
) (*NewsConsumer, error) {

    c, err := kafka.NewConsumer(&kafka.ConfigMap{
        "bootstrap.servers": "localhost:9092",
        "group.id":          "content-processor1",
        "auto.offset.reset": "earliest",
    })
    if err != nil {
        return nil, err
    }

    c.SubscribeTopics([]string{"news.article"}, nil)

    return &NewsConsumer{
        consumer:          c,
        processedProducer: processedProducer,
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

		bodyText, url_err := fetcher.Fetch(event.URL)
		if url_err != nil {
			log.Printf("Failed to fetch news from %s with %s\n", event.URL, url_err)
			bodyText = ""
		}
		keywords := processor.ProcessEvent(event, bodyText)
		//log.Printf("words=%v", words)
		//log.Println(event.ID, len(workeywordsds))

		log.Printf("✅ Received event: %+v\n", event)


		for _, kw := range keywords {
			publishedTime := int64(event.PublishAt)
			wordIndexEvent := model.KeywordIndexEvent{
				Keyword:     kw,
				NewsID:      event.ID,
				URL:         event.URL,
				PublishedAt: publishedTime,
				ExpiresAt:   publishedTime + 7*24*3600,
				Source:      event.Source,
			}
	
			if err := n.processedProducer.Send(wordIndexEvent); err != nil {
				log.Printf("Failed to send word index event to Kafka with %v\n", err)
				continue
			}
		}
	}
}
