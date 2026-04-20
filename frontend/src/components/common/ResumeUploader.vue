<template>
  <el-upload
    class="resume-uploader"
    drag
    action="/api/v1/resumes/upload"
    :on-success="handleSuccess"
    :on-error="handleError"
    :before-upload="beforeUpload"
    accept=".pdf,.doc,.docx"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖拽文件到此处或 <em>点击上传</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持 PDF、Word 格式，文件大小不超过 10MB
      </div>
    </template>
  </el-upload>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['success', 'error'])

const beforeUpload = (file) => {
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  const isAllowed = allowedTypes.includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isAllowed) {
    ElMessage.error('只支持 PDF、Word 格式的文件')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  return true
}

const handleSuccess = (response) => {
  ElMessage.success('简历上传成功')
  emit('success', response)
}

const handleError = () => {
  ElMessage.error('上传失败，请重试')
  emit('error')
}
</script>

<style lang="scss" scoped>
.resume-uploader {
  width: 100%;
}
</style>
