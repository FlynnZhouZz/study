# HTML 拖放

```html
<div id="drag" draggable="true" style="width:120px;height:40px;background:#67c;color:#fff;">
  拖我
</div>

<div id="drop"
     style="width:200px;height:100px;border:2px dashed #aaa;margin-top:20px;">
  放在这里
</div>

<script>
  drag.addEventListener('dragstart', e => {
    e.dataTransfer.setData('text/plain', '从拖动处带来的数据');
  });

  drop.addEventListener('dragover', e => e.preventDefault());

  drop.addEventListener('drop', e => {
    drop.innerText = e.dataTransfer.getData('text/plain');
  });
</script>
```

## 讲解

### `<div id="drag" draggable="true">`

`draggable="true"` 是 拖放的唯一必要 HTML 属性。

### dragstart 事件

开始拖拽时触发，用于设置拖拽数据

- dragstart - 拖动开始时触发
- e.dataTransfer - 专门用于携带拖动时的数据
- setData(type, value) - 设置要传给 drop 的数据

### dragover 事件

在放置目标上移动时触发，必须调用preventDefault()才能允许放置

> 必须阻止默认行为，否则不能放下

### drop 事件

在放置目标上释放时触发，处理放置逻辑

- getData - 从 dataTransfer 取出拖动时设置的数据
- innerText - 显示到放置区域