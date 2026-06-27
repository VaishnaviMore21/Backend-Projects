package com.urlshortner.dto;

import jakarta.validation.constraints.NotBlank;

public record ShortenUrlRequest(
        @NotBlank(message = "fullUrl is required")
        String fullUrl
) {
}

