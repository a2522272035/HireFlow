<template>
  <div class="report-viewer">
    <div v-if="report" class="report-container">
      <!-- 顶部个人信息区 -->
      <div class="profile-section">
        <div class="profile-main">
          <div class="avatar">
            <img v-if="report.avatar" :src="report.avatar" alt="avatar" />
            <span v-else>{{ report.name ? report.name[0] : '?' }}</span>
          </div>
          <div class="profile-info">
            <div class="name-row">
              <h1 class="name">{{ report.name || '未识别姓名' }}</h1>
              <span class="position">{{ report.position || '应聘职位' }}</span>
            </div>
            <div class="basic-tags">
              <span v-if="report.gender" class="tag">{{ report.gender }}</span>
              <span v-if="report.age" class="tag">{{ report.age }}岁</span>
              <span v-if="report.location" class="tag">{{ report.location }}</span>
              <span v-if="report.education" class="tag blue">{{ report.education }}</span>
              <span v-if="report.workYears" class="tag blue">{{ report.workYears }}年经验</span>
            </div>
            <div class="contact-info">
              <span v-if="report.phone" class="contact-item">
                <el-icon><Phone /></el-icon> {{ report.phone }}
              </span>
              <span v-if="report.email" class="contact-item">
                <el-icon><Message /></el-icon> {{ report.email }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 简历亮点 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon blue">✦</span>
          <span>简历亮点</span>
        </div>
        <div class="highlights-list">
          <div v-for="(item, index) in highlights" :key="index" class="highlight-item">
            <span class="highlight-dot blue"></span>
            <span class="highlight-text">{{ item }}</span>
          </div>
        </div>
      </div>

      <!-- 风险标签 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon red">⚠</span>
          <span>风险标签</span>
        </div>
        <div class="risk-tags">
          <span
            v-for="(tag, index) in riskTags"
            :key="index"
            class="risk-tag"
            :class="tag.type"
          >
            {{ tag.label }}
          </span>
        </div>
      </div>

      <!-- 综合评估 - 雷达图 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon purple">◈</span>
          <span>综合评估</span>
        </div>
        <div class="chart-container">
          <v-chart class="radar-chart" :option="abilityRadarOption" autoresize />
        </div>
      </div>

      <!-- 行业分析 - 雷达图 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon green">◈</span>
          <span>行业分析</span>
        </div>
        <div class="chart-container">
          <v-chart class="radar-chart" :option="industryRadarOption" autoresize />
        </div>
      </div>

      <!-- 职能分析 - 环形图 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon orange">◈</span>
          <span>职能分析</span>
        </div>
        <div class="chart-container">
          <v-chart class="pie-chart" :option="functionPieOption" autoresize />
        </div>
      </div>

      <!-- 技能标签 -->
      <div class="section-card">
        <div class="section-title">
          <span class="title-icon blue">◈</span>
          <span>技能标签</span>
        </div>
        <div class="skill-tags">
          <span
            v-for="(skill, index) in skillTags"
            :key="index"
            class="skill-tag"
            :style="getSkillTagStyle(index)"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- 原始数据 -->
      <div class="section-card">
        <el-collapse>
          <el-collapse-item title="查看原始报告数据">
            <pre class="raw-json">{{ JSON.stringify(report, null, 2) }}</pre>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>

    <el-empty v-else description="暂无报告数据" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Phone, Message } from '@element-plus/icons-vue'

const props = defineProps({
  report: {
    type: Object,
    required: true,
  },
})

// 简历亮点数据
const highlights = computed(() => {
  if (props.report?.strengths?.length) {
    return props.report.strengths
  }
  return [
    '具备扎实的专业技能和丰富的工作经验',
    '在相关领域有深入的研究和实践',
    '具有良好的团队协作能力和沟通能力',
    '工作态度认真负责，执行力强',
  ]
})

