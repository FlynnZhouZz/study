# node16版本之后报兼容问题

问题
```shell
error glob@10.4.3: The engine "node" is incompatible with this module. Expected version ">=18". Got "16.20.2"
error Found incompatible module.
```

按照依赖的时候添加参数，忽略引擎版本检查
```shell
yarn install --ignore-engines

# or
yarn add xxx --ignore-engines
```
