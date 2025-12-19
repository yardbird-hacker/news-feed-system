package parser

import (
	"content-processor/model"
	"content-processor/util"
)

func ParseContent(headline, summary, body string) model.ParsedContent {
    return model.ParsedContent{
        Headline: util.Tokenize(headline),
        Summary:  util.Tokenize(summary),
        Body:     util.Tokenize(body),
    }
}

