package com.ordering.order.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ordering.events.*;
import com.ordering.order.model.*;
import com.ordering.order.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;

@Slf4j @Component @RequiredArgsConstructor
public class OrderEventConsumer {

    private final OrderRepository orderRepository;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = "payment.processed", groupId = "order-service-group")
    public void onPaymentProcessed(String message) {
        try {
            PaymentProcessedEvent event = objectMapper.readValue(message, PaymentProcessedEvent.class);
            log.info("✅ Payment processed for orderId={}", event.getOrderId());
            updateStatus(event.getOrderId(), OrderStatus.CONFIRMED);
        } catch (Exception e) {
            log.error("Failed to process payment.processed event", e);
        }
    }

    @KafkaListener(topics = "payment.failed", groupId = "order-service-group")
    public void onPaymentFailed(String message) {
        try {
            PaymentFailedEvent event = objectMapper.readValue(message, PaymentFailedEvent.class);
            log.warn("❌ Payment failed for orderId={}", event.getOrderId());
            updateStatus(event.getOrderId(), OrderStatus.CANCELLED);
        } catch (Exception e) {
            log.error("Failed to process payment.failed event", e);
        }
    }

    @KafkaListener(topics = "inventory.failed", groupId = "order-service-group")
    public void onInventoryFailed(String message) {
        try {
            InventoryFailedEvent event = objectMapper.readValue(message, InventoryFailedEvent.class);
            log.warn("❌ Inventory failed for orderId={}", event.getOrderId());
            updateStatus(event.getOrderId(), OrderStatus.CANCELLED);
        } catch (Exception e) {
            log.error("Failed to process inventory.failed event", e);
        }
    }

    private void updateStatus(String orderId, OrderStatus status) {
        orderRepository.findById(orderId).ifPresent(o -> {
            o.setStatus(status);
            o.setUpdatedAt(LocalDateTime.now());
            orderRepository.save(o);
            log.info("🔄 Order {} → {}", orderId, status);
        });
    }
}
