package com.notification.service;

import com.notification.dto.NotificationEventDto;
import com.notification.entity.Notification;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class EmailNotificationService {

    public void sendEmail(NotificationEventDto event, Notification notification) {
        try {
            log.info("Sending email to: {}", event.getRecipientAddress());
            
            // Simulate email sending
            // In production, integrate with SendGrid, AWS SES, etc.
            simulateEmailSending(event);

            notification.setStatus("SENT");
            notification.setSentAt(java.time.LocalDateTime.now());
            log.info("Email sent successfully: {}", notification.getId());

        } catch (Exception e) {
            log.error("Failed to send email: {}", e.getMessage());
            notification.setStatus("FAILED");
            notification.setErrorMessage(e.getMessage());
            notification.setRetryCount(notification.getRetryCount() + 1);
            throw new RuntimeException("Email sending failed", e);
        }
    }

    private void simulateEmailSending(NotificationEventDto event) {
        // Simulate API call or email service
        log.debug("Simulating email send to {} with subject: {}", 
                event.getRecipientAddress(), event.getSubject());
        // In real implementation:
        // - Use SendGrid API
        // - Use AWS SES
        // - Use Mailgun
        // - Use any other email service
    }
}
