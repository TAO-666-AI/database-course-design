<template>
  <section class="chat-page">
    <div class="chat-head">
      <div class="brand-logo">问</div>
      <div>
        <h1>中山陵文本问答</h1>
        <p>围绕中山陵景点、路线、预约、交通和游览须知进行问答</p>
      </div>
      <button class="history-toggle" @click="showHistory = !showHistory">历史</button>
    </div>
    <div class="suggestions">
      <button v-for="q in quick" :key="q" @click="ask(q)">{{ q }}</button>
    </div>
    <div class="history-panel" v-if="showHistory">
      <div class="history-head">
        <strong>历史问答</strong>
        <button @click="startNewChat">新问答</button>
      </div>
      <div v-if="historyLoading" class="history-empty">正在加载历史记录...</div>
      <div v-else-if="!histories.length" class="history-empty">暂无历史问答</div>
      <button
        v-for="item in histories"
        v-else
        :key="item.session_id"
        class="history-item"
        :class="{ active: item.session_id === sessionId }"
        @click="openHistory(item.session_id)"
      >
        <span>{{ item.title }}</span>
        <em>{{ item.updated_at }} · {{ item.message_count }} 条</em>
      </button>
    </div>
    <div class="messages" ref="boxRef">
      <div class="msg assistant">你好，我是景区导览助手。你可以问我景点、路线、门票、开放时间等问题。</div>
      <div v-for="(m, index) in messages" :key="index" class="msg" :class="m.role">
        <span>{{ m.content }}</span>
        <em v-if="m.role === 'assistant' && m.source">来源：{{ sourceText(m.source) }}</em>
      </div>
    </div>
    <div class="chat-input">
      <el-input v-model="question" size="large" placeholder="请输入中山陵相关问题，例如：中山陵需要预约吗？" @keyup.enter="send" />
      <el-button type="primary" circle :loading="loading" @click="send"><Promotion /></el-button>
    </div>
  </section>
</template>

<script setup>
import { Promotion } from '@element-plus/icons-vue'
import { nextTick, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getChatDetail, getChatHistory, sendChat } from '../../api/tourist'

const question = ref('')
const loading = ref(false)
const historyLoading = ref(false)
const sessionId = ref('')
const messages = ref([])
const histories = ref([])
const showHistory = ref(false)
const boxRef = ref(null)
const route = useRoute()
const quick = ['中山陵需要预约吗？', '中山陵门票多少钱？', '推荐一条2小时路线', '音乐台有什么特色？']
const sourceText = (v) => ({ faq: 'FAQ', deepseek: 'DeepSeek', fallback: '兜底回复' }[v] || v)
const scrollBottom = () => nextTick(() => (boxRef.value.scrollTop = boxRef.value.scrollHeight))
const loadHistories = async () => {
  historyLoading.value = true
  try {
    const res = await getChatHistory()
    if (res.code === 200) histories.value = res.data.items
  } finally {
    historyLoading.value = false
  }
}
const openHistory = async (id) => {
  const res = await getChatDetail(id)
  if (res.code === 200) {
    sessionId.value = id
    messages.value = res.data.items
    showHistory.value = false
    scrollBottom()
  }
}
const startNewChat = () => {
  sessionId.value = ''
  messages.value = []
  showHistory.value = false
}
const ask = (q) => {
  question.value = q
  send()
}
const send = async () => {
  const q = question.value.trim()
  if (!q) return
  messages.value.push({ role: 'user', content: q })
  question.value = ''
  loading.value = true
  scrollBottom()
  try {
    const res = await sendChat({ question: q, session_id: sessionId.value || undefined })
    if (res.code === 200) {
      sessionId.value = res.data.session_id
      messages.value.push({ role: 'assistant', content: res.data.reply, source: res.data.source })
      loadHistories()
    }
  } finally {
    loading.value = false
    scrollBottom()
  }
}
onMounted(() => {
  showHistory.value = route.query.history === '1'
  loadHistories()
})
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 134px);
  display: flex;
  flex-direction: column;
}
.chat-head {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-bottom: 14px;
}
.history-toggle {
  margin-left: auto;
  border: 1px solid #bfe6e2;
  background: #fff;
  color: var(--primary-dark);
  border-radius: 999px;
  padding: 8px 14px;
  white-space: nowrap;
  cursor: pointer;
}
h1 {
  margin: 0;
}
p {
  margin: 6px 0 0;
  color: var(--muted);
}
.suggestions {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 8px 0 16px;
}
.suggestions button {
  white-space: nowrap;
  border: 1px solid #bfe6e2;
  color: var(--primary-dark);
  background: #fff;
  border-radius: 999px;
  padding: 10px 16px;
  cursor: pointer;
}
.history-panel {
  background: #fff;
  border-radius: 16px;
  padding: 12px;
  margin-bottom: 12px;
  box-shadow: 0 10px 24px rgba(25, 68, 91, 0.05);
}
.history-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.history-head button {
  border: 0;
  background: #e9f7f5;
  color: var(--primary-dark);
  border-radius: 999px;
  padding: 6px 12px;
  cursor: pointer;
}
.history-empty {
  color: #8ca0b4;
  padding: 10px 4px;
}
.history-item {
  width: 100%;
  border: 1px solid #edf2f5;
  background: #fff;
  border-radius: 12px;
  padding: 10px 12px;
  margin-top: 8px;
  display: block;
  text-align: left;
  cursor: pointer;
}
.history-item.active {
  border-color: var(--primary);
  background: #f0fbfa;
}
.history-item span,
.history-item em {
  display: block;
}
.history-item span {
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.history-item em {
  color: #8ca0b4;
  font-style: normal;
  font-size: 12px;
  margin-top: 4px;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 2px;
}
.msg {
  max-width: 82%;
  margin-bottom: 14px;
  padding: 13px 15px;
  border-radius: 16px;
  line-height: 1.7;
}
.msg.user {
  margin-left: auto;
  background: var(--primary);
  color: #fff;
}
.msg.assistant {
  background: #fff;
  color: var(--text);
}
.msg em {
  display: block;
  font-style: normal;
  color: #8ca0b4;
  font-size: 12px;
  margin-top: 4px;
}
.chat-input {
  display: grid;
  grid-template-columns: 1fr 48px;
  gap: 10px;
  padding-top: 10px;
}
.chat-input :deep(.el-button svg) {
  width: 22px;
  height: 22px;
}
</style>
