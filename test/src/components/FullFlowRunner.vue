<template>
  <div class="container">
    <!-- ✅ 使用共用元件處理環境與商戶 -->
    <EnvSelector @update="handleEnvUpdate" />

    <!-- 執行按鈕 -->
    <div class="test-button">
      <button :disabled="isRunning" @click="runTest">
        {{ isRunning ? '執行中...' : '執行測試' }}
      </button>
    </div>

    <!-- 🔸 輸入參數區 -->
    <div class="input-area">
      <div class="field-group">
        <label>帳號：</label>
        <input v-model="userNameInput" type="text" placeholder="請輸入帳號" />
      </div>
      <div class="field-group">
        <label>密碼：</label>
        <input v-model="passwordInput" type="password" placeholder="請輸入密碼" />
      </div>
      <div class="field-group">
        <label>姓名：</label>
        <input v-model="userRealNameInput" type="text" placeholder="未輸入自動帶入[测试]" />
      </div>
      <div class="field-group">
        <label>金額：</label>
        <input v-model="amountInput" type="number" placeholder="請輸入金額" />
      </div>
    </div>

    <!-- 結果區 -->
    <div class="result-box">
      <h3>測試結果：</h3>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EnvSelector from '@/components/common/EnvSelector.vue'

const isRunning = ref(false)
const result = ref('尚未執行測試')

// 使用者輸入參數
const userNameInput = ref('')
const userRealNameInput = ref('')
const passwordInput = ref('')
const amountInput = ref(0)


const API_BASE = `http://localhost:8000`
// const API_BASE = `https://teach-awful-trusted-minolta.trycloudflare.com`

// 從 EnvSelector 傳回來的環境與商戶狀態
const currentEnv = ref('TestEnv')
const currentMerchant = ref('Merchant1')

function handleEnvUpdate({ env, merchant }) {
  currentEnv.value = env
  currentMerchant.value = merchant
  result.value = `✅ 已切換環境為 ${env}，商戶為 ${merchant}`
}

const runTest = async () => {
  if (!userNameInput.value.trim() || !passwordInput.value.trim()) {
    result.value = '❌ 請輸入帳號與密碼'
    return
  }

  isRunning.value = true
  result.value = '執行中...\n'

  try {
    const response = await fetch(`${API_BASE}/run-login_deposit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        env: currentEnv.value,
        merchant: currentMerchant.value,
        userName: userNameInput.value,
        user_name: userRealNameInput.value,
        password: passwordInput.value,
        amount: parseFloat(amountInput.value)
      })
    })
    const data = await response.json()
    result.value = JSON.stringify(data, null, 2)
  } catch (error) {
    result.value = '錯誤：' + error.message
  } finally {
    isRunning.value = false
  }
}
</script>

<style scoped>
/* 原樣保留所有 CSS */
.container {
  padding: 20px;
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.env-switch, .merchant-switch, .test-button {
  display: flex;
  align-items: center;
  gap: 8px;
}
.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}
.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0;
  right: 0; bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 20px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #2196F3;
}
input:checked + .slider:before {
  transform: translateX(20px);
}
.input-area {
  display: flex;
  flex-wrap: wrap;
  gap: 1px;
  margin-bottom: 20px;
  align-items: center;
}
.field-group {
  display: flex;
  align-items: center;
  gap: 6px;
}
.field-group label {
  font-weight: 500;
  min-width: 20px;
}
.input-area input {
  padding: 6px 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
.result-box {
  background: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  min-height: 200px;
}
pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
