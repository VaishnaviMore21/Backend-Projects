package com.urlshortner.repository;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Repository;

@Repository
public class UrlIdSequenceRepository {

    @PersistenceContext
    private EntityManager entityManager;

    public long nextId() {
        Number nextValue = (Number) entityManager
                .createNativeQuery("SELECT nextval(pg_get_serial_sequence('url_mapping', 'id'))")
                .getSingleResult();

        return nextValue.longValue();
    }
}

