<template>
  <div class="resume-page">
    <!-- 个人信息卡 -->
    <div class="profile-card">
      <div class="info">
        <div class="name-row">
          <h2 class="name">{{ resume.name }}</h2>
          <span class="position-tag">{{ resume.position }}</span>
        </div>
        <div class="basic-tags">
          <span class="tag">{{ resume.gender }}</span>
          <span class="tag">{{ resume.age }}岁</span>
          <span class="tag">{{ resume.city }}</span>
          <span class="tag blue">{{ resume.experience }}年经验</span>
        </div>
        <div class="contact-info">
          <span class="contact-item">📞 {{ resume.phone }}</span>
          <span class="contact-item">✉️ {{ resume.email }}</span>
        </div>
      </div>
      <img :src="resume.avatar" alt="头像" class="avatar" />
    </div>

    <!-- 简历亮点 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon blue">✦</span>
        <span>简历亮点</span>
      </div>
      <div class="highlights-list">
        <div v-for="(item, index) in resume.highlights" :key="index" class="highlight-item">
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
      <div class="risk-section">
        <div v-for="(tags, category) in resume.riskTags" :key="category" class="risk-row">
          <span class="risk-category">{{ category }}:</span>
          <div class="risk-tags">
            <span
              v-for="tag in tags"
              :key="tag.name"
              class="risk-tag"
              :class="tag.type"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 技能标签 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon purple">◈</span>
        <span>技能标签</span>
      </div>
      <div class="tags-section">
        <div v-for="(tags, category) in resume.tags" :key="category" class="tag-row">
          <span class="tag-category">{{ category }}:</span>
          <div class="tag-list">
            <span
              v-for="(tag, index) in tags"
              :key="tag"
              class="tag-item"
              :style="getTagStyle(category, index)"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 能力雷达图 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon purple">◈</span>
        <span>综合评估 - 能力指数</span>
      </div>
      <div class="chart-container">
        <v-chart :option="radarOption" style="height: 350px;"></v-chart>
      </div>
    </div>

    <!-- 一级行业雷达图 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon green">◈</span>
        <span>行业分析 - 一级行业</span>
      </div>
      <div class="chart-container">
        <v-chart :option="industryRadarOption" style="height: 350px;"></v-chart>
      </div>
    </div>

    <!-- 二级行业饼图 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon orange">◈</span>
        <span>行业分析 - 二级行业</span>
      </div>
      <div class="chart-container">
        <v-chart :option="industryPieOption" style="height: 300px;"></v-chart>
      </div>
    </div>

    <!-- 职位职能饼图 -->
    <div class="section-card">
      <div class="section-title">
        <span class="title-icon blue">◈</span>
        <span>职能分析</span>
      </div>
      <div class="chart-container">
        <v-chart :option="rolePieOption" style="height: 300px;"></v-chart>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import VChart from 'vue-echarts'

const resume = reactive({
  avatar: 'https://example.com/avatar.jpg',
  name: '初婷',
  position: '总账会计',
  gender: '女',
  age: 36,
  city: 'XX市',
  experience: 12,
  phone: '18943972347',
  email: 'xxx@xxx.com',
  highlights: [
    '平均每段工作经历持续35个月',
    '在会计师职能领域有丰富经验',
    '熟悉会计、报表、财务分析流程'
  ],
  riskTags: {
    '基本信息': [
      { name: '36岁', type: 'blue' },
      { name: '12年经验', type: 'blue' }
    ],
    '教育专业': [
      { name: '大学学历', type: 'blue' },
      { name: '电子商务专业', type: 'blue' },
      { name: '吉林交通职业技术学院', type: 'blue' }
    ],
    '风险点': [
      { name: '专业不对口', type: 'red' },
      { name: '跳槽频繁', type: 'red' }
    ],
    '证书': [
      { name: '会计从业资格证', type: 'orange' },
      { name: '会计初级职称', type: 'orange' }
    ]
  },
  tags: {
    '职位技能': ['总账会计', '会计核算', '财务报表'],
    '教育专业': ['大学学历', '电子商务专业', '吉林交通职业技术学院'],
    '证书': ['会计从业资格证', '会计初级职称'],
    '其他能力': ['团队协作', '逻辑分析', '沟通能力']
  },
  radar: {
    '工作能力': 80,
    '学习能力': 75,
    '沟通能力': 85,
    '管理能力': 70,
    '社会能力': 65,
    '逻辑能力': 78
  },
  industryRadar: {
    '计算机软件': 7,
    '专业服务': 7,
    '交通/运输/物流': 7,
    '会计/金融/银行/保险': 6,
    '制造/医疗': 5
  },
  industryPie: {
    '计算机软件': 7,
    '专业服务': 7,
    '交通/运输/物流': 7
  },
  rolePie: {
    '会计师': 60,
    '总账会计': 12,
    '财务主管/总账主管': 10,
    '会计经理/主管': 6
  }
})

// 标签颜色配置
const tagColors = {
  '职位技能': { bg: '#e6f7ff', color: '#1890ff', border: '#91d5ff' },
  '教育专业': { bg: '#f6ffed', color: '#52c41a', border: '#b7eb8f' },
  '证书': { bg: '#fff7e6', color: '#fa8c16', border: '#ffd591' },
  '其他能力': { bg: '#f9f0ff', color: '#722ed1', border: '#d3adf7' }
}

function getTagStyle(category, index) {
  const colors = [
    { bg: '#e6f7ff', color: '#1890ff', border: '#91d5ff' },
    { bg: '#f6ffed', color: '#52c41a', border: '#b7eb8f' },
    { bg: '#fff7e6', color: '#fa8c16', border: '#ffd591' },
    { bg: '#fff1f0', color: '#f5222d', border: '#ffa39e' },
    { bg: '#f9f0ff', color: '#722ed1', border: '#d3adf7' },
    { bg: '#e6fffb', color: '#13c2c2', border: '#87e8de' }
  ]
  const color = tagColors[category] || colors[index % colors.length]
  return {
    backgroundColor: color.bg,
    color: color.color,
    borderColor: color.border
  }
}

