package com.ordering.payment.kafka;

import com.ordering.events.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class PaymentEventProducer {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishProcessed(PaymentProcessedEvent e) {
        log.info("📤 PaymentProcessedEvent → orderId={}", e.getOrderId());
        kafkaTemplate.send("payment.processed", e.getOrderId(), e);
    }

    public void publishFailed(PaymentFailedEvent e) {
        log.warn("📤 PaymentFailedEvent → orderId={}", e.getOrderId());
        kafkaTemplate.send("payment.failed", e.getOrderId(), e);
    }
}
