# 背景 GIF 优化方案

## 问题

`/about` 页面 Hero 区域使用了一张约 30MB 的 GIF 动画 (`public/assets/about/about_bg.gif`) 作为全屏背景，并通过 Next.js `<Image>` 组件的 `priority` 属性预加载。

每次访问 About 页面时，浏览器需要下载完整的 30MB GIF 文件后才能完成首屏渲染，导致页面白屏时间过长。

## 原因分析

| 问题 | 说明 |
|------|------|
| **文件体积大** | GIF 格式无帧间压缩，30MB 包含所有帧的完整像素数据 |
| **阻塞渲染** | `priority` 属性使 Next.js 将其作为关键资源预加载，浏览器在下载完成前不会完成渲染 |
| **内存占用高** | GIF 解码后将所有帧常驻内存 |
| **无流式加载** | 图片资源需要完整下载后才能显示 |

## 优化方案

将 GIF 动画替换为视频格式（WebM + MP4），利用视频的帧间压缩和流式加载特性。

### 核心优势

| 指标 | 优化前（GIF） | 优化后（Video） |
|------|-------------|---------------|
| 文件大小 | ~30MB | ~1-2MB |
| 首屏阻塞 | `priority` 阻塞渲染 | 异步加载 + poster 即时显示 |
| 内存占用 | 全部帧常驻内存 | 流式解码，仅当前帧 |
| 加载体验 | 白屏等待 | 立即看到静态背景 → 动画淡入 |

### 技术实现

#### 1. 新增客户端组件 `VideoBackground.tsx`

`src/components/about/VideoBackground.tsx` — 专门处理视频背景的客户端组件：

- **Poster 即时渲染**：先用一张静态 JPG 图（几十KB）作为即时背景，确保首屏秒开
- **视频异步加载**：`<video>` 标签异步加载 WebM/MP4，不阻塞页面渲染
- **平滑过渡**：视频就绪后通过 CSS `opacity` 0.6s 淡入切换，视觉无缝
- **格式回退**：优先加载体积最小的 WebM，MP4 作兼容回退
- **移动端兼容**：`muted` + `playsInline` 确保 iOS/Android 自动播放

```tsx
'use client';

export function VideoBackground() {
  const [videoReady, setVideoReady] = useState(false);

  return (
    <>
      {/* Poster 占位 — 即时显示 */}
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: 'url(/assets/about/about_bg_poster.jpg)',
          opacity: videoReady ? 0 : 1,
          transition: 'opacity 0.6s ease-in-out',
        }}
        aria-hidden="true"
      />
      {/* 视频背景 — WebM 优先，MP4 回退 */}
      <video
        autoPlay loop muted playsInline preload="metadata"
        className="absolute inset-0 h-full w-full object-cover"
        onCanPlay={() => setVideoReady(true)}
      >
        <source src="/assets/about/about_bg.webm" type="video/webm" />
        <source src="/assets/about/about_bg.mp4" type="video/mp4" />
      </video>
    </>
  );
}
```

#### 2. 更新 `AboutHero.tsx`

将原来的 `<Image src="/assets/about/about_bg.gif" fill priority />` 替换为 `<VideoBackground />`。

```diff
- <Image
-     src="/assets/about/about_bg.gif"
-     alt=""
-     fill
-     priority
-     sizes="100vw"
-     className="object-cover"
- />
+ <VideoBackground />
```

## GIF 转换为视频

在 `public/assets/about/` 目录下执行以下命令：

### 安装 ffmpeg

```powershell
# Windows (winget)
winget install ffmpeg

# Windows (chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg
```

### 转换命令

```bash
# 1. GIF → WebM（主格式，体积最小，约 500KB-1MB）
ffmpeg -i about_bg.gif \
  -c:v libvpx-vp9 \
  -crf 30 \
  -b:v 0 \
  -pix_fmt yuva420p \
  -an \
  -loop 0 \
  about_bg.webm

# 2. GIF → MP4（兼容回退，约 1-2MB）
ffmpeg -i about_bg.gif \
  -c:v libx264 \
  -crf 23 \
  -pix_fmt yuv420p \
  -an \
  -movflags +faststart \
  about_bg.mp4

# 3. 提取第一帧作为 poster 占位图
ffmpeg -i about_bg.gif \
  -vframes 1 \
  -q:v 2 \
  about_bg_poster.jpg
```

### 参数说明

| 参数 | 含义 |
|------|------|
| `-c:v libvpx-vp9` | 使用 VP9 编码器（WebM） |
| `-c:v libx264` | 使用 H.264 编码器（MP4） |
| `-crf 30` | VP9 质量参数，30 为中等质量（0-63，越低越好） |
| `-crf 23` | H.264 质量参数，23 为中等质量（0-51，越低越好） |
| `-an` | 移除音频轨道 |
| `-loop 0` | WebM 无限循环 |
| `-movflags +faststart` | MP4 元数据前置，支持流式播放 |
| `-pix_fmt yuva420p` | WebM 支持透明通道 |

## 生成产物

转换完成后 `public/assets/about/` 下应新增以下文件：

```
public/assets/about/
├── about_bg.gif          # 原始文件（可删除）
├── about_bg.webm         # WebM 视频（主格式）
├── about_bg.mp4          # MP4 视频（兼容回退）
└── about_bg_poster.jpg   # Poster 静态图（首屏占位）
```

## 影响范围

- **新增文件**：`src/components/about/VideoBackground.tsx`
- **修改文件**：`src/components/about/AboutHero.tsx`
- **新增资源**：`about_bg.webm`、`about_bg.mp4`、`about_bg_poster.jpg`
- **不影响**：页面其他功能、其他组件、国际化、SEO 等均无影响

## 注意事项

1. 视频 `autoPlay` 必须在 `<video>` 标签上同时设置 `muted`，否则浏览器会阻止自动播放
2. `playsInline` 确保 iOS Safari 内联播放，而非全屏
3. Poster 图作为 `background-image` 而非 `<img>`，可避免额外的网络请求优先级干扰
4. 如需调整视频质量/体积，可修改 `-crf` 参数（值越大体积越小，质量越低）
