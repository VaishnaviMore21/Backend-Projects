package com.ordering.order.kafka;

import com.ordering.events.OrderPlacedEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class OrderEventProducer {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishOrderPlaced(OrderPlacedEvent event) {
        log.info("📤 Publishing OrderPlacedEvent for orderId={}", event.getOrderId());
        kafkaTemplate.send("order.placed", event.getOrderId(), event);
    }
}
