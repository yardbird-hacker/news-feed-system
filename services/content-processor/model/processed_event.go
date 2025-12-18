package model

type ProcessedEvent struct {
	ID       int      `json:"id"`
	Headline string   `json:"headline"`
	Keywords []string `json:"keywords"`
	URL      string   `json:"url"`
}