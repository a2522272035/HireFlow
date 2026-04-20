import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket(url) {
  const ws = ref(null)
  const isConnected = ref(false)
  const messages = ref([])
  const error = ref(null)

  const connect = () => {
    const wsUrl = `${import.meta.env.VITE_WS_BASE_URL}${url}`
    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      isConnected.value = true
      error.value = null
      console.log('WebSocket connected')
    }

    ws.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      messages.value.push(data)
    }

    ws.value.onerror = (err) => {
      error.value = err
      console.error('WebSocket error:', err)
    }

    ws.value.onclose = () => {
      isConnected.value = false
      console.log('WebSocket disconnected')
    }
  }

  const disconnect = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  const send = (data) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify(data))
    }
  }

  const sendBinary = (data) => {
    if (ws.value && isConnected.value) {
      ws.value.send(data)
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    ws,
    isConnected,
    messages,
    error,
    connect,
    disconnect,
    send,
    sendBinary,
  }
}
