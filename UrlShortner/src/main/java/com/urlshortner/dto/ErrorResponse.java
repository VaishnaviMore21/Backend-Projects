package com.urlshortner.dto;

import java.time.OffsetDateTime;

public class ErrorResponse {

    private final String error;
    private final int status;
    private final OffsetDateTime timestamp;

    public ErrorResponse(String error, int status, OffsetDateTime timestamp) {
        this.error = error;
        this.status = status;
        this.timestamp = timestamp;
    }

    public String getError() {
        return error;
    }

    public int getStatus() {
        return status;
    }

    public OffsetDateTime getTimestamp() {
        return timestamp;
    }
}

