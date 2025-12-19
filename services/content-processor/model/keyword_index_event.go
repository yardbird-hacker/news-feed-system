package model

type KeywordIndexEvent struct {
    Keyword     	string	`json:"keyword"`        // PK
    NewsID      	int64	`json:"news_id"`
    URL         	string	`json:"url,omitempty"`

    PublishedAt 	int64 	`json:"published_at"`   // epoch seconds
    ExpiresAt   	int64	`json:"expires_at"`     // TTL (epoch seconds)

    Source      	string	`json:"source"`         // gdelt, newsapi
}