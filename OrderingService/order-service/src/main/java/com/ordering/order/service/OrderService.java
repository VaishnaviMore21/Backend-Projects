package com.ordering.order.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ordering.events.OrderPlacedEvent;
import com.ordering.order.dto.CreateOrderRequest;
import com.ordering.order.kafka.OrderEventProducer;
import com.ordering.order.model.*;
import com.ordering.order.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j @Service @RequiredArgsConstructor
public class OrderService {

    private final OrderRepository repo;
    private final OrderEventProducer producer;
    private final ObjectMapper mapper;

    public Order createOrder(CreateOrderRequest req) {
        String id = UUID.randomUUID().toString();
        BigDecimal total = req.getItems().stream()
            .map(i -> i.getUnitPrice().multiply(BigDecimal.valueOf(i.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);

        String itemsJson;
        try { itemsJson = mapper.writeValueAsString(req.getItems()); }
        catch (JsonProcessingException e) { itemsJson = "[]"; }

        Order order = Order.builder()
            .id(id).customerId(req.getCustomerId())
            .customerEmail(req.getCustomerEmail())
            .status(OrderStatus.PENDING).totalAmount(total)
            .itemsJson(itemsJson).createdAt(LocalDateTime.now())
            .updatedAt(LocalDateTime.now()).build();

        repo.save(order);
        log.info("📝 Order created: {}", id);

        List<OrderPlacedEvent.OrderItem> eventItems = req.getItems().stream()
            .map(i -> OrderPlacedEvent.OrderItem.builder()
                .productId(i.getProductId()).productName(i.getProductName())
                .quantity(i.getQuantity()).unitPrice(i.getUnitPrice()).build())
            .collect(Collectors.toList());

        producer.publishOrderPlaced(OrderPlacedEvent.builder()
            .orderId(id).customerId(req.getCustomerId())
            .customerEmail(req.getCustomerEmail())
            .items(eventItems).totalAmount(total)
            .placedAt(LocalDateTime.now()).build());

        return order;
    }

    public List<Order> getAll() { return repo.findAll(); }

    public Order getById(String id) {
        return repo.findById(id).orElseThrow(() ->
            new RuntimeException("Order not found: " + id));
    }
}
