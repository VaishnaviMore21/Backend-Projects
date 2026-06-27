package com.ordering.payment.service;

import com.ordering.events.*;
import com.ordering.payment.kafka.PaymentEventProducer;
import com.ordering.payment.model.*;
import com.ordering.payment.repository.PaymentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.UUID;

@Slf4j @Service @RequiredArgsConstructor
public class PaymentService {

    private final PaymentRepository repo;
    private final PaymentEventProducer producer;

    public void processPayment(InventoryReservedEvent event) {
        log.info("💳 Processing payment orderId={} amount={}", event.getOrderId(), event.getTotalAmount());
        String txId = UUID.randomUUID().toString();

        // Demo rule: payment fails if total > 10,000
        boolean success = event.getTotalAmount().doubleValue() <= 10_000.0;

        if (success) {
            repo.save(Payment.builder().transactionId(txId).orderId(event.getOrderId())
                .customerId(event.getCustomerId()).amount(event.getTotalAmount())
                .status(PaymentStatus.SUCCESS).createdAt(LocalDateTime.now()).build());
            producer.publishProcessed(PaymentProcessedEvent.builder()
                .orderId(event.getOrderId()).customerId(event.getCustomerId())
                .customerEmail(event.getCustomerEmail()).transactionId(txId)
                .amount(event.getTotalAmount()).processedAt(LocalDateTime.now()).build());
        } else {
            String reason = "Declined: amount " + event.getTotalAmount() + " exceeds limit 10000";
            repo.save(Payment.builder().transactionId(txId).orderId(event.getOrderId())
                .customerId(event.getCustomerId()).amount(event.getTotalAmount())
                .status(PaymentStatus.FAILED).failureReason(reason)
                .createdAt(LocalDateTime.now()).build());
            producer.publishFailed(PaymentFailedEvent.builder()
                .orderId(event.getOrderId()).customerId(event.getCustomerId())
                .customerEmail(event.getCustomerEmail())
                .reason(reason).failedAt(LocalDateTime.now()).build());
        }
    }
}
