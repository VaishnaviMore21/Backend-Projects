package com.ordering.inventory.kafka;

import com.ordering.events.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class InventoryEventProducer {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishReserved(InventoryReservedEvent e) {
        log.info("📤 InventoryReservedEvent → orderId={}", e.getOrderId());
        kafkaTemplate.send("inventory.reserved", e.getOrderId(), e);
    }

    public void publishFailed(InventoryFailedEvent e) {
        log.warn("📤 InventoryFailedEvent → orderId={}", e.getOrderId());
        kafkaTemplate.send("inventory.failed", e.getOrderId(), e);
    }
}
