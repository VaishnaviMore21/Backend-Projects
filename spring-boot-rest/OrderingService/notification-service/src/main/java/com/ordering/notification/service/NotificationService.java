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
