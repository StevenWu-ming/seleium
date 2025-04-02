import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 綁定所有網卡，讓區網設備能訪問
    port: 5173,      // 可自定其他 port，例如 3000、8080 等
    strictPort: true // 如果 port 被占用會直接報錯，不會自動換 port（可選）
  }
})
