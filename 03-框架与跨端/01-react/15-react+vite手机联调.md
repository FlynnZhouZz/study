# react+vite本地开发，如何手机联调

## 1. 修改Vite配置

方式A：启动时指定参数
```bash
npm run dev -- --host
# 或
yarn dev --host
# 或
pnpm dev --host
```

方式B：修改vite.config.js
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // 监听所有地址
    port: 5173,        // Vite默认端口，可修改
    strictPort: false, // 如果端口被占用，尝试其他端口
    // 如果需要HTTPS（某些功能需要）
    // https: true,
    
    // 代理配置（如果需要）
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      }
    }
  }
})
```

方式C：修改package.json
```json
{
  "scripts": {
    "dev": "vite --host",
    "dev:mobile": "vite --host --port 3000"
  }
}
```

## 2. 启动并获取IP
```bash
# 启动开发服务器
npm run dev

# 获取IP地址（选择en0或en1）
ifconfig en0 | grep "inet "
# 或
ipconfig getifaddr en0
```

## 手机访问
```text
http://[电脑IP]:5173
```