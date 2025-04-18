<template>
    <div class="main-layout">
      <!-- 左側分頁 -->
      <aside class="sidebar">
        <ul>
          <li
            v-for="tab in tabs"
            :key="tab"
            @click="currentTab = tab"
            :class="{ active: currentTab === tab }"
          >
            {{ tab }}
          </li>
        </ul>
      </aside>
  
      <!-- 右側對應元件 -->
      <main class="main-content">
        <component :is="tabComponentMap[currentTab]" />
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import TestPanel from './TestPanel.vue'
  import FullFlowRunner from './FullFlowRunner.vue'
  
  const tabs = ['UI自動化', '自動化工具']
  const currentTab = ref(tabs[0])
  
  const tabComponentMap = {
    'UI自動化': TestPanel,
    '自動化工具': FullFlowRunner
  }
  </script>
  
  <style scoped>
  .main-layout {
    display: flex;
    height: 100vh;
  }
  .sidebar {
    width: 200px;
    background: #f5f5f5;
    padding: 20px;
    border-right: 1px solid #ddd;
  }
  .sidebar li {
    list-style: none;
    padding: 10px;
    cursor: pointer;
    margin-bottom: 10px;
  }
  .sidebar li.active {
    font-weight: bold;
    color: white;
    background-color: #007bff;
    border-radius: 4px;
  }
  .main-content {
    flex: 1;
    padding: 20px;
  }
  </style>
  