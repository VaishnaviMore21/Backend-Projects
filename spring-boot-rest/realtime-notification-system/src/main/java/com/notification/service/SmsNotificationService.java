package com.notification.service;

import com.notification.dto.NotificationEventDto;
import com.notification.entity.Notification;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SmsNotificationService {

    public void sendSms(NotificationEventDto event, Notification notification) {
        try {
            log.info("Sending SMS to: {}", event.getRecipientAddress());
            
            // Simulate SMS sending
            simulateSmsSending(event);

            notification.setStatus("SENT");
            notification.setSentAt(java.time.LocalDateTime.now());
            log.info("SMS sent successfully: {}", notification.getId());

        } catch (Exception e) {
            log.error("Failed to send SMS: {}", e.getMessage());
            notification.setStatus("FAILED");
            notification.setErrorMessage(e.getMessage());
            notification.setRetryCount(notification.getRetryCount() + 1);
            throw new RuntimeException("SMS sending failed", e);
        }
    }

    private void simulateSmsSending(NotificationEventDto event) {
        // Simulate API call to SMS service
        log.debug("Simulating SMS send to: {}", event.getRecipientAddress());
        // In real implementation:
        // - Use Twilio API
        // - Use AWS SNS
        // - Use Nexmo/Vonage
        // - Use any other SMS provider
    }
}
