package com.example.chat.controller;

import com.example.chat.dto.ChatMessageInbound;
import com.example.chat.dto.ChatMessageResponse;
import com.example.chat.dto.RoomCreateRequest;
import com.example.chat.dto.RoomResponse;
import com.example.chat.service.ChatService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/rooms")
public class ChatRoomController {

    private final ChatService chatService;

    public ChatRoomController(ChatService chatService) {
        this.chatService = chatService;
    }

    @PostMapping
    public ResponseEntity<RoomResponse> createRoom(@Valid @RequestBody RoomCreateRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(chatService.createRoom(request));
    }

    @GetMapping
    public ResponseEntity<List<RoomResponse>> getRooms() {
        return ResponseEntity.ok(chatService.getRooms());
    }

    @GetMapping("/{roomId}/messages")
    public ResponseEntity<List<ChatMessageResponse>> getRecentMessages(@PathVariable Long roomId) {
        return ResponseEntity.ok(chatService.getLatestMessages(roomId));
    }

    @PostMapping("/{roomId}/messages")
    public ResponseEntity<ChatMessageResponse> postMessage(@PathVariable Long roomId,
                                                           @Valid @RequestBody ChatMessageInbound request) {
        ChatMessageResponse response = chatService.saveMessage(roomId, request.senderId(), request.content());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
