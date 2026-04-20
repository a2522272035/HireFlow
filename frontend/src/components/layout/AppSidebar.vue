<template>
  <el-aside width="220px" class="app-sidebar">
    <el-menu
      :default-active="$route.path"
      router
      class="sidebar-menu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409eff"
    >
      <el-menu-item index="/">
        <el-icon><Odometer /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>

      <el-menu-item index="/resumes">
        <el-icon><Document /></el-icon>
        <span>简历分析</span>
      </el-menu-item>

      <el-menu-item index="/interviews">
        <el-icon><User /></el-icon>
        <span>候选人管理</span>
      </el-menu-item>

      <el-menu-item index="/questions">
        <el-icon><ChatDotRound /></el-icon>
        <span>提问清单</span>
      </el-menu-item>

      <el-menu-item index="/policies">
        <el-icon><Collection /></el-icon>
        <span>规章制度问答</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { Odometer, Document, User, ChatDotRound, Collection } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
.app-sidebar {
  background-color: #304156;
  min-height: 100vh;
}

.sidebar-menu {
  border-right: none;
  min-height: 100vh;
}
</style>
