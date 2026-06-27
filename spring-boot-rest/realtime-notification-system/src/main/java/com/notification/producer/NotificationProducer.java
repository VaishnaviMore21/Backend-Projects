package com.notification.producer;

import com.notification.dto.NotificationEventDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationProducer {

    private final KafkaTemplate<String, NotificationEventDto> kafkaTemplate;

    private static final String NOTIFICATION_TOPIC = "notification-events";

    public void sendNotification(NotificationEventDto event) {
        try {
            String eventId = event.getEventId();
            if (eventId == null) {
                eventId = UUID.randomUUID().toString();
                event.setEventId(eventId);
            }

            Message<NotificationEventDto> message = MessageBuilder
                    .withPayload(event)
                    .setHeader(KafkaHeaders.TOPIC, NOTIFICATION_TOPIC)
                    .setHeader("kafka_messageKey", event.getRecipientId())
                    .setHeader("X-Priority", event.getPriority())
                    .build();

            kafkaTemplate.send(message);
            log.info("Notification event published: eventId={}, recipient={}, channel={}", 
                    eventId, event.getRecipientId(), event.getChannel());

        } catch (Exception e) {
            log.error("Failed to publish notification event", e);
            throw new RuntimeException("Failed to publish notification event", e);
        }
    }

    public void sendNotificationBatch(java.util.List<NotificationEventDto> events) {
        events.forEach(this::sendNotification);
        log.info("Published batch of {} notification events", events.size());
    }
}
