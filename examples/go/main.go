package main

import (
 "fmt"
 "io"
 "net/http"
 "net/url"
 "os"
 "strings"
 "time"
)

func main() {
 key := strings.TrimSpace(os.Getenv("SOLDFETCH_API_KEY"))
 if key == "" { fmt.Fprintln(os.Stderr,"Set SOLDFETCH_API_KEY"); os.Exit(1) }
 query := url.Values{"keyword":{"sony wh-1000xm5"},"ebaySite":{"ebay.com"},"count":{"20"}}
 req, err := http.NewRequest("GET", "https://soldfetch.com/v1/scrape?"+query.Encode(), nil)
 if err != nil { panic(err) }
 req.Header.Set("Authorization", "Bearer "+key)
 req.Header.Set("Accept", "application/json")
 client := &http.Client{Timeout:65*time.Second, CheckRedirect:func(req *http.Request, via []*http.Request) error {return http.ErrUseLastResponse}}
 res, err := client.Do(req)
 if err != nil { fmt.Fprintln(os.Stderr,"SoldFetch request failed"); os.Exit(1) }
 defer res.Body.Close()
 if res.StatusCode != 200 { fmt.Fprintf(os.Stderr,"SoldFetch HTTP %d; request ID: %s\n",res.StatusCode,res.Header.Get("X-Request-Id")); os.Exit(1) }
 if _,err := io.Copy(os.Stdout,io.LimitReader(res.Body,10<<20)); err != nil { panic(err) }
}
