package com.notification.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "notifications", indexes = {
    @Index(name = "idx_recipient_id", columnList = "recipient_id"),
    @Index(name = "idx_status", columnList = "status"),
    @Index(name = "idx_channel", columnList = "channel"),
    @Index(name = "idx_created_at", columnList = "created_at")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Notification {

    @Id
    @Column(name = "id")
    private String id;

    @Column(name = "recipient_id", nullable = false)
    private String recipientId;

    @Column(name = "channel", nullable = false)
    private String channel; // EMAIL, SMS, PUSH

    @Column(name = "subject")
    private String subject;

    @Column(name = "message", columnDefinition = "TEXT")
    private String message;

    @Column(name = "recipient_address", nullable = false)
    private String recipientAddress;

    @Column(name = "template_id")
    private String templateId;

    @Column(name = "status", nullable = false)
    private String status; // PENDING, SENT, FAILED, DELIVERED

    @Column(name = "retry_count")
    private Integer retryCount = 0;

    @Column(name = "max_retries")
    private Integer maxRetries = 3;

    @Column(name = "priority")
    private String priority = "NORMAL"; // HIGH, NORMAL, LOW

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "sent_at")
    private LocalDateTime sentAt;

    @Column(name = "metadata", columnDefinition = "TEXT")
    private String metadata;
}
