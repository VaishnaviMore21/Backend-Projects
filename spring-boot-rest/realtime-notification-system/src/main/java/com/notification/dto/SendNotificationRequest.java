package com.notification.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.*;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SendNotificationRequest {

    @NotBlank(message = "Recipient ID is required")
    @JsonProperty("recipient_id")
    private String recipientId;

    @NotBlank(message = "Channel is required")
    @JsonProperty("channel")
    private String channel; // EMAIL, SMS, PUSH

    @JsonProperty("subject")
    private String subject;

    @NotBlank(message = "Message is required")
    @JsonProperty("message")
    private String message;

    @NotBlank(message = "Recipient address is required")
    @JsonProperty("recipient_address")
    private String recipientAddress;

    @JsonProperty("template_id")
    private String templateId;

    @JsonProperty("template_variables")
    private Map<String, Object> templateVariables;

    @JsonProperty("priority")
    private String priority = "NORMAL";

    @JsonProperty("metadata")
    private Map<String, Object> metadata;
}
