package com.urlshortner.controller;

import com.urlshortner.dto.ShortenUrlRequest;
import com.urlshortner.dto.ShortenUrlResponse;
import com.urlshortner.service.UrlShortenerService;
import jakarta.validation.Valid;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.net.URI;

@RestController
public class UrlShortenerController {

    private final UrlShortenerService urlShortenerService;

    public UrlShortenerController(UrlShortenerService urlShortenerService) {
        this.urlShortenerService = urlShortenerService;
    }

    @PostMapping("/shorten")
    public ResponseEntity<ShortenUrlResponse> shortenUrl(@Valid @RequestBody ShortenUrlRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(urlShortenerService.shortenUrl(request.fullUrl()));
    }

    @GetMapping("/{shortCode:[0-9a-zA-Z]+}")
    public ResponseEntity<Void> redirectToOriginalUrl(@PathVariable String shortCode) {
        String originalUrl = urlShortenerService.resolveOriginalUrl(shortCode);
        return ResponseEntity.status(HttpStatus.FOUND)
                .header(HttpHeaders.LOCATION, URI.create(originalUrl).toString())
                .build();
    }
}

