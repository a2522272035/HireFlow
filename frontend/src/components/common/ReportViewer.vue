<template>
  <div class="report-viewer">
    <el-card v-if="report" class="report-card">
      <template #header>
        <div class="report-header">
          <h2>评估报告</h2>
          <el-tag :type="recommendationType">
            {{ report.recommendation }}
          </el-tag>
        </div>
      </template>

      <!-- Executive Summary -->
      <div class="report-section">
        <h3>执行摘要</h3>
        <p>{{ report.executive_summary }}</p>
      </div>

      <!-- Scores -->
      <div class="report-section">
        <h3>评分</h3>
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="score-item">
              <el-progress
                type="dashboard"
                :percentage="Math.round(report.overall_score || 0)"
                :color="scoreColors"
              />
              <span class="score-label">综合评分</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="score-item">
              <el-progress
                type="dashboard"
                :percentage="Math.round(report.technical_score || 0)"
                :color="scoreColors"
              />
              <span class="score-label">技术能力</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="score-item">
              <el-progress
                type="dashboard"
                :percentage="Math.round(report.behavioral_score || 0)"
                :color="scoreColors"
              />
              <span class="score-label">行为表现</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="score-item">
              <el-progress
                type="dashboard"
                :percentage="Math.round(report.credibility_score || 0)"
                :color="scoreColors"
              />
              <span class="score-label">可信度</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- Strengths -->
      <div class="report-section">
        <h3>优势</h3>
        <ul>
          <li v-for="(strength, index) in report.strengths" :key="index">
            {{ strength }}
          </li>
        </ul>
      </div>

      <!-- Weaknesses -->
      <div class="report-section">
        <h3>待改进</h3>
        <ul>
          <li v-for="(weakness, index) in report.weaknesses" :key="index">
            {{ weakness }}
          </li>
        </ul>
      </div>

      <!-- Recommendations -->
      <div class="report-section">
        <h3>建议</h3>
        <ul>
          <li v-for="(rec, index) in report.recommendations" :key="index">
            {{ rec }}
          </li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  report: {
    type: Object,
    required: true,
  },
})

const scoreColors = [
  { color: '#f56c6c', percentage: 40 },
  { color: '#e6a23c', percentage: 60 },
  { color: '#67c23a', percentage: 80 },
  { color: '#409eff', percentage: 100 },
]

const recommendationType = computed(() => {
  switch (props.report?.recommendation) {
    case 'strong_hire':
      return 'success'
    case 'hire':
      return 'primary'
    case 'neutral':
      return 'warning'
    case 'no_hire':
      return 'danger'
    default:
      return 'info'
  }
})
</script>

<style lang="scss" scoped>
.report-viewer {
  .report-card {
    margin-bottom: 20px;
  }

  .report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }
  }

  .report-section {
    margin-bottom: 24px;

    h3 {
      margin-bottom: 12px;
      color: #303133;
      font-size: 16px;
      border-bottom: 1px solid #e4e7ed;
      padding-bottom: 8px;
    }

    ul {
      padding-left: 20px;

      li {
        margin-bottom: 8px;
        line-height: 1.6;
      }
    }
  }

  .score-item {
    text-align: center;

    .score-label {
      display: block;
      margin-top: 8px;
      color: #606266;
    }
  }
}
</style>
