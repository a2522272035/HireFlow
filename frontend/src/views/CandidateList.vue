<template>
  <div class="candidate-list">
    <h1>候选人管理</h1>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>候选人列表</span>
          <el-button type="primary" @click="showAddDialog = true">
            添加候选人
          </el-button>
        </div>
      </template>

      <el-table :data="candidates" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="position" label="应聘职位" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewResume(row)">
              查看简历
            </el-button>
            <el-button type="success" size="small" @click="startInterview(row)">
              开始面试
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        class="pagination"
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        @current-change="handlePageChange"
      />
    </el-card>

    <!-- Add Candidate Dialog -->
    <el-dialog v-model="showAddDialog" title="添加候选人" width="500px">
      <el-form :model="newCandidate" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="newCandidate.name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="newCandidate.email" />
        </el-form-item>
        <el-form-item label="职位">
          <el-input v-model="newCandidate.position" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addCandidate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const candidates = ref([])
const loading = ref(false)
const total = ref(0)
const pageSize = ref(10)
const showAddDialog = ref(false)
const newCandidate = ref({
  name: '',
  email: '',
  position: '',
})

const getStatusType = (status) => {
  const types = {
    new: 'info',
    screening: 'warning',
    interviewing: 'primary',
    offer: 'success',
    rejected: 'danger',
  }
  return types[status] || 'info'
}

const viewResume = (candidate) => {
  router.push(`/resumes?id=${candidate.resume_id}`)
}

const startInterview = (candidate) => {
  router.push(`/interview/${candidate.id}`)
}

const addCandidate = async () => {
  // TODO: Add candidate API call
  showAddDialog.value = false
}

const handlePageChange = (page) => {
  // TODO: Fetch candidates for page
  console.log('Page:', page)
}

onMounted(() => {
  // TODO: Fetch candidates
})
</script>

<style lang="scss" scoped>
.candidate-list {
  h1 {
    margin-bottom: 24px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .candidate-list {
    h1 {
      margin-bottom: 16px;
    }
  }

  .card-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }

  .card-header .el-button {
    width: 100%;
  }

  .pagination {
    margin-top: 16px;
    justify-content: center;
  }
}
</style>
