package com.ordering.inventory.service;

import com.ordering.events.*;
import com.ordering.inventory.kafka.InventoryEventProducer;
import com.ordering.inventory.model.Inventory;
import com.ordering.inventory.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime;

@Slf4j @Service @RequiredArgsConstructor
public class InventoryService {

    private final InventoryRepository repo;
    private final InventoryEventProducer producer;

    @Transactional
    public void processOrderPlaced(OrderPlacedEvent event) {
        for (OrderPlacedEvent.OrderItem item : event.getItems()) {
            Inventory inv = repo.findById(item.getProductId()).orElse(null);
            if (inv == null || inv.getAvailableQuantity() < item.getQuantity()) {
                String reason = inv == null
                    ? "Product not found: " + item.getProductId()
                    : "Insufficient stock for " + item.getProductName()
                      + " (available=" + inv.getAvailableQuantity()
                      + ", requested=" + item.getQuantity() + ")";
                log.warn("❌ {}", reason);
                producer.publishFailed(InventoryFailedEvent.builder()
                    .orderId(event.getOrderId()).customerId(event.getCustomerId())
                    .customerEmail(event.getCustomerEmail())
                    .reason(reason).failedAt(LocalDateTime.now()).build());
                return;
            }
        }
        // All items available — deduct stock
        event.getItems().forEach(item -> repo.findById(item.getProductId()).ifPresent(inv -> {
            inv.setAvailableQuantity(inv.getAvailableQuantity() - item.getQuantity());
            repo.save(inv);
            log.info("✅ Reserved {} × {}", item.getQuantity(), item.getProductName());
        }));

        producer.publishReserved(InventoryReservedEvent.builder()
            .orderId(event.getOrderId()).customerId(event.getCustomerId())
            .customerEmail(event.getCustomerEmail())
            .totalAmount(event.getTotalAmount())
            .reservedAt(LocalDateTime.now()).build());
    }
}
