import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isLoading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || '')

  // Actions
  const setUser = (userData) => {
    user.value = userData
  }

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const logout = () => {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  const fetchUserInfo = async () => {
    // TODO: Implement API call to fetch user info
    isLoading.value = true
    try {
      // const response = await getUserInfo()
      // setUser(response.data)
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    token,
    isLoading,
    isLoggedIn,
    userRole,
    setUser,
    setToken,
    logout,
    fetchUserInfo,
  }
})
