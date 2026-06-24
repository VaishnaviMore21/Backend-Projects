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
