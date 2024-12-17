<template>
    <div class="notification-container">
      <div
        v-for="(notification, index) in notifications"
        :key="index"
        :class="['notification', notification.type]"
      >
        <span class="notification-message">{{ notification.message }}</span>
        <button class="close-button" @click="$emit('dismiss', notification.id)">✖</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      notifications: {
        type: Array,
        required: true,
      },
    }
  };
  </script>
  
  <style>
  .notification-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    align-items: center; 
  }
  
  .notification {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    background-color: #f2dede; 
    color: #a94442; 
    padding: 1rem;
    margin: 0; 
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid #ddd;
  }
  
  .notification.info {
    background-color: #d9edf7;
    color: #31708f;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 18px;
    color: inherit; 
    cursor: pointer;
    margin-left: auto; 
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  .notification-message {
    flex-grow: 1; 
    text-align: center; 
  }
  </style>
  