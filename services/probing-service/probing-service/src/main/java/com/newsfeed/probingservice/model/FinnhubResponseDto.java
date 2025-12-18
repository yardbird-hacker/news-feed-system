package com.newsfeed.probingservice.model;


/*
[{'category': 'top news', 'datetime': 1765902360, 'headline': 'Why Oracle and these 3 unloved software stocks could be the next leg of the AI trade', 'id': 7562764, 'image': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/market_watch_logo.png', 'related': '', 'source': 'MarketWatch', 'summary': '“We see 2026 as the year that investors begin to shift their focus from hardware to software positions,” an HSBC analyst wrote.', 'url': 'https://www.marketwatch.com/story/why-oracle-and-these-3-unloved-software-stocks-could-be-the-next-leg-of-the-ai-trade-0f116600'}
related': '', 'source': 'MarketWatch', 'summary'
 */

import java.time.Instant;

public record FinnHubNewsDto(
        Integer id,
        String category,
        Long datetime,
        String headline,
        String related,
        String source,
        String summary,
        String url
) {}