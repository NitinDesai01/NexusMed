import { io } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000';

let socket = null;

export const connectSocket = (token) => {
  if (!socket) {
    socket = io(SOCKET_URL, {
      auth: { token },
      transports: ['websocket'],
    });

    socket.on('connect', () => {
      console.log('Socket connected');
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });

    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });
  }
  return socket;
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const getSocket = () => socket;

export const sendMessage = (event, data) => {
  if (socket) {
    socket.emit(event, data);
  }
};

export const onMessage = (event, callback) => {
  if (socket) {
    socket.on(event, callback);
  }
};

export const offMessage = (event, callback) => {
  if (socket) {
    socket.off(event, callback);
  }
};