// 风险标签数据
const riskTags = computed(() => {
  const tags = []
  if (props.report?.weaknesses?.length) {
    props.report.weaknesses.forEach(w => {
      tags.push({ label: w, type: 'red' })
    })
  }
  if (props.report?.risk_factors?.length) {
    props.report.risk_factors.forEach(r => {
      tags.push({ label: r, type: 'orange' })
    })
  }
  // 默认风险标签
  if (tags.length === 0) {
    tags.push(
      { label: '跳槽频繁', type: 'red' },
      { label: '工作空窗期', type: 'orange' },
      { label: '学历不匹配', type: 'blue' }
    )
  }
  return tags
})

// 技能标签
const skillTags = computed(() => {
  const skills = []
  if (props.report?.skills?.length) {
    skills.push(...props.report.skills)
  }
  if (props.report?.skill_tags?.length) {
    skills.push(...props.report.skill_tags)
  }
  if (skills.length === 0) {
    skills.push('Java', 'Spring', 'MySQL', 'Redis', '微服务', 'Docker', 'Linux', 'Git')
  }
  return skills.slice(0, 20)
})

// 能力雷达图配置
const abilityRadarOption = computed(() => {
  const indicators = [
    { name: '专业技能', max: 100 },
    { name: '工作经验', max: 100 },
    { name: '学历背景', max: 100 },
    { name: '沟通能力', max: 100 },
    { name: '团队协作', max: 100 },
    { name: '学习能力', max: 100 },
  ]
  const values = [
    props.report?.technical_score || 75,
    props.report?.experience_score || 80,
    props.report?.education_score || 70,
    props.report?.communication_score || 85,
    props.report?.teamwork_score || 78,
    props.report?.learning_score || 82,
  ]

  return {
    color: ['#5470c6'],
    radar: {
      indicator: indicators,
      radius: '65%',
      center: ['50%', '50%'],
      axisName: {
        color: '#666',
        fontSize: 12,
      },
      splitArea: {
        areaStyle: {
          color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff'],
        },
      },
      axisLine: {
        lineStyle: {
          color: '#ddd',
        },
      },
      splitLine: {
        lineStyle: {
          color: '#ddd',
        },
      },
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: '能力评估',
        areaStyle: {
          color: 'rgba(84, 112, 198, 0.3)',
        },
        lineStyle: {
          color: '#5470c6',
          width: 2,
        },
        itemStyle: {
          color: '#5470c6',
        },
      }],
    }],
  }
})

// 行业雷达图配置
const industryRadarOption = computed(() => {
  const indicators = [
    { name: '互联网', max: 100 },
    { name: '金融', max: 100 },
    { name: '教育', max: 100 },
    { name: '医疗', max: 100 },
    { name: '制造', max: 100 },
    { name: '零售', max: 100 },
  ]
  const values = [85, 60, 45, 55, 70, 65]

  return {
    color: ['#91cc75'],
    radar: {
      indicator: indicators,
      radius: '65%',
      center: ['50%', '50%'],
      axisName: {
        color: '#666',
        fontSize: 12,
      },
      splitArea: {
        areaStyle: {
          color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff'],
        },
      },
      axisLine: {
        lineStyle: {
          color: '#ddd',
        },
      },
      splitLine: {
        lineStyle: {
          color: '#ddd',
        },
      },
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: '行业匹配',
        areaStyle: {
          color: 'rgba(145, 204, 117, 0.3)',
        },
        lineStyle: {
          color: '#91cc75',
          width: 2,
        },
        itemStyle: {
          color: '#91cc75',
        },
      }],
    }],
  }
})

// 职能分析环形图配置
const functionPieOption = computed(() => {
  const data = [
    { value: 35, name: '后端开发' },
    { value: 25, name: '架构设计' },
    { value: 20, name: '技术管理' },
    { value: 12, name: '前端开发' },
    { value: 8, name: '数据分析' },
  ]

  return {
    color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}%',
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        fontSize: 12,
        color: '#666',
      },
    },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold',
        },
      },
      labelLine: {
        show: false,
      },
      data,
    }],
  }
})

