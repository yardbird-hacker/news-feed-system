package model

import "time"

type ExternalNews struct {
	ID				int			`json:"id"`
	Category		string		`json:"category"`
	PublishAt		time.Time	`json:"publishedAt"`
	Headline    	string    	`json:"headline"`
	Related     	string    	`json:"related"`
	Source      	string    	`json:"source"`
	Summary     	string    	`json:"summary"`
	URL         	string    	`json:"url"`
}