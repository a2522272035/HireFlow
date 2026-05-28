<template>
  <div class="question-list">
    <h1>面试提问清单</h1>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>问题库</span>
          <el-button type="primary" @click="generateQuestions">
            生成新问题
          </el-button>
        </div>
      </template>

      <el-table :data="questions" style="width: 100%">
        <el-table-column type="index" width="50" />
        <el-table-column prop="category" label="类别" width="120">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)">
              {{ row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="question" label="问题" />
        <el-table-column prop="intent" label="考察意图" width="200" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="useQuestion(row)">
              使用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const questions = ref([])

const getCategoryType = (category) => {
  const types = {
    technical: 'primary',
    behavioral: 'success',
    gap: 'warning',
  }
  return types[category] || 'info'
}

const generateQuestions = async () => {
  // TODO: Generate questions from API
}

const useQuestion = (question) => {
  // TODO: Add question to current interview
}

onMounted(() => {
  // TODO: Fetch questions
})
</script>

<style lang="scss" scoped>
.question-list {
  h1 {
    margin-bottom: 24px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .question-list {
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
}
</style>
