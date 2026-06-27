package com.example.chat.controller;

import com.example.chat.dto.ChatMessageInbound;
import com.example.chat.dto.ChatMessageResponse;
import com.example.chat.service.ChatService;
import jakarta.validation.Valid;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;

@Controller
public class ChatWebSocketController {

    private final ChatService chatService;
    private final SimpMessagingTemplate messagingTemplate;

    public ChatWebSocketController(ChatService chatService, SimpMessagingTemplate messagingTemplate) {
        this.chatService = chatService;
        this.messagingTemplate = messagingTemplate;
    }

    @MessageMapping("/chat.send/{roomId}")
    public void sendMessage(@DestinationVariable Long roomId,
                            @Valid @Payload ChatMessageInbound request) {
        ChatMessageResponse response = chatService.saveMessage(roomId, request.senderId(), request.content());
        messagingTemplate.convertAndSend("/topic/rooms/" + roomId, response);
    }
}
