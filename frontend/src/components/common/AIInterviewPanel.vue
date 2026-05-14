<template>
  <aside class="ai-panel">
    <div class="ai-header">
      <div class="ai-title">
        <span class="robot-icon">🤖</span>
        <span>AI面试助手</span>
      </div>
      <button class="close-btn" @click="closePanel">×</button>
    </div>

    <!-- AI分析 -->
    <section class="ai-section">
      <div class="section-header">
        <h3>AI分析</h3>
        <button class="refresh-btn" @click="reAnalyze" :disabled="isLoading">↻ 重新分析</button>
      </div>

      <div class="analysis-group">
        <div class="group-header" @click="showAnalysis = !showAnalysis">
          <span class="group-title">AI分析详情</span>
          <span class="collapse-arrow" :class="{ expanded: showAnalysis }">▼</span>
        </div>
        <div class="group-content" v-show="showAnalysis">
          <div class="score-card">
            <div>
              <p class="label">岗位匹配度</p>
              <p class="score">{{ matchScore }}%</p>
            </div>
            <span class="score-icon">✓</span>
          </div>

          <div class="analysis-card success">
            <div class="card-title">
              <span>👍</span>
              <strong>核心优势</strong>
            </div>
            <ul>
              <li v-for="(item, index) in coreAdvantages" :key="index">{{ item }}</li>
            </ul>
          </div>

          <div class="analysis-card warning">
            <div class="card-title">
              <span>⚠️</span>
              <strong>潜在风险</strong>
            </div>
            <ul>
              <li v-for="(item, index) in potentialRisks" :key="index">{{ item }}</li>
            </ul>
          </div>

          <div class="analysis-card info">
            <div class="card-title">
              <span>🎯</span>
              <strong>建议追问方向</strong>
            </div>
            <ul>
              <li v-for="(item, index) in followUpDirections" :key="index">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="question-card">
        <div>
          <h4>面试问题生成</h4>
          <p>基于简历生成针对性面试问题，支持按方向一键生成。</p>
        </div>
        <button @click="generateQuestions" :disabled="isLoading">生成问题</button>
      </div>
    </section>

    <!-- AI对话窗口 -->
    <section class="chat-section">
      <h3>AI对话窗口</h3>

      <div class="chat-list" ref="chatContainer">
        <div
          v-for="(msg, index) in messages"
          :key="`${msg.id}-${index}-${renderKey}`"
          class="message"
          :class="msg.role"
          :data-id="msg.id"
        >
          <div class="avatar">
            {{ msg.role === 'user' ? '面' : 'AI' }}
          </div>

          <div class="bubble-wrap">
            <div class="meta">
              {{ msg.role === 'user' ? '面试官' : 'AI助手' }}
              <span>{{ msg.time }}</span>
            </div>
            <div class="bubble" v-html="getBubbleContent(msg)"></div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="inputText"
          placeholder="继续追问候选人经历 / 让 AI 生成更多问题"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">➤</button>
      </div>
    </section>
  </aside>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'

const API_BASE = '/api/v1/ai'

const props = defineProps({
  resumeData: {
    type: Object,
    default: () => ({})
  },
  profilerData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close'])

const inputText = ref('')
const showAnalysis = ref(true)
const isLoading = ref(false)

const matchScore = ref(0)
const coreAdvantages = ref([])
const potentialRisks = ref([])
const followUpDirections = ref([])

const messages = ref([])
const chatContainer = ref(null)
const chatHistory = ref([])
const renderKey = ref(0)

// 监听来自外部（如TermTooltip）的AI提问请求
let askTimeout = null
window.addEventListener('ai-ask-message', (e) => {
  if (e.detail?.message) {
    inputText.value = e.detail.message
    if (askTimeout) clearTimeout(askTimeout)
    askTimeout = setTimeout(() => {
      askTimeout = null
      sendMessage()
    }, 300)
  }
})

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

function forceRender() {
  renderKey.value++
}

function getBubbleContent(msg) {
  if (msg.content) return msg.content
  return '<span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>'
}

async function callAnalyze() {
  if (!props.resumeData || !props.resumeData.name) return
  isLoading.value = true
  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_data: props.resumeData,
        profiler_data: props.profilerData || null,
      }),
    })
    const json = await res.json()
    if (json.success && json.data) {
      const d = json.data
      coreAdvantages.value = d.coreAdvantages || []
      potentialRisks.value = d.potentialRisks || []
      followUpDirections.value = d.followUpDirections || []
      const highlights = props.profilerData?.highlights?.items?.length || 0
      const risks = props.profilerData?.risks?.items?.length || 0
      matchScore.value = Math.max(50, Math.min(98, 80 + highlights * 3 - risks * 5))
    }
  } catch (e) {
    console.error('分析失败:', e)
    coreAdvantages.value = ['候选人履历值得关注']
    potentialRisks.value = ['需要进一步沟通确认']
    followUpDirections.value = ['请结合简历深入追问']
    matchScore.value = 75
  } finally {
    isLoading.value = false
  }
}

