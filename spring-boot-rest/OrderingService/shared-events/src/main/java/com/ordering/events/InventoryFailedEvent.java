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
