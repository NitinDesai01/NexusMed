import React from 'react';

const MessageBubble = ({ text, sender, timestamp }) => {
  const isBot = sender === 'bot';
  
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-2`}>
      <div className={`max-w-[80%] ${isBot ? 'mr-4' : 'ml-4'}`}>
        <div className={`p-3 rounded-lg ${
          isBot 
            ? 'bg-gray-100 text-gray-800 rounded-tl-none' 
            : 'bg-blue-500 text-white rounded-tr-none'
        }`}>
          <p className="whitespace-pre-wrap break-words">{text}</p>
        </div>
        {timestamp && (
          <div className={`text-xs text-gray-400 mt-1 ${isBot ? 'text-left' : 'text-right'}`}>
            {new Date(timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
