import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useInterviewStore = defineStore('interview', () => {
  // State
  const currentInterview = ref(null)
  const messages = ref([])
  const questions = ref([])
  const isRecording = ref(false)
  const transcripts = ref([])

  // Getters
  const hasActiveInterview = computed(() => !!currentInterview.value)
  const currentQuestion = computed(() => {
    return questions.value.find(q => q.status === 'current')
  })

  // Actions
  const setCurrentInterview = (interview) => {
    currentInterview.value = interview
  }

  const addMessage = (message) => {
    messages.value.push(message)
  }

  const setQuestions = (newQuestions) => {
    questions.value = newQuestions
  }

  const updateQuestionStatus = (questionId, status) => {
    const question = questions.value.find(q => q.id === questionId)
    if (question) {
      question.status = status
    }
  }

  const setRecording = (recording) => {
    isRecording.value = recording
  }

  const addTranscript = (transcript) => {
    transcripts.value.push(transcript)
  }

  const clearInterview = () => {
    currentInterview.value = null
    messages.value = []
    questions.value = []
    transcripts.value = []
    isRecording.value = false
  }

  return {
    currentInterview,
    messages,
    questions,
    isRecording,
    transcripts,
    hasActiveInterview,
    currentQuestion,
    setCurrentInterview,
    addMessage,
    setQuestions,
    updateQuestionStatus,
    setRecording,
    addTranscript,
    clearInterview,
  }
})
