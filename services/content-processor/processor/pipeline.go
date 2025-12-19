package processor

import (
	"content-processor/keyword"
	"content-processor/model"
	"content-processor/parser"
)

func ProcessEvent(event model.ExternalNews, bodyText string) []string {
    parsed := parser.ParseContent(
        event.Headline,
        event.Summary,
        bodyText,
    )

    words := keyword.Aggregate(parsed)
    return words
}
