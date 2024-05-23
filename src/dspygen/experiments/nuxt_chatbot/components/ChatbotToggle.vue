<template>
    <button class="chatbot-toggler" @click="toggleChatbot">
      <span class="material-symbols-outlined">RFC</span>
      <span class="material-symbols-outlined">Done</span>
    </button>
  </template>
  
  <script setup>
  const toggleChatbot = () => {
    document.body.classList.toggle('show-chatbot')
  }
  </script>
  