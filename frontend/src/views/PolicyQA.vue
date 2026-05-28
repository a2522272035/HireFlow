<template>
  <div class="policy-qa">
    <h1>规章制度问答</h1>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="chat-card">
          <div class="chat-messages">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message', message.role]"
            >
              <div class="message-content">
                <p>{{ message.content }}</p>
                <div v-if="message.sources" class="message-sources">
                  <el-divider />
                  <p class="sources-title">参考来源:</p>
                  <ul>
                    <li v-for="(source, idx) in message.sources" :key="idx">
                      {{ source.title }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="chat-input">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="请输入您的问题..."
              @keyup.enter.ctrl="sendMessage"
            />
            <el-button
              type="primary"
              :loading="isLoading"
              @click="sendMessage"
            >
              发送
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <span>文档管理</span>
          </template>
          <el-upload
            drag
            action="/api/v1/policies/upload"
            :on-success="handleUploadSuccess"
            accept=".pdf,.doc,.docx,.txt"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
          </el-upload>

          <el-divider />

          <h4>已上传文档</h4>
          <el-list>
            <el-list-item v-for="doc in documents" :key="doc.id">
              <span>{{ doc.title }}</span>
              <el-button type="danger" size="small" @click="deleteDocument(doc.id)">
                删除
              </el-button>
            </el-list-item>
          </el-list>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'

const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const documents = ref([])

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  const userMessage = inputMessage.value
  messages.value.push({
    role: 'user',
    content: userMessage,
  })

  inputMessage.value = ''
  isLoading.value = true

  try {
    // TODO: Call API to get answer
    messages.value.push({
      role: 'assistant',
      content: '这是一个示例回答...',
      sources: [{ title: '员工手册.pdf' }],
    })
  } finally {
    isLoading.value = false
  }
}

const handleUploadSuccess = () => {
  // TODO: Refresh document list
}

const deleteDocument = (id) => {
  // TODO: Delete document
}

onMounted(() => {
  // TODO: Fetch documents
})
</script>

<style lang="scss" scoped>
.policy-qa {
  h1 {
    margin-bottom: 24px;
  }
}

.chat-card {
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
  max-height: 500px;
}

.message {
  margin-bottom: 16px;

  &.user {
    text-align: right;

    .message-content {
      background-color: #409eff;
      color: white;
      display: inline-block;
      padding: 12px 16px;
      border-radius: 16px 16px 0 16px;
      max-width: 80%;
    }
  }

  &.assistant {
    .message-content {
      background-color: white;
      display: inline-block;
      padding: 12px 16px;
      border-radius: 16px 16px 16px 0;
      max-width: 80%;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }
}

.message-sources {
  margin-top: 12px;
  font-size: 12px;

  .sources-title {
    font-weight: 600;
    margin-bottom: 4px;
  }

  ul {
    padding-left: 16px;
    margin: 0;
  }
}

.chat-input {
  display: flex;
  gap: 12px;

  .el-textarea {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .policy-qa {
    h1 {
      margin-bottom: 16px;
    }
  }

  .chat-card {
    min-height: calc(100vh - 160px);
  }

  .chat-messages {
    max-height: 52vh;
    padding: 12px;
  }

  .message {
    &.user,
    &.assistant {
      .message-content {
        max-width: 92%;
        overflow-wrap: anywhere;
        text-align: left;
      }
    }
  }

  .chat-input {
    flex-direction: column;
    gap: 10px;
  }

  .chat-input .el-button {
    width: 100%;
  }
}
</style>
