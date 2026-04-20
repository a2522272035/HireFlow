<template>
  <div class="resume-analysis">
    <h1>简历分析</h1>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>上传简历</span>
          </template>
          <ResumeUploader @success="handleUploadSuccess" />
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card v-if="currentResume">
          <template #header>
            <span>简历详情</span>
          </template>

          <div class="resume-info">
            <h3>{{ currentResume.candidate_name }}</h3>
            <p v-if="currentResume.candidate_email">
              <el-icon><Message /></el-icon>
              {{ currentResume.candidate_email }}
            </p>
            <p v-if="currentResume.candidate_phone">
              <el-icon><Phone /></el-icon>
              {{ currentResume.candidate_phone }}
            </p>
          </div>

          <div class="resume-section">
            <h4>技能</h4>
            <div class="skills-list">
              <SkillTag
                v-for="skill in currentResume.skills"
                :key="skill.id"
                :name="skill.skill_name"
                :level="skill.proficiency"
                :proficiency="skill.proficiency"
              />
            </div>
          </div>

          <div class="resume-section">
            <h4>工作经历</h4>
            <el-timeline>
              <el-timeline-item
                v-for="exp in currentResume.experiences"
                :key="exp.id"
                :timestamp="formatDate(exp.start_date) + ' - ' + (exp.is_current ? '至今' : formatDate(exp.end_date))"
              >
                <h5>{{ exp.title }} @ {{ exp.company }}</h5>
                <p>{{ exp.description }}</p>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>

        <el-card v-if="gaps.length > 0" class="gaps-card">
          <template #header>
            <span>简历漏洞分析</span>
          </template>
          <el-alert
            v-for="(gap, index) in gaps"
            :key="index"
            :title="gap.type"
            :description="gap.description"
            :type="gap.severity === 'high' ? 'error' : gap.severity === 'medium' ? 'warning' : 'info'"
            show-icon
            :closable="false"
            class="gap-alert"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ResumeUploader from '@/components/common/ResumeUploader.vue'
import SkillTag from '@/components/common/SkillTag.vue'
import { useResumeStore } from '@/stores/resume'
import { Message, Phone } from '@element-plus/icons-vue'

const resumeStore = useResumeStore()

const currentResume = ref(null)
const gaps = ref([])

const handleUploadSuccess = async (response) => {
  // TODO: Fetch resume details
  currentResume.value = response
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}
</script>

<style lang="scss" scoped>
.resume-analysis {
  h1 {
    margin-bottom: 24px;
  }
}

.resume-info {
  margin-bottom: 24px;

  h3 {
    margin-bottom: 12px;
  }

  p {
    color: #606266;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.resume-section {
  margin-bottom: 24px;

  h4 {
    margin-bottom: 12px;
    color: #303133;
  }
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
}

.gaps-card {
  margin-top: 20px;
}

.gap-alert {
  margin-bottom: 12px;
}
</style>
