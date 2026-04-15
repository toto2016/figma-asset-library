/**
 * Figma AI 自动出图 - 工作流模板集合
 * 每个模板可直接用于 use_figma 的 code 参数
 */

// ============================================================
// 模板 1: 搜索设计系统资产 (search_design_system)
// ============================================================
// 调用方式: CallMcpTool('plugin-figma-figma', 'search_design_system', {
//   query: 'button',
//   fileKey: 'YOUR_FILE_KEY',
//   includeComponents: true,
//   includeVariables: true,
//   includeStyles: true,
// })

// ============================================================
// 模板 2: 从现有页面提取组件映射表 (use_figma)
// ============================================================
const TEMPLATE_EXTRACT_COMPONENTS = `
const frame = figma.currentPage.findOne(n => n.name === 'TARGET_FRAME_NAME');
if (!frame) return { error: 'Frame not found' };

const uniqueSets = new Map();
frame.findAll(n => n.type === 'INSTANCE').forEach(inst => {
  const mc = inst.mainComponent;
  const cs = mc?.parent?.type === 'COMPONENT_SET' ? mc.parent : null;
  const key = cs ? cs.key : mc?.key;
  const name = cs ? cs.name : mc?.name;
  if (key && !uniqueSets.has(key)) {
    uniqueSets.set(key, { name, key, isSet: !!cs, sampleVariant: mc.name });
  }
});
return [...uniqueSets.values()];
`;

// ============================================================
// 模板 3: 提取已绑定的变量 (use_figma)
// ============================================================
const TEMPLATE_EXTRACT_VARIABLES = `
const frame = figma.currentPage.findOne(n => n.name === 'TARGET_FRAME_NAME');
if (!frame) return { error: 'Frame not found' };

const varMap = new Map();
const allNodes = frame.findAll(() => true);
for (const node of allNodes) {
  const bv = node.boundVariables;
  if (!bv) continue;
  for (const [prop, binding] of Object.entries(bv)) {
    const bindings = Array.isArray(binding) ? binding : [binding];
    for (const b of bindings) {
      if (b?.id && !varMap.has(b.id)) {
        const v = await figma.variables.getVariableByIdAsync(b.id);
        if (v) varMap.set(b.id, {
          name: v.name, id: v.id, key: v.key,
          type: v.resolvedType, remote: v.remote,
        });
      }
    }
  }
}
return [...varMap.values()];
`;

// ============================================================
// 模板 4: 创建自动布局容器 (use_figma)
// ============================================================
const TEMPLATE_CREATE_AUTOLAYOUT = `
let maxX = 0;
for (const child of figma.currentPage.children) {
  maxX = Math.max(maxX, child.x + child.width);
}

const frame = figma.createFrame();
frame.name = 'FRAME_NAME';
frame.layoutMode = 'VERTICAL';  // or 'HORIZONTAL'
frame.primaryAxisAlignItems = 'CENTER';
frame.counterAxisAlignItems = 'CENTER';
frame.resize(1440, 100);
frame.layoutSizingHorizontal = 'FIXED';
frame.layoutSizingVertical = 'HUG';
frame.x = maxX + 200;
frame.y = 0;
frame.itemSpacing = 0;
frame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];

return { success: true, frameId: frame.id };
`;

// ============================================================
// 模板 5: 导入设计系统组件并创建实例 (use_figma)
// ============================================================
const TEMPLATE_IMPORT_COMPONENT = `
const componentSet = await figma.importComponentSetByKeyAsync('COMPONENT_SET_KEY');
const variant = componentSet.children.find(c =>
  c.type === 'COMPONENT' && c.name.includes('VARIANT_MATCH')
) || componentSet.defaultVariant;

const parent = await figma.getNodeByIdAsync('PARENT_NODE_ID');
const instance = variant.createInstance();
parent.appendChild(instance);
instance.layoutSizingHorizontal = 'FILL';

return {
  success: true,
  instanceId: instance.id,
  componentName: variant.name,
};
`;

