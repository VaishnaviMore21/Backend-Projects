package com.notification.service;

import com.notification.dto.NotificationEventDto;
import com.notification.dto.NotificationStatusDto;
import com.notification.dto.SendNotificationRequest;
import com.notification.entity.Notification;
import com.notification.entity.UserPreference;
import com.notification.exception.NotificationNotFoundException;
import com.notification.producer.NotificationProducer;
import com.notification.repository.NotificationRepository;
import com.notification.repository.UserPreferenceRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationService {

    private final NotificationRepository notificationRepository;
    private final UserPreferenceRepository userPreferenceRepository;
    private final NotificationProducer notificationProducer;

    @Transactional
    public String sendNotification(SendNotificationRequest request) {
        log.info("Processing notification request for recipient: {}", request.getRecipientId());

        // Check user preferences
        Optional<UserPreference> userPref = userPreferenceRepository.findByUserId(request.getRecipientId());
        
        String notificationId = UUID.randomUUID().toString();
        
        // Build notification event
        NotificationEventDto event = NotificationEventDto.builder()
                .eventId(notificationId)
                .recipientId(request.getRecipientId())
                .channel(request.getChannel())
                .subject(request.getSubject())
                .message(request.getMessage())
                .recipientAddress(request.getRecipientAddress())
                .templateId(request.getTemplateId())
                .templateVariables(request.getTemplateVariables())
                .retryCount(0)
                .priority(request.getPriority())
                .timestamp(System.currentTimeMillis())
                .metadata(request.getMetadata())
                .build();

        // Send to Kafka
        notificationProducer.sendNotification(event);
        log.info("Notification sent to Kafka: {}", notificationId);

        return notificationId;
    }

    public NotificationStatusDto getNotificationStatus(String notificationId) {
        Notification notification = notificationRepository.findById(notificationId)
                .orElseThrow(() -> new NotificationNotFoundException(
                        "Notification not found with id: " + notificationId));

        return NotificationStatusDto.builder()
                .notificationId(notification.getId())
                .recipientId(notification.getRecipientId())
                .channel(notification.getChannel())
                .status(notification.getStatus())
                .errorMessage(notification.getErrorMessage())
                .retryCount(notification.getRetryCount())
                .createdAt(notification.getCreatedAt().atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli())
                .updatedAt(notification.getUpdatedAt().atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli())
                .build();
    }

    public List<NotificationStatusDto> getNotificationsByRecipient(String recipientId) {
        List<Notification> notifications = notificationRepository.findByRecipientIdOrderByCreatedAtDesc(recipientId);
        return notifications.stream()
                .map(this::convertToStatusDto)
                .collect(Collectors.toList());
    }

    public List<NotificationStatusDto> getNotificationsByChannel(String channel) {
        List<Notification> notifications = notificationRepository.findByChannel(channel);
        return notifications.stream()
                .map(this::convertToStatusDto)
                .collect(Collectors.toList());
    }

    @Transactional
    public void saveUserPreference(String userId, UserPreference preference) {
        preference.setUserId(userId);
        userPreferenceRepository.save(preference);
        log.info("User preferences saved for: {}", userId);
    }

    public Optional<UserPreference> getUserPreference(String userId) {
        return userPreferenceRepository.findByUserId(userId);
    }

    @Scheduled(fixedDelay = 60000) // Run every 60 seconds
    @Transactional
    public void retryFailedNotifications() {
        log.debug("Starting retry of failed notifications");
        LocalDateTime retryAfter = LocalDateTime.now().minusMinutes(5);
        List<Notification> failedNotifications = notificationRepository
                .findFailedNotificationsForRetry(retryAfter);

        for (Notification notification : failedNotifications) {
            try {
                log.info("Retrying notification: {} (retry count: {})", 
                        notification.getId(), notification.getRetryCount());

                NotificationEventDto event = NotificationEventDto.builder()
                        .eventId(notification.getId())
                        .recipientId(notification.getRecipientId())
                        .channel(notification.getChannel())
                        .subject(notification.getSubject())
                        .message(notification.getMessage())
                        .recipientAddress(notification.getRecipientAddress())
                        .templateId(notification.getTemplateId())
                        .retryCount(notification.getRetryCount() + 1)
                        .priority(notification.getPriority())
                        .timestamp(System.currentTimeMillis())
                        .build();

                notificationProducer.sendNotification(event);
            } catch (Exception e) {
                log.error("Error retrying notification: {}", notification.getId(), e);
            }
        }
    }

    private NotificationStatusDto convertToStatusDto(Notification notification) {
        return NotificationStatusDto.builder()
                .notificationId(notification.getId())
                .recipientId(notification.getRecipientId())
                .channel(notification.getChannel())
                .status(notification.getStatus())
                .errorMessage(notification.getErrorMessage())
                .retryCount(notification.getRetryCount())
                .createdAt(notification.getCreatedAt().atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli())
                .updatedAt(notification.getUpdatedAt().atZone(java.time.ZoneId.systemDefault()).toInstant().toEpochMilli())
                .build();
    }
}
