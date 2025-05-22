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

    <!-- 第三方體育轉跳檢查工具區塊 -->
    <hr />
    <div class="screenshot-section">
      <h2>第三方體育轉跳檢查</h2>
      <button :disabled="isRunningScreenshot" @click="runScreenshot">
        {{ isRunningScreenshot ? '擷取中...' : '執行體育截圖' }}
      </button>

      <div v-if="screenshotResult" class="screenshot-result">
        <h3>擷取結果：</h3>
        <ul>
          <li><strong>✅ 成功：</strong>
            <span v-if="screenshotResult.success?.length">{{ screenshotResult.success.join(', ') }}</span>
            <span v-else>無</span>
          </li>
          <li><strong>❌ 失敗：</strong>
            <span v-if="screenshotResult.failed?.length">{{ screenshotResult.failed.join(', ') }}</span>
            <span v-else>無</span>
          </li>
          <li><strong>統計：</strong> 成功 {{ screenshotResult.count?.success || 0 }} / 總共 {{ screenshotResult.count?.total || 0 }}</li>
        </ul>

        <details style="margin-top: 8px;">
          <summary>查看原始回應 JSON</summary>
          <pre>{{ screenshotResult }}</pre>
        </details>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EnvSelector from '@/components/common/EnvSelector.vue'
import { API_BASE } from '@/config/api'

const isRunning = ref(false)
const result = ref('尚未執行測試')
const isRunningScreenshot = ref(false)
const screenshotResult = ref(null)

const userNameInput = ref('')
const userRealNameInput = ref('')
const passwordInput = ref('')
const amountInput = ref(0)

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

const runScreenshot = async () => {
  isRunningScreenshot.value = true
  screenshotResult.value = null
  try {
    const res = await fetch(`${API_BASE}/run-sports-screenshot`, {
      method: 'POST'
    })
    const data = await res.json()
    screenshotResult.value = data
  } catch (error) {
    screenshotResult.value = {
      message: '❌ 擷取失敗',
      success: [],
      failed: [],
      count: { total: 0, success: 0, fail: 0 }
    }
  } finally {
    isRunningScreenshot.value = false
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}
.test-button {
  margin-top: 8px;
}
.input-area {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
  align-items: center;
}
.field-group {
  display: flex;
  align-items: center;
  gap: 6px;
}
.field-group label {
  font-weight: 500;
  min-width: 40px;
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
  margin-top: 16px;
}
.screenshot-section {
  margin-top: 32px;
}
.screenshot-result {
  margin-top: 12px;
  background: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
