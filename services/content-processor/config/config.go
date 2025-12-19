package config

import "os"

type Config struct {
    KafkaBrokers string
    KeywordTopic string
}

func Load() Config {
    return Config{
        KafkaBrokers: getEnv("KAFKA_BROKERS", "localhost:9092"),
        KeywordTopic: getEnv("KAFKA_KEYWORD_TOPIC", "news.keyword.index"),
    }
}

func getEnv(key, def string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return def
}
