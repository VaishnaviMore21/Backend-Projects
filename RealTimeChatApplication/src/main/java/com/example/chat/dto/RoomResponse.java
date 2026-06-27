package com.example.chat.dto;

import java.time.Instant;

public record RoomResponse(Long id, String name, Instant createdAt) {
}
