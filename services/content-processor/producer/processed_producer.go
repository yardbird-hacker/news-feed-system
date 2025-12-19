package producer

import (
	"encoding/json"
	"log"

	"content-processor/model"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

// interface
type ProcessedProducer interface {
    Send(event model.KeywordIndexEvent) error
    Close()
}

type KafkaProcessedProducer struct {
    producer *kafka.Producer
    topic    string
}

func NewKafkaProcessedProducer(brokers, topic string) (*KafkaProcessedProducer, error) {
    p, err := kafka.NewProducer(&kafka.ConfigMap{
        "bootstrap.servers": brokers,

        "acks":              "all",
        "linger.ms":         10,
        "batch.size":        64 * 1024,
        "compression.type": "lz4",
        "enable.idempotence": true,
    })
    if err != nil {
        return nil, err
    }

    // delivery report goroutine
    go func() {
        for e := range p.Events() {
            switch ev := e.(type) {
            case *kafka.Message:
                if ev.TopicPartition.Error != nil {
                    log.Printf("❌ delivery failed: %v\n", ev.TopicPartition)
                }
            }
        }
    }()

    return &KafkaProcessedProducer{
        producer: p,
        topic:    topic,
    }, nil
}

func (k *KafkaProcessedProducer) Send(event model.KeywordIndexEvent) error {
    payload, err := json.Marshal(event)
    if err != nil {
        return err
    }

    return k.producer.Produce(&kafka.Message{
        TopicPartition: kafka.TopicPartition{
            Topic:     &k.topic,
            Partition: kafka.PartitionAny,
        },
        Key:   []byte(event.Keyword), // ⭐ 파티션 키
        Value: payload,
    }, nil)
}

func (k *KafkaProcessedProducer) Close() {
    k.producer.Flush(5000)
    k.producer.Close()
}