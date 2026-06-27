package com.urlshortner.service;

import com.urlshortner.dto.ShortenUrlResponse;
import com.urlshortner.entity.UrlMapping;
import com.urlshortner.exception.InvalidUrlException;
import com.urlshortner.exception.ShortCodeNotFoundException;
import com.urlshortner.repository.UrlIdSequenceRepository;
import com.urlshortner.repository.UrlMappingRepository;
import com.urlshortner.util.Base62Encoder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Locale;

@Service
public class UrlShortenerService {

    private final UrlMappingRepository urlMappingRepository;
    private final UrlIdSequenceRepository urlIdSequenceRepository;
    private final RedisCacheService redisCacheService;
    private final String baseUrl;

    public UrlShortenerService(
            UrlMappingRepository urlMappingRepository,
            UrlIdSequenceRepository urlIdSequenceRepository,
            RedisCacheService redisCacheService,
            @Value("${app.base-url}") String baseUrl
    ) {
        this.urlMappingRepository = urlMappingRepository;
        this.urlIdSequenceRepository = urlIdSequenceRepository;
        this.redisCacheService = redisCacheService;
        this.baseUrl = baseUrl;
    }

    @Transactional
    public ShortenUrlResponse shortenUrl(String fullUrl) {
        validateUrl(fullUrl);

        long id = urlIdSequenceRepository.nextId();

        // The database sequence gives us a monotonically increasing numeric id.
        // Encoding that id in Base62 yields short, URL-safe, deterministic short codes.
        String shortCode = Base62Encoder.encode(id);
        UrlMapping urlMapping = new UrlMapping(id, fullUrl, shortCode);
        urlMappingRepository.save(urlMapping);

        // Write-through caching: newly created mappings are stored in Redis immediately
        // so the very first redirect can already take the low-latency cache path.
        redisCacheService.put(shortCode, fullUrl);

        return new ShortenUrlResponse(buildShortUrl(shortCode));
    }

    @Transactional(readOnly = true)
    public String resolveOriginalUrl(String shortCode) {
        String cachedUrl = redisCacheService.get(shortCode);
        if (cachedUrl != null) {
            return cachedUrl;
        }

        return loadFromDatabaseAndCache(shortCode);
    }

    private String loadFromDatabaseAndCache(String shortCode) {
        UrlMapping urlMapping = urlMappingRepository.findByShortCode(shortCode)
                .orElseThrow(() -> new ShortCodeNotFoundException(shortCode));

        redisCacheService.put(shortCode, urlMapping.getOriginalUrl());
        return urlMapping.getOriginalUrl();
    }

    private void validateUrl(String fullUrl) {
        try {
            URI uri = new URI(fullUrl);
            String scheme = uri.getScheme();
            if (scheme == null || uri.getHost() == null) {
                throw new InvalidUrlException("URL must be absolute and include a valid host");
            }

            String normalizedScheme = scheme.toLowerCase(Locale.ROOT);
            if (!"http".equals(normalizedScheme) && !"https".equals(normalizedScheme)) {
                throw new InvalidUrlException("Only HTTP and HTTPS URLs are supported");
            }
        } catch (URISyntaxException exception) {
            throw new InvalidUrlException("Malformed URL provided");
        }
    }

    private String buildShortUrl(String shortCode) {
        return baseUrl.endsWith("/") ? baseUrl + shortCode : baseUrl + "/" + shortCode;
    }
}

