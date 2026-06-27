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
