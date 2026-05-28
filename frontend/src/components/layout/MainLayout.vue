<template>
  <el-container class="main-layout">
    <el-container direction="vertical">
      <AppHeader />
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
</script>

<style lang="scss" scoped>
.main-layout {
  min-height: 100vh;
}

.main-content {
  background-color: #f5f7fa;
  padding: 24px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .main-content {
    padding: 12px;
  }
}
</style>
