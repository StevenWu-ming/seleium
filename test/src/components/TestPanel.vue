<template>
  <div class="container">
    <!-- 左上控制區 -->
    <div class="top-bar">
      <div class="env-switch">
        <label>選擇環境：</label>
        <div class="switch-wrapper">
          <span :class="{ active: selectedEnv === 'TestEnv' }">TestEnv</span>
          <label class="switch">
            <input type="checkbox" v-model="isProdEnv" @change="switchEnv" />
            <span class="slider"></span>
          </label>
          <span :class="{ active: selectedEnv === 'ProdEnv' }">ProdEnv</span>
        </div>
      </div>

      <!-- 新增：商戶切換區 -->
      <div class="merchant-switch">
        <label>選擇商戶：</label>
        <select v-model="selectedMerchant" @change="updateMerchant">
          <option value="Merchant1">Merchant1</option>
          <option value="Merchant2">Merchant2</option>
          <option value="Merchant5">Merchant5</option>
          <option value="Merchant7">Merchant7</option>
        </select>
      </div>

      <div class="test-button">
        <button :disabled="isRunning" @click="runTests">執行測試</button>
      </div>
    </div>

    <!-- 測試結果輸出 -->
    <div class="result-panel" :class="{ success: !error, failure: error }">
      <h3>測試結果：</h3>
      <div id="result-box">{{ resultText }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';


export default {
  name: 'TestPanel',
  setup() {
    // 環境切換相關
    const selectedEnv = ref('TestEnv');
    const isProdEnv = ref(false);
    // const API_BASE = `http://${window.location.hostname}:8000`;
    const API_BASE = `https://hidden-kelkoo-principle-satisfied.trycloudflare.com`;
    const resultText = ref('尚未執行測試');
    const isRunning = ref(false);
    const error = ref(false);

    const switchEnv = async () => {
      selectedEnv.value = isProdEnv.value ? 'ProdEnv' : 'TestEnv';
      try {
        await axios.post(`${API_BASE}/set-env`, { env: selectedEnv.value });
        resultText.value = `已切換到 ${selectedEnv.value} 環境\n請重新執行測試`;
        error.value = false;
      } catch (err) {
        resultText.value = `❌ 切換環境失敗: ${err.message}`;
        error.value = true;
      }
    };

    // 執行測試功能（保留原有邏輯）
    const runTests = async () => {
      isRunning.value = true;
      resultText.value = '測試執行中...';
      error.value = false;
      try {
        const response = await fetch(`${API_BASE}/run-tests`);
        if (!response.ok) {
          throw new Error(`伺服器回傳錯誤: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        if (!data.summary || !data.passed_tests || !data.failed_tests || !data.run_time) {
          throw new Error('回傳的資料結構不符合預期，缺少必要的鍵');
        }
        let text = `✅ 成功數: ${data.summary.pass_count}\n❌ 失敗數: ${data.summary.fail_count}\n⏱️ 執行時間: ${data.run_time}\n\n`;
        if (data.passed_tests.length > 0) {
          text += '🟢 成功的測試:\n';
          text += data.passed_tests.join('\n') + '\n\n';
        } else {
          text += '⚠️ 沒有成功的測試用例\n\n';
        }
        if (data.failed_tests.length > 0) {
          text += '🔴 失敗的測試:\n';
          text += data.failed_tests.join('\n');
        } else {
          text += '🎉 所有測試通過!';
        }
        resultText.value = text;
      } catch (err) {
        resultText.value = `❌ 測試執行失敗：${err.message}`;
        error.value = true;
      } finally {
        isRunning.value = false;
      }
    };

    // 新增：商戶切換功能
    const selectedMerchant = ref('Merchant1');
    const updateMerchant = async () => {
      try {
        await axios.post(`${API_BASE}/set-merchant`, { merchant: selectedMerchant.value });
        resultText.value = `已切換到商戶 ${selectedMerchant.value}`;
        error.value = false;
      } catch (err) {
        resultText.value = `❌ 切換商戶失敗: ${err.message}`;
        error.value = true;
      }
    };

    return {
      selectedEnv,
      isProdEnv,
      switchEnv,
      runTests,
      resultText,
      isRunning,
      error,
      // 商戶切換相關
      selectedMerchant,
      updateMerchant,
    };
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f5f5f5;
}

/* 上方控制區 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #ffffff;
  border-bottom: 1px solid #ccc;
}

/* 環境切換樣式 */
.env-switch label {
  margin-right: 10px;
  font-weight: bold;
}
.switch-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
.switch-wrapper span {
  font-size: 14px;
  color: #777;
}
.switch-wrapper span.active {
  color: #000;
  font-weight: bold;
}

/* 新增：商戶切換樣式 */
.merchant-switch {
  margin-left: 20px;
}
.merchant-switch label {
  font-weight: bold;
  margin-right: 5px;
}

/* 切換開關 */
.switch {
  position: relative;
  width: 50px;
  height: 26px;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 26px;
  transition: 0.4s;
}
.slider:before {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
}
input:checked + .slider {
  background-color: #2196f3;
}
input:checked + .slider:before {
  transform: translateX(24px);
}

/* 按鈕樣式 */
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

/* 測試結果輸出區 */
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

/* 成功／失敗配色 */
.success #result-box {
  border-left-color: #4caf50;
}
.failure #result-box {
  border-left-color: #f44336;
  color: #c62828;
}
</style>
