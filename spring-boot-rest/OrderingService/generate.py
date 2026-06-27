#!/usr/bin/env python3
"""
generate.py — Run once to scaffold the entire Event-Driven Ordering System.
Usage:  python generate.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = {}

# ─────────────────────────────────────────────────────────
# shared-events
# ─────────────────────────────────────────────────────────
FILES["shared-events/pom.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.ordering</groupId>
    <artifactId>ordering-system</artifactId>
    <version>1.0.0</version>
  </parent>
  <artifactId>shared-events</artifactId>
  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.datatype</groupId>
      <artifactId>jackson-datatype-jsr310</artifactId>
    </dependency>
    <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <optional>true</optional>
    </dependency>
  </dependencies>
</project>
"""

SE = "shared-events/src/main/java/com/ordering/events"

FILES[f"{SE}/OrderPlacedEvent.java"] = """\
package com.ordering.events;

import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class OrderPlacedEvent {
    private String orderId;
    private String customerId;
    private String customerEmail;
    private List<OrderItem> items;
    private BigDecimal totalAmount;
    private LocalDateTime placedAt;

    @Data @Builder @NoArgsConstructor @AllArgsConstructor
    public static class OrderItem {
        private String productId;
        private String productName;
        private int quantity;
        private BigDecimal unitPrice;
    }
}
"""

FILES[f"{SE}/InventoryReservedEvent.java"] = """\
package com.ordering.events;

import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class InventoryReservedEvent {
    private String orderId;
    private String customerId;
    private String customerEmail;
    private BigDecimal totalAmount;
    private LocalDateTime reservedAt;
}
"""

FILES[f"{SE}/InventoryFailedEvent.java"] = """\
package com.ordering.events;

import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class InventoryFailedEvent {
    private String orderId;
    private String customerId;
    private String customerEmail;
    private String reason;
    private LocalDateTime failedAt;
}
"""

FILES[f"{SE}/PaymentProcessedEvent.java"] = """\
package com.ordering.events;

import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class PaymentProcessedEvent {
    private String orderId;
    private String customerId;
    private String customerEmail;
    private String transactionId;
    private BigDecimal amount;
    private LocalDateTime processedAt;
}
"""

FILES[f"{SE}/PaymentFailedEvent.java"] = """\
package com.ordering.events;

import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class PaymentFailedEvent {
    private String orderId;
    private String customerId;
    private String customerEmail;
    private String reason;
    private LocalDateTime failedAt;
}
"""

