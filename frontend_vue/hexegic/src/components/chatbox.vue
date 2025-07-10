<template>
    <div class="chatbox">
        <div class="messages">
            <div
                v-for="(msg, idx) in messages"
                :key="idx"
                :class="['message', msg.role]"
            >
                <span class="role">{{ msg.role === 'user' ? 'You' : 'AI' }}:</span>
                <span class="content">{{ msg.content }}</span>
            </div>
        </div>
        <form @submit.prevent="sendMessage('question')" class="input-area">
            <input
                v-model="input"
                type="text"
                placeholder="Type your message..."
                :disabled="loading"
                required
            />
            <button type="button" :disabled="loading || !input.trim()" @click="sendMessage('question')">Ask</button>
            <button type="button" :disabled="loading || !input.trim()" @click="sendMessage('contextsearch')">Context Search</button>
        </form>
    </div>
</template>

<script>
export default {
    name: "Chatbox",
    data() {
        return {
            input: "",
            messages: [],
            loading: false,
        };
    },
    methods: {
        async sendMessage(type) {
            if (!this.input.trim()) return;
            const userMsg = { role: "user", content: this.input };
            this.messages.push(userMsg);
            const userInput = this.input;
            this.input = "";
            this.loading = true;
            let endpoint = "";
            let body = {};
            if (type === "question") {
                endpoint = `${import.meta.env.VITE_API_URL}/llm/question`;
                body = { query: userInput };
            } else if (type === "contextsearch") {
                endpoint = `${import.meta.env.VITE_API_URL}/llm/contextsearch`;
                body = { query: userInput };
            }
            try {
                const response = await fetch(endpoint, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(body),
                });
                const data = await response.json();
                this.messages.push({
                    role: "assistant",
                    content: data.content || data.reply || "No response from LLM.",
                });
            } catch (e) {
                this.messages.push({
                    role: "assistant",
                    content: "Error: Unable to reach LLM backend.",
                });
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
.chatbox {
    border: 1px solid #ccc;
    border-radius: 8px;
    width: 500px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    height: 600px;
    background: #fafafa;
}
.messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}
.message {
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
}
.message.user .role {
    color: #1976d2;
    font-weight: bold;
}
.message.assistant .role {
    color: #43a047;
    font-weight: bold;
}
.message .content {
    color: #000; /* Set output text to black */
}
.input-area {
    display: flex;
    border-top: 1px solid #eee;
    padding: 8px;
    background: #fff;
}
.input-area input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.input-area button {
    margin-left: 8px;
    padding: 8px 16px;
    background: #1976d2;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.input-area button:disabled {
    background: #aaa;
    cursor: not-allowed;
}
</style>