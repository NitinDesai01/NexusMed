import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);

  const addNotification = (notification) => {
    setNotifications(prev => [notification, ...prev]);
  };

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const value = {
    theme,
    notifications,
    addNotification,
    removeNotification,
    toggleTheme: () => setTheme(prev => prev === 'light' ? 'dark' : 'light'),
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
