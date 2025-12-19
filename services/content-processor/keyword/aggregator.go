package keyword

import "content-processor/model"

func Aggregate(pc model.ParsedContent) []string {
    // merge + dedup
	 var result []string
    result = append(result, pc.Headline...)
    result = append(result, pc.Summary...)
    result = append(result, pc.Body...)
    return result
}
