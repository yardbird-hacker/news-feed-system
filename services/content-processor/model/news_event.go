package model

type ExternalNews struct {
	ID				int64			`json:"id"`
	Category		string		`json:"category"`
	PublishAt		float64		`json:"publishedAt"`
	Headline    	string    	`json:"headline"`
	Related     	string    	`json:"related"`
	Source      	string    	`json:"source"`
	Summary     	string    	`json:"summary"`
	URL         	string    	`json:"url"`
}