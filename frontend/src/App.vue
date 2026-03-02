<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="header-left">
          <h2>病种分值管理系统</h2>
        </div>
        <div class="header-right">
          <span class="version">v3.1</span>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
// App入口
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #409eff;
  color: white;
}

.header-left h2 {
  margin: 0;
  font-weight: 500;
}

.header-right .version {
  font-size: 14px;
  opacity: 0.8;
}

.el-main {
  padding: 0;
}
</style>
