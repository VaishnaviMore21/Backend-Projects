package com.urlshortner.service;

import com.urlshortner.dto.ShortenUrlResponse;
import com.urlshortner.entity.UrlMapping;
import com.urlshortner.exception.InvalidUrlException;
import com.urlshortner.exception.ShortCodeNotFoundException;
import com.urlshortner.repository.UrlIdSequenceRepository;
import com.urlshortner.repository.UrlMappingRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class UrlShortenerServiceTest {

    @Mock
    private UrlMappingRepository urlMappingRepository;

    @Mock
    private UrlIdSequenceRepository urlIdSequenceRepository;

    @Mock
    private RedisCacheService redisCacheService;

    private UrlShortenerService urlShortenerService;

    @BeforeEach
    void setUp() {
        urlShortenerService = new UrlShortenerService(
                urlMappingRepository,
                urlIdSequenceRepository,
                redisCacheService,
                "http://localhost:8080"
        );
    }

    @Test
    void shouldCreateShortUrlAndWarmCache() {
        when(urlIdSequenceRepository.nextId()).thenReturn(62L);
        when(urlMappingRepository.save(any(UrlMapping.class))).thenAnswer(invocation -> invocation.getArgument(0));

        ShortenUrlResponse response = urlShortenerService.shortenUrl("https://example.com/some/path");

        assertEquals("http://localhost:8080/10", response.shortUrl());
        verify(redisCacheService).put("10", "https://example.com/some/path");
    }

    @Test
    void shouldRejectUnsupportedUrlSchemes() {
        assertThrows(InvalidUrlException.class, () -> urlShortenerService.shortenUrl("ftp://example.com/file"));
        verify(urlIdSequenceRepository, never()).nextId();
    }

    @Test
    void shouldResolveFromCacheWhenPresent() {
        when(redisCacheService.get("abc123")).thenReturn("https://cached.example.com");

        String resolvedUrl = urlShortenerService.resolveOriginalUrl("abc123");

        assertEquals("https://cached.example.com", resolvedUrl);
        verify(urlMappingRepository, never()).findByShortCode(any());
    }

    @Test
    void shouldResolveFromDatabaseAndPopulateCacheOnMiss() {
        when(redisCacheService.get("abc123")).thenReturn(null);
        when(urlMappingRepository.findByShortCode("abc123"))
                .thenReturn(Optional.of(new UrlMapping(999L, "https://db.example.com", "abc123")));

        String resolvedUrl = urlShortenerService.resolveOriginalUrl("abc123");

        assertEquals("https://db.example.com", resolvedUrl);
        verify(redisCacheService).put("abc123", "https://db.example.com");
    }

    @Test
    void shouldThrowNotFoundWhenShortCodeDoesNotExist() {
        when(redisCacheService.get("missing")).thenReturn(null);
        when(urlMappingRepository.findByShortCode("missing")).thenReturn(Optional.empty());

        assertThrows(ShortCodeNotFoundException.class, () -> urlShortenerService.resolveOriginalUrl("missing"));
    }
}

