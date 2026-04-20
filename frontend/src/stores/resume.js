import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useResumeStore = defineStore('resume', () => {
  // State
  const resumes = ref([])
  const currentResume = ref(null)
  const gaps = ref([])
  const isLoading = ref(false)

  // Getters
  const resumeCount = computed(() => resumes.value.length)
  const hasCurrentResume = computed(() => !!currentResume.value)
  const hasGaps = computed(() => gaps.value.length > 0)

  // Actions
  const setResumes = (newResumes) => {
    resumes.value = newResumes
  }

  const setCurrentResume = (resume) => {
    currentResume.value = resume
  }

  const setGaps = (newGaps) => {
    gaps.value = newGaps
  }

  const addResume = (resume) => {
    resumes.value.unshift(resume)
  }

  const updateResume = (id, updates) => {
    const index = resumes.value.findIndex(r => r.id === id)
    if (index !== -1) {
      resumes.value[index] = { ...resumes.value[index], ...updates }
    }
  }

  const removeResume = (id) => {
    resumes.value = resumes.value.filter(r => r.id !== id)
  }

  const clearCurrentResume = () => {
    currentResume.value = null
    gaps.value = []
  }

  return {
    resumes,
    currentResume,
    gaps,
    isLoading,
    resumeCount,
    hasCurrentResume,
    hasGaps,
    setResumes,
    setCurrentResume,
    setGaps,
    addResume,
    updateResume,
    removeResume,
    clearCurrentResume,
  }
})
