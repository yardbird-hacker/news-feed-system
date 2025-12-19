package fetcher

import (
	"io"
	"net/http"
	"time"
)

func Fetch(url string) (string, error) {
    client := &http.Client{
        Timeout: 5 * time.Second,
    }

    resp, err := client.Get(url)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    return string(body), nil
}
