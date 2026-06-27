package com.urlshortner.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

@Service
public class RedisCacheService {

    private static final Logger log = LoggerFactory.getLogger(RedisCacheService.class);

    private final RedisTemplate<String, String> redisTemplate;
    private final long cacheTtlSeconds;

    public RedisCacheService(
            RedisTemplate<String, String> redisTemplate,
            @Value("${app.cache.ttl-seconds:86400}") long cacheTtlSeconds
    ) {
        this.redisTemplate = redisTemplate;
        this.cacheTtlSeconds = cacheTtlSeconds;
    }

    public String get(String shortCode) {
        String cachedValue = redisTemplate.opsForValue().get(shortCode);
        if (cachedValue != null) {
            log.debug("Redis cache HIT for shortCode={}", shortCode);
            return cachedValue;
        }

        log.debug("Redis cache MISS for shortCode={}", shortCode);
        return null;
    }

    /**
     * Writes the shortCode -> originalUrl mapping into Redis immediately after create/load.
     * This keeps redirects on the fast path for subsequent reads and reduces database load.
     */
    public void put(String shortCode, String originalUrl) {
        redisTemplate.opsForValue().set(shortCode, originalUrl, cacheTtlSeconds, java.util.concurrent.TimeUnit.SECONDS);
        log.debug("Stored shortCode={} in Redis with ttlSeconds={}", shortCode, cacheTtlSeconds);
    }
}

