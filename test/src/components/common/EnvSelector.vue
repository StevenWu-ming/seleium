<template>
  <div class="top-bar">
    <!-- 環境切換 -->
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

    <!-- 商戶切換 -->
    <div class="merchant-switch">
      <label>選擇商戶：</label>
      <select v-model="selectedMerchant" @change="switchMerchant">
        <option value="Merchant1">Merchant1</option>
        <option value="Merchant2">Merchant2</option>
        <option value="Merchant5">Merchant5</option>
        <option value="Merchant7">Merchant7</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['update'])
const API_BASE = `http://localhost:8000`

const selectedEnv = ref('TestEnv')
const isProdEnv = ref(false)
const selectedMerchant = ref('Merchant1')

function emitStatus() {
  emit('update', {
    env: selectedEnv.value,
    merchant: selectedMerchant.value
  })
}

const switchEnv = async () => {
  selectedEnv.value = isProdEnv.value ? 'ProdEnv' : 'TestEnv'
  try {
    await axios.post(`${API_BASE}/set-env`, { env: selectedEnv.value })
    emitStatus()
  } catch (err) {
    console.error('❌ 切換環境失敗:', err.message)
  }
}

const switchMerchant = async () => {
  try {
    await axios.post(`${API_BASE}/set-merchant`, { merchant: selectedMerchant.value })
    emitStatus()
  } catch (err) {
    console.error('❌ 切換商戶失敗:', err.message)
  }
}
</script>

<style scoped>
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #ffffff;
  border-bottom: 1px solid #ccc;
}

.env-switch label,
.merchant-switch label {
  font-weight: bold;
  margin-right: 8px;
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

.merchant-switch {
  display: flex;
  align-items: center;
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 20px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #2196f3;
}
input:checked + .slider:before {
  transform: translateX(20px);
}
</style>
