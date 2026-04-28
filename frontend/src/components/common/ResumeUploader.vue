<template>
  <div class="resume-uploader">
    <input
      type="file"
      ref="fileInput"
      style="display: none"
      accept=".pdf,.doc,.docx"
      @change="handleFileChange"
    />
    <div
      class="upload-area"
      @click="fileInput.click()"
      @drop.prevent="handleDrop"
      @dragover.prevent
    >
      <el-icon class="upload-icon"><upload-filled /></el-icon>
      <div class="upload-text">
        拖拽文件到此处或 <em>点击上传</em>
      </div>
      <div class="upload-tip">
        支持 PDF、Word 格式，文件大小不超过 30MB
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { resumeApi } from '@/api/resume'

const emit = defineEmits(['success', 'error'])
const fileInput = ref(null)

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  await uploadFile(file)
}

const handleDrop = async (event) => {
  const file = event.dataTransfer.files[0]
  if (!file) return
  await uploadFile(file)
}

const uploadFile = async (file) => {
  // 验证文件类型
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  const isAllowed = allowedTypes.includes(file.type) || file.name.endsWith('.pdf') || file.name.endsWith('.doc') || file.name.endsWith('.docx')

  if (!isAllowed) {
    ElMessage.error('只支持 PDF、Word 格式的文件')
    return
  }

  // 验证文件大小
  const isLt30M = file.size / 1024 / 1024 < 30
  if (!isLt30M) {
    ElMessage.error('文件大小不能超过 30MB')
    return
  }

  console.log('开始上传文件:', file.name)
  ElMessage.info('正在上传并解析简历，请稍候...')

  try {
    const response = await resumeApi.upload(file)
    console.log('上传成功，响应:', response)
    ElMessage.success('简历上传并解析成功')
    emit('success', response)
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error(error.message || '上传失败，请重试')
    emit('error', error)
  }

  // 清空 input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style lang="scss" scoped>
.resume-uploader {
  width: 100%;
}

.upload-area {
  border: 2px dashed #dcdfe6;
  border-radius: 6px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;

  &:hover {
    border-color: #409eff;
  }
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-text {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;

  em {
    color: #409eff;
    font-style: normal;
  }
}

.upload-tip {
  color: #909399;
  font-size: 12px;
}
</style>