// 能力雷达图
const radarOption = {
  color: ['#5470c6'],
  tooltip: {},
  radar: {
    indicator: Object.keys(resume.radar).map(k => ({ name: k, max: 100 })),
    radius: '65%',
    axisName: {
      color: '#666',
      fontSize: 12
    },
    splitArea: {
      areaStyle: {
        color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff']
      }
    },
    axisLine: {
      lineStyle: { color: '#ddd' }
    },
    splitLine: {
      lineStyle: { color: '#ddd' }
    }
  },
  series: [
    {
      type: 'radar',
      data: [{
        value: Object.values(resume.radar),
        name: '能力评分',
        areaStyle: { color: 'rgba(84, 112, 198, 0.3)' },
        lineStyle: { color: '#5470c6', width: 2 },
        itemStyle: { color: '#5470c6' }
      }]
    }
  ]
}

// 一级行业雷达图
const industryRadarOption = {
  color: ['#91cc75'],
  tooltip: {},
  radar: {
    indicator: Object.keys(resume.industryRadar).map(k => ({ name: k, max: 10 })),
    radius: '65%',
    axisName: {
      color: '#666',
      fontSize: 11
    },
    splitArea: {
      areaStyle: {
        color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff']
      }
    },
    axisLine: {
      lineStyle: { color: '#ddd' }
    },
    splitLine: {
      lineStyle: { color: '#ddd' }
    }
  },
  series: [
    {
      type: 'radar',
      data: [{
        value: Object.values(resume.industryRadar),
        name: '行业匹配',
        areaStyle: { color: 'rgba(145, 204, 117, 0.3)' },
        lineStyle: { color: '#91cc75', width: 2 },
        itemStyle: { color: '#91cc75' }
      }]
    }
  ]
}

// 二级行业饼图
const industryPieOption = {
  color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
  tooltip: { trigger: 'item', formatter: '{b}: {c}' },
  legend: {
    orient: 'vertical',
    right: '5%',
    top: 'center',
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { fontSize: 12, color: '#666' }
  },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['35%', '50%'],
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' }
      },
      labelLine: { show: false },
      data: Object.entries(resume.industryPie).map(([name, value]) => ({ name, value }))
    }
  ]
}

// 职位职能饼图
const rolePieOption = {
  color: ['#5470c6', '#91cc75', '#fac858', '#ee6666'],
  tooltip: { trigger: 'item', formatter: '{b}: {c}%' },
  legend: {
    orient: 'vertical',
    right: '5%',
    top: 'center',
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { fontSize: 12, color: '#666' }
  },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['35%', '50%'],
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' }
      },
      labelLine: { show: false },
      data: Object.entries(resume.rolePie).map(([name, value]) => ({ name, value }))
    }
  ]
}
</script>

<style scoped>
.resume-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f5f5;
  min-height: 100vh;
}

/* 个人信息卡 */
.profile-card {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  object-fit: cover;
}

.info {
  flex: 1;
  margin-right: 20px;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.name {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #262626;
}

.position-tag {
  font-size: 14px;
  color: #1890ff;
  background: #e6f7ff;
  padding: 4px 12px;
  border-radius: 4px;
  border: 1px solid #91d5ff;
}

.basic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  padding: 4px 10px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 13px;
  color: #595959;
}

.tag.blue {
  background: #e6f7ff;
  color: #1890ff;
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.contact-item {
  font-size: 13px;
  color: #8c8c8c;
}

/* 卡片区块 */
.section-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 区块标题 */
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  margin-bottom: 16px;
}

.title-icon {
  font-size: 16px;
}

.title-icon.blue { color: #1890ff; }
.title-icon.red { color: #f5222d; }
.title-icon.green { color: #52c41a; }
.title-icon.orange { color: #fa8c16; }
.title-icon.purple { color: #722ed1; }

/* 简历亮点 */
.highlights-list {
  padding-left: 4px;
}

.highlight-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 6px 0;
}

.highlight-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.highlight-dot.blue {
  background: #1890ff;
}

.highlight-text {
  font-size: 14px;
  color: #595959;
  line-height: 1.6;
}

/* 风险标签 */
.risk-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.risk-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.risk-category {
  font-size: 13px;
  color: #8c8c8c;
  font-weight: 500;
  flex-shrink: 0;
  min-width: 70px;
}

.risk-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.risk-tag {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  border: 1px solid;
}

.risk-tag.blue {
  background: #e6f7ff;
  color: #1890ff;
  border-color: #91d5ff;
}

.risk-tag.red {
  background: #fff1f0;
  color: #f5222d;
  border-color: #ffa39e;
}

.risk-tag.orange {
  background: #fff7e6;
  color: #fa8c16;
  border-color: #ffd591;
}

/* 技能标签 */
.tags-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tag-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.tag-category {
  font-size: 13px;
  color: #8c8c8c;
  font-weight: 500;
  flex-shrink: 0;
  min-width: 70px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  border: 1px solid;
  transition: all 0.3s;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 图表容器 */
.chart-container {
  margin: 10px 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .resume-page {
    padding: 10px;
  }

  .profile-card {
    flex-direction: column-reverse;
    align-items: center;
    text-align: center;
  }

  .info {
    margin-right: 0;
    margin-top: 16px;
  }

  .name-row {
    flex-direction: column;
    gap: 8px;
  }

  .basic-tags,
  .contact-info {
    justify-content: center;
  }

  .tag-row,
  .risk-row {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
