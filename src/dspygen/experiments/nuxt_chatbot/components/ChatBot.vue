<template>
    <div class="chatbot">
      <header>
        <h2>cRAGbot</h2>
        <span class="close-btn material-symbols-outlined" @click="closeChatbot">Done</span>
      </header>
      <ul class="chatbox">
        <li class="chat outgoing" v-if="userMessage">
          <p v-html="userMessage.message"></p>
        </li>
        <li v-for="(chat, index) in chats" :key="index" :class="`chat ${index % 2 === 0 ? 'incoming' : 'outgoing'}`">
          <span v-if="index % 2 === 0" class="material-symbols-outlined">CB</span>
          <p v-html="chat.message"></p>
        </li>
      </ul>
      <div class="chat-input-container">
        <div class="model-selector">
          <select id="model-select" v-model="selectedModel">
            <option value="groq:llama3-70b-8192">Groq: Llama3-70B-8192</option>
            <option value="openai:gpt-4">OpenAI: GPT-4</option>
            <option value="openai:gpt-4o">OpenAI: GPT-4o</option>
          </select>
        </div>
        <div class="chat-input">
          <textarea v-model="message" placeholder="Enter a message..." spellcheck="false" @keydown="handleKeydown"></textarea>
          <button @click="sendChat">Send</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useFetch } from '#imports'
  
  const chats = ref([{ message: "Hi 👋🏼 <br> May I help you?" }])
  const userMessage = ref(null)
  const responseMessage = ref(null)
  const message = ref('')
  const selectedModel = ref('groq:llama3-70b-8192')
  
  const closeChatbot = () => {
    document.body.classList.remove('show-chatbot')
  }
  
  const updateServiceAndModel = () => {
    const [service, model] = selectedModel.value.split(':')
    return { service, model }
  }
  
  const sendChat = async () => {
    if (message.value.trim() === '') return
    const userMessageContent = message.value.trim()
    const { service, model } = updateServiceAndModel()
    userMessage.value = { message: userMessageContent }
  
    try {
      const { data, error } = await useFetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message: userMessageContent, service, model }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      if (error.value) {
        throw new Error(error.value)
      }
      responseMessage.value = { message: data.value.text }

      chats.value.unshift(userMessage.value)
      chats.value.unshift(responseMessage.value)
      userMessage.value = null
      responseMessage.value = null
    } catch (error) {
      console.error('Error fetching response:', error)
      responseMessage.value = { message: 'Oops! Something went wrong. Please try again.' }
    }
  
    message.value = ''
  }
  
  const handleKeydown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && window.innerWidth > 800) {
      e.preventDefault()
      sendChat()
    }
  }
  </script>
  
  <style scoped>
  .chatbot-toggler {
    position: fixed;
    right: 40px;
    bottom: 35px;
    height: 50px;
    width: 50px;
    color: #7d4141;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    outline: none;
    background: #5d6d4f;
    cursor: pointer;
    border-radius: 50%;
    transition: all 0.2s ease;
  }
  
  .show-chatbot .chatbot-toggler {
    transform: rotate(90deg);
  }
  
  .chatbot-toggler span {
    position: absolute;
  }
  
  .show-chatbot .chatbot-toggler span:first-child,
  .chatbot-toggler span:last-child {
    opacity: 0;
  }
  
  .show-chatbot .chatbot-toggler span:last-child {
    opacity: 1;
  }
  
  .chatbot {
    position: fixed;
    right: 40px;
    bottom: 100px;
    width: 520px;
    transform: scale(0.5);
    opacity: 0;
    pointer-events: none;
    overflow: hidden;
    background: #683535;
    border-radius: 15px;
    transform-origin: bottom right;
    box-shadow: 0 0 128px 0 rgba(0, 0, 0, 0.1),
      0 32px 64px -48px rgba(0, 0, 0, 0.5);
    transition: all 0.1s ease;
  }
  
  .show-chatbot .chatbot {
    transform: scale(1);
    opacity: 1;
    pointer-events: auto;
  }
  
  .chatbot header {
    background: #49445a;
    padding: 18px 0;
    text-align: center;
    position: relative;
  }
  
  .chatbot header h2 {
    color: #fff;
    font-size: 1.4rem;
  }
  
  .chatbot header span {
    position: absolute;
    right: 20px;
    top: 50%;
    color: #fff;
    cursor: pointer;
    display: none;
    transform: translateY(-50%);
  }
  
  .chatbot .chatbox {
    height: 510px;
    overflow-y: auto;
    padding: 15px 20px 70px 20px;
  }
  
  .chatbox .chat {
    display: flex;
  }
  
  .chatbox .chat p {
    color: #fff;
    max-width: 75%;
    white-space: pre-wrap;
    font-size: 0.95rem;
    padding: 12px 16px;
    border-radius: 10px 10px 0px 10px;
    background: #5d6d4f;
  }
  
  .chatbox .chat p.error {
    color: #721c24;
    background: #f8d7da;
  }
  
  .chatbox .incoming span {
    height: 32px;
    width: 32px;
    color: #fff;
    align-self: flex-end;
    background: #5d6d4f;
    text-align: center;
    line-height: 32px;
    border-radius: 8px;
    margin: 0 10px 7px 0;
  }
  
  .chatbox .outgoing {
    margin: 20px 0;
    justify-content: flex-end;
  }
  
  .chatbox .incoming p {
    color: #000;
    background: #f2f2f2;
    padding: 12px 16px;
    border-radius: 10px 10px 10px 0;
    font-size: 0.95rem;
  }
  
  .chatbot .chat-input-container {
    position: absolute;
    bottom: 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    background: #f2f2f2;
    padding: 5px 20px;
    border-top: 1px solid #d2c3c3;
  }
  
  .model-selector {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  .model-selector label {
    font-size: 0.95rem;
    color: #49445a;
  }
  
  .model-selector select {
    padding: 5px 10px;
    border: 1px solid #d2c3c3;
    border-radius: 5px;
    background: #fff;
    color: #000;
  }
  
  .chat-input {
    display: flex;
    gap: 5px;
  }
  
  .chat-input textarea {
    height: 55px;
    width: 100%;
    border: none;
    outline: none;
    max-height: 180px;
    font-size: 0.95rem;
    resize: none;
    padding: 16px 15px 16px 0;
    background: #3e337a;
  }
  
  .chat-input button {
    align-self: flex-end;
    height: 55px;
    line-height: 55px;
    color: #fff;
    background: #5d6d4f;
    border: none;
    padding: 0 20px;
    font-size: 1.35rem;
    cursor: pointer;
    border-radius: 5px;
    transition: background 0.3s ease;
  }
  
  .chat-input button:hover {
    background: #4b5a40;
  }
  
  @media (max-width: 490px) {
    .chatbot {
      right: 0;
      bottom: 0;
      width: 100%;
      height: 100%;
      border-radius: 0;
    }
  
    .chatbot .chatbox {
      height: 90%;
    }
  
    .chatbot header span {
      display: block;
    }
  }
  </style>
  