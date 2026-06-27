let stompClient = null;
let activeRoom = null;
let currentUser = { id: null, username: null, token: null };

const els = {};

function bindElements() {
    [
        'healthBadge', 'apiStatus', 'wsStatus', 'refreshHealthBtn',
        'lookupUsername', 'lookupUserBtn', 'lookupResult',
        'authUsername', 'authEmail', 'authPassword', 'registerBtn', 'loginBtn',
        'currentUsername', 'currentUserId', 'tokenState',
        'loadRoomsBtn', 'newRoomBtn', 'roomName', 'createRoomBtn', 'roomsList',
        'activeRoomLabel', 'activeRoomName', 'activeRoomId', 'messagesList',
        'messageSenderId', 'messageContent', 'sendMessageBtn',
        'connectWsBtn', 'disconnectWsBtn', 'loadMessagesBtn'
    ].forEach((id) => { els[id] = document.getElementById(id); });
}

function setBadge(el, text, kind) {
    el.textContent = text;
    el.className = `badge ${kind}`;
}

function renderMessageCard(message) {
    const item = document.createElement('div');
    item.className = 'message-item';
    item.innerHTML = `
        <div class="message-meta">
            <strong>@${message.senderUsername}</strong>
            <span>#${message.id} • user ${message.senderId}</span>
        </div>
        <div class="message-content">${escapeHtml(message.content)}</div>
    `;
    return item;
}

