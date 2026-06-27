package com.example.chat.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record ChatMessageInbound(
    @NotNull Long senderId,
    @NotBlank @Size(max = 2000) String content
) {
}
