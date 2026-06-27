package com.notification.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.io.Serializable;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class NotificationEventDto implements Serializable {

    private static final long serialVersionUID = 1L;

    @JsonProperty("event_id")
    private String eventId;

    @JsonProperty("recipient_id")
    private String recipientId;

    @JsonProperty("channel")
    private String channel; // EMAIL, SMS, PUSH

    @JsonProperty("subject")
    private String subject;

    @JsonProperty("message")
    private String message;

    @JsonProperty("recipient_address")
    private String recipientAddress; // email, phone, device token

    @JsonProperty("template_id")
    private String templateId;

    @JsonProperty("template_variables")
    private Map<String, Object> templateVariables;

    @JsonProperty("retry_count")
    private Integer retryCount;

    @JsonProperty("priority")
    private String priority; // HIGH, NORMAL, LOW

    @JsonProperty("timestamp")
    private Long timestamp;

    @JsonProperty("metadata")
    private Map<String, Object> metadata;
}
