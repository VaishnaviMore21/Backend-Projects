package com.ordering.notification.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ordering.events.*;
import com.ordering.notification.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class NotificationEventConsumer {

    private final NotificationService service;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = "payment.processed", groupId = "notification-service-group")
    public void onPaymentProcessed(String message) {
        try {
            PaymentProcessedEvent e = objectMapper.readValue(message, PaymentProcessedEvent.class);
            log.info("📥 PaymentProcessedEvent → orderId={}", e.getOrderId());
            service.notifyConfirmed(e);
        } catch (Exception e) {
            log.error("Failed to process payment.processed event", e);
        }
    }

    @KafkaListener(topics = "payment.failed", groupId = "notification-service-group")
    public void onPaymentFailed(String message) {
        try {
            PaymentFailedEvent e = objectMapper.readValue(message, PaymentFailedEvent.class);
            log.info("📥 PaymentFailedEvent → orderId={}", e.getOrderId());
            service.notifyPaymentFailed(e);
        } catch (Exception e) {
            log.error("Failed to process payment.failed event", e);
        }
    }

    @KafkaListener(topics = "inventory.failed", groupId = "notification-service-group")
    public void onInventoryFailed(String message) {
        try {
            InventoryFailedEvent e = objectMapper.readValue(message, InventoryFailedEvent.class);
            log.info("📥 InventoryFailedEvent → orderId={}", e.getOrderId());
            service.notifyInventoryFailed(e);
        } catch (Exception e) {
            log.error("Failed to process inventory.failed event", e);
        }
    }
}
