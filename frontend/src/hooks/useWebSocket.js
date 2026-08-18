import { useState, useEffect, useCallback } from 'react';
import { connectSocket, onMessage, offMessage, sendMessage } from '../services/socket';

export const useWebSocket = (event) => {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const socket = connectSocket(token);
      
      socket.on('connect', () => {
        setIsConnected(true);
      });

      socket.on('disconnect', () => {
        setIsConnected(false);
      });

      onMessage(event, (data) => {
        setMessages(prev => [...prev, data]);
      });

      return () => {
        offMessage(event);
      };
    }
  }, [event]);

  const send = useCallback((data) => {
    sendMessage(event, data);
  }, [event]);

  return { messages, send, isConnected };
};