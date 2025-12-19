package main

import (
	"log"

	"content-processor/consumer"
)

func main() {
	c, err := consumer.NewNewsConsumer()
	if err != nil {
		log.Fatal(err)
	}

	c.Start()
}
