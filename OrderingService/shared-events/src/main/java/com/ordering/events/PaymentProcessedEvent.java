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
