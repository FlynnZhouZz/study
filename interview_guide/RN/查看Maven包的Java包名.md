# 查看Maven包的Java包名

[Maven central repository](https://central.sonatype.com/)
[maven包](https://repo1.maven.org/maven2/)，后面可直接拼接；引入地址

下载arr包

手动解压 .aar 文件
```bash
unzip uverify-2.6.5.aar -d uverify_aar
```

然后你会看到结构如下：
```tree
uverify_aar/
├── AndroidManifest.xml
├── classes.jar   ← Java 代码都在这里
├── res/          ← 资源文件
├── R.txt
└── other files...
```

查看 classes.jar 中的包名
```bash
cd uverify_aar
jar xf classes.jar
```

然后查看里面的文件结构，例如：
```
com/umeng/verify/UVerifyHelper.class
com/umeng/verify/utils/SomeUtil.class
```
这些路径就对应 Java 的包名：
```java
package com.umeng.verify;
package com.umeng.verify.utils;
```