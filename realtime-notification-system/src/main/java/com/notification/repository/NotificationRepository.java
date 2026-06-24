package com.notification.repository;

import com.notification.entity.Notification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, String> {

    List<Notification> findByRecipientIdOrderByCreatedAtDesc(String recipientId);

    List<Notification> findByStatus(String status);

    List<Notification> findByStatusAndRetryCountLessThan(String status, Integer retryCount);

    @Query("SELECT n FROM Notification n WHERE n.status = 'FAILED' AND n.retryCount < n.maxRetries " +
           "AND n.updatedAt < :retryAfter ORDER BY n.priority DESC, n.createdAt ASC")
    List<Notification> findFailedNotificationsForRetry(LocalDateTime retryAfter);

    List<Notification> findByChannel(String channel);

    @Query("SELECT COUNT(n) FROM Notification n WHERE n.recipientId = ?1 AND n.status = 'SENT' " +
           "AND n.createdAt >= ?2")
    long countSentNotifications(String recipientId, LocalDateTime since);
}