function escapeHtml(text) {
    return String(text)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

async function checkHealth() {
    try {
        const response = await fetch('/actuator/health');
        const data = await response.json();
        const isUp = data.status === 'UP';
        setBadge(els.healthBadge, data.status, isUp ? 'ok' : 'warn');
        els.apiStatus.textContent = isUp ? 'Available' : 'Degraded';
    } catch (error) {
        setBadge(els.healthBadge, 'DOWN', 'warn');
        els.apiStatus.textContent = 'Unavailable';
    }
}

async function lookupUser() {
    const username = els.lookupUsername.value.trim();
    if (!username) return;
    const response = await fetch(`/api/users/by-username/${encodeURIComponent(username)}`);
    if (!response.ok) {
        els.lookupResult.textContent = 'User not found';
        return;
    }
    const user = await response.json();
    els.lookupResult.innerHTML = `<strong>${user.username}</strong><span>senderId: ${user.id}</span>`;
    els.messageSenderId.value = user.id;
}

async function registerUser() {
    const payload = {
        username: els.authUsername.value.trim(),
        email: els.authEmail.value.trim(),
        password: els.authPassword.value.trim()
    };
    const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Register failed');
    setCurrentUser(payload.username, null, data.token);
    const userResponse = await fetch(`/api/users/by-username/${encodeURIComponent(payload.username)}`);
    if (userResponse.ok) {
        const user = await userResponse.json();
        setCurrentUser(user.username, user.id, data.token);
        els.messageSenderId.value = user.id;
    }
}

async function loginUser() {
    const payload = {
        username: els.authUsername.value.trim(),
        password: els.authPassword.value.trim()
    };
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Login failed');
    setCurrentUser(payload.username, null, data.token);
    const userResponse = await fetch(`/api/users/by-username/${encodeURIComponent(payload.username)}`);
    if (userResponse.ok) {
        const user = await userResponse.json();
        setCurrentUser(user.username, user.id, data.token);
        els.messageSenderId.value = user.id;
    }
}

function setCurrentUser(username, id, token) {
    currentUser = { username, id, token };
    els.currentUsername.textContent = username || 'Guest';
    els.currentUserId.textContent = id ?? '-';
    els.tokenState.textContent = token ? `${token.slice(0, 18)}...` : 'Not set';
    if (id) els.messageSenderId.value = id;
}

async function loadRooms() {
    const response = await fetch('/api/rooms');
    const rooms = await response.json();
    els.roomsList.innerHTML = '';
    rooms.forEach((room) => {
        const item = document.createElement('div');
        item.className = `room-item ${activeRoom?.id === room.id ? 'active' : ''}`;
        item.innerHTML = `
            <div>
                <strong>${escapeHtml(room.name)}</strong>
                <span>ID ${room.id}</span>
            </div>
            <span>${new Date(room.createdAt).toLocaleString()}</span>
        `;
        item.addEventListener('click', () => selectRoom(room));
        els.roomsList.appendChild(item);
    });
    if (!rooms.length) {
        els.roomsList.innerHTML = '<div class="result-card">No rooms yet</div>';
    }
}

async function createRoom() {
    const name = els.roomName.value.trim();
    if (!name) return;
    const response = await fetch('/api/rooms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Room creation failed');
    els.roomName.value = '';
    await loadRooms();
    await selectRoom(data);
}

async function selectRoom(room) {
    activeRoom = room;
    els.activeRoomName.textContent = room.name;
    els.activeRoomId.textContent = room.id;
    els.activeRoomLabel.textContent = `Room ${room.name} selected`;
    await loadMessages();
    connectWs();
    await loadRooms();
}

async function loadMessages() {
    if (!activeRoom) {
        els.messagesList.innerHTML = '<div class="result-card">Select a room first</div>';
        return;
    }
    const response = await fetch(`/api/rooms/${activeRoom.id}/messages`);
    const messages = await response.json();
    els.messagesList.innerHTML = '';
    if (!messages.length) {
        els.messagesList.innerHTML = '<div class="result-card">No messages in this room yet</div>';
        return;
    }
    messages.reverse().forEach((message) => els.messagesList.appendChild(renderMessageCard(message)));
}

async function sendMessage() {
    if (!activeRoom) throw new Error('Select a room first');
    const senderId = Number(els.messageSenderId.value);
    const content = els.messageContent.value.trim();
    if (!senderId || !content) return;
    const response = await fetch(`/api/rooms/${activeRoom.id}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ senderId, content })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Message send failed');
    els.messageContent.value = '';
    await loadMessages();
}

function connectWs() {
    if (!activeRoom || stompClient?.connected) return;
    const socket = new SockJS('/ws');
    stompClient = Stomp.over(socket);
    stompClient.debug = null;
    stompClient.connect({}, () => {
        els.wsStatus.textContent = 'Connected';
        setBadge(els.healthBadge, 'UP', 'ok');
        stompClient.subscribe(`/topic/rooms/${activeRoom.id}`, (frame) => {
            const message = JSON.parse(frame.body);
            els.messagesList.prepend(renderMessageCard(message));
        });
    }, () => {
        els.wsStatus.textContent = 'Disconnected';
    });
}

function disconnectWs() {
    if (stompClient) {
        stompClient.disconnect(() => {
            els.wsStatus.textContent = 'Disconnected';
        });
        stompClient = null;
    }
}

function wireEvents() {
    els.refreshHealthBtn.addEventListener('click', checkHealth);
    els.lookupUserBtn.addEventListener('click', () => lookupUser().catch(showError));
    els.registerBtn.addEventListener('click', () => registerUser().catch(showError));
    els.loginBtn.addEventListener('click', () => loginUser().catch(showError));
    els.loadRoomsBtn.addEventListener('click', () => loadRooms().catch(showError));
    els.newRoomBtn.addEventListener('click', () => els.roomName.focus());
    els.createRoomBtn.addEventListener('click', () => createRoom().catch(showError));
    els.sendMessageBtn.addEventListener('click', () => sendMessage().catch(showError));
    els.connectWsBtn.addEventListener('click', connectWs);
    els.disconnectWsBtn.addEventListener('click', disconnectWs);
    els.loadMessagesBtn.addEventListener('click', () => loadMessages().catch(showError));
}

function showError(error) {
    els.lookupResult.textContent = error.message || 'Something went wrong';
}

async function init() {
    bindElements();
    wireEvents();
    await checkHealth();
    await loadRooms();
}

document.addEventListener('DOMContentLoaded', init);
