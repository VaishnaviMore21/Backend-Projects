package com.notification.repository;

import com.notification.entity.NotificationTemplate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface NotificationTemplateRepository extends JpaRepository<NotificationTemplate, String> {

    Optional<NotificationTemplate> findByTemplateNameAndChannelAndIsActiveTrue(
            String templateName, String channel);

    Optional<NotificationTemplate> findByTemplateName(String templateName);
}
