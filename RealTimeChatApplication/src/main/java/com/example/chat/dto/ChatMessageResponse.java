package com.example.chat.dto;

import java.time.Instant;

public record ChatMessageResponse(
    Long id,
    Long roomId,
    Long senderId,
    String senderUsername,
    String content,
    Instant createdAt
) {
}
