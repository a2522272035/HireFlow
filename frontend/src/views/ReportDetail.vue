<template>
  <div class="report-detail">
    <h1>评估报告详情</h1>

    <ReportViewer v-if="report" :report="report" />

    <el-empty v-else description="暂无报告数据" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ReportViewer from '@/components/common/ReportViewer.vue'

const route = useRoute()
const report = ref(null)

onMounted(() => {
  // TODO: Fetch report data
  const reportId = route.params.id
  console.log('Fetching report:', reportId)
})
</script>

<style lang="scss" scoped>
.report-detail {
  h1 {
    margin-bottom: 24px;
  }
}
</style>
