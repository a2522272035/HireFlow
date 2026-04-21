<template>
  <div class="resume-analysis">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <div class="navbar-container">
        <!-- Brand -->
        <a class="navbar-brand" href="#">
          <span class="brand-resume">RESUME</span><span class="brand-sdk">SDK</span>
        </a>

        <!-- Navigation -->
        <nav class="navbar-nav">
          <a href="#" class="nav-link active">首页</a>
          <div class="nav-item-dropdown">
            <a href="#" class="nav-link dropdown-toggle">
              产品
              <svg class="dropdown-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </a>
            <div class="dropdown-menu">
              <a href="#" class="dropdown-item">
                <div class="dropdown-icon-wrap">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 3H17C19.2091 3 21 4.79086 21 7C21 9.20914 19.2091 11 17 11H7C4.79086 11 3 9.20914 3 7C3 4.79086 4.79086 3 7 3Z" fill="#335EEA"/>
                    <path d="M7 13H17C19.2091 13 21 14.7909 21 17C21 19.2091 19.2091 21 17 21H7C4.79086 21 3 19.2091 3 17C3 14.7909 4.79086 13 7 13Z" fill="#335EEA" opacity="0.3"/>
                  </svg>
                </div>
                <div class="dropdown-content">
                  <h5 class="dropdown-title">简历解析</h5>
                  <p class="dropdown-desc">附件简历结构化解析</p>
                </div>
              </a>
              <a href="#" class="dropdown-item">
                <div class="dropdown-icon-wrap">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5.5 4H9.5C10.3284 4 11 4.67157 11 5.5V6.5C11 7.32843 10.3284 8 9.5 8H5.5C4.67157 8 4 7.32843 4 6.5V5.5C4 4.67157 4.67157 4 5.5 4Z" fill="#335EEA"/>
                    <path d="M14.5 16H18.5C19.3284 16 20 16.6716 20 17.5V18.5C20 19.3284 19.3284 20 18.5 20H14.5C13.6716 20 13 19.3284 13 18.5V17.5C13 16.6716 13.6716 16 14.5 16Z" fill="#335EEA"/>
                    <path d="M5.5 10H9.5C10.3284 10 11 10.6716 11 11.5V18.5C11 19.3284 10.3284 20 9.5 20H5.5C4.67157 20 4 19.3284 4 18.5V11.5C4 10.6716 4.67157 10 5.5 10Z" fill="#335EEA" opacity="0.3"/>
                    <path d="M14.5 4H18.5C19.3284 4 20 4.67157 20 5.5V12.5C20 13.3284 19.3284 14 18.5 14H14.5C13.6716 14 13 13.3284 13 12.5V5.5C13 4.67157 13.6716 4 14.5 4Z" fill="#335EEA" opacity="0.3"/>
                  </svg>
                </div>
                <div class="dropdown-content">
                  <h5 class="dropdown-title">简历画像</h5>
                  <p class="dropdown-desc">简历多维度标签提取及人才画像</p>
                </div>
              </a>
              <a href="#" class="dropdown-item">
                <div class="dropdown-icon-wrap">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M2.56066 10.682L4.68198 8.56066C5.26777 7.97487 6.21751 7.97487 6.8033 8.56066L8.92462 10.682C9.51041 11.2678 9.51041 12.2175 8.92462 12.8033L6.8033 14.9246C6.21751 15.5104 5.26777 15.5104 4.68198 14.9246L2.56066 12.8033C1.97487 12.2175 1.97487 11.2678 2.56066 10.682Z" fill="#335EEA" opacity="0.3"/>
                    <path d="M14.5607 10.682L16.682 8.56066C17.2678 7.97487 18.2175 7.97487 18.8033 8.56066L20.9246 10.682C21.5104 11.2678 21.5104 12.2175 20.9246 12.8033L18.8033 14.9246C18.2175 15.5104 17.2678 15.5104 16.682 14.9246L14.5607 12.8033C13.9749 12.2175 13.9749 11.2678 14.5607 10.682Z" fill="#335EEA" opacity="0.3"/>
                    <path d="M8.56066 16.682L10.682 14.5607C11.2678 13.9749 12.2175 13.9749 12.8033 14.5607L14.9246 16.682C15.5104 17.2678 15.5104 18.2175 14.9246 18.8033L12.8033 20.9246C12.2175 21.5104 11.2678 21.5104 10.682 20.9246L8.56066 18.8033C7.97487 18.2175 7.97487 17.2678 8.56066 16.682Z" fill="#335EEA"/>
                    <path d="M8.56066 4.68198L10.682 2.56066C11.2678 1.97487 12.2175 1.97487 12.8033 2.56066L14.9246 4.68198C15.5104 5.26777 15.5104 6.21751 14.9246 6.8033L12.8033 8.92462C12.2175 9.51041 11.2678 9.51041 10.682 8.92462L8.56066 6.8033C7.97487 6.21751 7.97487 5.26777 8.56066 4.68198Z" fill="#335EEA"/>
                  </svg>
                </div>
                <div class="dropdown-content">
                  <h5 class="dropdown-title">人才推荐</h5>
                  <p class="dropdown-desc">以岗推人和以人推岗</p>
                </div>
              </a>
            </div>
          </div>
          <a href="#" class="nav-link">开发文档</a>
          <a href="#" class="nav-link">关于我们</a>
        </nav>

        <!-- Actions -->
        <div class="navbar-actions">
          <button class="btn btn-primary">立即体验</button>
          <button class="btn btn-outline">申请试用</button>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 个人信息头部 -->
      <div class="profile-header-section">
        <div class="profile-main">
          <div class="avatar-section">
            <div class="avatar">{{ resumeData.basic.name ? resumeData.basic.name[0] : '?' }}</div>
          </div>
          <div class="profile-info">
            <div class="name-position">
              <h1 class="name">{{ resumeData.basic.name }}</h1>
              <span class="position-tag">{{ resumeData.basic.currentPosition }}</span>
            </div>
            <div class="basic-info-row">
              <span class="info-tag blue">{{ resumeData.basic.gender }}</span>
              <span class="info-tag blue">{{ resumeData.basic.age }}岁</span>
              <span class="info-tag">{{ resumeData.basic.education }}</span>
              <span class="info-tag">{{ resumeData.basic.workYears }}年经验</span>
            </div>
            <div class="contact-row">
              <span class="contact-item">📞 {{ resumeData.contact.phone }}</span>
              <span class="contact-item">✉️ {{ resumeData.contact.email || '暂无邮箱' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 简历信息 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">📄</span>
          <h3 class="section-title">简历信息</h3>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">简历类型:</span>
            <span class="info-value">{{ resumeData.resumeInfo.type }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">简历完整度:</span>
            <span class="info-value">{{ resumeData.resumeInfo.integrity }}%</span>
          </div>
          <div class="info-item">
            <span class="info-label">简历解析时间:</span>
            <span class="info-value">{{ resumeData.resumeInfo.parseTime }}</span>
          </div>
        </div>
      </div>

      <!-- 基本信息 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">👤</span>
          <h3 class="section-title">基本信息</h3>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">姓名:</span>
            <span class="info-value">{{ resumeData.basic.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">性别:</span>
            <span class="info-value">{{ resumeData.basic.gender }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">年龄:</span>
            <span class="info-value">{{ resumeData.basic.age }}岁</span>
          </div>
          <div class="info-item">
            <span class="info-label">工作年限:</span>
            <span class="info-value">{{ resumeData.basic.workYears }}年</span>
          </div>
          <div class="info-item">
            <span class="info-label">毕业时间:</span>
            <span class="info-value">{{ resumeData.basic.graduateYear }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">毕业学校:</span>
            <span class="info-value">{{ resumeData.basic.school }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学校类型:</span>
            <span class="info-value">{{ resumeData.basic.schoolType }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">所学专业:</span>
            <span class="info-value">{{ resumeData.basic.major }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学历:</span>
            <span class="info-value">{{ resumeData.basic.education }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">参加工作时间:</span>
            <span class="info-value">{{ resumeData.basic.workStartTime }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">当前职位:</span>
            <span class="info-value">{{ resumeData.basic.currentPosition }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">当前单位:</span>
            <span class="info-value">{{ resumeData.basic.currentCompany }}</span>
          </div>
        </div>
      </div>

      <!-- 联系方式 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">📞</span>
          <h3 class="section-title">联系方式</h3>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">联系电话:</span>
            <span class="info-value">{{ resumeData.contact.phone }}</span>
          </div>
        </div>
      </div>

      <!-- 期望工作 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">🎯</span>
          <h3 class="section-title">期望工作</h3>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">期望职位:</span>
            <span class="info-value">{{ resumeData.expectation.position }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">期望薪资:</span>
            <span class="info-value highlight">{{ resumeData.expectation.salary }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">期望工作地点:</span>
            <span class="info-value">{{ resumeData.expectation.location }}</span>
          </div>
        </div>
      </div>

      <!-- 简历亮点 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">✦</span>
          <h3 class="section-title">简历亮点</h3>
        </div>
        <div class="highlights-content">
          <div class="highlight-list">
            <div v-for="(item, index) in highlights" :key="index" class="highlight-item">
              <span class="highlight-dot blue"></span>
              <span class="highlight-text">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 风险标签 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon red">⚠</span>
          <h3 class="section-title">风险标签</h3>
        </div>
        <div class="risk-content">
          <div v-for="(category, catName) in riskCategories" :key="catName" class="risk-category-row">
            <span class="risk-cat-name">{{ catName }}:</span>
            <div class="risk-tags-row">
              <span
                v-for="tag in category"
                :key="tag.name"
                class="risk-tag-item"
                :class="tag.type"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 教育经历 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">🎓</span>
          <h3 class="section-title">教育经历</h3>
        </div>
        <div class="timeline-list">
          <div v-for="(edu, index) in resumeData.education" :key="index" class="timeline-item">
            <div class="timeline-period">{{ edu.period }}</div>
            <div class="timeline-content">
              <div class="timeline-title">{{ edu.school }}（{{ edu.schoolType }}）</div>
              <div class="timeline-detail">{{ edu.major }} | {{ edu.degree }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 工作经历 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">💼</span>
          <h3 class="section-title">工作经历</h3>
        </div>
        <div class="timeline-list">
          <div v-for="(work, index) in resumeData.workExperience" :key="index" class="timeline-item work-item">
            <div class="timeline-header">
              <div class="timeline-period">{{ work.period }} | {{ work.duration }}</div>
              <div class="timeline-title">{{ work.company }}</div>
              <div class="timeline-subtitle">{{ work.position }} | {{ work.functionType }}</div>
            </div>
            <div class="timeline-desc">{{ work.description }}</div>
          </div>
        </div>
      </div>

      <!-- 证书及奖项 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">🏆</span>
          <h3 class="section-title">证书及奖项</h3>
        </div>
        <div class="cert-list">
          <div v-for="(cert, index) in resumeData.certificates" :key="index" class="cert-item">
            <span class="cert-icon">📜</span>
            <span class="cert-name">{{ cert }}</span>
          </div>
        </div>
      </div>

      <!-- 技能列表 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">🔧</span>
          <h3 class="section-title">技能列表</h3>
        </div>
        <div class="skills-cloud">
          <span
            v-for="(skill, index) in resumeData.skills"
            :key="index"
            class="skill-tag"
            :style="getSkillTagStyle(index)"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- 自我评价 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon blue">📝</span>
          <h3 class="section-title">自我评价</h3>
        </div>
        <div class="summary-box">
          {{ resumeData.selfEvaluation }}
        </div>
      </div>

      <!-- 综合评估 - 能力雷达图 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon purple">◈</span>
          <h3 class="section-title">综合评估</h3>
        </div>
        <div class="chart-wrapper">
          <div class="chart-title">能力指数</div>
          <v-chart class="radar-chart" :option="abilityRadarOption" autoresize />
        </div>
      </div>

      <!-- 行业分析 - 一级行业雷达图 -->
      <div class="content-section">
        <div class="section-header">
          <span class="section-icon green">◈</span>
          <h3 class="section-title">行业分析</h3>
        </div>
        <div class="chart-wrapper">
          <div class="chart-title">一级行业</div>
          <v-chart class="radar-chart" :option="industryRadarOption" autoresize />
        </div>
      </div>

      <!-- 二级行业饼图 -->
      <div class="content-section">
        <div class="chart-wrapper">
          <div class="chart-title">二级行业</div>
          <v-chart class="pie-chart" :option="industryPieOption" autoresize />
        </div>
      </div>

      <!-- 职能分析饼图 -->
      <div class="content-section">
        <div class="chart-wrapper">
          <div class="chart-title">职能分析</div>
          <v-chart class="pie-chart" :option="rolePieOption" autoresize />
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">RESUME SDK</div>
        <div class="footer-links">
          <div class="link-group">
            <h4>产品</h4>
            <a href="#">简历解析</a>
            <a href="#">简历画像</a>
            <a href="#">人岗匹配</a>
          </div>
          <div class="link-group">
            <h4>开发文档</h4>
            <a href="#">API文档</a>
            <a href="#">SDK下载</a>
            <a href="#">更新日志</a>
          </div>
          <div class="link-group">
            <h4>关于我们</h4>
            <a href="#">公司介绍</a>
            <a href="#">联系我们</a>
            <a href="#">加入我们</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import VChart from 'vue-echarts'

// 简历数据
const resumeData = reactive({
  resumeInfo: {
    type: '中文',
    integrity: 60,
    parseTime: '2026-04-21 12:53:00'
  },
  basic: {
    name: '初婷',
    gender: '女',
    age: 36,
    workYears: 12,
    graduateYear: 2014,
    school: '吉林交通职业技术学院',
    schoolType: '职业教育',
    major: '电子商务',
    education: '大专',
    workStartTime: '2020.03',
    currentPosition: '总账会计',
    currentFunction: '会计',
    currentCompany: '吉林省凝德医药有限公司'
  },
  contact: {
    phone: '18943972347',
    email: ''
  },
  expectation: {
    position: '会计',
    salary: '6000元/月',
    salaryMin: 6000,
    salaryMax: 6000,
    location: '长春',
    locationNorm: '中国-吉林省-长春市'
  },
  education: [
    {
      period: '2011~2014',
      school: '吉林交通职业技术学院',
      schoolType: '职业教育',
      major: '电子商务',
      degree: '大专'
    }
  ],
  workExperience: [
    {
      period: '2023.05~2026.03',
      duration: '2年10个月',
      company: '吉林省凝德医药有限公司',
      position: '总账会计',
      functionType: '会计',
      description: '1.账务处理:负责公司全盘账务核算,包括原始凭证审核、记账凭证编制、明细账登记、总账汇总,往来款项(应收账款、应付账款),确保账务处理真实、准确、合规,做到账证相符、账实相符,定期编制资产负债表、利润表、现金流量表等财务报表,为公司经营决策提供数据支撑。\n2.税务处理:处理增值税、企业所得税、个人所得税等各类税种的申报工作,准确填报纳税申报表,按时完成纳税申报及税款缴纳,规避税务风险;合理进行税务筹划,降低企业税务成本;配合税务机关的稽查、核查工作,整理并提供相关财务资料。\n3.成本与费用管理:负责公司成本核算,归集采购成本、生产成本、销售费用等,核算产品成本,审核各项费用报销单据,严格把控费用支出,规范费用报销流程,确保费用支出合理、合规。\n4.发票与票据管理:负责增值税专用发票、普通发票的开具、保管、核销工作;整理、归档各类财务票据、凭证,确保财务资料完整可查。\n5.往来款项管理:负责公司往来款项的核对、清理工作,定期与供应商、客户对账,及时催收应收账款,合理安排应付账款支付。\n6.财务对接与配合:配合公司内部审计、外部审计工作,提供所需财务资料,协助完成审计报告;对接公司各部门,核对财务相关数据,解答各部门财务相关疑问,协调处理财务工作中的各类问题;整理、归档财务档案,确保档案管理符合相关规定。'
    },
    {
      period: '2020.03~2023.04',
      duration: '3年1个月',
      company: '吉林省聚星供应链管理有限公司',
      position: '会计',
      functionType: '会计',
      description: '1、负责公司财务、税务、工商、统计等工作\n2、负责日常费用报销单据的审核。\n3、编制记账凭证,月末结转审核当月工资表,保险表。\n4、编制财务报表,计算各项税金,并向税务申报各项税种及时缴纳税款,把控公司税负,与税务维护工作。\n5、配合财务部门开展财务部门的相关工作。处理过内外帐等全部账目,懂得一般人,小规模纳税申报和相关要求。\n6、负责企业工商年检,汇算清缴。\n7、指导出纳工作,工资发放,维护企业税务合规,降低公司费用等。'
    }
  ],
  certificates: ['会计从业资格证', '会计初级职称'],
  skills: [
    '账务处理', '财务', '税务申报', '汇算清缴', '缴纳税款', '财务核算', '税务处理',
    '规避税务风险', '核算', '纳税申报表', '会计', '账务', '费用报销单据', '税务成本',
    '全盘账务', '财务票据', '现金流量表', '原始凭证审核', '账实相符', '应付账款',
    '外部审计', '发票管理', '工商年检', '明细账', '所得税', '税务机关', '企业所得税',
    '税务筹划', '费用支出', '总账会计', '财务管理制度', '财务对接', '结转', '出纳',
    '利润表', '税务合规', '成本核算', '资产负债表', '款项管理', '归档财务', '账务管理',
    '核销', '票据管理', '普通发票', '客户对账', '内部审计', '审计报告'
  ],
  selfEvaluation: '拥有12年全职会计工作经验,熟悉财务核算、税务处理、账务管理等核心工作,具备扎实的会计专业功底。目前任职于医药公司,熟悉医药行业财务管理制度、发票管理规范、及相关税收优惠政策,严谨细致、责任心强,擅长精准处理各类账务问题、具备良好的沟通协调能力和团队协作意识,能够高效完成各项会计相关工作。'
})

// 简历亮点
const highlights = [
  '【工作稳定性】平均每段工作经历持续约3年，工作稳定性较好',
  '【职位专注度】在会计师职能领域有丰富经验，专业技能扎实',
  '【专业技能】熟悉会计、报表、财务分析、税务处理等核心流程',
  '【行业经验】具备医药行业财务管理经验，熟悉行业规范'
]

// 风险标签分类
const riskCategories = {
  '基本信息': [
    { name: '36岁', type: 'blue' },
    { name: '12年经验', type: 'blue' }
  ],
  '教育专业': [
    { name: '大专学历', type: 'blue' },
    { name: '电子商务专业', type: 'blue' },
    { name: '职业教育', type: 'blue' }
  ],
  '风险点': [
    { name: '专业不对口', type: 'red' },
    { name: '学历偏低', type: 'orange' }
  ],
  '证书': [
    { name: '会计从业资格证', type: 'green' },
    { name: '会计初级职称', type: 'green' }
  ]
}

// 技能标签样式
function getSkillTagStyle(index) {
  const colors = [
    { bg: '#e6f7ff', color: '#1890ff', border: '#91d5ff' },
    { bg: '#f6ffed', color: '#52c41a', border: '#b7eb8f' },
    { bg: '#fff7e6', color: '#fa8c16', border: '#ffd591' },
    { bg: '#fff1f0', color: '#f5222d', border: '#ffa39e' },
    { bg: '#f9f0ff', color: '#722ed1', border: '#d3adf7' },
    { bg: '#e6fffb', color: '#13c2c2', border: '#87e8de' }
  ]
  const color = colors[index % colors.length]
  return {
    backgroundColor: color.bg,
    color: color.color,
    borderColor: color.border
  }
}

// 能力雷达图配置
const abilityRadarOption = {
  color: ['#5470c6'],
  radar: {
    indicator: [
      { name: '工作能力', max: 100 },
      { name: '学习能力', max: 100 },
      { name: '沟通能力', max: 100 },
      { name: '管理能力', max: 100 },
      { name: '社会能力', max: 100 },
      { name: '逻辑能力', max: 100 }
    ],
    radius: '60%',
    center: ['50%', '50%'],
    axisName: { color: '#666', fontSize: 12 },
    splitArea: { areaStyle: { color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff'] } },
    axisLine: { lineStyle: { color: '#ddd' } },
    splitLine: { lineStyle: { color: '#ddd' } }
  },
  series: [{
    type: 'radar',
    data: [{
      value: [85, 75, 80, 70, 75, 82],
      name: '能力指数',
      areaStyle: { color: 'rgba(84, 112, 198, 0.3)' },
      lineStyle: { color: '#5470c6', width: 2 },
      itemStyle: { color: '#5470c6' }
    }]
  }]
}

// 行业雷达图配置
const industryRadarOption = {
  color: ['#91cc75'],
  radar: {
    indicator: [
      { name: '医药', max: 10 },
      { name: '供应链', max: 10 },
      { name: '专业服务', max: 10 },
      { name: '零售', max: 10 },
      { name: '制造', max: 10 }
    ],
    radius: '60%',
    center: ['50%', '50%'],
    axisName: { color: '#666', fontSize: 11 },
    splitArea: { areaStyle: { color: ['#f8f9fa', '#fff', '#f8f9fa', '#fff'] } },
    axisLine: { lineStyle: { color: '#ddd' } },
    splitLine: { lineStyle: { color: '#ddd' } }
  },
  series: [{
    type: 'radar',
    data: [{
      value: [9, 8, 7, 6, 5],
      name: '行业匹配',
      areaStyle: { color: 'rgba(145, 204, 117, 0.3)' },
      lineStyle: { color: '#91cc75', width: 2 },
      itemStyle: { color: '#91cc75' }
    }]
  }]
}

// 二级行业饼图
const industryPieOption = {
  color: ['#5470c6', '#91cc75', '#fac858', '#ee6666'],
  tooltip: { trigger: 'item', formatter: '{b}: {c}' },
  legend: {
    orient: 'vertical',
    right: '10%',
    top: 'center',
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { fontSize: 12, color: '#666' }
  },
  series: [{
    type: 'pie',
    radius: ['40%', '65%'],
    center: ['35%', '50%'],
    label: { show: false },
    emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
    labelLine: { show: false },
    data: [
      { name: '医药', value: 45 },
      { name: '供应链', value: 30 },
      { name: '专业服务', value: 15 },
      { name: '其他', value: 10 }
    ]
  }]
}

// 职能分析饼图
const rolePieOption = {
  color: ['#5470c6', '#91cc75', '#fac858'],
  tooltip: { trigger: 'item', formatter: '{b}: {c}%' },
  legend: {
    orient: 'vertical',
    right: '10%',
    top: 'center',
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { fontSize: 12, color: '#666' }
  },
  series: [{
    type: 'pie',
    radius: ['40%', '65%'],
    center: ['35%', '50%'],
    label: { show: false },
    emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
    labelLine: { show: false },
    data: [
      { name: '总账会计', value: 50 },
      { name: '会计', value: 35 },
      { name: '财务主管', value: 15 }
    ]
  }]
}
</script>

<style lang="scss" scoped>
.resume-analysis {
  min-height: 100vh;
  background: #f5f7fa;
}

// 顶部导航栏
.navbar {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 40px;
  height: 70px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;

  .navbar-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .navbar-brand {
    display: flex;
    align-items: center;
    text-decoration: none;
    font-size: 22px;
    font-weight: 700;

    .brand-resume {
      color: #335EEA;
    }

    .brand-sdk {
      color: #2D3748;
    }
  }

  .navbar-nav {
    display: flex;
    align-items: center;
    gap: 8px;

    .nav-link {
      color: #4A5568;
      text-decoration: none;
      font-size: 15px;
      font-weight: 500;
      padding: 10px 16px;
      border-radius: 6px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 4px;

      &:hover {
        color: #335EEA;
        background: #F7FAFC;
      }

      &.active {
        color: #335EEA;
      }

      .dropdown-icon {
        transition: transform 0.2s;
      }
    }

    .nav-item-dropdown {
      position: relative;

      &:hover {
        .dropdown-menu {
          opacity: 1;
          visibility: visible;
          transform: translateY(0);
        }

        .dropdown-icon {
          transform: rotate(180deg);
        }
      }
    }

    .dropdown-menu {
      position: absolute;
      top: 100%;
      left: 0;
      margin-top: 8px;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
      padding: 12px;
      min-width: 320px;
      opacity: 0;
      visibility: hidden;
      transform: translateY(-10px);
      transition: all 0.2s;

      .dropdown-item {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 16px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s;

        &:hover {
          background: #F7FAFC;
        }

        .dropdown-icon-wrap {
          flex-shrink: 0;
          width: 48px;
          height: 48px;
          background: #EBF0FF;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .dropdown-content {
          flex: 1;

          .dropdown-title {
            font-size: 14px;
            font-weight: 700;
            color: #335EEA;
            text-transform: uppercase;
            margin: 0 0 4px 0;
            letter-spacing: 0.5px;
          }

          .dropdown-desc {
            font-size: 13px;
            color: #718096;
            margin: 0;
            line-height: 1.5;
          }
        }
      }
    }
  }

  .navbar-actions {
    display: flex;
    gap: 12px;

    .btn {
      padding: 10px 24px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;

      &.btn-primary {
        background: #335EEA;
        color: white;

        &:hover {
          background: #2B4FD1;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(51, 94, 234, 0.3);
        }
      }

      &.btn-outline {
        background: transparent;
        color: #335EEA;
        border: 2px solid #335EEA;

        &:hover {
          background: #335EEA;
          color: white;
        }
      }
    }
  }
}

// 主内容区
.main-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 20px;
}

// 个人信息头部
.profile-header-section {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  .profile-main {
    display: flex;
    align-items: flex-start;
    gap: 20px;
  }

  .avatar-section {
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
        font-size: 24px;
        font-weight: 600;
        color: #262626;
        margin: 0;
      }

      .position-tag {
        font-size: 14px;
        color: #1890ff;
        background: #e6f7ff;
        padding: 4px 12px;
        border-radius: 4px;
        border: 1px solid #91d5ff;
      }
    }

    .basic-info-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;

      .info-tag {
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

    .contact-row {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;

      .contact-item {
        font-size: 13px;
        color: #8c8c8c;
      }
    }
  }
}

// 内容区块
.content-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

// 区块头部
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;

  .section-icon {
    font-size: 16px;

    &.blue { color: #1890ff; }
    &.red { color: #f5222d; }
    &.green { color: #52c41a; }
    &.orange { color: #fa8c16; }
    &.purple { color: #722ed1; }
  }

  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #262626;
    margin: 0;
  }
}

// 信息网格
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;

  .info-item {
    display: flex;
    gap: 8px;
    font-size: 14px;

    .info-label {
      color: #8c8c8c;
      flex-shrink: 0;
    }

    .info-value {
      color: #262626;

      &.highlight {
        color: #f5222d;
        font-weight: 600;
      }
    }
  }
}

// 简历亮点
.highlight-list {
  .highlight-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 6px 0;

    .highlight-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      margin-top: 8px;
      flex-shrink: 0;

      &.blue { background: #1890ff; }
    }

    .highlight-text {
      font-size: 14px;
      color: #595959;
      line-height: 1.6;
    }
  }
}

// 风险标签
.risk-content {
  display: flex;
  flex-direction: column;
  gap: 12px;

  .risk-category-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;

    .risk-cat-name {
      font-size: 13px;
      color: #8c8c8c;
      font-weight: 500;
      flex-shrink: 0;
      min-width: 70px;
    }

    .risk-tags-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;

      .risk-tag-item {
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        border: 1px solid;

        &.blue {
          background: #e6f7ff;
          color: #1890ff;
          border-color: #91d5ff;
        }

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

        &.green {
          background: #f6ffed;
          color: #52c41a;
          border-color: #b7eb8f;
        }
      }
    }
  }
}

// 时间线列表
.timeline-list {
  .timeline-item {
    padding: 16px 0;
    border-bottom: 1px solid #f0f0f0;

    &:last-child { border-bottom: none; }

    &.work-item {
      .timeline-header {
        margin-bottom: 12px;
      }
    }

    .timeline-period {
      font-size: 13px;
      color: #8c8c8c;
      margin-bottom: 4px;
    }

    .timeline-title {
      font-size: 15px;
      font-weight: 600;
      color: #262626;
      margin-bottom: 4px;
    }

    .timeline-subtitle {
      font-size: 13px;
      color: #1890ff;
      margin-bottom: 8px;
    }

    .timeline-detail {
      font-size: 13px;
      color: #666;
    }

    .timeline-desc {
      font-size: 13px;
      color: #595959;
      line-height: 1.8;
      padding: 12px;
      background: #fafafa;
      border-radius: 4px;
      white-space: pre-line;
    }
  }
}

// 证书列表
cert-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;

  .cert-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: #f6ffed;
    border: 1px solid #b7eb8f;
    border-radius: 4px;

    .cert-icon { font-size: 16px; }

    .cert-name {
      font-size: 14px;
      color: #52c41a;
      font-weight: 500;
    }
  }
}

// 技能云
.skills-cloud {
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

// 自我评价
.summary-box {
  padding: 16px;
  background: #fafafa;
  border-radius: 4px;
  font-size: 14px;
  color: #595959;
  line-height: 1.8;
}

// 图表区域
.chart-wrapper {
  .chart-title {
    text-align: center;
    font-size: 14px;
    color: #666;
    margin-bottom: 16px;
  }

  .radar-chart { height: 300px; }
  .pie-chart { height: 260px; }
}

// 底部
.footer {
  background: #fff;
  border-top: 1px solid #e8e8e8;
  padding: 40px;
  margin-top: 40px;

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
  }

  .footer-logo {
    font-size: 20px;
    font-weight: 600;
    color: #1890ff;
  }

  .footer-links {
    display: flex;
    gap: 60px;

    .link-group {
      h4 {
        font-size: 14px;
        color: #333;
        margin: 0 0 16px 0;
        font-weight: 600;
      }

      a {
        display: block;
        font-size: 13px;
        color: #666;
        text-decoration: none;
        margin-bottom: 8px;

        &:hover { color: #1890ff; }
      }
    }
  }
}

// 响应式
@media (max-width: 768px) {
  .top-header {
    padding: 0 20px;
    .header-nav { display: none; }
  }

  .main-container { padding: 16px; }

  .profile-header-section {
    .profile-main {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .profile-info {
      .name-position { flex-direction: column; gap: 8px; }
      .basic-info-row, .contact-row { justify-content: center; }
    }
  }

  .info-grid { grid-template-columns: 1fr; }

  .timeline-list {
    .timeline-item {
      .timeline-header {
        flex-direction: column;
      }
    }
  }

  .risk-category-row { flex-direction: column; gap: 8px; }

  .footer {
    .footer-content { flex-direction: column; gap: 30px; }
    .footer-links { flex-wrap: wrap; gap: 30px; }
  }
}
</style>
