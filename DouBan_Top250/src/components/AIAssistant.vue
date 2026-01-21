<template>
  <div>
    <!-- AI 助手按钮 -->
    <el-button 
      @click="aiStore.toggleDrawer" 
      class="ai-toggle-btn"
      type="primary"
      :icon="ChatDotRound"
      circle
    >
    </el-button>

    <!-- AI 对话抽屉 -->
    <el-drawer
      v-model="aiStore.drawerVisible"
      :with-header="false"
      direction="rtl"
      size="400px"
      class="ai-drawer"
      @close="onClose"
    >
      <div class="ai-chat-container">
        <div class="chat-header">
          <h3>AI 电影助手</h3>
          <el-button 
            @click="aiStore.toggleDrawer" 
            type="text" 
            :icon="Close"
            class="close-btn"
          />
        </div>
        
        <div class="chat-messages" ref="chatContainerRef">
          <div 
            v-for="(msg, index) in aiStore.messages" 
            :key="index" 
            :class="['message', msg.role]"
          >
            <div class="message-content">
              <div v-if="msg.role === 'assistant'" class="assistant-icon">
                <el-icon><ChatLineRound /></el-icon>
              </div>
              <div class="content-text">{{ msg.content }}</div>
              <div v-if="msg.role === 'user'" class="user-icon">
                <el-icon><User /></el-icon>
              </div>
            </div>
          </div>
          
          <!-- 加载指示器 -->
          <div v-if="aiStore.isLoading" class="message assistant">
            <div class="message-content">
              <div class="assistant-icon">
                <el-icon><ChatLineRound /></el-icon>
              </div>
              <div class="content-text typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input-area">
          <el-input
            v-model="aiStore.inputText"
            placeholder="询问电影相关信息..."
            @keyup.enter="handleSendMessage"
            :disabled="aiStore.isLoading"
            class="chat-input"
          >
            <template #suffix>
              <el-button 
                @click="handleSendMessage" 
                type="primary" 
                :disabled="!aiStore.inputText.trim() || aiStore.isLoading"
                :icon="Promotion"
              />
            </template>
          </el-input>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from 'vue';
import { useAIStore } from '@/stores/store';
import { 
  ChatDotRound, 
  Close, 
  ChatLineRound, 
  User, 
  Promotion 
} from '@element-plus/icons-vue';

// 使用 Pinia store
const aiStore = useAIStore();
const chatContainerRef = ref(null);



// 发送消息处理函数
const handleSendMessage = async () => {
  if (!aiStore.inputText.trim() || aiStore.isLoading) return;
  await aiStore.sendMessage();
  scrollToBottom();
};

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainerRef.value) {
    chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight;
  }
};

// 监听消息变化，自动滚动到底部
watch(() => aiStore.messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
}, { deep: true });

// 关闭抽屉时的处理
const onClose = () => {
  // 可以在这里添加清理逻辑
};

// 组件挂载后初始化
onMounted(() => {
  // 初始化逻辑
});

// 导出 store 供父组件使用
defineExpose({
  aiStore
});
</script>

<style scoped>
.ai-toggle-btn {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 9999;
  width: 60px;
  height: 60px;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
}

.ai-toggle-btn:hover,
.ai-toggle-btn:focus {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.ai-drawer {
  :deep(.el-drawer__body) {
    padding: 0;
    display: flex;
    flex-direction: column;
  }
}

.ai-chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
}

.chat-header h3 {
  margin: 0;
  font-weight: 500;
}

.close-btn {
  color: white;
  font-size: 18px;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background-color: #f9f9f9;
}

.message {
  display: flex;
  max-width: 90%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.assistant-icon,
.user-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  flex-shrink: 0;
}

.assistant-icon {
  background-color: #667eea;
  color: white;
}

.user-icon {
  background-color: #764ba2;
  color: white;
}

.content-text {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user .content-text {
  background-color: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .content-text {
  background-color: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #999;
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.6;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input-area {
  padding: 20px;
  border-top: 1px solid #eee;
  background-color: white;
}

.chat-input {
  width: 100%;
}

.chat-input :deep(.el-input__wrapper) {
  border-radius: 24px;
}

.chat-input :deep(.el-input__suffix) {
  display: flex;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ai-toggle-btn {
    right: 15px;
    bottom: 15px;
    width: 50px;
    height: 50px;
  }
  
  .ai-drawer {
    :deep(.el-drawer) {
      --el-drawer-size: 320px;
    }
  }
  
  .message {
    max-width: 95%;
  }
}
</style>