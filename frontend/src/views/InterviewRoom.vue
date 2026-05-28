<template>
  <div class="interview-room">
    <el-card class="interview-card">
      <template #header>
        <div class="interview-header">
          <h2>面试间</h2>
          <div class="header-actions">
            <el-tag :type="interviewStatusType">{{ interviewStatus }}</el-tag>
            <el-button type="danger" @click="endInterview">结束面试</el-button>
          </div>
        </div>
      </template>

      <div class="interview-content">
        <!-- Candidate Info -->
        <div class="candidate-info">
          <el-avatar :size="64" :icon="UserFilled" />
          <div class="candidate-details">
            <h3>{{ candidateName }}</h3>
            <p>{{ candidatePosition }}</p>
          </div>
        </div>

        <!-- Questions Panel -->
        <div class="questions-panel">
          <h4>面试问题</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(question, index) in questions"
              :key="index"
              :type="question.status === 'current' ? 'primary' : question.status === 'answered' ? 'success' : ''"
            >
              <el-card :class="{ 'current-question': question.status === 'current' }">
                <p>{{ question.text }}</p>
                <div v-if="question.status === 'answered'" class="answer-section">
                  <p class="answer-text">{{ question.answer }}</p>
                  <el-tag :type="getCredibilityType(question.credibility)">
                    可信度: {{ question.credibility }}%
                  </el-tag>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>

        <!-- Real-time Transcription -->
        <div class="transcription-panel">
          <h4>实时转录</h4>
          <div class="transcript-container">
            <div
              v-for="(item, index) in transcripts"
              :key="index"
              :class="['transcript-item', item.speaker]"
            >
              <span class="speaker">{{ item.speaker === 'interviewer' ? '面试官' : '候选人' }}:</span>
              <span class="text">{{ item.text }}</span>
            </div>
          </div>
        </div>

        <!-- Recording Controls -->
        <div class="recording-controls">
          <AudioRecorder :interview-id="interviewId" @transcript="handleTranscript" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { UserFilled } from '@element-plus/icons-vue'
import AudioRecorder from '@/components/common/AudioRecorder.vue'

const route = useRoute()
const router = useRouter()

const interviewId = computed(() => route.params.id)

const interviewStatus = ref('进行中')
const candidateName = ref('候选人')
const candidatePosition = ref('职位')
const questions = ref([])
const transcripts = ref([])

const interviewStatusType = computed(() => {
  switch (interviewStatus.value) {
    case '进行中':
      return 'primary'
    case '已完成':
      return 'success'
    default:
      return 'info'
  }
})

const getCredibilityType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

const handleTranscript = (transcript) => {
  transcripts.value.push(transcript)
}

const endInterview = async () => {
  // TODO: End interview and generate report
  router.push('/interviews')
}

onMounted(() => {
  // TODO: Fetch interview data
})
</script>

<style lang="scss" scoped>
.interview-room {
  .interview-card {
    min-height: calc(100vh - 120px);
  }
}

.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h2 {
    margin: 0;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

.interview-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.candidate-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;

  .candidate-details {
    h3 {
      margin: 0 0 4px 0;
    }

    p {
      margin: 0;
      color: #606266;
    }
  }
}

.questions-panel {
  h4 {
    margin-bottom: 16px;
  }
}

.current-question {
  border: 2px solid #409eff;
}

.answer-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e4e7ed;

  .answer-text {
    margin-bottom: 8px;
    color: #606266;
  }
}

.transcription-panel {
  h4 {
    margin-bottom: 16px;
  }
}

.transcript-container {
  max-height: 300px;
  overflow-y: auto;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.transcript-item {
  margin-bottom: 8px;
  padding: 8px;
  border-radius: 4px;

  &.interviewer {
    background-color: #ecf5ff;
  }

  &.candidate {
    background-color: #f0f9ff;
  }

  .speaker {
    font-weight: 600;
    margin-right: 8px;
  }
}

.recording-controls {
  display: flex;
  justify-content: center;
  padding: 24px;
  border-top: 1px solid #e4e7ed;
}

@media (max-width: 768px) {
  .interview-room {
    .interview-card {
      min-height: auto;
    }
  }

  .interview-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;

    .header-actions {
      width: 100%;
      justify-content: space-between;
    }
  }

  .candidate-info {
    align-items: flex-start;
    padding: 12px;
  }

  .transcript-container {
    max-height: 260px;
    padding: 12px;
  }

  .recording-controls {
    padding: 16px 0 0;
  }
}

@media (max-width: 480px) {
  .interview-header {
    .header-actions {
      align-items: stretch;
      flex-direction: column;
    }
  }
}
</style>
