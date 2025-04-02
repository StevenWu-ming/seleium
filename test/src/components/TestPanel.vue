<template>
    <div class="container">
      <!-- 環境切換區域 -->
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
  
      <!-- 左欄：操作區域 -->
      <div class="left-panel">
        <h2>執行按鈕</h2>
        <button :disabled="isRunning" @click="runTests">執行測試</button>
      </div>
  
      <!-- 右欄：結果區域 -->
      <div class="right-panel">
        <h3>測試結果：</h3>
        <div id="result-box" :class="{ success: !error, failure: error }">
          {{ resultText }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  import Config from '../config';
  
  export default {
    name: 'TestPanel',
    setup() {
      // 環境切換相關
      const selectedEnv = ref(Config.ENV); // 當前選擇的環境，預設為 Config.ENV
      const isProdEnv = ref(selectedEnv.value === 'ProdEnv'); // 控制切換按鈕的狀態
  
      // 動態計算當前配置
      const currentConfig = computed(() => {
        return Config.getCurrentConfig(selectedEnv.value);
      });
  
      // 切換環境
      const switchEnv = () => {
        selectedEnv.value = isProdEnv.value ? 'ProdEnv' : 'TestEnv';
        resultText.value = `已切換到 ${selectedEnv.value} 環境\n請重新執行測試`;
        error.value = false;
      };
  
      // 測試執行相關
      const resultText = ref('尚未執行測試'); // 結果文字
      const isRunning = ref(false); // 按鈕是否禁用
      const error = ref(false); // 是否有錯誤
  
      const runTests = async () => {
        isRunning.value = true; // 禁用按鈕
        resultText.value = '測試執行中...'; // 更新結果文字
        error.value = false; // 重置錯誤狀態
  
        try {
          // 使用當前環境的 BASE_SC_URL 發送 API 請求
          const response = await fetch(`http://127.0.0.1:8000/run-tests`);
          // const API_BASE_URL = "http://127.0.0.1:8000"; // local
          // const API_BASE_URL = "http://192.168.0.157:8000"; // 區網
          if (!response.ok) {
            throw new Error(`伺服器回傳錯誤: ${response.status} ${response.statusText}`);
          }
          const data = await response.json();
  
          // 檢查資料結構是否符合預期
          if (!data.summary || !data.passed_tests || !data.failed_tests || !data.run_time) {
            throw new Error('回傳的資料結構不符合預期，缺少必要的鍵');
          }
  
          // 構建結果文字
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
  
          resultText.value = text; // 更新結果文字
        } catch (err) {
          resultText.value = `❌ 測試執行失敗：${err.message}\n請檢查伺服器是否運行，或確認 API 回傳格式是否正確`;
          error.value = true; // 標記為錯誤狀態
          console.error('錯誤:', err);
        } finally {
          isRunning.value = false; // 重新啟用按鈕
        }
      };
  
      return {
        selectedEnv,
        isProdEnv,
        switchEnv,
        currentConfig,
        resultText,
        isRunning,
        error,
        runTests,
      };
    },
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  /* 環境切換區域 */
  .env-switch {
    width: 100%;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .switch-wrapper {
    display: inline-flex;
    align-items: center;
    gap: 10px;
  }
  
  .switch-wrapper span {
    font-size: 16px;
    color: #666;
  }
  
  .switch-wrapper span.active {
    color: #000;
    font-weight: bold;
  }
  
  /* 切換按鈕樣式 */
  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }
  
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.4s;
    border-radius: 34px;
  }
  
  .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
  }
  
  input:checked + .slider {
    background-color: #2196f3;
  }
  
  input:checked + .slider:before {
    transform: translateX(26px);
  }
  
  /* 左欄：操作區域 */
  .left-panel {
    width: 30%;
    text-align: center;
  }
  
  .left-panel h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .left-panel button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .left-panel button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  /* 右欄：結果區域 */
  .right-panel {
    width: 65%;
  }
  
  .right-panel h3 {
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  #result-box {
    padding: 10px;
    border: 1px solid #ddd;
    background-color: #f9f9f9;
    text-align: left;
    white-space: pre-line;
    min-height: 100px;
  }
  
  .success {
    color: green;
  }
  
  .failure {
    color: red;
  }
  </style>