package com.notification.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class NotificationStatusDto {

    @JsonProperty("notification_id")
    private String notificationId;

    @JsonProperty("recipient_id")
    private String recipientId;

    @JsonProperty("channel")
    private String channel;

    @JsonProperty("status")
    private String status; // PENDING, SENT, FAILED, DELIVERED

    @JsonProperty("error_message")
    private String errorMessage;

    @JsonProperty("retry_count")
    private Integer retryCount;

    @JsonProperty("created_at")
    private Long createdAt;

    @JsonProperty("updated_at")
    private Long updatedAt;
}
