<template>
  <div class="resume-analysis" :class="{ 'ai-panel-open': showAIPanel }">
    <button class="ai-panel-toggle-btn" :class="{ 'panel-open': showAIPanel }" @click="showAIPanel = !showAIPanel">
      <span class="ai-icon">🤖</span>
      <span>AI面试助手</span>
    </button>

    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <div class="loading-text">{{ loadingText }}</div>
    </div>

    <div class="main-container">
      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        <i class="bi-exclamation-triangle-fill mr-2"></i>{{ error }}
        <button type="button" class="close" @click="error = ''">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <div v-if="!parsedData" class="upload-section">
        <div class="upload-card">
          <div class="upload-area"
               @click="$refs.fileInput.click()"
               @drop.prevent="handleDrop"
               @dragover.prevent="dragover = true"
               @dragleave.prevent="dragover = false"
               :class="{ dragover: dragover }">
            <div class="upload-icon">
              <i class="bi-cloud-upload-fill"></i>
            </div>
            <div class="upload-title">点击或拖拽上传简历文件</div>
            <div class="upload-desc">支持 PDF、Word、TXT、HTML 等 40+ 种格式，最大 30MB</div>
            <div class="upload-formats">
              <span class="format-tag">PDF</span>
              <span class="format-tag">DOC</span>
              <span class="format-tag">DOCX</span>
              <span class="format-tag">TXT</span>
              <span class="format-tag">HTML</span>
            </div>
          </div>
          <input type="file" ref="fileInput" class="file-input" @change="handleFileSelect" accept=".pdf,.doc,.docx,.txt,.html,.htm,.rtf">
        </div>
      </div>

      <template v-else>
        <div class="profile-header-section mybg-primary">
          <div class="profile-main d-flex">
            <div class="avatar-section me-4">
              <img v-if="avatarUrl" :src="avatarUrl" alt="头像" class="avatar-img">
              <div v-else class="avatar">{{ resumeData.name ? resumeData.name[0] : '?' }}</div>
            </div>
            <div class="profile-info flex-grow-1">
              <div class="name-position d-flex align-items-center mb-3">
                <h1 class="name mytext-primary mb-0 me-3">{{ resumeData.name }}</h1>
                <span class="position-tag mybadge mybadge-primary mybadge-pill">{{ resumeData.position }}</span>
              </div>
              <div class="badges-row mb-3">
            <span v-for="(badge, index) in highlightBadges" :key="'h-'+index" class="mybadge mybadge-primary me-2 mb-1">
              {{ badge }}
            </span>
            <span v-if="profilerData.salaryBadge" class="mybadge mybadge-info me-2 mb-1">{{ profilerData.salaryBadge }}</span>
            <span v-for="(badge, index) in riskBadges" :key="'r-'+index" class="mybadge mybadge-warning me-2 mb-1">
              {{ badge }}
            </span>
          </div>
              <div class="basic-info-row d-flex flex-wrap mb-2">
                <span class="info-item me-4 mb-1"><i class="bi-gender-ambiguous me-1"></i> {{ resumeData.gender }}</span>
                <span class="info-item me-4 mb-1"><i class="bi-calendar me-1"></i> {{ resumeData.age }}岁</span>
                <span class="info-item me-4 mb-1"><i class="bi-geo-alt me-1"></i> {{ resumeData.location }}</span>
                <span class="info-item me-4 mb-1"><i class="bi-briefcase me-1"></i> {{ resumeData.experience }}年经验</span>
              </div>
              <div class="contact-row d-flex flex-wrap">
                <span class="info-item me-4 mb-1"><i class="bi-building me-1"></i> {{ resumeData.school }}</span>
                <span class="info-item me-4 mb-1"><i class="bi-mortarboard me-1"></i> {{ resumeData.degree }}</span>
                <span class="info-item me-4 mb-1"><i class="bi-telephone me-1"></i> {{ resumeData.phone }}</span>
                <span class="info-item me-4 mb-1"><i class="bi-envelope me-1"></i> {{ resumeData.email || '暂无邮箱' }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="tabs-section">
          <div class="tabs-nav d-flex border-bottom">
            <div class="tab-item flex-grow-1 text-center py-3" :class="{ active: activeTab === 'parser' }" @click="activeTab = 'parser'">
              <i class="bi-file-text me-2"></i> 简历解析
            </div>
            <div class="tab-item flex-grow-1 text-center py-3" :class="{ active: activeTab === 'profiler' }" @click="activeTab = 'profiler'">
              <i class="bi-person-badge me-2"></i> 简历画像
            </div>
          </div>

          <div v-show="activeTab === 'parser'" class="tab-content">


            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-person section-icon mytext-primary"></i>
                <span class="mytext-primary">基本信息</span>
              </div>
              <table class="table-layout">
                <tr>
                  <td class="mytext-muted" style="width: 120px;">姓名</td>
                  <td>{{ parserData.basicInfo.name }}</td>
                  <td class="mytext-muted" style="width: 120px;">性别</td>
                  <td>{{ parserData.basicInfo.gender }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">年龄</td>
                  <td>{{ parserData.basicInfo.age }}岁</td>
                  <td class="mytext-muted">工作年限(规范化)</td>
                  <td>{{ parserData.basicInfo.workYears }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">毕业时间</td>
                  <td>{{ parserData.basicInfo.graduationTime }}</td>
                  <td class="mytext-muted">毕业学校</td>
                  <td>{{ parserData.basicInfo.school }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">毕业学校类型</td>
                  <td>{{ parserData.basicInfo.schoolType }}</td>
                  <td class="mytext-muted">所学专业</td>
                  <td>{{ parserData.basicInfo.major }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">学历</td>
                  <td>{{ parserData.basicInfo.degree }}</td>
                  <td class="mytext-muted">参加工作时间</td>
                  <td>{{ parserData.basicInfo.workStartTime }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">参加工作时间(推断)</td>
                  <td>{{ parserData.basicInfo.workStartTimeInferred }}</td>
                  <td class="mytext-muted">当前职位</td>
                  <td>{{ parserData.basicInfo.currentPosition }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">当前职能类型</td>
                  <td>{{ parserData.basicInfo.currentFunctionType }}</td>
                  <td class="mytext-muted">当前单位</td>
                  <td>{{ parserData.basicInfo.currentCompany }}</td>
                </tr>
              </table>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-telephone section-icon mytext-primary"></i>
                <span class="mytext-primary">联系方式</span>
              </div>
              <table class="table-layout">
                <tr>
                  <td class="mytext-muted" style="width: 100px;">联系电话</td>
                  <td colspan="3">{{ parserData.contact.phone }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted">电子邮箱</td>
                  <td colspan="3">{{ parserData.contact.email || '暂无' }}</td>
                </tr>
              </table>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-bullseye section-icon mytext-primary"></i>
                <span class="mytext-primary">期望工作</span>
              </div>
              <table class="table-layout">
                <tr>
                  <td class="mytext-muted" style="width: 120px;">期望职位</td>
                  <td>{{ parserData.expectation.position }}</td>
                  <td class="mytext-muted" style="width: 120px;">期望薪资</td>
                  <td class="salary-highlight">{{ parserData.expectation.salary }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted" style="width: 120px;">期望月薪(下限)</td>
                  <td>{{ parserData.expectation.salaryMin || '暂无' }}</td>
                  <td class="mytext-muted" style="width: 120px;">期望月薪(上限)</td>
                  <td>{{ parserData.expectation.salaryMax || '暂无' }}</td>
                </tr>
                <tr>
                  <td class="mytext-muted" style="width: 120px;">期望工作地点</td>
                  <td>{{ parserData.expectation.jlocation || parserData.expectation.location || '暂无' }}</td>
                  <td class="mytext-muted" style="width: 120px;">期望工作地点(规范化)</td>
                  <td>{{ parserData.expectation.jlocationNorm || '暂无' }}</td>
                </tr>
              </table>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-mortarboard section-icon mytext-primary"></i>
                <span class="mytext-primary">教育经历</span>
              </div>
              <div class="r_content">
                <div v-for="(edu, index) in parserData.educationList" :key="index" class="mb-4">
                  <div class="d-flex align-items-center mb-2">
                    <span class="r_circle"></span>
                    <span class="mytext-primary fw-bold">{{ edu.school }}</span>
                    <span class="mx-2 mytext-muted">-</span>
                    <span class="fw-medium">{{ edu.major }}</span>
                    <span class="ms-auto r_small">{{ edu.period }}</span>
                  </div>
                  <div v-if="edu.degree" class="r_indent2 mytext-muted">{{ edu.degree }}</div>
                </div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-briefcase section-icon mytext-primary"></i>
                <span class="mytext-primary">工作经历</span>
              </div>
              <table class="table-layout">
                <template v-for="(work, index) in parserData.workExperience" :key="index">
                  <tr>
                    <td colspan="4">
                      <div><i class="r_circle mybg-primary"></i> <span class="fw-bold">{{ work.period }}</span></div>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="4">
                      <div><i class="r_circle mybg-primary"></i> <strong>公司信息：名称:{{ work.company }}</strong></div>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="4">
                      <div><i class="r_circle mybg-primary"></i> <strong>职位信息：名称:{{ work.position }}<span v-if="work.positionType"> | 职能类型:{{ work.positionType }}</span></strong></div>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="4">
                      <div><i class="r_circle mybg-primary"></i> <strong>工作描述：</strong><br>
                        <div class="ml-4 description-text" v-html="formatDescription(work.description)"></div>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="index < parserData.workExperience.length - 1"><td colspan="4">&nbsp;</td></tr>
                </template>
              </table>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-trophy section-icon mytext-primary"></i>
                <span class="mytext-primary">证书及奖项</span>
              </div>
              <div class="r_content">
                <div v-if="parserData.certificates && parserData.certificates.length > 0">
                  <div v-for="(cert, index) in parserData.certificates" :key="index" class="mb-2">
                    <span class="r_circle"></span>
                    <span class="mytext-muted">证书{{ index + 1 }}：</span>
                    <span class="fw-medium">{{ cert }}</span>
                  </div>
                </div>
                <div v-else class="empty-hint">暂无证书信息</div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-file-text section-icon mytext-primary"></i>
                <span class="mytext-primary">所获证书（文本）</span>
              </div>
              <div class="r_content">
                <div v-if="parserData.certificate_text" class="mytext-muted">{{ parserData.certificate_text }}</div>
                <div v-else class="empty-hint">暂无证书文本信息</div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-tools section-icon mytext-primary"></i>
                <span class="mytext-primary">技能列表</span>
              </div>
              <div class="r_content">
                <div v-if="parserData.skills && parserData.skills.length > 0">
                  <span v-for="(skill, index) in parserData.skills" :key="index"
                        class="mybadge mybadge-info mybadge-pill me-2 mb-2 term-clickable skill-term"
                        @mouseenter="explainTerm(skill, $event)"
                        @mouseleave="handleTermLeave">
                    {{ skill }}
                  </span>
                </div>
                <div v-else class="empty-hint">暂无技能信息</div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header row-bordered">
                <i class="bi-chat-quote section-icon mytext-primary"></i>
                <span class="mytext-primary">自我评价</span>
              </div>
              <div class="ml-4">
                <div v-if="parserData.selfEvaluation" class="description-text" v-html="formatDescription(parserData.selfEvaluation)"></div>
                <div v-else class="empty-hint">暂无自我评价</div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'profiler'" class="tab-content">
            <table class="w-100" style="font-size:90%;">
              <tr>
                <td colspan="4"><h5 class="row-bordered font-weight-bold"><i class="bi-play-fill mytext-primary r_indent2"></i>简历亮点</h5></td>
              </tr>
              <tr>
                <td colspan="4">
                  <h6><i class="bi-hand-thumbs-up ml-3 mr-2 mytext-primary"></i>亮点信息 <span class="mybadge mybadge-pill mybadge-primary">{{ profilerData.highlights.count }}</span></h6>
                  <div class="highlight-list" v-if="profilerData.highlights.items.length > 0">
                    <div v-for="(item, index) in profilerData.highlights.items" :key="'h-'+index" class="my-1 ml-4">
                      <i class="r_circle mx-2 my-1 mybg-primary"></i><span class="r_small" v-html="item"></span>
                    </div>
                  </div>
                  <div v-else class="my-1 ml-4">
                    <i class="r_circle mx-2 my-1 mybg-primary"></i><span class="r_small">暂无突出亮点</span>
                  </div>

                  <h6 class="mt-3"><i class="bi-info-circle ml-3 mr-2 mytext-warning"></i>风险信息 <span class="mybadge mybadge-pill mybadge-warning">{{ profilerData.risks.count }}</span></h6>
                  <div class="risk-list" v-if="profilerData.risks.items.length > 0">
                    <div v-for="(item, index) in profilerData.risks.items" :key="'r-'+index" class="my-1 ml-4">
                      <i class="r_circle mx-2 my-1 mybg-warning"></i><span class="r_small" v-html="item"></span>
                    </div>
                  </div>
                  <div v-else class="my-1 ml-4">
                    <i class="r_circle mx-2 my-1 mybg-warning"></i><span class="r_small">未发现明显风险</span>
                  </div>

                  <h6 class="mt-3"><i class="bi-pencil ml-3 mr-2 mytext-info"></i>智能评估 <span class="mybadge mybadge-pill mybadge-info">{{ profilerData.assessment.count }}</span></h6>
                  <div class="my-1 ml-4">
                    <i class="r_circle mx-2 my-1 mybg-info"></i><span class="r_small" v-html="profilerData.assessment.html"></span>
                  </div>
                </td>
              </tr>

              <tr>
                <td colspan="4"><h5 class="row-bordered font-weight-bold mt-3"><i class="bi-play-fill mytext-primary r_indent2"></i>简历标签</h5></td>
              </tr>
              <tr v-for="(tagCat, tIndex) in profilerData.tags" :key="'tagcat-'+tIndex">
                <td colspan="4">
                  <h6 class="mt-3"><i class="bi-play ml-3 mr-2" :class="tagCat.iconClass"></i>{{ tagCat.category }}</h6>
                  <h5>
                    <div v-for="(sub, sIndex) in tagCat.subs" :key="'sub-'+sIndex" class="my-1 ml-4">
                      <i class="r_circle mx-1" :class="'mybg-' + tagCat.badgeColor"></i>
                      <span class="r_small_70">{{ sub.label }}</span>
                      <span
                        v-for="(item, iIndex) in sub.items"
                        :key="'item-'+iIndex"
                        class="mybadge term-clickable"
                        :class="'mybadge-' + tagCat.badgeColor"
                        :data-original-title="item.tooltip"
                        @mouseenter="explainTerm(item.text, $event)"
                        @mouseleave="handleTermLeave"
                      >{{ item.text }}</span>
                    </div>
                  </h5>
                </td>
              </tr>

              <tr>
                <td colspan="4"><h5 class="row-bordered font-weight-bold mt-3"><i class="bi-play-fill mytext-primary r_indent2"></i>综合评估</h5></td>
              </tr>
              <tr>
                <td colspan="4"><h5 class="text-center mt-3">能力指数</h5></td>
              </tr>
              <tr>
                <td colspan="4">
                  <div class="chart-container">
                    <v-chart class="radar-chart" :option="capacityChartOption" autoresize />
                  </div>
                </td>
              </tr>
              <tr v-if="profilerData.hasIndustryData">
                <td colspan="4"><h5 class="text-center mt-3">一级行业</h5></td>
              </tr>
              <tr v-if="profilerData.hasIndustryData">
                <td colspan="4">
                  <div class="chart-container">
                    <v-chart class="radar-chart" :option="industryChartOption" autoresize />
                  </div>
                </td>
              </tr>
              <tr v-if="profilerData.hasIndustryData">
                <td colspan="4"><h5 class="text-center mt-3">二级行业</h5></td>
              </tr>
              <tr v-if="profilerData.hasIndustryData">
                <td colspan="4">
                  <div class="chart-container">
                    <v-chart class="pie-chart" :option="industryChart2Option" autoresize />
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="4"><h5 class="text-center mt-3">职位职能</h5></td>
              </tr>
              <tr>
                <td colspan="4">
                  <div class="chart-container">
                    <v-chart class="pie-chart" :option="positionTypeChartOption" autoresize />
                  </div>
                </td>
              </tr>
            </table>
          </div>
        </div>
      </template>
    </div>

    <AIInterviewPanel
      v-show="showAIPanel && parsedData"
      :resume-data="resumeData"
      :profiler-data="profilerData"
      @close="showAIPanel = false"
    />
    <TermTooltip ref="termTooltipRef" />
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { RadarChart, PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import AIInterviewPanel from '@/components/common/AIInterviewPanel.vue'
import TermTooltip from '@/components/common/TermTooltip.vue'

use([RadarChart, PieChart, TooltipComponent, LegendComponent, CanvasRenderer])

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001'

const loading = ref(false)
const loadingText = ref('正在解析简历...')
const error = ref('')
const dragover = ref(false)
const activeTab = ref('parser')
const parsedData = ref(null)
const showAIPanel = ref(false)

const resumeData = ref({})
const parserData = ref({})
const profilerData = ref({})

const capacityChartOption = ref({})
const industryChartOption = ref({})
const industryChart2Option = ref({})
const positionTypeChartOption = ref({})

const avatarUrl = ref('')
const termTooltipRef = ref(null)

function explainTerm(term, event) {
  if (termTooltipRef.value) {
    termTooltipRef.value.show(term, event)
  }
}

function handleTermLeave() {
  if (termTooltipRef.value) {
    termTooltipRef.value.scheduleClose?.()
  }
}

// 监听AI问答事件
window.addEventListener('ai-interview-ask', (e) => {
  showAIPanel.value = true
  showAnalysis.value = false
  const inputEvent = new CustomEvent('ai-ask-message', { detail: e.detail })
  window.dispatchEvent(inputEvent)
})

const highlightBadges = computed(() => {
  return profilerData.value?.highlightBadges || []
})

const riskBadges = computed(() => {
  return profilerData.value?.riskBadges || []
})

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) parseResume(file)
}

const handleDrop = (event) => {
  dragover.value = false
  const file = event.dataTransfer.files[0]
  if (file) parseResume(file)
}

const parseResume = async (file) => {
  const allowedTypes = ['.pdf', '.doc', '.docx', '.txt', '.html', '.htm', '.rtf']
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowedTypes.includes(ext)) {
    error.value = '不支持的文件格式，请上传 PDF、Word、TXT 或 HTML 文件'
    return
  }

  if (file.size > 30 * 1024 * 1024) {
    error.value = '文件大小超过 30MB 限制'
    return
  }

  loading.value = true
  loadingText.value = '正在读取文件...'
  error.value = ''
  
  await nextTick()

  try {
    loadingText.value = '正在上传并解析简历...'
    await nextTick()

    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/v1/resumes/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error(`API 请求失败: ${response.status}`)
    }

    const result = await response.json()

    if (!result.success) {
      throw new Error(result.error || '解析失败')
    }

    const avatarData = result.parsed_data?.raw_result?.result?.avatar_data ||
                       result.parsed_data?.avatar_data ||
                       ''

    avatarUrl.value = avatarData

    transformData(result.parsed_data, avatarData)
    parsedData.value = result.parsed_data

    nextTick(() => {
      initCharts()
    })

  } catch (err) {
    error.value = err.message || '解析失败，请检查网络连接后重试'
    console.error('Resume parse error:', err)
  } finally {
    loading.value = false
  }
}

const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const base64 = reader.result.split(',')[1]
      resolve(base64)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const toFiniteNumber = (value) => {
  const num = Number(value)
  return Number.isFinite(num) ? num : 0
}

const formatSdkWeight = (value) => {
  const num = toFiniteNumber(value)
  if (!num) return ''
  return num <= 1 ? `权重：${Math.round(num * 100)}%` : `权重：${Math.round(num * 100) / 100}`
}

const getTermName = (item) => {
  if (!item || typeof item !== 'object') return ''
  return item.tag_name || item.skills_name || item.skill_name || item.cert_name || item.certificate_name || item.name || ''
}

const buildSdkTermPayload = (item, source) => {
  const explicit = item.tag_desc || item.tag_explain || item.explain || item.explanation || item.desc || item.description || ''
  const meta = [
    `来源：${source}`,
    item.tag_category ? `类型：${item.tag_category}` : '',
    formatSdkWeight(item.tag_weight)
  ].filter(Boolean)

  return {
    source,
    explanation: explicit,
    sdkMeta: meta.join('\n'),
    context: [explicit, ...meta].filter(Boolean).join('\n'),
    aiFallback: !explicit
  }
}

const addTermInfo = (map, item, source) => {
  const name = getTermName(item)
  if (!name) return
  map[name] = buildSdkTermPayload(item, source)
}

const buildTermExplanationMap = (result, tagsData, certificates = []) => {
  const map = {}

  ;(result.skills_objs || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 技能抽取'))
  ;(tagsData.skills_tags || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 技能标签'))
  ;(tagsData.pos_tags || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 职位标签'))
  ;(tagsData.pos_types || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 职能标签'))
  ;(tagsData.industries || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 行业标签'))
  ;(certificates || []).forEach(item => addTermInfo(map, item, 'ResumeSDK 证书抽取'))

  return map
}

const transformData = (parsedData, avatarData) => {
  const result = parsedData.raw_result?.result || {}
  const evalData = parsedData.eval || {}
  const tagsData = parsedData.tags || {}
  
  // 从parsed_data中获取新添加的字段
  const graduationTime = parsedData.graduation_time || result.graduation_time || result.graduation_date || ''
  const collegeType = parsedData.college_type || result.college_type || ''
  const workStartTime = parsedData.work_start_time || result.work_start_time || result.first_work_date || ''
  const workStartTimeInferred = parsedData.work_start_time_inferred || result.work_start_time_inf || result.first_work_date_inferred || ''
  const workPosTypeP = parsedData.work_pos_type_p || result.work_pos_type_p || ''
  const workYearNorm = parsedData.work_year_norm || result.work_year_norm || ''
  
  // 从parsed_data中获取期望工作字段
  const expectSalaryMin = parsedData.expect_salary_min || result.expect_salary_min || ''
  const expectSalaryMax = parsedData.expect_salary_max || result.expect_salary_max || ''
  const expectJlocation = parsedData.expect_jlocation || result.expect_jlocation || ''
  const expectJlocationNorm = parsedData.expect_jlocation_norm || result.expect_jlocation_norm || ''

  const skills = result.skills_objs && Array.isArray(result.skills_objs)
    ? result.skills_objs.map(s => s.skills_name).filter(s => s)
    : result.skills
      ? Array.isArray(result.skills)
        ? result.skills.filter(s => s)
        : typeof result.skills === 'string'
          ? result.skills.split(',').map(s => s.trim()).filter(s => s)
          : []
      : []

  const educationList = (result.education_objs || []).map(edu => ({
    period: `${edu.start_date || ''}~${edu.end_date || ''}`,
    school: edu.edu_college || '',
    major: edu.edu_major || '',
    degree: edu.edu_degree || ''
  }))

  const workExperience = (result.job_exp_objs || []).map(job => ({
    period: `${job.start_date || ''}~${job.end_date || ''}${job.job_duration ? ' | ' + job.job_duration : ''}`,
    position: job.job_position || '',
    company: job.job_cpy || '',
    description: job.job_content || '',
    positionType: job.job_pos_type_p || '',
    duration: job.job_duration || ''
  }))

  const finalAvatarUrl = avatarData || result.avatar_data || ''

  const workExps = result.job_exp_objs || []
  const educations = result.edu_exp_objs || []
  const skillsList = result.skills_objs || result.skills || []
  const certificatesList = result.all_cert_objs || result.certificate_objs || []
  const projects = result.project_objs || []

  const mergeSkills = (rawSkills) => {
    if (!Array.isArray(rawSkills) || rawSkills.length === 0) return '未提供'
    
    const skillNames = rawSkills.map(s => {
      if (typeof s === 'string') return s
      if (typeof s === 'object' && s !== null) return s.skill_name || s.skills_name || s.name || ''
      return String(s)
    }).filter(Boolean)
    
    const skillGroups = [
      { name: '总账核算', keywords: ['总账会计', '总账', '账务处理', '财务核算', '会计账务', '财务账务管理', '账务', '明细账', '核算', '结转'] },
      { name: '税务管理', keywords: ['税务处理', '税务申报', '纳税申报', '汇算清缴', '缴纳税款', '规避税务风险', '纳税申报表', '税务筹划', '税务合规', '所得税', '企业所得税', '税务机关', '税款'] },
      { name: '票据管理', keywords: ['票据管理', '发票管理', '财务票据', '普通发票', '费用报销', '原始凭证审核', '单据'] },
      { name: '财务报表', keywords: ['资产负债表', '利润表', '现金流量表', '账实相符'] },
      { name: '往来管理', keywords: ['应付账款', '客户对账', '款项管理', '核销'] },
      { name: '审计对接', keywords: ['外部审计', '内部审计', '审计报告', '工商年检'] },
      { name: '成本核算', keywords: ['成本核算', '成本全盘账务', '成本', '费用支出', '费用'] },
      { name: '出纳管理', keywords: ['出纳', '归档'] },
      { name: '财务管理', keywords: ['财务管理制度', '财务对接', '财务税务申报'] },
    ]
    
    const merged = new Set()
    const remaining = []
    
    for (const skill of skillNames) {
      const skillStr = String(skill).trim()
      let matched = false
      for (const group of skillGroups) {
        if (group.keywords.some(kw => skillStr.includes(kw) || kw.includes(skillStr))) {
          merged.add(group.name)
          matched = true
          break
        }
      }
      if (!matched) {
        remaining.push(skillStr)
      }
    }
    
    const result = [...merged, ...remaining.slice(0, 3)]
    return result.length > 0 ? result.join('、') : '未提供'
  }

  const mergedSkills = mergeSkills(skillsList)

  resumeData.value = {
    name: result.name || '未知',
    position: result.work_position || result.current_job_title || result.title || '未知职位',
    tags: generateTags(result),
    gender: result.gender || '未知',
    age: result.age || 0,
    location: result.location || result.current_location || '未知',
    experience: result.work_year || calculateWorkYears(result.job_exp_objs),
    school: result.college || (educationList[0] && educationList[0].school) || '未知',
    degree: result.degree || (educationList[0] && educationList[0].degree) || '未知',
    phone: maskPhone(result.phone),
    email: result.email || '',
    avatar: finalAvatarUrl,
    expected_salary: result.expect_salary || result.desired_salary || '未提供',
    certificates: certificatesList.length > 0 ? certificatesList.map(c => c.cert_name || c.certificate_name).filter(Boolean) : '未提供',
    skills: mergedSkills,
    major: result.major || (educations[0] && educations[0].major) || '未提供',
    self_evaluation: result.self_evaluation || result.cont_my_desc || result.personal_summary || '',
    current_company: result.work_company || result.current_company || '',
    current_function_type: workPosTypeP || result.current_function_type || '',
    work_experiences: workExps.map(job => ({
      company: job.job_company || job.company || '',
      position: job.job_pos_name || job.position || '',
      duration: job.job_duration || job.period || '',
      description: job.job_desc || job.description || ''
    })),
    education_experiences: educations.map(edu => ({
      school: edu.edu_school_name || edu.school || '',
      major: edu.edu_major || edu.major || '',
      degree: edu.edu_degree_name || edu.degree || '',
      duration: edu.edu_time || edu.period || ''
    })),
    project_experiences: projects.map(p => ({
      name: p.project_name || '',
      role: p.project_role || '',
      duration: p.project_time || '',
      description: p.project_desc || ''
    }))
  }

  const certificates = result.all_cert_objs && Array.isArray(result.all_cert_objs)
    ? result.all_cert_objs.map(c => c.cert_name).filter(s => s)
    : result.certificate_objs && Array.isArray(result.certificate_objs)
      ? result.certificate_objs.map(c => c.certificate_name || c.cert_name).filter(s => s)
      : []

  parserData.value = {
    basicInfo: {
      name: result.name || '未知',
      gender: result.gender || '未知',
      age: result.age || 0,
      workYears: (workYearNorm || result.work_year || calculateWorkYears(result.job_exp_objs)) + '年',
      graduationTime: graduationTime || '未知',
      school: result.college || (educationList[0] && educationList[0].school) || '未知',
      schoolType: collegeType || '未知',
      major: result.major || (educationList[0] && educationList[0].major) || '未知',
      degree: result.degree || (educationList[0] && educationList[0].degree) || '未知',
      workStartTime: workStartTime || '未知',
      workStartTimeInferred: workStartTimeInferred || '未知',
      currentPosition: result.work_position || result.current_job_title || result.title || '未知',
      currentFunctionType: workPosTypeP || result.current_function_type || '未知',
      currentCompany: result.work_company || result.current_company || '未知'
    },
    contact: {
      phone: result.phone || '',
      email: result.email || ''
    },
    expectation: {
      position: result.expect_job || result.desired_job_title || '未知',
      salary: result.expect_salary || result.desired_salary || '面议',
      location: result.desired_location || '未知',
      salaryMin: expectSalaryMin || '',
      salaryMax: expectSalaryMax || '',
      jlocation: expectJlocation || '',
      jlocationNorm: expectJlocationNorm || ''
    },
    educationList: educationList.length > 0 ? educationList : [{ period: '未知', school: '未知', major: '未知', degree: '未知' }],
    workExperience: workExperience.length > 0 ? workExperience : [{ period: '未知', position: '未知', company: '未知', description: '' }],
    certificates: certificates,
    certificate_text: result.cont_certificate || '',
    skills: skills.length > 0 ? skills : ['暂无技能信息'],
    selfEvaluation: parsedData.summary || result.self_evaluation || result.cont_my_desc || result.personal_summary || ''
  }

  profilerData.value = generateProfilerData(result, evalData, tagsData, certificates)

  const industryData = tagsData.industries || []
  const posTypeData = tagsData.pos_types || []
  profilerData.value.hasIndustryData = industryData.length > 0
  updateChartOptions(evalData, industryData, posTypeData, result, tagsData, certificates)
}

const generateTags = (result) => {
  const tags = []

  if (result.age && result.age < 35) {
    tags.push({ text: '年轻人才', type: 'primary' })
  }

  if (result.job_exp_objs && result.job_exp_objs.length >= 3) {
    tags.push({ text: '经验丰富', type: 'success' })
  }

  const desiredSalary = result.desired_salary || result.expect_salary || ''
  if (desiredSalary) {
    tags.push({ text: desiredSalary, type: 'info' })
  }

  if (result.degree) {
    if (result.degree.includes('硕士') || result.degree.includes('博士')) {
      tags.push({ text: result.degree, type: 'success' })
    } else if (result.degree.includes('本科')) {
      tags.push({ text: '本科学历', type: 'primary' })
    }
  }

  if (tags.length === 0) {
    tags.push({ text: '简历已解析', type: 'primary' })
  }

  return tags
}

const generateProfilerData = (result, evalData, tagsData, certificates = []) => {
  const highlightBadges = []
  const highlights = { count: 0, items: [] }
  const riskBadges = []
  const risks = { count: 0, items: [] }
  let salaryBadge = ''

  // 优先使用候选人自己的期望薪资，其次使用AI评估薪资
  if (result.expect_salary) {
    const salaryStr = result.expect_salary.replace(/[,，\s]/g, '')
    const salaryMatch = salaryStr.match(/([\d.]+)/)
    if (salaryMatch) {
      const num = parseFloat(salaryMatch[1])
      if (num > 100) {
        salaryBadge = `${Math.round(num / 1000)}K`
      } else {
        salaryBadge = `${num}K`
      }
    }
  } else if (evalData && evalData.salary) {
    const salaryK = Math.round(evalData.salary / 1000)
    salaryBadge = `${salaryK}K`
  }

  // ===== 简历亮点 =====

  // 1. 工作稳定性亮点
  if (result.job_exp_objs) {
    const avgDuration = calculateAvgDuration(result.job_exp_objs)
    if (avgDuration >= 24) {
      highlightBadges.push('工作稳定')
      let stabilityText = `【<span class="mytext-primary">工作稳定</span>】：平均每段工作经历持续【<span class="mytext-primary">${Math.round(avgDuration)}</span>】个月`
      const longJobs = result.job_exp_objs.filter(job => {
        if (job.job_duration) {
          const match = job.job_duration.match(/(\d+)年/)
          return match && parseInt(match[1]) >= 2
        }
        return false
      }).length
      if (longJobs > 0) {
        stabilityText += `，且存在【<span class="mytext-primary">${longJobs}</span>】段工作经历2年以上`
      }
      stabilityText += '；'
      highlights.count++
      highlights.items.push(stabilityText)
    }
  }

  // 2. 技能丰富度亮点
  const skills = result.skills_objs && Array.isArray(result.skills_objs)
    ? result.skills_objs.map(s => s.skills_name).filter(s => s)
    : result.skills
      ? Array.isArray(result.skills)
        ? result.skills.filter(s => s)
        : typeof result.skills === 'string'
          ? result.skills.split(',').map(s => s.trim()).filter(s => s)
          : []
      : []

  if (skills.length > 5) {
    highlightBadges.push('技能丰富')
    highlights.count++
    highlights.items.push(`【<span class="mytext-primary">技能丰富</span>】：掌握【<span class="mytext-primary">${skills.length}</span>】项专业技能；`)
  }

  // 3. 职能领域经验亮点
  const posTypes = tagsData.pos_types || []
  const industries = tagsData.industries || []
  if (posTypes.length > 0) {
    const topPosType = posTypes[0].tag_name
    let expText = `在【<span class="mytext-primary">${topPosType}</span>】职能领域`
    if (industries.length > 0) {
      const topIndustry = industries[0].tag_name
      expText += `和【<span class="mytext-primary">${topIndustry}</span>】行业`
    }
    expText += `里有【<span class="mytext-primary">较丰富</span>】工作经历；`
    highlights.count++
    highlights.items.push(expText)
  }

  // 4. 技能领域深度亮点 (从 skills_tags 分组)
  const skillsTags = tagsData.skills_tags || []
  if (skillsTags.length > 0) {
    const skillGroups = {
      '会计': [],
      '财务': [],
      '审计': [],
      '税务': []
    }
    skillsTags.forEach(st => {
      for (const key of Object.keys(skillGroups)) {
        if (st.tag_name.includes(key)) {
          skillGroups[key].push(st)
        }
      }
    })
    const groupLabels = {
      '会计': '会计',
      '财务': '财务',
      '审计': '审计/税务',
      '税务': '审计/税务'
    }
    const mergedGroups = {}
    Object.entries(skillGroups).forEach(([key, items]) => {
      const label = groupLabels[key]
      if (!mergedGroups[label]) {
        mergedGroups[label] = []
      }
      mergedGroups[label] = mergedGroups[label].concat(items)
    })
    Object.entries(mergedGroups).forEach(([label, items]) => {
      if (items.length >= 2) {
        const totalWeight = items.reduce((sum, item) => sum + item.tag_weight, 0)
        const richness = totalWeight > 1.5 ? '很丰富' : '较丰富'
        const allSkills = items.sort((a, b) => b.tag_weight - a.tag_weight).map(s => s.tag_name)
        const skillsText = allSkills.join('、')
        highlights.count++
        highlights.items.push(`【<span class="mytext-primary">${richness}</span>】的【<span class="mytext-primary">${label}</span>】经验：在${skillsText}等技能上有深入的理解；`)
      }
    })
  }

  // ===== 风险信息 =====

  // 1. 学历提示（合并院校类型和学历层次，避免重复）
  const collegeType = result.college_type || ''
  const isVocational = collegeType === '6'
  const isCollege = result.degree && (result.degree.includes('大专') || result.degree.includes('专科'))
  if (isVocational || isCollege) {
    riskBadges.push('学历提示')
    risks.count++
    if (isVocational && isCollege) {
      risks.items.push(`【<span class="mytext-warning">学历提示</span>】：毕业于【<span class="mytext-warning">职业教育</span>】院校，最高学历为【<span class="mytext-warning">${result.degree}</span>】`)
    } else if (isVocational) {
      risks.items.push(`【<span class="mytext-warning">学历提示</span>】：毕业于【<span class="mytext-warning">职业教育</span>】院校`)
    } else {
      risks.items.push(`【<span class="mytext-warning">学历提示</span>】：最高学历为【<span class="mytext-warning">${result.degree}</span>】`)
    }
  }

  // 2. 职业空档期风险
  const eduObjs = result.education_objs || []
  if (eduObjs.length > 0 && eduObjs[0].end_date && result.work_start_time) {
    const eduEnd = eduObjs[0].end_date
    const workStart = result.work_start_time
    const eduEndYear = parseInt(eduEnd)
    const eduEndMonth = eduEnd.includes('.') ? parseInt(eduEnd.split('.')[1]) : 6
    const workStartParts = workStart.split('.')
    const workStartYear = parseInt(workStartParts[0])
    const workStartMonth = workStartParts.length > 1 ? parseInt(workStartParts[1]) : 1
    const gapMonths = (workStartYear - eduEndYear) * 12 + (workStartMonth - eduEndMonth)
    if (gapMonths >= 6) {
      riskBadges.push('空档期')
      risks.count++
      risks.items.push(`【<span class="mytext-warning">空档期</span>】：候选人在 ${eduEnd}~${workStart} 期间共存在【<span class="mytext-warning">${gapMonths}个月</span>】的职业空档期；`)
    }
  }

  // ===== 智能评估 =====
  let assessmentHTML = ''
  if (evalData && evalData.salary) {
    const salaryK = Math.round(evalData.salary / 1000)
    assessmentHTML = `综合工作经历、教育背景、工作年限、行业地域等因素，该候选人的市场薪资约为 <span class="mytext-info underline font-weight-bold">${salaryK}K</span> /月；`
  } else {
    const salaryText = result.expect_salary || result.desired_salary || '面议'
    assessmentHTML = `综合工作经历、教育背景、工作年限、行业地域等因素，该候选人的市场薪资约为 <span class="mytext-info underline font-weight-bold">${salaryText}</span> /月；`
  }

  // ===== 简历标签 =====
  const tags = []

  // 基本标签
  const basicItems = []
  if (result.gender) basicItems.push({ text: result.gender, tooltip: 'gender' })
  if (result.age) {
    const age = parseInt(result.age)
    const ageRange = age < 25 ? '25岁以下' : age < 30 ? '25-30岁' : age < 35 ? '31-35岁' : age < 40 ? '35-40岁' : '40岁以上'
    basicItems.push({ text: ageRange, tooltip: 'age' })
  }
  const workYears = result.work_year || calculateWorkYears(result.job_exp_objs)
  if (workYears) {
    basicItems.push({ text: `${workYears}年以上经验`, tooltip: 'experience' })
  }
  if (salaryBadge) {
    basicItems.push({ text: `期望${salaryBadge}`, tooltip: 'expect_salary' })
  }
  if (basicItems.length > 0) {
    tags.push({
      category: '基本标签',
      iconClass: 'mytext-warning',
      badgeColor: 'primary',
      subs: [{ label: '基本：', tooltip: '', items: basicItems }]
    })
  }

  // 教育标签
  const eduSubs = []
  if (result.degree) {
    const degreeText = result.degree.includes('学历') ? result.degree : result.degree + '学历'
    eduSubs.push({ label: '基本：', tooltip: '学历标签', items: [{ text: degreeText, tooltip: '学历标签' }] })
  }
  if (result.major) {
    eduSubs.push({ label: '专业：', tooltip: '专业标签', items: [{ text: result.major + '专业', tooltip: '专业标签' }] })
  }
  const schoolName = result.college || (eduObjs.length > 0 && eduObjs[0].edu_college) || ''
  if (schoolName) {
    eduSubs.push({ label: '学校：', tooltip: '学校标签', items: [{ text: schoolName, tooltip: '学校标签' }] })
  }
  if (eduSubs.length > 0) {
    tags.push({
      category: '教育标签',
      iconClass: 'text-success',
      badgeColor: 'success',
      subs: eduSubs
    })
  }

  // 职业标签
  const careerSubs = []
  const workPositions = []
  if (result.work_position) workPositions.push(result.work_position)
  if (result.current_job_title) workPositions.push(result.current_job_title)
  if (result.title) workPositions.push(result.title)
  const posTags = tagsData.pos_tags || []
  posTags.forEach(pt => {
    if (!workPositions.includes(pt.tag_name)) {
      workPositions.push(pt.tag_name)
    }
  })
  if (workPositions.length > 0) {
    careerSubs.push({
      label: '职位：',
      tooltip: '职位标签',
      items: workPositions.slice(0, 6).map(p => ({ text: p, tooltip: '职位标签' }))
    })
  }
  if (posTypes.length > 0) {
    careerSubs.push({
      label: '职能：',
      tooltip: '职能类型标签',
      items: posTypes.map(pt => ({ text: pt.tag_name, tooltip: '职能类型标签' }))
    })
  }
  if (industries.length > 0) {
    careerSubs.push({
      label: '行业：',
      tooltip: '行业标签',
      items: industries.map(ind => ({ text: ind.tag_name, tooltip: '行业标签' }))
    })
  }
  if (careerSubs.length > 0) {
    tags.push({
      category: '职业标签',
      iconClass: 'mytext-info',
      badgeColor: 'info',
      subs: careerSubs
    })
  }

  // 其他标签 (证书)
  if (certificates.length > 0) {
    tags.push({
      category: '其他标签',
      iconClass: 'mytext-warning',
      badgeColor: 'warning',
      subs: [{
        label: '证书：',
        tooltip: '证书',
        items: certificates.map(c => ({ text: c, tooltip: '证书' }))
      }]
    })
  }

  // 技能标签
  const skillSubs = []
  const softSkillKeywords = ['责任', '沟通', '协调', '团队', '细心', '认真', '敬业', '态度', '抗压', '耐心', '严谨', '适应', '学习', '表达', '合作', '管理', '组织']
  const softSkills = skillsTags.filter(st => softSkillKeywords.some(kw => st.tag_name.includes(kw)))
  if (softSkills.length > 0) {
    skillSubs.push({
      label: '软素质：',
      tooltip: '软素质',
      items: softSkills.map(s => ({ text: s.tag_name, tooltip: '软素质' }))
    })
  }
  const techSkills = skillsTags.filter(st => !softSkills.includes(st))
  if (techSkills.length > 0) {
    skillSubs.push({
      label: '技能：',
      tooltip: '',
      items: techSkills.map(s => ({
        text: s.tag_name,
        tooltip: s.tag_category ? `类型:${s.tag_category}，权重:${Math.round(s.tag_weight * 100)}` : `权重:${Math.round(s.tag_weight * 100)}`
      }))
    })
  }
  if (skillSubs.length > 0) {
    tags.push({
      category: '技能标签',
      iconClass: 'mytext-danger',
      badgeColor: 'danger',
      subs: skillSubs
    })
  }

  return {
    highlightBadges,
    highlights,
    riskBadges,
    risks,
    salaryBadge,
    assessment: {
      count: 1,
      html: assessmentHTML
    },
    tags
  }
}

const clampScore = (value, min = 0, max = 100) => Math.max(min, Math.min(max, Math.round(value)))

const pickEvalScore = (evalData, keys) => {
  for (const key of keys) {
    const value = toFiniteNumber(evalData?.[key])
    if (value) return value <= 1 ? value * 100 : value
  }
  return 0
}

const hasText = (text, words) => words.some(word => String(text || '').includes(word))

const scoreEducation = (result) => {
  const degree = result.degree || ''
  const collegeType = String(result.college_type || '')
  let score = 45

  if (hasText(degree, ['博士'])) score = 95
  else if (hasText(degree, ['硕士', '研究生'])) score = 86
  else if (hasText(degree, ['本科'])) score = 76
  else if (hasText(degree, ['大专', '专科'])) score = 62

  const collegeBonus = {
    1: 3,
    2: 8,
    3: 10,
    4: 9,
    5: -4,
    6: -6,
    7: 6
  }

  return clampScore(score + (collegeBonus[collegeType] || 0), 35, 100)
}

const getSkillCount = (result, tagsData) => {
  if (Array.isArray(result.skills_objs)) return result.skills_objs.length
  if (Array.isArray(tagsData.skills_tags)) return tagsData.skills_tags.length
  if (Array.isArray(result.skills)) return result.skills.length
  if (typeof result.skills === 'string') return result.skills.split(',').filter(Boolean).length
  return 0
}

const buildCapacityValues = (evalData, result, tagsData, certificates = []) => {
  const jobExps = result.job_exp_objs || []
  const workYears = toFiniteNumber(result.work_year_norm || result.work_year || result.work_year_inf)
  const skillCount = getSkillCount(result, tagsData)
  const titleText = [
    result.work_position,
    result.current_job_title,
    ...(jobExps || []).map(job => job.job_position)
  ].filter(Boolean).join(' ')
  const softSkillCount = (tagsData.skills_tags || []).filter(item =>
    hasText(item.tag_name, ['沟通', '协调', '团队', '责任', '管理', '组织', '表达', '合作'])
  ).length
  const certCount = Array.isArray(certificates) ? certificates.length : 0
  const langCount = Array.isArray(result.lang_objs) ? result.lang_objs.length : 0

  return [
    pickEvalScore(evalData, ['education_score', 'edu_score', 'education', 'edu']) || scoreEducation(result),
    pickEvalScore(evalData, ['work_score', 'work_ability', 'job_score', 'career_score']) || clampScore(45 + workYears * 4 + Math.min(skillCount, 12) * 2 + jobExps.length * 3, 35, 96),
    pickEvalScore(evalData, ['management_score', 'manage_score', 'management']) || clampScore((hasText(titleText, ['经理', '主管', '负责人', '总监', '管理']) ? 62 : 42) + Math.min(workYears, 12) * 2, 30, 92),
    pickEvalScore(evalData, ['social_score', 'communication_score', 'social']) || clampScore(48 + Math.min(softSkillCount, 6) * 7 + Math.min(jobExps.length, 4) * 4, 35, 90),
    pickEvalScore(evalData, ['language_score', 'lang_score', 'language']) || clampScore(langCount ? 55 + langCount * 12 : 45, 30, 90),
    pickEvalScore(evalData, ['honor_score', 'certificate_score', 'honor']) || clampScore(38 + certCount * 14 + Math.min(toFiniteNumber(result.resume_integrity), 100) * 0.15, 30, 95)
  ]
}

const noDataChartOption = (text) => ({
  title: {
    text,
    left: 'center',
    top: 'middle',
    textStyle: {
      color: '#9aabbf',
      fontSize: 13,
      fontWeight: 500
    }
  },
  tooltip: { show: false },
  series: []
})

const radarOption = (labels, values, name, color) => ({
  tooltip: {
    trigger: 'item',
    formatter: (params) => {
      const rows = labels.map((label, index) => `${label}：${values[index]}`).join('<br/>')
      return `${params.name}<br/>${rows}`
    }
  },
  radar: {
    indicator: labels.map(label => ({ name: label, max: 100 })),
    shape: 'circle',
    center: ['50%', '50%'],
    radius: '65%',
    axisName: {
      color: '#4a5568',
      fontSize: 12
    },
    splitArea: {
      areaStyle: {
        color: [`${color}08`, `${color}14`]
      }
    },
    axisLine: {
      lineStyle: {
        color: `${color}33`
      }
    }
  },
  series: [{
    type: 'radar',
    data: [{
      value: values,
      name,
      areaStyle: {
        color: `${color}33`
      },
      lineStyle: {
        color,
        width: 2
      },
      itemStyle: {
        color
      }
    }]
  }]
})

const weightedTagData = (items = []) => {
  const validItems = items
    .map(item => ({
      name: item.tag_name,
      rawValue: toFiniteNumber(item.tag_weight)
    }))
    .filter(item => item.name && item.rawValue > 0)
  const maxWeight = Math.max(...validItems.map(item => item.rawValue), 0)

  return validItems.map(item => ({
    name: item.name,
    value: maxWeight ? clampScore((item.rawValue / maxWeight) * 100) : 0,
    rawValue: Math.round(item.rawValue * 100) / 100
  }))
}

const firstLevelIndustryData = (industryData = []) => {
  const grouped = {}
  industryData.forEach(item => {
    const name = item.tag_name || ''
    if (!name) return
    const firstLevel = name.split('-')[0] || name
    grouped[firstLevel] = (grouped[firstLevel] || 0) + toFiniteNumber(item.tag_weight)
  })

  return Object.entries(grouped)
    .map(([name, rawValue]) => ({ tag_name: name, tag_weight: rawValue }))
    .sort((a, b) => b.tag_weight - a.tag_weight)
    .slice(0, 6)
}

const pieOption = (seriesName, data, emptyText) => {
  if (!data.length) return noDataChartOption(emptyText)

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}<br/>SDK权重：{c}<br/>占比：{d}%'
    },
    legend: {
      type: 'scroll',
      top: '5%',
      left: 'center'
    },
    series: [{
      name: seriesName,
      type: 'pie',
      radius: '60%',
      center: ['50%', '58%'],
      itemStyle: {
        borderRadius: 0,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%'
      },
      data
    }]
  }
}

const updateChartOptions = (evalData, industryData = [], posTypeData = [], result = {}, tagsData = {}, certificates = []) => {
  const capacityLabels = ['教育背景', '工作能力', '管理能力', '社会能力', '语言能力', '荣誉指数']
  const capacityValues = buildCapacityValues(evalData, result, tagsData, certificates)
  capacityChartOption.value = radarOption(capacityLabels, capacityValues, '能力指数', '#335EEA')

  const industryRadarData = weightedTagData(firstLevelIndustryData(industryData))
  industryChartOption.value = industryRadarData.length
    ? radarOption(
        industryRadarData.map(item => item.name),
        industryRadarData.map(item => item.value),
        '行业匹配',
        '#42BA96'
      )
    : noDataChartOption('SDK 未返回行业标签')

  const industryChart2Data = (industryData || [])
    .filter(item => item.tag_name && toFiniteNumber(item.tag_weight) > 0)
    .map(item => ({
      name: item.tag_name,
      value: Math.round(toFiniteNumber(item.tag_weight) * 100) / 100
    }))

  industryChart2Option.value = pieOption('二级行业', industryChart2Data, 'SDK 未返回二级行业')

  const posTypeChartData = (posTypeData || [])
    .filter(item => item.tag_name && toFiniteNumber(item.tag_weight) > 0)
    .map(item => ({
      name: item.tag_name,
      value: Math.round(toFiniteNumber(item.tag_weight) * 100) / 100
    }))

  positionTypeChartOption.value = pieOption('职位职能', posTypeChartData, 'SDK 未返回职位职能')
}

const initCharts = () => {
}

const calculateWorkYears = (jobExps) => {
  if (!jobExps || jobExps.length === 0) return 0
  let totalMonths = 0
  jobExps.forEach(job => {
    if (job.start_date) {
      const start = new Date(job.start_date)
      const end = job.end_date ? new Date(job.end_date) : new Date()
      totalMonths += (end - start) / (1000 * 60 * 60 * 24 * 30)
    }
  })
  return Math.round(totalMonths / 12)
}

const calculateAvgDuration = (jobExps) => {
  if (!jobExps || jobExps.length === 0) return 0
  let totalMonths = 0
  let count = 0
  jobExps.forEach(job => {
    if (job.start_date) {
      const start = new Date(job.start_date)
      const end = job.end_date ? new Date(job.end_date) : new Date()
      totalMonths += (end - start) / (1000 * 60 * 60 * 24 * 30)
      count++
    }
  })
  return count > 0 ? totalMonths / count : 0
}

const maskPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const formatDescription = (text) => {
  if (!text) return ''
  return text.replace(/\n\s*(?=\d)/g, '<br>')
}

const reset = () => {
  parsedData.value = null
  resumeData.value = {}
  parserData.value = {}
  profilerData.value = {}
  avatarUrl.value = ''
  activeTab.value = 'parser'
  error.value = ''
}
</script>

<style lang="scss" scoped>
.resume-analysis {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 0;

  &.ai-panel-open {
    // AI面板为fixed定位，不挤压主内容区域
  }
}

.main-container {
  transition: margin-right 0.3s ease, transform 0.3s ease;
}

.ai-panel-toggle-btn {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 201;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  transition: right 0.3s ease, box-shadow 0.3s ease;

  &.panel-open {
    right: 560px;
  }

  &:hover {
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
  }

  .ai-icon {
    font-size: 18px;
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(51, 94, 234, 0.1);
    border-top-color: #335EEA;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .loading-text {
    margin-top: 1rem;
    color: #335EEA;
    font-weight: 500;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.main-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 20px 60px;
}

.upload-section {
  margin-bottom: 24px;

  .upload-card {
    background: #fff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  }

  .upload-area {
    border: 2px dashed #d0d5e0;
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover, &.dragover {
      border-color: #335EEA;
      background: rgba(51, 94, 234, 0.03);
    }

    .upload-icon {
      font-size: 48px;
      color: #335EEA;
      margin-bottom: 16px;
    }

    .upload-title {
      font-size: 18px;
      font-weight: 600;
      color: #1a2332;
      margin-bottom: 8px;
    }

    .upload-desc {
      font-size: 14px;
      color: #8695a8;
      margin-bottom: 16px;
    }

    .upload-formats {
      display: flex;
      justify-content: center;
      gap: 8px;

      .format-tag {
        padding: 4px 14px;
        background: #f0f2f5;
        border-radius: 6px;
        font-size: 12px;
        color: #5a6a7e;
        font-weight: 500;
      }
    }
  }

  .file-input { display: none; }
}

.profile-header-section {
  background: #fff;
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #eef1f5;

  .profile-main {
    display: flex;
    align-items: flex-start;
    gap: 24px;
  }

  .avatar-section {
    .avatar {
      width: 88px;
      height: 88px;
      border-radius: 50%;
      background: linear-gradient(135deg, #335EEA 0%, #1a3fa0 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 36px;
      color: white;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(51, 94, 234, 0.25);
    }

    .avatar-img {
      width: 88px;
      height: 88px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid #eef1f5;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
  }

  .profile-info {
    flex: 1;

    .name-position {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;

      .name {
        font-size: 26px;
        font-weight: 700;
        color: #1a2332;
        margin: 0;
        letter-spacing: 1px;
      }

      .position-tag {
        font-size: 13px;
        color: #335EEA;
        background: rgba(51, 94, 234, 0.08);
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 500;
        border: 1px solid rgba(51, 94, 234, 0.15);
      }
    }

    .badges-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }

    .basic-info-row, .contact-row {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 6px;

      .info-item {
        font-size: 13px;
        color: #5a6a7e;
        display: flex;
        align-items: center;
        gap: 6px;

        i {
          color: #9aabbf;
          font-size: 14px;
        }
      }
    }
  }
}

.mybadge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
  white-space: nowrap;

  i {
    font-size: 12px;
  }

  &.mybadge-primary {
    background: rgba(51, 94, 234, 0.1);
    color: #335EEA;
    border: 1px solid rgba(51, 94, 234, 0.2);
  }

  &.mybadge-success {
    background: rgba(66, 186, 150, 0.1);
    color: #2a8e6e;
    border: 1px solid rgba(66, 186, 150, 0.2);
  }

  &.mybadge-warning {
    background: rgba(245, 158, 11, 0.1);
    color: #b8860b;
    border: 1px solid rgba(245, 158, 11, 0.2);
  }

  &.mybadge-info {
    background: rgba(124, 105, 239, 0.1);
    color: #5a4abd;
    border: 1px solid rgba(124, 105, 239, 0.2);
  }

  &.mybadge-danger {
    background: rgba(223, 71, 89, 0.1);
    color: #c0392b;
    border: 1px solid rgba(223, 71, 89, 0.2);
  }
}

.tabs-section {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #eef1f5;
  overflow: hidden;
}

.tabs-nav {
  display: flex;
  border-bottom: 1px solid #eef1f5;
  background: #fafbfc;

  .tab-item {
    padding: 14px 28px;
    font-size: 14px;
    font-weight: 600;
    color: #5a6a7e;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;

    &:hover {
      color: #335EEA;
      background: rgba(51, 94, 234, 0.03);
    }

    &.active {
      color: #335EEA;
      border-bottom-color: #335EEA;
      background: rgba(51, 94, 234, 0.04);
    }

    i {
      font-size: 16px;
    }
  }
}

.tab-content {
  padding: 24px 28px;
}

.content-section {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #1a2332;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eef1f5;

  .section-icon {
    font-size: 16px;
    color: #335EEA;
  }

  .chart-icon-purple {
    color: #7C69EF;
  }

  .chart-icon-green {
    color: #42BA96;
  }

  .chart-icon-orange {
    color: #F39C12;
  }

  .chart-icon-red {
    color: #E74C3C;
  }
}

.info-grid {
  &.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 32px;
  }

  .info-row {
    display: flex;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px dashed #f0f2f5;

    .info-label {
      font-size: 13px;
      color: #8695a8;
      flex-shrink: 0;
      min-width: 80px;
    }

    .info-value {
      font-size: 14px;
      color: #1a2332;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 8px;

      &.salary-highlight {
        color: #DF4759;
        font-weight: 700;
      }
    }
  }
}

.completeness-bar {
  display: inline-block;
  width: 80px;
  height: 6px;
  background: #eef1f5;
  border-radius: 3px;
  overflow: hidden;
  vertical-align: middle;

  .completeness-fill {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #42BA96, #335EEA);
    border-radius: 3px;
    transition: width 0.6s ease;
  }
}

.completeness-text {
  font-weight: 600;
  color: #335EEA;
}

.timeline-list {
  position: relative;
  padding-left: 20px;

  &::before {
    content: '';
    position: absolute;
    left: 6px;
    top: 4px;
    bottom: 4px;
    width: 2px;
    background: #e8ecf2;
    border-radius: 1px;
  }

  .timeline-item {
    position: relative;
    padding: 0 0 20px 16px;

    &:last-child {
      padding-bottom: 0;
    }

    .timeline-marker {
      position: absolute;
      left: -20px;
      top: 4px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #335EEA;
      border: 3px solid #e0e7ff;
      z-index: 1;

      &.work-marker {
        background: #42BA96;
        border-color: #d4f0e6;
      }
    }

    .timeline-content {
      .timeline-period {
        font-size: 12px;
        color: #9aabbf;
        font-weight: 500;
        margin-bottom: 4px;
      }

      .timeline-title {
        font-size: 15px;
        font-weight: 600;
        color: #1a2332;
        margin-bottom: 2px;
      }

      .timeline-subtitle {
        font-size: 13px;
        color: #5a6a7e;
      }

      .timeline-desc {
        font-size: 13px;
        color: #5a6a7e;
        line-height: 1.6;
        margin-top: 8px;
        padding: 10px 14px;
        background: #f8f9fb;
        border-radius: 8px;
        white-space: pre-line;
      }
    }
  }
}

.cert-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  .cert-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: rgba(245, 158, 11, 0.08);
    color: #b8860b;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid rgba(245, 158, 11, 0.15);

    i {
      color: #f59e0b;
    }
  }
}

.empty-hint {
  font-size: 13px;
  color: #9aabbf;
  font-style: italic;
  padding: 8px 0;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  .skill-tag {
    padding: 6px 16px;
    background: rgba(51, 94, 234, 0.06);
    color: #335EEA;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid rgba(51, 94, 234, 0.12);
    transition: all 0.2s;

    &:hover {
      background: rgba(51, 94, 234, 0.12);
      transform: translateY(-1px);
    }
  }
}

.evaluation-text {
  font-size: 14px;
  color: #1a2332;
  line-height: 1.8;
  padding: 8px 0;
  white-space: pre-line;
}

.profile-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;

  .profile-card {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #eef1f5;
    overflow: hidden;
    transition: box-shadow 0.2s;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }

    &.card-highlights .card-header-custom {
      background: rgba(51, 94, 234, 0.04);
      border-bottom: 1px solid rgba(51, 94, 234, 0.1);
    }

    &.card-risks .card-header-custom {
      background: rgba(245, 158, 11, 0.04);
      border-bottom: 1px solid rgba(245, 158, 11, 0.1);
    }

    &.card-assessment {
      grid-column: 1 / -1;

      .card-header-custom {
        background: rgba(124, 105, 239, 0.04);
        border-bottom: 1px solid rgba(124, 105, 239, 0.1);
      }
    }

    .card-header-custom {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      font-size: 14px;
      font-weight: 600;
      color: #1a2332;

      .card-badge {
        margin-left: auto;
        background: #335EEA;
        color: white;
        font-size: 11px;
        padding: 2px 10px;
        border-radius: 10px;
        font-weight: 600;

        &.warning {
          background: #f59e0b;
        }

        &.info {
          background: #7C69EF;
        }
      }
    }

    .card-body-custom {
      padding: 14px 16px;
    }
  }
}

.profile-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 5px 0;
  font-size: 13px;
  color: #5a6a7e;
  line-height: 1.5;

  .profile-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;

    &.dot-primary { background: #335EEA; }
    &.dot-warning { background: #f59e0b; }
    &.dot-info { background: #7C69EF; }
  }

  .assessment-value {
    color: #335EEA;
    font-size: 15px;
  }
}

.tag-categories {
  .tag-category {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;

    &:last-child { margin-bottom: 0; }

    .category-name {
      font-size: 13px;
      color: #8695a8;
      font-weight: 500;
      flex-shrink: 0;
      min-width: 56px;
      line-height: 28px;
    }

    .category-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
  }
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 4px;

  .chart-section {
    background: #fafbfc;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #eef1f5;

    .section-header {
      margin-bottom: 12px;
      padding-bottom: 8px;
    }
  }

  .chart-wrapper {
    .chart-title {
      text-align: center;
      font-size: 13px;
      color: #8695a8;
      margin-bottom: 12px;
      font-weight: 500;
    }

    .radar-chart {
      height: 280px;
    }

    .pie-chart {
      height: 300px;
    }
  }

  .chart-container .radar-chart,
  .chart-container .pie-chart {
    width: 100%;
    height: 100%;
  }
}

.row-bordered {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 8px;
  margin-bottom: 16px;
  font-weight: 600;
  color: #495057;
}

.mytext-primary {
  color: #335EEA !important;
}

.mytext-muted {
  color: #6c757d !important;
}

.mybadge-pill {
  border-radius: 50px !important;
  padding: 1px 8px !important;
  font-size: 12px !important;
  min-width: 20px;
  height: 20px;
  line-height: 1 !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.mybg-primary {
  background-color: rgba(51, 94, 234, 0.1) !important;
}

.mybg-info {
  background-color: rgba(66, 186, 150, 0.1) !important;
}

.mybg-warning {
  background-color: rgba(245, 158, 11, 0.1) !important;
}

.mybg-success {
  background-color: rgba(66, 186, 150, 0.1) !important;
}

.mybg-danger {
  background-color: rgba(223, 71, 89, 0.1) !important;
}

.mytext-warning {
  color: #f59e0b !important;
}

.text-success {
  color: #28a745 !important;
}

.mytext-info {
  color: #7C69EF !important;
}

.mytext-danger {
  color: #c0392b !important;
}

.r_small_70 {
  font-size: 13px;
  color: #6c757d;
  margin-right: 4px;
  font-weight: 500;
}

.r_content {
  margin-left: 16px;
  padding-left: 8px;
  border-left: 2px solid #e9ecef;
}

.r_circle {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  vertical-align: middle;
  margin-top: -2px;
}

.r_circle.mybg-primary {
  background-color: #1d4ed8 !important;
}

.r_circle.mybg-warning {
  background-color: #d97706 !important;
}

.r_circle.mybg-info {
  background-color: #6d28d9 !important;
}

.r_circle.mybg-success {
  background-color: #047857 !important;
}

.r_circle.mybg-danger {
  background-color: #b91c1c !important;
}

.r_small {
  font-size: 14px;
  color: #6c757d;
  line-height: 1.7;

  :deep(.mytext-primary) {
    color: #335EEA !important;
  }

  :deep(.mytext-warning) {
    color: #f59e0b !important;
  }

  :deep(.mytext-info) {
    color: #7C69EF !important;
  }

  :deep(.mytext-danger) {
    color: #c0392b !important;
  }

  :deep(.mytext-success) {
    color: #42BA96 !important;
  }

  :deep(.underline) {
    text-decoration: underline;
  }

  :deep(.font-weight-bold) {
    font-weight: 700;
  }
}

.tab-content table.w-100 td {
  padding: 4px 8px;
  vertical-align: top;
}

.r_indent2 {
  margin-left: 32px;
}

.ml-1 { margin-left: 0.25rem !important; }
.ml-2 { margin-left: 0.5rem !important; }
.ml-3 { margin-left: 1rem !important; }
.ml-4 { margin-left: 1.5rem !important; }
.mr-1 { margin-right: 0.25rem !important; }
.mr-2 { margin-right: 0.5rem !important; }
.mt-1 { margin-top: 0.25rem !important; }
.mt-2 { margin-top: 0.5rem !important; }
.mt-3 { margin-top: 1rem !important; }
.mb-1 { margin-bottom: 0.25rem !important; }
.mb-2 { margin-bottom: 0.5rem !important; }
.mb-3 { margin-bottom: 1rem !important; }
.my-1 { margin-top: 0.25rem !important; margin-bottom: 0.25rem !important; }
.mx-1 { margin-left: 0.25rem !important; margin-right: 0.25rem !important; }
.mx-2 { margin-left: 0.5rem !important; margin-right: 0.5rem !important; }
.font-weight-bold { font-weight: 700 !important; }
.fw-bold { font-weight: 700 !important; }
.fw-medium { font-weight: 500 !important; }

.description-text {
  white-space: normal;
  line-height: 1.7;
}

.term-clickable {
  cursor: pointer;
  position: relative;
  transition: all 0.25s ease;
}

.term-clickable:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(51, 94, 234, 0.25);
  filter: brightness(1.1);
}

.term-clickable:active {
  transform: translateY(0);
}

.skill-term.mybadge-info {
  background: rgba(124, 105, 239, 0.12);
  color: #5a4abd;
  border: 1px solid rgba(124, 105, 239, 0.25);
}

.skill-term.mybadge-info:hover {
  background: rgba(124, 105, 239, 0.22);
  color: #4a3aad;
  border-color: rgba(124, 105, 239, 0.5);
}

.term-clickable.mybadge-primary:hover {
  background: rgba(51, 94, 234, 0.22) !important;
  color: #1d4ed8 !important;
  border-color: rgba(51, 94, 234, 0.5) !important;
}

.term-clickable.mybadge-warning:hover {
  background: rgba(245, 158, 11, 0.22) !important;
  color: #b45309 !important;
  border-color: rgba(245, 158, 11, 0.5) !important;
}

.term-clickable.mybadge-success:hover {
  background: rgba(16, 185, 129, 0.22) !important;
  color: #047857 !important;
  border-color: rgba(16, 185, 129, 0.5) !important;
}

.term-clickable.mybadge-danger:hover {
  background: rgba(239, 68, 68, 0.22) !important;
  color: #dc2626 !important;
  border-color: rgba(239, 68, 68, 0.5) !important;
}

.term-clickable.mybadge-info:hover {
  background: rgba(14, 165, 233, 0.22) !important;
  color: #0369a1 !important;
  border-color: rgba(14, 165, 233, 0.5) !important;
}

.chart-container {
  width: 100%;
  max-width: 540px;
  height: 360px;
  margin: 0 auto;
}

.table-layout {
  width: 100%;
  border-collapse: collapse;
  
  td {
    padding: 8px 12px;
    vertical-align: top;
    border-bottom: 1px solid #e9ecef;
  }
  
  tr:last-child td {
    border-bottom: none;
  }
  
  // 防止表头文本换行
  td.mytext-muted {
    white-space: nowrap;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 16px;
  }

  .profile-header-section {
    padding: 20px;

    .profile-main {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .profile-info {
      .name-position { flex-direction: column; }
      .basic-info-row, .contact-row { justify-content: center; }
    }
  }

  .info-grid.two-col {
    grid-template-columns: 1fr;
  }

  .tabs-nav .tab-item {
    padding: 12px 18px;
    font-size: 13px;
  }

  .tab-content {
    padding: 16px;
  }

  .profile-cards {
    grid-template-columns: 1fr;
  }

  .chart-grid {
    grid-template-columns: 1fr;
  }
}
</style>
