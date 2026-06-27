package com.notification.consumer;

import com.notification.dto.NotificationEventDto;
import com.notification.entity.Notification;
import com.notification.repository.NotificationRepository;
import com.notification.service.EmailNotificationService;
import com.notification.service.SmsNotificationService;
import com.notification.service.PushNotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationConsumer {

    private final NotificationRepository notificationRepository;
    private final EmailNotificationService emailNotificationService;
    private final SmsNotificationService smsNotificationService;
    private final PushNotificationService pushNotificationService;

    @KafkaListener(
            topics = "notification-events",
            groupId = "notification-consumer-group",
            containerFactory = "kafkaListenerContainerFactory"
    )
    public void consumeNotification(NotificationEventDto event) {
        try {
            log.info("Received notification event: eventId={}, recipient={}, channel={}", 
                    event.getEventId(), event.getRecipientId(), event.getChannel());

            // Save notification to database
            Notification notification = Notification.builder()
                    .id(event.getEventId())
                    .recipientId(event.getRecipientId())
                    .channel(event.getChannel())
                    .subject(event.getSubject())
                    .message(event.getMessage())
                    .recipientAddress(event.getRecipientAddress())
                    .templateId(event.getTemplateId())
                    .status("PENDING")
                    .retryCount(event.getRetryCount() != null ? event.getRetryCount() : 0)
                    .priority(event.getPriority() != null ? event.getPriority() : "NORMAL")
                    .metadata(event.getMetadata() != null ? event.getMetadata().toString() : null)
                    .build();

            notificationRepository.save(notification);
            log.debug("Notification saved to database: {}", notification.getId());

            // Process based on channel
            processNotification(event, notification);

        } catch (Exception e) {
            log.error("Error processing notification event: {}", event.getEventId(), e);
            // Update notification status to FAILED if possible
        }
    }

    private void processNotification(NotificationEventDto event, Notification notification) {
        try {
            switch (event.getChannel().toUpperCase()) {
                case "EMAIL":
                    emailNotificationService.sendEmail(event, notification);
                    notificationRepository.save(notification);
                    break;
                case "SMS":
                    smsNotificationService.sendSms(event, notification);
                    notificationRepository.save(notification);
                    break;
                case "PUSH":
                    pushNotificationService.sendPush(event, notification);
                    notificationRepository.save(notification);
                    break;
                default:
                    log.warn("Unknown notification channel: {}", event.getChannel());
                    notification.setStatus("FAILED");
                    notification.setErrorMessage("Unknown channel: " + event.getChannel());
                    notificationRepository.save(notification);
            }
        } catch (Exception e) {
            log.error("Error processing notification: {}", notification.getId(), e);
            notification.setStatus("FAILED");
            notification.setErrorMessage(e.getMessage());
            notification.setUpdatedAt(LocalDateTime.now());
            notificationRepository.save(notification);
        }
    }
}
