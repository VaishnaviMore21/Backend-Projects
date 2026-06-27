package com.example.chat.service;

import com.example.chat.domain.ChatMessage;
import com.example.chat.domain.ChatRoom;
import com.example.chat.domain.User;
import com.example.chat.dto.ChatMessageResponse;
import com.example.chat.dto.RoomCreateRequest;
import com.example.chat.dto.RoomResponse;
import com.example.chat.exception.ConflictException;
import com.example.chat.exception.NotFoundException;
import com.example.chat.repository.ChatMessageRepository;
import com.example.chat.repository.ChatRoomRepository;
import com.example.chat.repository.UserRepository;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ChatService {

    private final ChatRoomRepository chatRoomRepository;
    private final ChatMessageRepository chatMessageRepository;
    private final UserRepository userRepository;

    public ChatService(ChatRoomRepository chatRoomRepository,
                       ChatMessageRepository chatMessageRepository,
                       UserRepository userRepository) {
        this.chatRoomRepository = chatRoomRepository;
        this.chatMessageRepository = chatMessageRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public RoomResponse createRoom(RoomCreateRequest request) {
        chatRoomRepository.findByName(request.name()).ifPresent(r -> {
            throw new ConflictException("Room name already exists");
        });

        ChatRoom room = new ChatRoom();
        room.setName(request.name());
        ChatRoom saved = chatRoomRepository.save(room);
        return new RoomResponse(saved.getId(), saved.getName(), saved.getCreatedAt());
    }

    @Transactional(readOnly = true)
    public List<RoomResponse> getRooms() {
        return chatRoomRepository.findAll().stream()
            .map(room -> new RoomResponse(room.getId(), room.getName(), room.getCreatedAt()))
            .toList();
    }

    @Transactional
    public ChatMessageResponse saveMessage(Long roomId, Long senderId, String content) {
        ChatRoom room = chatRoomRepository.findById(roomId)
            .orElseThrow(() -> new NotFoundException("Room not found: " + roomId));
        User user = userRepository.findById(senderId)
            .orElseThrow(() -> new NotFoundException("User not found: " + senderId));

        ChatMessage message = new ChatMessage();
        message.setRoom(room);
        message.setSender(user);
        message.setContent(content);

        ChatMessage saved = chatMessageRepository.save(message);
        return toResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<ChatMessageResponse> getLatestMessages(Long roomId) {
        if (!chatRoomRepository.existsById(roomId)) {
            throw new NotFoundException("Room not found: " + roomId);
        }
        return chatMessageRepository.findTop100ByRoomIdOrderByCreatedAtDesc(roomId).stream()
            .map(this::toResponse)
            .toList();
    }

    private ChatMessageResponse toResponse(ChatMessage message) {
        return new ChatMessageResponse(
            message.getId(),
            message.getRoom().getId(),
            message.getSender().getId(),
            message.getSender().getUsername(),
            message.getContent(),
            message.getCreatedAt()
        );
    }
}
