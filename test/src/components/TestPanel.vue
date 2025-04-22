<template>
  <div class="container">
    <!-- ✅ 共用元件處理環境與商戶切換 -->
    <EnvSelector @update="handleUpdate" />

    <div class="test-button">
      <button :disabled="isRunning" @click="runTests">執行測試</button>
    </div>

    <div class="result-panel" :class="{ success: !error, failure: error }">
      <h3>測試結果：</h3>
      <div id="result-box">{{ resultText }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EnvSelector from '@/components/common/EnvSelector.vue'

const resultText = ref('尚未執行測試')
const isRunning = ref(false)
const error = ref(false)

// 接收環境與商戶狀態
const currentEnv = ref('TestEnv')
const currentMerchant = ref('Merchant1')

// const API_BASE = `http://localhost:8000`
const API_BASE = `https://ou-debut-composite-hawk.trycloudflare.com`

const handleUpdate = ({ env, merchant }) => {
  currentEnv.value = env
  currentMerchant.value = merchant
  resultText.value = `✅ 已切換環境為 ${env}，商戶為 ${merchant}`
  error.value = false
}

const runTests = async () => {
  isRunning.value = true
  resultText.value = '測試執行中...'
  error.value = false

  try {
    const response = await fetch(`${API_BASE}/run-tests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        env: currentEnv.value,
        merchant: currentMerchant.value
      })
    })

    const data = await response.json()

    if (data.status === 'still_running') {
      resultText.value = '⚠️ 前一輪測試尚未完成，請稍後再試'
      isRunning.value = false
      return
    }

    resultText.value = '✅ 測試已啟動，等待結果...'

    const poll = setInterval(async () => {
      const res = await fetch(`${API_BASE}/test-results`)
      const statusData = await res.json()

      if (statusData.status === 'completed') {
        clearInterval(poll)
        const d = statusData.data

        let text = `✅ 成功數: ${d.summary.pass_count}\n❌ 失敗數: ${d.summary.fail_count}\n⏱️ 執行時間: ${d.run_time}\n\n`

        if (d.passed_tests.length > 0) {
          text += '🟢 成功的測試:\n' + d.passed_tests.join('\n') + '\n\n'
        } else {
          text += '⚠️ 沒有成功的測試用例\n\n'
        }

        if (d.failed_tests.length > 0) {
          text += '🔴 失敗的測試:\n' + d.failed_tests.join('\n')
        } else {
          text += '🎉 所有測試通過!'
        }

        resultText.value = text
        error.value = false
        isRunning.value = false
      } else if (statusData.status === 'failed') {
        clearInterval(poll)
        resultText.value = `❌ 測試失敗: ${statusData.data.error}`
        error.value = true
        isRunning.value = false
      } else {
        resultText.value = '⏳ 測試執行中...'
      }
    }, 10000)
  } catch (err) {
    resultText.value = `❌ 執行測試時發生錯誤: ${err.message}`
    error.value = true
    isRunning.value = false
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f5f5f5;
}

.test-button {
  padding: 16px 24px;
  background-color: #ffffff;
  border-bottom: 1px solid #ccc;
}
.test-button button {
  padding: 8px 16px;
  font-size: 14px;
  border: 1px solid #aaa;
  background-color: #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.test-button button:hover {
  background-color: #e0e0e0;
}
.test-button button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.result-panel {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
#result-box {
  padding: 16px;
  background-color: #ffffff;
  border-left: 4px solid #ccc;
  border-radius: 4px;
  white-space: pre-line;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  min-height: 300px;
}
.success #result-box {
  border-left-color: #4caf50;
}
.failure #result-box {
  border-left-color: #f44336;
  color: #c62828;
}
</style>