// 技能标签样式
function getSkillTagStyle(index) {
  const colors = [
    { bg: '#e6f7ff', color: '#1890ff', border: '#91d5ff' },
    { bg: '#f6ffed', color: '#52c41a', border: '#b7eb8f' },
    { bg: '#fff7e6', color: '#fa8c16', border: '#ffd591' },
    { bg: '#fff1f0', color: '#f5222d', border: '#ffa39e' },
    { bg: '#f9f0ff', color: '#722ed1', border: '#d3adf7' },
    { bg: '#e6fffb', color: '#13c2c2', border: '#87e8de' },
  ]
  const color = colors[index % colors.length]
  return {
    backgroundColor: color.bg,
    color: color.color,
    borderColor: color.border,
  }
}
</script>

<style lang="scss" scoped>
.report-viewer {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.report-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

// 顶部个人信息区
.profile-section {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;

  .profile-main {
    display: flex;
    align-items: flex-start;
    gap: 20px;
  }

  .avatar {
    width: 80px;
    height: 80px;
    border-radius: 8px;
    background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: white;
    font-weight: 600;
    flex-shrink: 0;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .profile-info {
    flex: 1;

    .name-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;

      .name {
        font-size: 24px;
        font-weight: 600;
        color: #262626;
        margin: 0;
      }

      .position {
        font-size: 14px;
        color: #1890ff;
        background: #e6f7ff;
        padding: 4px 12px;
        border-radius: 4px;
      }
    }

    .basic-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;

      .tag {
        padding: 4px 10px;
        background: #f5f5f5;
        border-radius: 4px;
        font-size: 13px;
        color: #595959;

        &.blue {
          background: #e6f7ff;
          color: #1890ff;
        }
      }
    }

    .contact-info {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;

      .contact-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        color: #8c8c8c;

        .el-icon {
          font-size: 14px;
          color: #bfbfbf;
        }
      }
    }
  }
}

// 卡片区块
.section-card {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

// 区块标题
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  margin-bottom: 16px;

  .title-icon {
    font-size: 16px;

    &.blue {
      color: #1890ff;
    }

    &.red {
      color: #f5222d;
    }

    &.green {
      color: #52c41a;
    }

    &.orange {
      color: #fa8c16;
    }

    &.purple {
      color: #722ed1;
    }
  }
}

// 简历亮点
.highlights-list {
  .highlight-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;

    .highlight-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      margin-top: 8px;
      flex-shrink: 0;

      &.blue {
        background: #1890ff;
      }
    }

    .highlight-text {
      font-size: 14px;
      color: #595959;
      line-height: 1.6;
    }
  }
}

// 风险标签
.risk-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  .risk-tag {
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 13px;
    border: 1px solid;

    &.red {
      background: #fff1f0;
      color: #f5222d;
      border-color: #ffa39e;
    }

    &.orange {
      background: #fff7e6;
      color: #fa8c16;
      border-color: #ffd591;
    }

    &.blue {
      background: #e6f7ff;
      color: #1890ff;
      border-color: #91d5ff;
    }
  }
}

// 图表容器
.chart-container {
  display: flex;
  justify-content: center;

  .radar-chart {
    width: 100%;
    height: 300px;
  }

  .pie-chart {
    width: 100%;
    height: 280px;
  }
}

// 技能标签
.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  .skill-tag {
    padding: 6px 14px;
    border-radius: 4px;
    font-size: 13px;
    border: 1px solid;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }
}

// 原始数据
.raw-json {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 1.6;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
  margin: 0;
}

// 响应式
@media (max-width: 768px) {
  .report-viewer {
    padding: 10px;
  }

  .profile-section {
    padding: 16px;

    .profile-main {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .profile-info {
      .name-row {
        flex-direction: column;
        gap: 8px;
      }

      .basic-tags,
      .contact-info {
        justify-content: center;
      }
    }
  }

  .section-card {
    padding: 16px;
    overflow-wrap: anywhere;
  }

  .chart-container {
    overflow-x: auto;

    .radar-chart,
    .pie-chart {
      min-width: 280px;
      height: 250px;
    }
  }
}
</style>
