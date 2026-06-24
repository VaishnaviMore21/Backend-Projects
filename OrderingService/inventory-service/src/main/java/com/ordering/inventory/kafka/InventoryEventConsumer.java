package com.ordering.inventory.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ordering.events.OrderPlacedEvent;
import com.ordering.inventory.service.InventoryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class InventoryEventConsumer {

    private final InventoryService service;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = "order.placed", groupId = "inventory-service-group")
    public void onOrderPlaced(String message) {
        try {
            OrderPlacedEvent event = objectMapper.readValue(message, OrderPlacedEvent.class);
            log.info("📥 OrderPlacedEvent → orderId={}", event.getOrderId());
            service.processOrderPlaced(event);
        } catch (Exception e) {
            log.error("Failed to process order.placed event", e);
        }
    }
}
