# 基于umijs 4.0 搭建官网

## 相关官网

[Umijs](https://umijs.org)
[ProComponents](https://procomponents.ant.design)

## 创建项目
```shell
yarn create umi
```

## 新建`.editorconfig`
```
# http://editorconfig.org
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

## 配置开发环境https

1、修改本地hosts
```shell
# MacOS
sudo vim /ets/hosts

# i 进入编辑状态
# ESC 退出编辑状态
# :wq 保存并退出

# 添加如下行
127.0.0.1       umi_template.com
```

2、安装`mkcert`
```shell
# macOS
brew install mkcert
mkcert -install

# Windows
choco install mkcert
mkcert -install
```

校验安装是否成功：
```shell
mkcert --version
```

3、生成证书
在你的项目根目录下执行
```shell
mkcert localhost 127.0.0.1 umi_template.com
```

4、配置 UmiJS
```js
// .umirc.ts
import { defineConfig } from '@umijs/max';
import { resolve } from 'path';

export default defineConfig({
    https: {
        http2: false,
        hosts: ['umi_template.com'],
        key: resolve(__dirname, './umi_template.com-key.pem'),
        cert: resolve(__dirname, './umi_template.com.pem'),
    },
});
```

## 配置
```js
// .umirc.ts
import { defineConfig } from '@umijs/max';

export default defineConfig({
    antd: {},
    access: {},
    model: {},
    initialState: {},
    request: {},
    layout: {
        title: '@umijs/max',
    },
    theme: {
        '@primary-color': '#2b79b6',
    },
    https: {
        hosts: ['umi_template.com'],
    },
    proxy: {
        '/api': {
            target: process.env.NODE_ENV === 'development' ? 'http://8.130.80.26' : 'https://admin.8mile.net',
            changeOrigin: true,
        },
    },
    routes: [
        {
            path: '/',
            component: '@/layouts/index',
            routes: [
                { path: '/', component: '@/pages/home' },
                // 默认 404
                { path: '/404', component: '@/pages/404' },
                { path: '/*', component: '@/pages/404' },
            ],
        },
    ],
    npmClient: 'yarn',
});
```

## 使用scss

### 安装`sass`
```shell
yarn add sass stylelint-scss -D
```

### 编辑`.stylelintrc.js`
```js
module.exports = {
    extends: [
        require.resolve('@umijs/max/stylelint'),
        'stylelint-config-standard-scss',
    ],
    plugins: ['stylelint-scss'],
};
```

### 新建`var.scss`/`mixin.scss`/`main.scss`
```scss
// src/styles/var.scss
$main: #2b79b6;

$orange: #dab27d;
$white: #fff;
$black: #000;
$black60: rgba(0, 0, 0, 0.6);
$link: #4c1d85;
$green: #40e0d0;
$red: #e03236;

$font: #333;
$font1: #666;
$font2: #999;
$font3: #d1d1d1;

$line: #f0f0f0;
$line1: #ebeef5;

$bgd: #f4f5f6;
$bgd1: #ebeef5;
$bgd2: #f9f9f9;

$shadow: #ebecec;
$shadow2: rgba(#073d7d, 0.1);

$pcMinWidth: 1200px;

$dur: 0.2s;
$headHeight: 60px;
$headTopHeight: 0px;
$footerHeight: 400px;
:export {
    headHeight: $headHeight;
    headTopHeight: $headTopHeight;
    footerHeight: $footerHeight;
}
```

```scss
// src/styles/mixin.scss
@use "sass:math";
@use "sass:meta";
@use "sass:string";

@function fpx($val) {
    @return $val * 1.05px;
}

/**
 * 数值计算
 * @param  $val  值
 * @param  $isM  是否移动端，默认：false
 */
@function px($val, $isM: null) {
    // 自动判断移动端（如果未显式指定）
    @if $isM == null {
        $isM: if(&, string.index(#{&}, "mobile") or string.index(#{&}, ".mobile"), false);
    }
    @if math.is-unitless($val) {
        @if $isM {
            // 移动端
            @return math.div($val, 3.75) * 1vw;
        } @else {
            // pc端
            @return $val * 1px;
        }
    } @else {
        @if $isM {
            // 移动端
            @return math.div($val, 3.75);
        } @else {
            // pc端
            @return $val;
        }
    }
}

// 750基准
@function px2($val) {
    $newVal: math.div($val, 2);
    @if math.is-unitless($newVal) {
        @return math.div($newVal, 3.75) * 1vw;
    } @else {
        @return math.div($newVal, 3.75);
    }
}

@mixin shadow($x: 0, $y: 10px, $blur: 60px, $spe: 0, $color: $shadow) {
    box-shadow: $x $y $blur $spe $color;
}

@mixin clear {
    &:after {
        content: " ";
        display: block;
        clear: both;
    }
}

@mixin placeholder {
    input::-webkit-input-placeholder {
        @content;
        color: red;
    }
    input:-moz-placeholder {
        @content;
        color: red;
    }
    input::-moz-placeholder {
        @content;
        color: red;
    }
    input:-ms-input-placeholder {
        @content;
        color: red;
    }
}

/**
 * 流布局
 * @param  $fd  模式(row/row-reverse/column/column-reverse)，默认: row
 * @param  $layout  布局(SS/SC/SbC/SaC/CC)，默认: SS
 *   $layout值 说明：[S: flex-start; C: center; E: flex-end; Sb: space-between; Sa: space-around]
 * 具体效果可参考example的index flex 或者 entry.scss
 */
@mixin flex($fd: row, $layout: "SS", $fw: nowrap) {
    display: flex;
    flex-direction: $fd;
    @if $layout != "SS" {
        align-items: center;
    }
    @if $layout == "CC" {
        justify-content: center;
    }
    @if $layout == "SbC" {
        justify-content: space-between;
    }
    @if $layout == "SaC" {
        justify-content: space-around;
    }
    flex-wrap: $fw;
}

/**
 * 文本省略样式
 * @param  $line  文本限制行数，默认: 1
 */
@mixin ellipsis($line: 1) {
    overflow: hidden;
    text-overflow: ellipsis;
    @if $line == 1 {
        white-space: nowrap;
    } @else {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: $line;
    }
}

/**
 * 字体样式
 * @param  $fontSize  字体大小，默认: 14
 * @param  $color  字体颜色，默认: $font
 * @param  $fontWeight  字体粗细，默认: 'normal'
 */
@mixin fontStyle($fontSize: 16, $color: $font, $fontWeight: normal) {
    font-size: px($fontSize);
    color: $color;
    line-height: px($fontSize * 1.8);
    font-weight: $fontWeight;
    white-space: pre-line;
    // word-break: break-all;
    word-wrap: break-word;
}

/**
 * 背景图片样式
 * @param  $bgImg  背景图
 * @param  $bgSize  背景图大小(length/percentage/cover/contain)，默认: cover
 * @param  $posit  背景图定位，默认: center
 * @param  $repeat  背景图平铺方式，默认: no-repeat
 */
@mixin bgImgStyle($bgImg: "", $bgSize: cover, $posit: center, $repeat: no-repeat) {
    @if $bgImg {
        background-image: $bgImg;
    }
    background-size: $bgSize;
    background-position: $posit;
    background-repeat: $repeat;
}

/**
 * icon样式
 * @param  $w  箭头大小，默认: 14
 * @param  $icon  arrowRight
 */
@mixin icon($w: 14, $icon) {
    width: px($w);
    height: px($w);
    @include bgImgStyle($icon, cover);
}

/**
 * 页面内容宽度
 */
@mixin pageInnerW($w: 1200) {
    margin: 0 auto;
    width: px($w);

    // 移动端样式
    @media (max-width: 991px) {
        width: 100%;
        padding: 0 px(18);
    }
}
```


```scss
// src/styles/main.scss
@import 'var';
@import 'mixin';


.customReadcrumb {
    // PC端样式
    @media (min-width: 992px) {
        padding: px(18) 0;
        @include pageInnerW();
    }

    // 移动端样式
    @media (max-width: 991px) {
        width: 100%;
        padding: px(18);
    }
    span {
        font-size: fpx(16);
    }
}
.customDivider {
    margin: 0;
}
.box1 {
    // PC端样式
    @media (min-width: 992px) {
        padding: px(40) 0;
    }

    // 移动端样式
    @media (max-width: 991px) {
        padding: px(24) 0;
    }
    :global {
        .box1Inner {
            // PC端样式
            @media (min-width: 992px) {
                @include pageInnerW();
            }

            // 移动端样式
            @media (max-width: 991px) {
                width: 100%;
                padding: 0 px(18);
            }
        }
    }
}
.bg {
    background-color: #efefef;
}
.bg1 {
    background-color: $white;
}
:global {
    .my-mask {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        top: 0;
        z-index: 1;
        background-color: rgba(0, 0, 0, 0.5);
    }
}
.contentHtml {
    table {
        border-collapse: separate;
        border-spacing: 0;
        border-width: 1px 0 0 1px;
        margin: 0 0 1.5em;
        width: 100%;
    }
    table,
    td,
    th {
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    td,
    th {
        padding: px(8);
        border-width: 0 1px 1px 0;
    }
    p {
        @include fontStyle();
        margin-bottom: px(30);
    }
}
```

## 使用
```scss
// src/styles/home.scss
@use "~@/styles/main.scss" as *;

.homeContainer {
    background-color: $red;
}
```

`src/pages/home.tsx`
```tsx
import Guide from '@/components/Guide';
import styles from '@/styles/home.scss';
import { trim } from '@/utils/format';
import { useModel } from '@umijs/max';

const HomePage: React.FC = () => {
    const { name } = useModel('global');
    return (
        <div className={styles.homeContainer}>
            <Guide name={trim(name)} />
        </div>
    );
};

export default HomePage;
```

## 编辑`src/app.ts`

umi max默认使用的procomponent的ProLayout组件，是后台管理的布局。但是我们是要开发官网，所以需要重置ProLayout
```js
// 运行时配置

// 全局初始化数据配置，用于 Layout 用户信息和权限初始化
// 更多信息见文档：https://umijs.org/docs/api/runtime-config#getinitialstate
export async function getInitialState(): Promise<{ name: string }> {
    return { name: '@umijs/max' };
}

// 更多信息见文档：https://procomponents.ant.design/components/layout
export const layout = () => {
    return {
        layout: 'top',
        menuRender: false,
        headerRender: false,
        appListRender: false,
        contentStyle: {
            padding: '0px',
        },
    };
};
```

## svg组件

1、新建`public/assets/svg`目录，存放svg文件

2、新建`src/typing/components/DynamicSvg.ts`类型声明文件
```js
import React from 'react';

export type DynamicSvgProps = {
    url: string;
    // 默认100%
    width?: number | string;
    /**
     * 默认100%
     * 没传值情况，同width值
     */
    height?: number | string;
    // 颜色，默认: #333333
    color?: string;
    className?: string;
    style?: React.CSSProperties;
    onLoad?: () => void;
    onError?: (error: Error) => void;
};
```

3、新建`src/styles/components/DynamicSvg.scss`样式文件
```scss
@use "~@/styles/main.scss" as *;

.svgContainer {
    width: px(45);
    height: px(45);
}
```

4、新建`src/components/DynamicSvg.tsx`组件
```tsx
import { useEffect, useRef } from 'react';

import styles from '@/styles/components/dynamicSvg.scss';

import type * as Types from '@/typing/components/DynamicSvg';

/**
 * 动态加载svg
 * 需确保svg文件保存在public/assets/svg文件夹中。
 *
 * 使用方式
    <DynamicSvg url="/icon.svg" color="blue" />;
 */
const DynamicSvg = ({
    url,
    width: w,
    height: h,
    color = '#333333',
    className = '',
    style = {},
    onLoad,
    onError,
}: Types.DynamicSvgProps) => {
    const svgRef = useRef<HTMLDivElement>(null);

    const height = !h ? (w || "100%") : h;
    const width = w || '100%';

    // 处理宽高属性，将数字转换为像素字符串
    const getDimension = (value: number | string) => {
        return typeof value === 'number' ? `${value}px` : value;
    };

    useEffect(() => {
        const fetchSvg = async () => {
            try {
                if (!url) return;

                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`加载 SVG 失败: ${response.statusText}`);
                }

                const svgText = await response.text();
                if (!svgRef.current) return;

                svgRef.current.innerHTML = svgText;

                // 修改所有可填充元素的颜色
                const fillableElements = svgRef.current.querySelectorAll(
                    'path, polygon, rect, circle, ellipse',
                );
                fillableElements.forEach((element) => {
                    element.setAttribute('fill', color);
                });

                // 修改所有描边元素的颜色
                const strokeElements =
                    svgRef.current.querySelectorAll('[stroke]');
                strokeElements.forEach((element) => {
                    element.setAttribute('stroke', color);
                });

                // 设置 SVG 元素的宽高
                const svgElement = svgRef.current.querySelector('svg');
                if (svgElement) {
                    svgElement.setAttribute('width', getDimension(width));
                    svgElement.setAttribute('height', getDimension(height));

                    // 如果没有 viewBox，则添加 viewBox 以保持比例
                    if (!svgElement.getAttribute('viewBox')) {
                        const widthValue = getDimension(width);
                        const heightValue = getDimension(height);
                        svgElement.setAttribute(
                            'viewBox',
                            `0 0 ${widthValue} ${heightValue}`,
                        );
                    }
                }

                onLoad?.();
            } catch (error) {
                console.error('加载 SVG 失败:', error);
                onError?.(error as Error);
            }
        };

        fetchSvg();
    }, [url, color, onLoad, onError]);

    return (
        <div
            ref={svgRef}
            className={[styles.svgContainer, className].join(' ')}
            style={{
                display: 'inline-block',
                verticalAlign: 'middle',
                ...style,
            }}
        />
    );
};

export default DynamicSvg;
```

5、使用组件
```tsx
import DynamicSvg from '@/components/DynamicSvg';

<DynamicSvg url="/assets/svg/language.svg" color="blue" width={120} />
```

## layout布局

1、配置路由
```js
// .umirc.ts
import { defineConfig } from '@umijs/max';
import { resolve } from 'path';

export default defineConfig({
    routes: [
        {
            path: '/',
            component: '@/layouts/index',
            routes: [
                { path: '/', component: '@/pages/Home' },
                { path: '/home', component: '@/pages/Home' },
                { path: '/access', component: '@/pages/Access' },
                { path: '/table', component: '@/pages/Table' },
                // 默认 404
                // { path: '/404', component: '@/pages/404' },
                // { path: '/*', component: '@/pages/404' },
            ],
        },
    ],
});

```

2、新建`src/layouts/index.tsx`类型声明文件
```tsx
import { Outlet } from 'umi';
import { ConfigProvider } from 'antd';

const Page = () => {
    const isRTL = false;
    return (
        <ConfigProvider
            direction={isRTL ? 'rtl' : 'ltr'}
        >
            <div dir={isRTL ? 'rtl' : 'ltr'}>
                {/* <Header /> */}
                <Outlet />
                {/* <Footer /> */}
                {/* <BackTop /> */}
                {/* <Affix /> */}
            </div>
        </ConfigProvider>
    );
};

export default Page;
```