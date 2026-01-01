import { defineStore } from 'pinia';

export const useAIStore = defineStore('ai', {
  state: () => ({
    drawerVisible: false,
    inputText: '',
    messages: [
      { 
        role: 'assistant', 
        content: '你好！我是AI电影助手，可以为你介绍豆瓣Top250电影的相关信息。有什么想了解的吗？' 
      }
    ],
    isLoading: false,
    moviesData: [],
  }),

  actions: {
    toggleDrawer() {
      this.drawerVisible = !this.drawerVisible;
    },

    setDrawerVisible(visible) {
      this.drawerVisible = visible;
    },

    setInputText(text) {
      this.inputText = text;
    },

    addMessage(message) {
      this.messages.push(message);
    },

    updateMessage(index, content) {
      if (this.messages[index]) {
        this.messages[index].content = content;
      }
    },

    clearMessages() {
      this.messages = [
        { 
          role: 'assistant', 
          content: '你好！我是AI电影助手，可以为你介绍豆瓣Top250电影的相关信息。有什么想了解的吗？' 
        }
      ];
    },

    setLoading(loading) {
      this.isLoading = loading;
    },

    setMoviesData(data) {
      this.moviesData = data;
    },

    async sendMessage() {
      if (!this.inputText.trim() || this.isLoading) return;

      // 添加用户消息
      const userMessage = { 
        role: 'user', 
        content: this.inputText 
      };
      this.addMessage(userMessage);
      const currentInput = this.inputText;
      this.inputText = '';
      this.setLoading(true);

      try {
        // 调用AI API
        const aiResponse = await this.callAIAssistant(currentInput);
        
        this.addMessage({
          role: 'assistant',
          content: '好的'
        });
        this.setMoviesData(aiResponse);
        
        console.log(aiResponse)
      } catch (error) {
        this.addMessage({
          role: 'assistant',
          content: '抱歉，出现了一些问题，请稍后再试。'
        });
      } finally {
        this.setLoading(false);
      }
    },

    async callAIAssistant(query) {
      try {
        const response = await fetch('http://localhost:8000/api/v1/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: query })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results;
      } catch (error) {
        console.error('AI API Error:', error);
        return '抱歉，AI助手暂时无法响应，请稍后再试。';
      }
    }
  },

  getters: {
    getMessages: (state) => state.messages,
    getUserMessages: (state) => state.messages.filter(msg => msg.role === 'user'),
    getAssistantMessages: (state) => state.messages.filter(msg => msg.role === 'assistant'),
    getLastMessage: (state) => state.messages.length > 0 ? state.messages[state.messages.length - 1] : null,
    isDrawerOpen: (state) => state.drawerVisible,
    isSending: (state) => state.isLoading,
  }
});