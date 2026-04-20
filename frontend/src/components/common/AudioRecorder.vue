<template>
  <div class="audio-recorder">
    <el-button
      :type="isRecording ? 'danger' : 'primary'"
      :icon="isRecording ? 'CircleClose' : 'Microphone'"
      @click="toggleRecording"
      size="large"
      circle
    />
    <div v-if="isRecording" class="recording-indicator">
      <span class="recording-dot"></span>
      <span class="recording-time">{{ formattedTime }}</span>
    </div>
    <div v-if="transcript" class="transcript-preview">
      <p>{{ transcript }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

const props = defineProps({
  interviewId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['transcript'])

const isRecording = ref(false)
const recordingTime = ref(0)
const transcript = ref('')
let mediaRecorder = null
let audioChunks = []
let timerInterval = null

const { sendBinary, isConnected } = useWebSocket(`/ws/asr/${props.interviewId}`)

const formattedTime = computed(() => {
  const minutes = Math.floor(recordingTime.value / 60)
  const seconds = recordingTime.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const toggleRecording = async () => {
  if (isRecording.value) {
    await stopRecording()
  } else {
    await startRecording()
  }
}

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
      // Send audio data to WebSocket
      if (isConnected.value) {
        sendBinary(event.data)
      }
    }

    mediaRecorder.start(100) // Collect data every 100ms
    isRecording.value = true
    recordingTime.value = 0

    timerInterval = setInterval(() => {
      recordingTime.value++
    }, 1000)
  } catch (error) {
    console.error('Error starting recording:', error)
    ElMessage.error('无法访问麦克风')
  }
}

const stopRecording = async () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
  }

  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }

  isRecording.value = false
}

onUnmounted(() => {
  stopRecording()
})
</script>

<style lang="scss" scoped>
.audio-recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.recording-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.recording-dot {
  width: 12px;
  height: 12px;
  background-color: #f56c6c;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

.recording-time {
  font-size: 14px;
  color: #606266;
  font-family: monospace;
}

.transcript-preview {
  max-width: 400px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 8px;

  p {
    margin: 0;
    color: #606266;
    font-size: 14px;
  }
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>
