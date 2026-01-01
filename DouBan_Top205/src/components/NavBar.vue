<template>
  <el-menu
    mode="horizontal"
    class="navbar"
    :ellipsis="false"
    background-color="#f5f5f5"
    text-color="#333"
    active-text-color="#409EFF"
  >
    <!-- 左侧：普通 div，不是 menu-item -->
    <div class="navbar-brand">
      豆瓣 Top250
    </div>

    <!-- 右侧导航项 -->
    <el-menu-item index="home" @click="goTo('/')">首页</el-menu-item>
    <el-menu-item index="movies" @click="goTo('/movies')">电影</el-menu-item>
    <el-menu-item index="tv" @click="goTo('/tv')">电视剧</el-menu-item>
    <el-menu-item index="rankings" @click="goTo('/rankings')">榜单</el-menu-item>
    <el-menu-item index="profile" @click="goTo('/profile')">我的</el-menu-item>
  </el-menu>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goTo = (path) => router.push(path)
</script>

<style scoped>
.navbar {
  border: none;
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.navbar-brand {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  margin-right: auto; /* 推动右侧菜单靠右 */
  cursor: default;
}
</style>