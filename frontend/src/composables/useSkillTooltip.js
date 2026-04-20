import { ref } from 'vue'

export function useSkillTooltip() {
  const tooltipVisible = ref(false)
  const tooltipContent = ref('')
  const tooltipPosition = ref({ x: 0, y: 0 })

  const showTooltip = (content, event) => {
    tooltipContent.value = content
    tooltipPosition.value = {
      x: event.clientX + 10,
      y: event.clientY + 10,
    }
    tooltipVisible.value = true
  }

  const hideTooltip = () => {
    tooltipVisible.value = false
  }

  const updatePosition = (event) => {
    tooltipPosition.value = {
      x: event.clientX + 10,
      y: event.clientY + 10,
    }
  }

  return {
    tooltipVisible,
    tooltipContent,
    tooltipPosition,
    showTooltip,
    hideTooltip,
    updatePosition,
  }
}