# ─────────────────────────────────────────────────────────
# order-service
# ─────────────────────────────────────────────────────────
FILES["order-service/pom.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.ordering</groupId>
    <artifactId>ordering-system</artifactId>
    <version>1.0.0</version>
  </parent>
  <artifactId>order-service</artifactId>
  <dependencies>
    <dependency><groupId>com.ordering</groupId><artifactId>shared-events</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
    <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>
    <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    <dependency><groupId>com.fasterxml.jackson.datatype</groupId><artifactId>jackson-datatype-jsr310</artifactId></dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

OS_PKG = "order-service/src/main/java/com/ordering/order"

FILES[f"{OS_PKG}/OrderServiceApplication.java"] = """\
package com.ordering.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
"""

FILES[f"{OS_PKG}/model/OrderStatus.java"] = """\
package com.ordering.order.model;
public enum OrderStatus { PENDING, INVENTORY_RESERVED, CONFIRMED, CANCELLED }
"""

FILES[f"{OS_PKG}/model/Order.java"] = """\
package com.ordering.order.model;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "orders")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Order {
    @Id
    private String id;
    private String customerId;
    private String customerEmail;
    @Enumerated(EnumType.STRING)
    private OrderStatus status;
    private BigDecimal totalAmount;
    @Column(columnDefinition = "TEXT")
    private String itemsJson;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
"""

FILES[f"{OS_PKG}/repository/OrderRepository.java"] = """\
package com.ordering.order.repository;

import com.ordering.order.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, String> {}
"""

FILES[f"{OS_PKG}/dto/CreateOrderRequest.java"] = """\
package com.ordering.order.dto;

import lombok.Data;
import java.math.BigDecimal;
import java.util.List;

@Data
public class CreateOrderRequest {
    private String customerId;
    private String customerEmail;
    private List<OrderItemDto> items;

    @Data
    public static class OrderItemDto {
        private String productId;
        private String productName;
        private int quantity;
        private BigDecimal unitPrice;
    }
}
"""

FILES[f"{OS_PKG}/config/KafkaConfig.java"] = """\
package com.ordering.order.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.*;
import org.springframework.kafka.support.serializer.JsonSerializer;
import java.util.*;

@Configuration
public class KafkaConfig {

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        props.put(JsonSerializer.ADD_TYPE_INFO_HEADERS, false);
        return new DefaultKafkaProducerFactory<>(props);
    }

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper m = new ObjectMapper();
        m.registerModule(new JavaTimeModule());
        m.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return m;
    }
}
"""

FILES[f"{OS_PKG}/kafka/OrderEventProducer.java"] = """\
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
"""

FILES[f"{OS_PKG}/kafka/OrderEventConsumer.java"] = """\
package com.ordering.order.kafka;

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

    @KafkaListener(topics = "payment.processed", groupId = "order-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onPaymentProcessed(PaymentProcessedEvent event) {
        log.info("✅ Payment processed for orderId={}", event.getOrderId());
        updateStatus(event.getOrderId(), OrderStatus.CONFIRMED);
    }

    @KafkaListener(topics = "payment.failed", groupId = "order-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onPaymentFailed(PaymentFailedEvent event) {
        log.warn("❌ Payment failed for orderId={}", event.getOrderId());
        updateStatus(event.getOrderId(), OrderStatus.CANCELLED);
    }

    @KafkaListener(topics = "inventory.failed", groupId = "order-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onInventoryFailed(InventoryFailedEvent event) {
        log.warn("❌ Inventory failed for orderId={}", event.getOrderId());
        updateStatus(event.getOrderId(), OrderStatus.CANCELLED);
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
"""

FILES[f"{OS_PKG}/kafka/KafkaConsumerConfig.java"] = """\
package com.ordering.order.kafka;

import com.ordering.events.*;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import java.util.*;

@Configuration
public class KafkaConsumerConfig {

    private ConsumerFactory<String, Object> factory(Class<?> targetType) {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-service-group");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        JsonDeserializer<Object> deser = new JsonDeserializer<>(targetType, false);
        deser.addTrustedPackages("com.ordering.events");
        return new DefaultKafkaConsumerFactory<>(props, new StringDeserializer(), deser);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object>
            kafkaListenerContainerFactory() {
        // Use a router deserializer that maps topics to types
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-service-group");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        props.put(JsonDeserializer.TRUSTED_PACKAGES, "com.ordering.events");
        props.put(JsonDeserializer.USE_TYPE_INFO_HEADERS, false);
        props.put(JsonDeserializer.VALUE_DEFAULT_TYPE, Object.class.getName());

        var factory = new ConcurrentKafkaListenerContainerFactory<String, Object>();
        factory.setConsumerFactory(new DefaultKafkaConsumerFactory<>(props));
        factory.setRecordMessageConverter(topicTypeMapper());
        return factory;
    }

    @Bean
    public org.springframework.kafka.support.converter.RecordMessageConverter topicTypeMapper() {
        var converter = new org.springframework.kafka.support.converter.StringJsonMessageConverter();
        var resolver = new org.springframework.kafka.support.mapping.DefaultJackson2JavaTypeMapper();
        resolver.setTypePrecedence(org.springframework.kafka.support.mapping.Jackson2JavaTypeMapper.TypePrecedence.TYPE_ID);
        Map<String, Class<?>> mappings = new HashMap<>();
        mappings.put("payment.processed", PaymentProcessedEvent.class);
        mappings.put("payment.failed",    PaymentFailedEvent.class);
        mappings.put("inventory.failed",  InventoryFailedEvent.class);
        resolver.setIdClassMapping(mappings);
        converter.setTypeMapper(resolver);
        return converter;
    }
}
"""

FILES[f"{OS_PKG}/service/OrderService.java"] = """\
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
"""

FILES[f"{OS_PKG}/controller/OrderController.java"] = """\
package com.ordering.order.controller;

import com.ordering.order.dto.CreateOrderRequest;
import com.ordering.order.model.Order;
import com.ordering.order.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService svc;

    @PostMapping
    public ResponseEntity<Order> create(@RequestBody CreateOrderRequest req) {
        return ResponseEntity.status(HttpStatus.CREATED).body(svc.createOrder(req));
    }

    @GetMapping
    public ResponseEntity<List<Order>> getAll() {
        return ResponseEntity.ok(svc.getAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Order> get(@PathVariable String id) {
        return ResponseEntity.ok(svc.getById(id));
    }
}
"""

FILES["order-service/src/main/resources/application.yml"] = """\
server:
  port: 8081

spring:
  application:
    name: order-service
  datasource:
    url: jdbc:postgresql://localhost:5432/orderdb
    username: ordering
    password: ordering123
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
  kafka:
    bootstrap-servers: localhost:9092

logging:
  level:
    com.ordering: DEBUG
"""

# ─────────────────────────────────────────────────────────
# inventory-service
# ─────────────────────────────────────────────────────────
FILES["inventory-service/pom.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.ordering</groupId>
    <artifactId>ordering-system</artifactId>
    <version>1.0.0</version>
  </parent>
  <artifactId>inventory-service</artifactId>
  <dependencies>
    <dependency><groupId>com.ordering</groupId><artifactId>shared-events</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
    <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>
    <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    <dependency><groupId>com.fasterxml.jackson.datatype</groupId><artifactId>jackson-datatype-jsr310</artifactId></dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

INV = "inventory-service/src/main/java/com/ordering/inventory"

FILES[f"{INV}/InventoryServiceApplication.java"] = """\
package com.ordering.inventory;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class InventoryServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(InventoryServiceApplication.class, args);
    }
}
"""

FILES[f"{INV}/model/Inventory.java"] = """\
package com.ordering.inventory.model;

import jakarta.persistence.*;
import lombok.*;

@Entity @Table(name = "inventory")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Inventory {
    @Id
    private String productId;
    private String productName;
    private int availableQuantity;
}
"""

FILES[f"{INV}/repository/InventoryRepository.java"] = """\
package com.ordering.inventory.repository;

import com.ordering.inventory.model.Inventory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InventoryRepository extends JpaRepository<Inventory, String> {}
"""

FILES[f"{INV}/kafka/InventoryEventProducer.java"] = """\
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
"""

FILES[f"{INV}/kafka/InventoryEventConsumer.java"] = """\
package com.ordering.inventory.kafka;

import com.ordering.events.OrderPlacedEvent;
import com.ordering.inventory.service.InventoryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class InventoryEventConsumer {

    private final InventoryService service;

    @KafkaListener(topics = "order.placed", groupId = "inventory-service-group")
    public void onOrderPlaced(OrderPlacedEvent event) {
        log.info("📥 OrderPlacedEvent → orderId={}", event.getOrderId());
        service.processOrderPlaced(event);
    }
}
"""

FILES[f"{INV}/service/InventoryService.java"] = """\
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
"""

FILES[f"{INV}/controller/InventoryController.java"] = """\
package com.ordering.inventory.controller;

import com.ordering.inventory.model.Inventory;
import com.ordering.inventory.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/inventory") @RequiredArgsConstructor
public class InventoryController {

    private final InventoryRepository repo;

    @GetMapping
    public ResponseEntity<List<Inventory>> getAll() { return ResponseEntity.ok(repo.findAll()); }

    @PostMapping
    public ResponseEntity<Inventory> save(@RequestBody Inventory inv) {
        return ResponseEntity.ok(repo.save(inv));
    }
}
"""

FILES[f"{INV}/config/KafkaConfig.java"] = """\
package com.ordering.inventory.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ordering.events.OrderPlacedEvent;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import org.springframework.kafka.support.serializer.JsonSerializer;
import java.util.*;

@Configuration
public class KafkaConfig {

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> p = new HashMap<>();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        p.put(JsonSerializer.ADD_TYPE_INFO_HEADERS, false);
        return new DefaultKafkaProducerFactory<>(p);
    }

    @Bean public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }

    @Bean
    public ConsumerFactory<String, OrderPlacedEvent> consumerFactory() {
        Map<String, Object> p = new HashMap<>();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p.put(ConsumerConfig.GROUP_ID_CONFIG, "inventory-service-group");
        p.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        JsonDeserializer<OrderPlacedEvent> deser =
            new JsonDeserializer<>(OrderPlacedEvent.class, false);
        deser.addTrustedPackages("com.ordering.events");
        return new DefaultKafkaConsumerFactory<>(p, new StringDeserializer(), deser);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderPlacedEvent>
            kafkaListenerContainerFactory() {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, OrderPlacedEvent>();
        factory.setConsumerFactory(consumerFactory());
        return factory;
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper m = new ObjectMapper();
        m.registerModule(new JavaTimeModule());
        m.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return m;
    }
}
"""

FILES[f"{INV}/config/DataInitializer.java"] = """\
package com.ordering.inventory.config;

import com.ordering.inventory.model.Inventory;
import com.ordering.inventory.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final InventoryRepository repo;

    @Override
    public void run(String... args) {
        if (repo.count() == 0) {
            repo.save(Inventory.builder().productId("P001").productName("Laptop").availableQuantity(50).build());
            repo.save(Inventory.builder().productId("P002").productName("Mouse").availableQuantity(200).build());
            repo.save(Inventory.builder().productId("P003").productName("Keyboard").availableQuantity(150).build());
            repo.save(Inventory.builder().productId("P004").productName("Monitor").availableQuantity(30).build());
            log.info("✅ Sample inventory seeded");
        }
    }
}
"""

FILES["inventory-service/src/main/resources/application.yml"] = """\
server:
  port: 8082

spring:
  application:
    name: inventory-service
  datasource:
    url: jdbc:postgresql://localhost:5432/inventorydb
    username: ordering
    password: ordering123
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
  kafka:
    bootstrap-servers: localhost:9092

logging:
  level:
    com.ordering: DEBUG
"""

# ─────────────────────────────────────────────────────────
# payment-service
# ─────────────────────────────────────────────────────────
FILES["payment-service/pom.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.ordering</groupId>
    <artifactId>ordering-system</artifactId>
    <version>1.0.0</version>
  </parent>
  <artifactId>payment-service</artifactId>
  <dependencies>
    <dependency><groupId>com.ordering</groupId><artifactId>shared-events</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
    <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>
    <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    <dependency><groupId>com.fasterxml.jackson.datatype</groupId><artifactId>jackson-datatype-jsr310</artifactId></dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

PAY = "payment-service/src/main/java/com/ordering/payment"

FILES[f"{PAY}/PaymentServiceApplication.java"] = """\
package com.ordering.payment;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PaymentServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(PaymentServiceApplication.class, args);
    }
}
"""

FILES[f"{PAY}/model/PaymentStatus.java"] = """\
package com.ordering.payment.model;
public enum PaymentStatus { PENDING, SUCCESS, FAILED }
"""

FILES[f"{PAY}/model/Payment.java"] = """\
package com.ordering.payment.model;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity @Table(name = "payments")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class Payment {
    @Id private String transactionId;
    private String orderId;
    private String customerId;
    private BigDecimal amount;
    @Enumerated(EnumType.STRING)
    private PaymentStatus status;
    private String failureReason;
    private LocalDateTime createdAt;
}
"""

FILES[f"{PAY}/repository/PaymentRepository.java"] = """\
package com.ordering.payment.repository;

import com.ordering.payment.model.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PaymentRepository extends JpaRepository<Payment, String> {
    List<Payment> findByOrderId(String orderId);
}
"""

FILES[f"{PAY}/kafka/PaymentEventProducer.java"] = """\
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
"""

FILES[f"{PAY}/kafka/PaymentEventConsumer.java"] = """\
package com.ordering.payment.kafka;

import com.ordering.events.InventoryReservedEvent;
import com.ordering.payment.service.PaymentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class PaymentEventConsumer {

    private final PaymentService service;

    @KafkaListener(topics = "inventory.reserved", groupId = "payment-service-group")
    public void onInventoryReserved(InventoryReservedEvent event) {
        log.info("📥 InventoryReservedEvent → orderId={}", event.getOrderId());
        service.processPayment(event);
    }
}
"""

FILES[f"{PAY}/service/PaymentService.java"] = """\
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
"""

FILES[f"{PAY}/controller/PaymentController.java"] = """\
package com.ordering.payment.controller;

import com.ordering.payment.model.Payment;
import com.ordering.payment.repository.PaymentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/payments") @RequiredArgsConstructor
public class PaymentController {

    private final PaymentRepository repo;

    @GetMapping
    public ResponseEntity<List<Payment>> getAll() { return ResponseEntity.ok(repo.findAll()); }

    @GetMapping("/order/{orderId}")
    public ResponseEntity<List<Payment>> byOrder(@PathVariable String orderId) {
        return ResponseEntity.ok(repo.findByOrderId(orderId));
    }
}
"""

FILES[f"{PAY}/config/KafkaConfig.java"] = """\
package com.ordering.payment.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ordering.events.InventoryReservedEvent;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import org.springframework.kafka.support.serializer.JsonSerializer;
import java.util.*;

@Configuration
public class KafkaConfig {

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> p = new HashMap<>();
        p.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        p.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        p.put(JsonSerializer.ADD_TYPE_INFO_HEADERS, false);
        return new DefaultKafkaProducerFactory<>(p);
    }

    @Bean public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }

    @Bean
    public ConsumerFactory<String, InventoryReservedEvent> consumerFactory() {
        Map<String, Object> p = new HashMap<>();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p.put(ConsumerConfig.GROUP_ID_CONFIG, "payment-service-group");
        p.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        JsonDeserializer<InventoryReservedEvent> d =
            new JsonDeserializer<>(InventoryReservedEvent.class, false);
        d.addTrustedPackages("com.ordering.events");
        return new DefaultKafkaConsumerFactory<>(p, new StringDeserializer(), d);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, InventoryReservedEvent>
            kafkaListenerContainerFactory() {
        var f = new ConcurrentKafkaListenerContainerFactory<String, InventoryReservedEvent>();
        f.setConsumerFactory(consumerFactory());
        return f;
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper m = new ObjectMapper();
        m.registerModule(new JavaTimeModule());
        m.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return m;
    }
}
"""

FILES["payment-service/src/main/resources/application.yml"] = """\
server:
  port: 8083

spring:
  application:
    name: payment-service
  datasource:
    url: jdbc:postgresql://localhost:5432/paymentdb
    username: ordering
    password: ordering123
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
  kafka:
    bootstrap-servers: localhost:9092

logging:
  level:
    com.ordering: DEBUG
"""

# ─────────────────────────────────────────────────────────
# notification-service
# ─────────────────────────────────────────────────────────
FILES["notification-service/pom.xml"] = """\
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
           https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.ordering</groupId>
    <artifactId>ordering-system</artifactId>
    <version>1.0.0</version>
  </parent>
  <artifactId>notification-service</artifactId>
  <dependencies>
    <dependency><groupId>com.ordering</groupId><artifactId>shared-events</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
    <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    <dependency><groupId>com.fasterxml.jackson.datatype</groupId><artifactId>jackson-datatype-jsr310</artifactId></dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

NTF = "notification-service/src/main/java/com/ordering/notification"

FILES[f"{NTF}/NotificationServiceApplication.java"] = """\
package com.ordering.notification;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class NotificationServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(NotificationServiceApplication.class, args);
    }
}
"""

FILES[f"{NTF}/service/NotificationService.java"] = """\
package com.ordering.notification.service;

import com.ordering.events.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j @Service
public class NotificationService {

    public void notifyConfirmed(PaymentProcessedEvent e) {
        log.info("📧 [EMAIL] To={} Subject='Order Confirmed' | orderId={} txId={} amount={}",
            e.getCustomerEmail(), e.getOrderId(), e.getTransactionId(), e.getAmount());
    }

    public void notifyPaymentFailed(PaymentFailedEvent e) {
        log.warn("📧 [EMAIL] To={} Subject='Order Cancelled - Payment Failed' | orderId={} reason={}",
            e.getCustomerEmail(), e.getOrderId(), e.getReason());
    }

    public void notifyInventoryFailed(InventoryFailedEvent e) {
        log.warn("📧 [EMAIL] To={} Subject='Order Cancelled - Out of Stock' | orderId={} reason={}",
            e.getCustomerEmail(), e.getOrderId(), e.getReason());
    }
}
"""

FILES[f"{NTF}/kafka/NotificationEventConsumer.java"] = """\
package com.ordering.notification.kafka;

import com.ordering.events.*;
import com.ordering.notification.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j @Component @RequiredArgsConstructor
public class NotificationEventConsumer {

    private final NotificationService service;

    @KafkaListener(topics = "payment.processed", groupId = "notification-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onPaymentProcessed(PaymentProcessedEvent e) {
        log.info("📥 PaymentProcessedEvent → orderId={}", e.getOrderId());
        service.notifyConfirmed(e);
    }

    @KafkaListener(topics = "payment.failed", groupId = "notification-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onPaymentFailed(PaymentFailedEvent e) {
        log.info("📥 PaymentFailedEvent → orderId={}", e.getOrderId());
        service.notifyPaymentFailed(e);
    }

    @KafkaListener(topics = "inventory.failed", groupId = "notification-service-group",
        containerFactory = "kafkaListenerContainerFactory")
    public void onInventoryFailed(InventoryFailedEvent e) {
        log.info("📥 InventoryFailedEvent → orderId={}", e.getOrderId());
        service.notifyInventoryFailed(e);
    }
}
"""

FILES[f"{NTF}/config/KafkaConfig.java"] = """\
package com.ordering.notification.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ordering.events.*;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;
import org.springframework.kafka.support.converter.StringJsonMessageConverter;
import org.springframework.kafka.support.mapping.DefaultJackson2JavaTypeMapper;
import org.springframework.kafka.support.mapping.Jackson2JavaTypeMapper;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import java.util.*;

@Configuration
public class KafkaConfig {

    @Bean
    public ConsumerFactory<String, Object> consumerFactory() {
        Map<String, Object> p = new HashMap<>();
        p.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        p.put(ConsumerConfig.GROUP_ID_CONFIG, "notification-service-group");
        p.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        p.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        p.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        p.put(JsonDeserializer.TRUSTED_PACKAGES, "com.ordering.events");
        p.put(JsonDeserializer.USE_TYPE_INFO_HEADERS, false);
        p.put(JsonDeserializer.VALUE_DEFAULT_TYPE, Object.class.getName());
        return new DefaultKafkaConsumerFactory<>(p);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object>
            kafkaListenerContainerFactory() {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, Object>();
        factory.setConsumerFactory(consumerFactory());
        factory.setRecordMessageConverter(topicTypeMapper());
        return factory;
    }

    @Bean
    public StringJsonMessageConverter topicTypeMapper() {
        var converter = new StringJsonMessageConverter();
        var resolver = new DefaultJackson2JavaTypeMapper();
        resolver.setTypePrecedence(Jackson2JavaTypeMapper.TypePrecedence.TYPE_ID);
        Map<String, Class<?>> mappings = new HashMap<>();
        mappings.put("payment.processed", PaymentProcessedEvent.class);
        mappings.put("payment.failed",    PaymentFailedEvent.class);
        mappings.put("inventory.failed",  InventoryFailedEvent.class);
        resolver.setIdClassMapping(mappings);
        converter.setTypeMapper(resolver);
        return converter;
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper m = new ObjectMapper();
        m.registerModule(new JavaTimeModule());
        m.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return m;
    }
}
"""

FILES["notification-service/src/main/resources/application.yml"] = """\
server:
  port: 8084

spring:
  application:
    name: notification-service
  kafka:
    bootstrap-servers: localhost:9092

logging:
  level:
    com.ordering: DEBUG
"""

# ─────────────────────────────────────────────────────────
# README
# ─────────────────────────────────────────────────────────
FILES["README.md"] = """\
# Event-Driven Ordering System

**Stack:** Java 17 · Spring Boot 3.2 · Apache Kafka · PostgreSQL · Lombok · Maven (multi-module)

## Event Flow

```
Step 1  POST /orders  →  Order Service saves PENDING  →  publishes  order.placed
Step 2  Inventory Service  receives order.placed
           OK  →  deducts stock  →  inventory.reserved
           FAIL →  inventory.failed
Step 3  Payment Service  receives inventory.reserved
           OK  (amount ≤ 10 000)  →  payment.processed
           FAIL (amount > 10 000) →  payment.failed
Step 4  Order Service  receives terminal event
           payment.processed   →  status = CONFIRMED
           payment.failed      →  status = CANCELLED
           inventory.failed    →  status = CANCELLED
Step 5  Notification Service  receives terminal event  →  logs email
```

## Kafka Topics

| Topic                | Producer          | Consumer(s)                           |
|----------------------|-------------------|---------------------------------------|
| order.placed         | order-service     | inventory-service                     |
| inventory.reserved   | inventory-service | payment-service                       |
| inventory.failed     | inventory-service | order-service, notification-service   |
| payment.processed    | payment-service   | order-service, notification-service   |
| payment.failed       | payment-service   | order-service, notification-service   |

## Services

| Service              | Port | DB          |
|----------------------|------|-------------|
| order-service        | 8081 | orderdb     |
| inventory-service    | 8082 | inventorydb |
| payment-service      | 8083 | paymentdb   |
| notification-service | 8084 | —           |
| kafka-ui             | 8080 | —           |

## Quick Start

```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Build all modules
mvn clean install -DskipTests

# 3. Start services (separate terminals)
cd order-service        && mvn spring-boot:run
cd inventory-service    && mvn spring-boot:run
cd payment-service      && mvn spring-boot:run
cd notification-service && mvn spring-boot:run

# 4. Place an order
curl -X POST http://localhost:8081/orders \\
  -H "Content-Type: application/json" \\
  -d '{
    "customerId": "C001",
    "customerEmail": "alice@example.com",
    "items": [
      {"productId":"P001","productName":"Laptop","quantity":1,"unitPrice":999.99},
      {"productId":"P002","productName":"Mouse","quantity":2,"unitPrice":29.99}
    ]
  }'

# 5. Check order status
curl http://localhost:8081/orders/{orderId}

# 6. Check inventory
curl http://localhost:8082/inventory

# 7. Check payments
curl http://localhost:8083/payments
```

## Business Rules (Demo)
- Payment **succeeds** when total amount ≤ 10,000
- Payment **fails**   when total amount > 10,000
- Inventory pre-seeded: Laptop×50, Mouse×200, Keyboard×150, Monitor×30
"""

# ─────────────────────────────────────────────────────────
# Write all files
# ─────────────────────────────────────────────────────────
created = 0
skipped = 0
for rel_path, content in FILES.items():
    full = os.path.join(BASE, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if os.path.exists(full):
        skipped += 1
        print(f"  SKIP (exists)  {rel_path}")
        continue
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    created += 1
    print(f"  CREATE  {rel_path}")

print(f"\n✅  Done — {created} files created, {skipped} skipped.")
print("Next: python generate.py  →  mvn clean install  →  docker-compose up -d  →  run each service")
