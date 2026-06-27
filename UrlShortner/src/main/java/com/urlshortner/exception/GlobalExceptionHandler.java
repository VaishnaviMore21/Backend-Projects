package com.urlshortner.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(InvalidUrlException.class)
    public ResponseEntity<Map<String, Object>> handleInvalidUrl(InvalidUrlException exception) {
        return buildResponse(HttpStatus.BAD_REQUEST, exception.getMessage());
    }

    @ExceptionHandler(ShortCodeNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleShortCodeNotFound(ShortCodeNotFoundException exception) {
        return buildResponse(HttpStatus.NOT_FOUND, exception.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException exception) {
        FieldError firstFieldError = exception.getBindingResult().getFieldError();
        String errorMessage = "Validation failed";
        if (firstFieldError != null) {
            errorMessage = firstFieldError.getField() + ": " + firstFieldError.getDefaultMessage();
        }

        return buildResponse(HttpStatus.BAD_REQUEST, errorMessage);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleUnexpected(Exception exception) {
        return buildResponse(HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred");
    }

    private ResponseEntity<Map<String, Object>> buildResponse(HttpStatus status, String message) {
        Map<String, Object> responseBody = new LinkedHashMap<String, Object>();
        responseBody.put("error", message);
        responseBody.put("status", Integer.valueOf(status.value()));
        responseBody.put("timestamp", new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX").format(new Date()));

        return ResponseEntity.status(status).body(responseBody);
    }
}

