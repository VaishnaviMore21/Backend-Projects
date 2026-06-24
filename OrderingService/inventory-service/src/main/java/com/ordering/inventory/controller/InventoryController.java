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
