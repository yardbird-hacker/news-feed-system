package com.newsfeed.probingservice.client;


import com.newsfeed.probingservice.model.ExternalNewsDto;

import java.util.List;

public interface NewsSourceClient {
    List<ExternalNewsDto> fetchNews();
}