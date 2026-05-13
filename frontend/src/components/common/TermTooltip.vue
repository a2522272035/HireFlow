<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="term-tooltip-overlay"
      :style="tooltipStyle"
      @click.stop
    >
      <div class="term-tooltip-card">
        <div class="term-header">
          <span class="term-name">{{ term }}</span>
          <span v-if="sourceLabel" class="term-source">{{ sourceLabel }}</span>
          <button class="close-btn" @click="close">&times;</button>
        </div>
        <div v-if="loading" class="term-loading">
          <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          <span class="loading-label">正在查询</span>
        </div>
        <div v-else-if="explanation" class="term-explanation" v-html="formattedExplanation"></div>
        <div v-else class="term-error">暂无解释</div>
        <button class="ask-ai-btn" @click="askAI" :disabled="loading || !explanation">
          <span class="ai-icon">🤖</span> 问AI
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

const API_BASE = '/api/v1/ai'

const visible = ref(false)
const term = ref('')
const explanation = ref('')
const loading = ref(false)
const position = ref({ x: 0, y: 0 })
const sourceLabel = ref('')
const explanationCache = new Map()
let requestSeq = 0

const tooltipStyle = computed(() => ({
  left: position.value.x + 'px',
  top: position.value.y + 'px'
}))

const formattedExplanation = computed(() => {
  if (!explanation.value) return ''
  return explanation.value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>')
})

async function show(termText, event) {
  const currentSeq = ++requestSeq
  term.value = termText
  explanation.value = ''
  sourceLabel.value = ''
  loading.value = true
  visible.value = true

  await nextTick()

  const target = event.currentTarget || event.target
  const rect = target.getBoundingClientRect()
  const tooltipW = 320
  const tooltipH = 200
  let x = rect.left + rect.width / 2 - tooltipW / 2
  let y = rect.bottom + 10

  if (x < 8) x = 8
  if (x + tooltipW > window.innerWidth) x = window.innerWidth - tooltipW - 8
  if (y + tooltipH > window.innerHeight) y = rect.top - tooltipH - 8

  position.value = { x, y }

  const cacheKey = termText
  if (explanationCache.has(cacheKey)) {
    explanation.value = explanationCache.get(cacheKey).explanation
    sourceLabel.value = explanationCache.get(cacheKey).sourceLabel
    loading.value = false
    return
  }

  try {
    const res = await fetch(`${API_BASE}/explain-term`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ term: termText })
    })

    if (currentSeq !== requestSeq) return

    if (!res.ok || !res.body) {
      if (currentSeq === requestSeq) loading.value = false
      return
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let fullText = ''
    let isLocal = false

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      if (currentSeq !== requestSeq) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          let data = line.slice(6)
          if (!data) continue

          if (!isLocal && data.startsWith('__local__')) {
            isLocal = true
            data = data.slice(9)
            sourceLabel.value = ' 知识库'
          }

          fullText += data
          explanation.value = fullText
          if (!isLocal && !sourceLabel.value) {
            sourceLabel.value = ' AI 生成中...'
          }
          await new Promise(r => setTimeout(r, 30))
        }
      }
    }

    if (currentSeq !== requestSeq) return
    if (!isLocal && sourceLabel.value === ' AI 生成中...') {
      sourceLabel.value = ' AI 生成'
    }
    explanationCache.set(cacheKey, {
      explanation: fullText,
      sourceLabel: sourceLabel.value
    })
  } catch (e) {
    if (currentSeq === requestSeq) {
      explanation.value = ''
    }
    console.error('Explain term error:', e)
  } finally {
    if (currentSeq === requestSeq) {
      loading.value = false
    }
  }
}

function close() {
  visible.value = false
  term.value = ''
  explanation.value = ''
  sourceLabel.value = ''
}

function askAI() {
  window.dispatchEvent(new CustomEvent('ai-interview-ask', {
    detail: { message: `请解释一下「${term.value}」是什么意思？` }
  }))
  close()
}

document.addEventListener('click', (e) => {
  if (visible.value && !e.target.closest('.term-tooltip-overlay') && !e.target.closest('.term-clickable')) {
    close()
  }
})

defineExpose({ show, close })
</script>

<style scoped>
.term-tooltip-overlay {
  position: fixed;
  z-index: 9999;
}

.term-tooltip-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  width: 300px;
  padding: 14px 16px;
  font-size: 13px;
  border: 1px solid #e8ecf2;
}

.term-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.term-name {
  font-size: 15px;
  font-weight: 700;
  color: #335EEA;
}

.term-source {
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(51, 94, 234, 0.08);
  color: #335EEA;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #9aabbf;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}

.close-btn:hover {
  color: #5a6a7e;
}

.term-loading {
  display: flex;
  gap: 4px;
  align-items: center;
  justify-content: center;
  padding: 16px 0;
}

.loading-label {
  margin-left: 6px;
  color: #8695a8;
  font-size: 12px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #335EEA;
  animation: pulse 1.2s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s }
.dot:nth-child(3) { animation-delay: 0.4s }

@keyframes pulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8) }
  40% { opacity: 1; transform: scale(1) }
}

.term-explanation {
  color: #5a6a7e;
  line-height: 1.7;
  margin-bottom: 12px;
  padding: 8px 0;
}

.term-error {
  color: #9aabbf;
  text-align: center;
  padding: 8px 0;
  font-size: 12px;
}

.ask-ai-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 8px 0;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.ask-ai-btn:hover {
  opacity: 0.9;
}

.ask-ai-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-icon {
  font-size: 15px;
}
</style>
