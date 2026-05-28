<template>
  <div class="dashboard">
    <h1>仪表盘</h1>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.totalResumes }}</div>
          <div class="stat-label">简历总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.totalInterviews }}</div>
          <div class="stat-label">面试次数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.pendingReports }}</div>
          <div class="stat-label">待生成报告</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.avgScore }}</div>
          <div class="stat-label">平均评分</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近简历</span>
          </template>
          <el-table :data="recentResumes" style="width: 100%">
            <el-table-column prop="candidate_name" label="候选人" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="上传时间" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>待处理面试</span>
          </template>
          <el-table :data="pendingInterviews" style="width: 100%">
            <el-table-column prop="candidate_name" label="候选人" />
            <el-table-column prop="scheduled_at" label="预约时间" />
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="startInterview(row.id)">
                  开始
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref({
  totalResumes: 0,
  totalInterviews: 0,
  pendingReports: 0,
  avgScore: 0,
})

const recentResumes = ref([])
const pendingInterviews = ref([])

const getStatusType = (status) => {
  const types = {
    pending: 'info',
    parsed: 'success',
    analyzed: 'primary',
    error: 'danger',
  }
  return types[status] || 'info'
}

const startInterview = (id) => {
  router.push(`/interview/${id}`)
}

onMounted(() => {
  // TODO: Fetch dashboard data from API
})
</script>

<style lang="scss" scoped>
.dashboard {
  h1 {
    margin-bottom: 24px;
  }
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;

  .stat-value {
    font-size: 32px;
    font-weight: 600;
    color: #409eff;
    margin-bottom: 8px;
  }

  .stat-label {
    font-size: 14px;
    color: #606266;
  }
}

.content-row {
  .el-card {
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .dashboard {
    h1 {
      margin-bottom: 16px;
    }
  }

  .stats-row {
    margin-bottom: 16px;
  }

  .stat-card {
    .stat-value {
      font-size: 28px;
    }
  }

  .content-row {
    .el-card {
      min-height: auto;
    }
  }
}
</style>
