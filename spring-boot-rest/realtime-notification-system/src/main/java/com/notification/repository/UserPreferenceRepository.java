package com.notification.repository;

import com.notification.entity.UserPreference;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserPreferenceRepository extends JpaRepository<UserPreference, String> {

    Optional<UserPreference> findByUserId(String userId);
}
