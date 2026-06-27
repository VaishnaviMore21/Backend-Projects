package com.ordering.payment.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ordering.events.InventoryReservedEvent;
import com.ordering.payment.service.PaymentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class PaymentEventConsumer {

    private final PaymentService service;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = "inventory.reserved", groupId = "payment-service-group")
    public void onInventoryReserved(String message) {
        try {
            InventoryReservedEvent event = objectMapper.readValue(message, InventoryReservedEvent.class);
            log.info("📥 InventoryReservedEvent → orderId={}", event.getOrderId());
            service.processPayment(event);
        } catch (Exception e) {
            log.error("Failed to process inventory.reserved event", e);
        }
    }
}
