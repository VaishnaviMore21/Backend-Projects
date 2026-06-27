package com.example.chat.controller;

import com.example.chat.domain.User;
import com.example.chat.dto.UserLookupResponse;
import com.example.chat.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/by-username/{username}")
    public ResponseEntity<UserLookupResponse> getByUsername(@PathVariable String username) {
        User user = userService.findByUsernameOrThrow(username);
        return ResponseEntity.ok(new UserLookupResponse(user.getId(), user.getUsername()));
    }
}
