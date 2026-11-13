# 使用jszip 导出新闻

[jszip 官网](https://stuk.github.io/jszip)

## 思路

1. 服务器接口返回资源路径获取资源内容（资源内容引用了资源，需更改内容的引用路径为相对路径）；
2. 前端项目安装`jszip`依赖；
3. 使用依赖导出`zip`文件

## 后端接口
```php
/**
 * 获取反转资源url
 * @param string $initAssetsUrl
 * @param $assets
 * @return string
 */
private function getAssetsReversalUrl(string $initAssetsUrl, $assets) {
    $assetsDirName = 'index_files';
    $assetsUrl = $initAssetsUrl;
    $assetsNameArr = explode('/', $initAssetsUrl);
    $assetsName = end($assetsNameArr);
    if (!empty($assets[$assetsName])) {
        $assetsUrl = $assetsDirName . '/' . $assetsName;
    }
    return $assetsUrl;
}

/**
 * 导出
 * @param int $newsId
 * @return array|bool|string
 */
public function export(int $newsId)
{
    $detail = NewsModel::detail($newsId);
    if (empty($detail)) return $this -> renderError('新闻不存在');
    $detail = $detail -> toArray();

    $destinationFile = ($detail['suffix'] ?: $detail['id']) . '.zip';
    $assetsArr = json_decode($detail['assets'], true);
    $assets = [];
    $assetsMap = [];
    foreach ($assetsArr as $item) {
        $filePath = $item['file_path'];
        $filePathArr = explode('/', $filePath);
        $filePathName = end($filePathArr);
        $assets[$filePathName] = $item;

        $item['domain'] = Env::get('OSS_CUSTOM_DOMAIN');
        $item['file_path_name'] = $filePathName;
        $assetsMap[] = $item;
    }

    $fileContent = $detail['html_content'];
    $assetsDirName = 'index_files';

    $domain = request() -> domain();
    // 还原html，资源改为相对路径
    $fileContent = preg_replace_callback_array(
        [
            '/<link([^>]*)href="([^"]+)"([^>]*)>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<link{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>";
            },
            '/<script([^>]*)src="([^"]+)"([^>]*)>(.*?)<\/script>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<script{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>{$matches[4]}</script>";
            },
            '/<img([^>]*)[^\-]src="([^"]+)"([^>]*)>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<img{$matches[1]} src=\"{$assetsUrl}\"{$matches[3]}>";
            },
            '/<video[^>]*src="([^"]+)"([^>]*)>(.*?)<\/video>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<video{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>{$matches[4]}</video>";
            },
            '/<audio[^>]*src="([^"]+)"([^>]*)>(.*?)<\/audio>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<audio{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>{$matches[4]}</audio>";
            },
            '/<source[^>]*src="([^"]+)"([^>]*)>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<source{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>";
            },
            '/<track[^>]*src="([^"]+)"([^>]*)>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<track{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>";
            },
            '/<embed([^>]*)src="([^"]+)"([^>]*)>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<embed{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>";
            },
            '/<iframe([^>]*)src="([^"]+)"([^>]*)>(.*?)<\/iframe>/si' => function ($matches) use ($assets) {
                // 这里可以添加逻辑来处理 $matches[2]（原始值）
                $assetsUrl = $this -> getAssetsReversalUrl($matches[2], $assets);
                return "<iframe{$matches[1]}href=\"{$assetsUrl}\"{$matches[3]}>{$matches[4]}</iframe>";
            },
        ],
        $fileContent
    );

    $detail['assets'] = $assetsMap;
    $detail['assets_dir_name'] = $assetsDirName;
    $detail['cur_domain'] =  $domain;
    $detail['html_content'] = $fileContent;
    $detail['file_name'] = $destinationFile;
    return $this->renderSuccess($detail, '查询成功');
}
```

## 前端实现

1. 安装`jszip`依赖
```shell
yarn add jszip
# or
npm install jszip
```

2. 使用`jszip`导出资源
```js
handleExport(item) {
    NewsApi.exportNews({ newsId: item.news_id })
        .then(result => {
            const { data } = result;
            // 创建 zip
            const zip = new JSZip();
            // 添加html
            zip.file('index.html', data?.html_content);

            const folderObj = zip.folder(data?.assets_dir_name || 'index_files');
            const assets = data?.assets;
            const promises = [];
            assets?.forEach((item, index) => {
                // 更改请求前缀，如果是本地开发，使用代理字符；如果是oss对象存储，使用对应oss域名
                const url = (item?.storage === 'local' ? `/uplod/uploads/` : item?.domain) + item?.file_path;
                if (item?.file_path_name) {
                    const promise = new Promise((resolve, reject) => {
                        getAssetsBlob(url).then(res => {
                            resolve(res.data)
                        }).catch((err) => {
                            reject(err);
                        })
                    }).then(blob => {
                        if (blob) folderObj.file(item.file_path_name, blob, { binary: true });
                    });
                    promises.push(promise);
                }
            });
            // 使用Promise.all 等待前面请求资源全部完成，再导出zip文件，否则资源文件还没请求完全就执行了导出zip的操作
            Promise.all(promises).then(() => {
                // 生成 Blob 和导出 zip 文件
                zip.generateAsync({ type: 'blob' }).then(blob => {
                    // 创建一个链接
                    const link = document.createElement('a');
                    // 将 blob 作为链接的内容
                    link.href = URL.createObjectURL(blob);
                    // 设置链接的下载名称
                    link.download = data?.file_name || 'download.zip';
                    // 点击链接
                    link.click();
                }).catch(() => {
                    this.$message.success('导出失败，请稍后重试', 1.5)
                });
            });
        })
}
```