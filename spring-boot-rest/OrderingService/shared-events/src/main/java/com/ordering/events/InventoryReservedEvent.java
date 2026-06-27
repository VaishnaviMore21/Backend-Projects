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
