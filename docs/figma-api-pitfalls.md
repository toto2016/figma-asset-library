# Figma Plugin API 踩坑记录

在 `use_figma` 中编写脚本时的常见错误和正确写法。

---

## 颜色值范围

```javascript
// 错误：使用 0-255
fills = [{ type: 'SOLID', color: { r: 59, g: 89, b: 245 } }]

// 正确：使用 0-1
fills = [{ type: 'SOLID', color: { r: 0.23, g: 0.35, b: 0.95 } }]
```

颜色对象只有 `{r, g, b}`，不含 `a`。透明度在 paint 层级设置：
```javascript
{ type: 'SOLID', color: { r: 1, g: 1, b: 1 }, opacity: 0.5 }
```

---

## Auto Layout 尺寸模式

```javascript
// 错误：appendChild 之前设置 FILL
child.layoutSizingHorizontal = 'FILL';
parent.appendChild(child);

// 正确：appendChild 之后设置 FILL
parent.appendChild(child);
child.layoutSizingHorizontal = 'FILL';
```

---

## counterAxisAlignItems 取值

```javascript
// 错误：使用 STRETCH
frame.counterAxisAlignItems = 'STRETCH';

// 正确：只支持这四个值
frame.counterAxisAlignItems = 'MIN';     // 顶部/左侧对齐
frame.counterAxisAlignItems = 'MAX';     // 底部/右侧对齐
frame.counterAxisAlignItems = 'CENTER';  // 居中
frame.counterAxisAlignItems = 'BASELINE'; // 基线对齐
```

---

## 字体加载

```javascript
// 错误：不加载字体直接操作文本
text.characters = 'Hello';

// 正确：先加载字体
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
text.characters = 'Hello';

// 注意：Inter 的 Semi Bold 中间有空格
await figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' });  // 正确
await figma.loadFontAsync({ family: 'Inter', style: 'SemiBold' });   // 错误
```

字体不确定时，先查询可用字体：
```javascript
const fonts = await figma.listAvailableFontsAsync();
```

---

## 页面切换

```javascript
// 错误：同步赋值
figma.currentPage = targetPage;

// 正确：异步方法
await figma.setCurrentPageAsync(targetPage);
```

每次 `use_figma` 调用，页面上下文都会重置到第一页。

---

## 输出数据

```javascript
// 错误：使用 console.log（不会返回任何内容）
console.log(result);

// 错误：调用 closePlugin
figma.closePlugin();

// 正确：使用 return
return { success: true, createdNodeIds: [...] };
```

---

## 通知

```javascript
// 错误：figma.notify 会抛异常
figma.notify('Done!');

// 正确：通过 return 返回状态
return { message: 'Done!' };
```

---

## Fills 和 Strokes 修改

```javascript
// 错误：直接修改数组（只读）
node.fills[0].color = { r: 1, g: 0, b: 0 };

// 正确：克隆、修改、重新赋值
const fills = [...node.fills];
fills[0] = { ...fills[0], color: { r: 1, g: 0, b: 0 } };
node.fills = fills;
```

---

## 异步操作

```javascript
// 错误：忘记 await（静默失败）
figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

// 正确：所有异步操作都要 await
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
```

---

## 节点定位

```javascript
// 错误：新节点默认在 (0,0)，可能和已有内容重叠
const frame = figma.createFrame();

// 正确：扫描现有内容，放在右侧空白处
let maxX = 0;
for (const child of figma.currentPage.children) {
  maxX = Math.max(maxX, child.x + child.width);
}
frame.x = maxX + 200;
```

---

## resize 与 sizing 模式

```javascript
// 错误：先设 sizing 再 resize（resize 会重置为 FIXED）
frame.layoutSizingHorizontal = 'HUG';
frame.resize(400, 100);  // 重置为 FIXED

// 正确：先 resize 再设 sizing
frame.resize(400, 100);
frame.layoutSizingHorizontal = 'HUG';
```

---

## lineHeight 和 letterSpacing 格式

```javascript
// 错误：裸数字
text.lineHeight = 24;

// 正确：对象格式
text.lineHeight = { unit: 'PIXELS', value: 24 };
text.letterSpacing = { unit: 'PERCENT', value: 0 };
```

---

## 返回节点 ID

每次 `use_figma` 调用都必须返回创建/修改的节点 ID：

```javascript
const createdNodeIds = [];
const frame = figma.createFrame();
createdNodeIds.push(frame.id);
// ...更多操作...
return { success: true, createdNodeIds };
```

后续调用通过 ID 引用这些节点：
```javascript
const frame = await figma.getNodeByIdAsync('2:2');
```
