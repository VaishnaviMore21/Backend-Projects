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
