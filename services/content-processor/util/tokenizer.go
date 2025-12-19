package util

import (
	"regexp"
	"strings"
)

var wordRegex = regexp.MustCompile(`[a-zA-Z0-9]+`)

func Tokenize(text string) []string {
    text = strings.ToLower(text)
    return wordRegex.FindAllString(text, -1)
}