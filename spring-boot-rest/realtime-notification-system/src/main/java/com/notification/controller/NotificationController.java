package com.notification.controller;

import com.notification.dto.NotificationResponse;
import com.notification.dto.NotificationStatusDto;
import com.notification.dto.SendNotificationRequest;
import com.notification.entity.UserPreference;
import com.notification.service.NotificationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Slf4j
@RestController
@RequestMapping("/notifications")
@RequiredArgsConstructor
public class NotificationController {

    private final NotificationService notificationService;

    @PostMapping("/send")
    public ResponseEntity<NotificationResponse> sendNotification(
            @Valid @RequestBody SendNotificationRequest request) {
        log.info("Received notification request for recipient: {}", request.getRecipientId());
        
        String notificationId = notificationService.sendNotification(request);
        
        return ResponseEntity.status(HttpStatus.ACCEPTED)
                .body(NotificationResponse.builder()
                        .notificationId(notificationId)
                        .status("ACCEPTED")
                        .message("Notification queued for processing")
                        .timestamp(System.currentTimeMillis())
                        .build());
    }

    @GetMapping("/{notificationId}/status")
    public ResponseEntity<NotificationStatusDto> getNotificationStatus(
            @PathVariable String notificationId) {
        log.info("Fetching status for notification: {}", notificationId);
        NotificationStatusDto status = notificationService.getNotificationStatus(notificationId);
        return ResponseEntity.ok(status);
    }

    @GetMapping("/recipient/{recipientId}")
    public ResponseEntity<List<NotificationStatusDto>> getNotificationsByRecipient(
            @PathVariable String recipientId) {
        log.info("Fetching notifications for recipient: {}", recipientId);
        List<NotificationStatusDto> notifications = notificationService.getNotificationsByRecipient(recipientId);
        return ResponseEntity.ok(notifications);
    }

    @GetMapping("/channel/{channel}")
    public ResponseEntity<List<NotificationStatusDto>> getNotificationsByChannel(
            @PathVariable String channel) {
        log.info("Fetching notifications for channel: {}", channel);
        List<NotificationStatusDto> notifications = notificationService.getNotificationsByChannel(channel);
        return ResponseEntity.ok(notifications);
    }

    @PostMapping("/preferences/{userId}")
    public ResponseEntity<String> saveUserPreferences(
            @PathVariable String userId,
            @RequestBody UserPreference preference) {
        log.info("Saving preferences for user: {}", userId);
        notificationService.saveUserPreference(userId, preference);
        return ResponseEntity.ok("Preferences saved successfully");
    }

    @GetMapping("/preferences/{userId}")
    public ResponseEntity<UserPreference> getUserPreferences(
            @PathVariable String userId) {
        log.info("Fetching preferences for user: {}", userId);
        Optional<UserPreference> preference = notificationService.getUserPreference(userId);
        return preference.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Notification service is running");
    }
}
