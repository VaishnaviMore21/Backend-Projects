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