async function reAnalyze() {
  messages.value.push({
    id: Date.now(),
    role: 'ai',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    content: '正在重新分析简历，请稍候...'
  })
  scrollToBottom()
  await callAnalyze()
  const lastMsg = messages.value[messages.value.length - 1]
  if (lastMsg && lastMsg.content.includes('正在重新分析')) {
    lastMsg.content = `重新分析完成！岗位匹配度 ${matchScore.value}%，核心优势 ${coreAdvantages.value.length} 项，潜在风险 ${potentialRisks.value.length} 项。`
  }
  scrollToBottom()
}

async function sendMessage(forcedText = '') {
  const externalText = typeof forcedText === 'string' ? forcedText : ''
  const userMsg = (externalText || inputText.value).trim()
  if (!userMsg || isLoading.value) return

  inputText.value = ''

  messages.value.push({
    id: Date.now(),
    role: 'user',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    content: userMsg,
  })
  chatHistory.value.push({ role: 'user', content: userMsg })
  scrollToBottom()

  isLoading.value = true
  const aiMsgId = Date.now() + 1
  messages.value.push({
    id: aiMsgId,
    role: 'ai',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    content: ''
  })
  scrollToBottom()

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMsg,
        history: chatHistory.value.slice(-10),
        resume_data: props.resumeData,
      }),
    })

    if (!res.ok || !res.body) {
      const msg = messages.value.find(m => m.id === aiMsgId)
      if (msg) msg.content = '抱歉，AI 服务暂时不可用，请稍后重试。'
    } else {
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let fullText = ''
      const msgIdx = messages.value.findIndex(m => m.id === aiMsgId)

      await nextTick()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data) {
              fullText += data
              // 在"考察："前插入两个空行
              let processed = fullText.replace(/(\?|。|！|\n)?考察：/g, '\n\n\n考察：')
              // 在列表项（1. 2. 3. 等）前自动插入空行，但保留第一个
              processed = processed.replace(/([^\n\d])\n?(\d+\.)/g, '$1\n\n$2')
              messages.value[msgIdx].content = processed
              messages.value = [...messages.value]
              forceRender()
              scrollToBottom()
              await new Promise(r => setTimeout(r, 30))
            }
          }
        }
      }

      chatHistory.value.push({ role: 'assistant', content: fullText })
    }
  } catch (e) {
    console.error('对话失败:', e)
    const lastMsg = messages.value[messages.value.length - 1]
    if (lastMsg && lastMsg.role === 'ai' && !lastMsg.content) {
      lastMsg.content = '网络错误，请检查后端服务是否正常运行。'
    }
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

async function generateQuestions() {
  if (isLoading.value) return
  isLoading.value = true

  // 点击生成问题后自动收起AI分析详情
  showAnalysis.value = false

  const aiMsgId = Date.now()
  messages.value.push({
    id: aiMsgId,
    role: 'ai',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    content: ''
  })
  scrollToBottom()

  try {
    const res = await fetch(`${API_BASE}/generate-questions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_data: props.resumeData,
      }),
    })

    if (!res.ok || !res.body) {
      const msg = messages.value.find(m => m.id === aiMsgId)
      if (msg) msg.content = '问题生成失败，请稍后重试。'
    } else {
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let fullText = ''
      const msgIdx = messages.value.findIndex(m => m.id === aiMsgId)

      await nextTick()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data) {
              fullText += data
              // 在"考察："前插入两个空行
              let processed = fullText.replace(/(\?|。|！|\n)?考察：/g, '\n\n\n考察：')
              // 在列表项（1. 2. 3. 等）前自动插入空行，但保留第一个
              processed = processed.replace(/([^\n\d])\n?(\d+\.)/g, '$1\n\n$2')
              messages.value[msgIdx].content = processed
              messages.value = [...messages.value]
              forceRender()
              scrollToBottom()
              await new Promise(r => setTimeout(r, 30))
            }
          }
        }
      }
    }
  } catch (e) {
    console.error('生成问题失败:', e)
    const lastMsg = messages.value[messages.value.length - 1]
    if (lastMsg && lastMsg.role === 'ai' && !lastMsg.content) {
      lastMsg.content = '网络错误，请检查后端服务。'
    }
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const closePanel = () => {
  emit('close')
}

let analyzed = false
watch(
  () => props.resumeData?.name,
  (name) => {
    if (name && !isLoading.value && !analyzed) {
      analyzed = true
      callAnalyze()
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.ai-panel {
  position: fixed;
  top: 64px;
  right: 0;
  width: 540px;
  height: calc(100vh - 64px);
  background: #ffffff;
  border-left: 1px solid #e5eaf3;
  box-shadow: -4px 0 16px rgba(31, 56, 88, 0.08);
  display: flex;
  flex-direction: column;
  padding: 16px;
  box-sizing: border-box;
  overflow-y: auto;
  z-index: 200;
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.ai-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: #1f2d3d;
}

.robot-icon {
  font-size: 22px;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 22px;
  color: #8a94a6;
  cursor: pointer;
  line-height: 1;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f5f5f5;
}

.ai-section {
  padding-bottom: 12px;
  border-bottom: 1px solid #edf0f5;
  margin-bottom: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3,
.chat-section h3 {
  font-size: 15px;
  color: #2563eb;
  margin: 0 0 12px;
}

.refresh-btn {
  border: none;
  background: transparent;
  color: #2563eb;
  cursor: pointer;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: rgba(37, 99, 235, 0.1);
}

.score-card,
.analysis-card,
.question-card {
  border: 1px solid #e6eaf0;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 10px;
  background: #fff;
}

.score-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

.score {
  margin: 4px 0 0;
  font-size: 28px;
  font-weight: 700;
  color: #22c55e;
}

.score-icon {
  color: #22c55e;
  font-size: 22px;
}

.analysis-card .card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  color: #1f2d3d;
}

.analysis-group {
  border: 1px solid #e6eaf0;
  border-radius: 12px;
  margin-bottom: 10px;
  overflow: hidden;
}

.analysis-group .group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: #f8fafc;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.analysis-group .group-header:hover {
  background: #f1f5f9;
}

.analysis-group .group-title {
  font-size: 14px;
  font-weight: 600;
  color: #2563eb;
}

.analysis-group .collapse-arrow {
  font-size: 10px;
  transition: transform 0.3s ease;
  transform: rotate(-90deg);
}

.analysis-group .collapse-arrow.expanded {
  transform: rotate(0deg);
}

.analysis-group .group-content {
  padding: 10px;
  border-top: 1px solid #e6eaf0;
}

.analysis-group .analysis-card {
  border: none;
  padding: 10px;
  margin-bottom: 6px;
  background: #fff;
  border-radius: 8px;
}

.analysis-group .analysis-card:last-child {
  margin-bottom: 0;
}

.analysis-group .score-card {
  border: none;
  padding: 10px;
  margin-bottom: 10px;
  background: #fff;
  border-radius: 8px;
}

.analysis-card ul {
  margin: 0;
  padding-left: 22px;
  color: #4b5563;
  font-size: 13px;
  line-height: 1.7;
  transition: all 0.3s ease;
}

.analysis-card li {
  margin-bottom: 4px;
}

.analysis-card li:last-child {
  margin-bottom: 0;
}

.analysis-card.success {
  background: #f6fffb;
}

.analysis-card.warning {
  background: #fffaf4;
}

.analysis-card.info {
  background: #f6f9ff;
}

.question-card {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.question-card h4 {
  margin: 0 0 4px;
  font-size: 14px;
}

.question-card p {
  margin: 0;
  color: #6b7280;
  font-size: 12px;
  line-height: 1.5;
}

.question-card button,
.chat-input button {
  border: none;
  background: #2563eb;
  color: #fff;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s;
}

.question-card button:hover,
.chat-input button:hover {
  background: #1d4ed8;
}

.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 14px;
  min-height: 0;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.message {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #dbeafe;
  color: #2563eb;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.ai .avatar {
  background: #eef2ff;
  color: #6366f1;
}

.bubble-wrap {
  max-width: 260px;
}

.meta {
  font-size: 12px;
  color: #8a94a6;
  margin-bottom: 4px;
}

.meta span {
  margin-left: 6px;
}

.bubble {
  padding: 10px 12px;
  border-radius: 12px;
  background: #f3f6fb;
  color: #374151;
  font-size: 13px;
  line-height: 1.7;
  word-break: break-word;
  white-space: pre-line;
}

.message.user .bubble {
  background: #dbeafe;
  color: #1e40af;
}

.chat-input {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.chat-input input {
  flex: 1;
  border: 1px solid #d8dee9;
  border-radius: 8px;
  padding: 10px;
  outline: none;
  font-size: 13px;
  transition: border-color 0.2s;
}

.chat-input input:focus {
  border-color: #2563eb;
}

.typing-dots span {
  animation: blink 1.4s infinite both;
  font-size: 20px;
  line-height: 1;
}
.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
}
</style>
