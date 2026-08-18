import React, { useState, useRef, useEffect } from 'react';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm NexusMed Health Assistant. How can I help you today?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "Thank you for your question. I'm a demo assistant. Please consult a healthcare professional for medical advice.", 
        sender: 'bot' 
      }]);
      setIsTyping(false);
    }, 1000);
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 2px 15px rgba(0,0,0,0.08)',
      display: 'flex',
      flexDirection: 'column',
      height: '500px',
      overflow: 'hidden'
    }}>
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid #f3f4f6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: '#fafbfc'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            background: '#22c55e',
            animation: 'pulse 2s infinite'
          }}></div>
          <h3 style={{ fontWeight: 600, color: '#1f2937', fontSize: '16px' }}>Health Assistant</h3>
        </div>
        <span style={{ fontSize: '12px', color: '#6b7280' }}>Online</span>
      </div>

      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '16px 20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        background: '#fafbfc'
      }}>
        {messages.map((message, index) => (
          <div key={index} style={{
            display: 'flex',
            justifyContent: message.sender === 'bot' ? 'flex-start' : 'flex-end',
            marginBottom: '4px'
          }}>
            <div style={{
              maxWidth: '80%',
              padding: '10px 16px',
              borderRadius: '12px',
              wordWrap: 'break-word',
              lineHeight: 1.5,
              fontSize: '14px',
              background: message.sender === 'bot' ? 'white' : '#2563eb',
              color: message.sender === 'bot' ? '#1f2937' : 'white',
              borderBottomLeftRadius: message.sender === 'bot' ? '4px' : '12px',
              borderBottomRightRadius: message.sender === 'bot' ? '12px' : '4px',
              boxShadow: message.sender === 'bot' ? '0 1px 2px rgba(0,0,0,0.05)' : 'none'
            }}>
              {message.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 0'
          }}>
            <div style={{ display: 'flex', gap: '4px' }}>
              <span style={{
                width: '8px',
                height: '8px',
                background: '#9ca3af',
                borderRadius: '50%',
                animation: 'typingBounce 1.4s infinite both'
              }}></span>
              <span style={{
                width: '8px',
                height: '8px',
                background: '#9ca3af',
                borderRadius: '50%',
                animation: 'typingBounce 1.4s infinite both',
                animationDelay: '0.2s'
              }}></span>
              <span style={{
                width: '8px',
                height: '8px',
                background: '#9ca3af',
                borderRadius: '50%',
                animation: 'typingBounce 1.4s infinite both',
                animationDelay: '0.4s'
              }}></span>
            </div>
            <span style={{ fontSize: '13px', color: '#6b7280' }}>Assistant is typing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{
        padding: '12px 16px',
        borderTop: '1px solid #f3f4f6',
        display: 'flex',
        gap: '8px',
        background: 'white'
      }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
          placeholder="Type your health question..."
          style={{
            flex: 1,
            padding: '8px 12px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            resize: 'none',
            fontFamily: 'inherit',
            fontSize: '14px',
            outline: 'none',
            minHeight: '40px',
            maxHeight: '80px'
          }}
          rows={2}
        />
        <button
          onClick={handleSend}
          style={{
            padding: '8px 20px',
            background: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontWeight: 500,
            fontSize: '14px',
            cursor: 'pointer',
            alignSelf: 'flex-end',
            height: '40px'
          }}
        >
          Send
        </button>
      </div>

      <style>{`
        @keyframes typingBounce {
          0%, 60%, 100% {
            transform: translateY(0);
          }
          30% {
            transform: translateY(-8px);
          }
        }
      `}</style>
    </div>
  );
};

export default ChatBot;