// ============================================================
// 模板 6: 创建文本节点 (use_figma)
// ============================================================
const TEMPLATE_CREATE_TEXT = `
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

const parent = await figma.getNodeByIdAsync('PARENT_NODE_ID');
const text = figma.createText();
text.characters = 'YOUR_TEXT_CONTENT';
text.fontSize = 16;
text.fontName = { family: 'Inter', style: 'Regular' };
text.fills = [{ type: 'SOLID', color: { r: 0.07, g: 0.09, b: 0.15 } }];
text.lineHeight = { unit: 'PIXELS', value: 24 };
parent.appendChild(text);

return { success: true, textId: text.id };
`;

// ============================================================
// 模板 7: 创建输入框组件 (use_figma)
// ============================================================
const TEMPLATE_CREATE_INPUT = `
await figma.loadFontAsync({ family: 'Inter', style: 'Medium' });
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

const parent = await figma.getNodeByIdAsync('PARENT_NODE_ID');

const fieldGroup = figma.createFrame();
fieldGroup.name = 'FIELD_NAME';
fieldGroup.layoutMode = 'VERTICAL';
fieldGroup.itemSpacing = 6;
fieldGroup.fills = [];
parent.appendChild(fieldGroup);
fieldGroup.layoutSizingHorizontal = 'FILL';
fieldGroup.layoutSizingVertical = 'HUG';

const label = figma.createText();
label.characters = 'LABEL_TEXT';
label.fontSize = 14;
label.fontName = { family: 'Inter', style: 'Medium' };
label.fills = [{ type: 'SOLID', color: { r: 0.13, g: 0.16, b: 0.22 } }];
fieldGroup.appendChild(label);

const input = figma.createFrame();
input.name = 'Input';
input.layoutMode = 'HORIZONTAL';
input.counterAxisAlignItems = 'CENTER';
input.resize(400, 48);
input.paddingLeft = 16;
input.paddingRight = 16;
input.cornerRadius = 8;
input.fills = [{ type: 'SOLID', color: { r: 0.98, g: 0.98, b: 0.99 } }];
input.strokes = [{ type: 'SOLID', color: { r: 0.85, g: 0.87, b: 0.9 } }];
input.strokeWeight = 1;
fieldGroup.appendChild(input);
input.layoutSizingHorizontal = 'FILL';
input.layoutSizingVertical = 'FIXED';

const placeholder = figma.createText();
placeholder.characters = 'PLACEHOLDER_TEXT';
placeholder.fontSize = 14;
placeholder.fontName = { family: 'Inter', style: 'Regular' };
placeholder.fills = [{ type: 'SOLID', color: { r: 0.62, g: 0.65, b: 0.7 } }];
input.appendChild(placeholder);

return { success: true, fieldId: fieldGroup.id, inputId: input.id };
`;

// ============================================================
// 模板 8: 创建按钮 (use_figma)
// ============================================================
const TEMPLATE_CREATE_BUTTON = `
await figma.loadFontAsync({ family: 'Inter', style: 'Semi Bold' });

const parent = await figma.getNodeByIdAsync('PARENT_NODE_ID');

const btn = figma.createFrame();
btn.name = 'BUTTON_NAME';
btn.layoutMode = 'HORIZONTAL';
btn.primaryAxisAlignItems = 'CENTER';
btn.counterAxisAlignItems = 'CENTER';
btn.resize(400, 48);
btn.cornerRadius = 8;
btn.fills = [{ type: 'SOLID', color: { r: 0.23, g: 0.35, b: 0.95 } }];
parent.appendChild(btn);
btn.layoutSizingHorizontal = 'FILL';
btn.layoutSizingVertical = 'FIXED';

const btnText = figma.createText();
btnText.characters = 'BUTTON_TEXT';
btnText.fontSize = 16;
btnText.fontName = { family: 'Inter', style: 'Semi Bold' };
btnText.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
btn.appendChild(btnText);

return { success: true, buttonId: btn.id };
`;
