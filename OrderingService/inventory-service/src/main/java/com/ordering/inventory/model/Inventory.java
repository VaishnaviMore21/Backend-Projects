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
