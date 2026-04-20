<template>
  <el-tag
    :type="tagType"
    :effect="effect"
    class="skill-tag"
    @mouseenter="$emit('hover', $event)"
    @mouseleave="$emit('leave')"
  >
    {{ name }}
    <span v-if="level" class="skill-level">({{ level }})</span>
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  level: {
    type: String,
    default: '',
  },
  proficiency: {
    type: String,
    default: '',
    validator: (value) => ['', 'beginner', 'intermediate', 'advanced', 'expert'].includes(value),
  },
  effect: {
    type: String,
    default: 'light',
  },
})

defineEmits(['hover', 'leave'])

const tagType = computed(() => {
  switch (props.proficiency) {
    case 'expert':
      return 'success'
    case 'advanced':
      return 'primary'
    case 'intermediate':
      return 'warning'
    case 'beginner':
      return 'info'
    default:
      return ''
  }
})
</script>

<style lang="scss" scoped>
.skill-tag {
  margin: 4px;
}

.skill-level {
  font-size: 12px;
  opacity: 0.8;
  margin-left: 4px;
}
</style>
