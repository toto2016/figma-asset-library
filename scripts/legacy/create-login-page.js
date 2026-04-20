/**
 * Figma Login Page Builder - 完整版
 * 分 4 个 use_figma 调用执行，每次调用一个 step
 *
 * Step 1: 创建 wrapper + 左侧品牌面板
 * Step 2: 创建右侧表单面板 + 输入框
 * Step 3: 添加按钮、分隔线、第三方登录
 * Step 4: 截图验证
 */

// ============== STEP 1: Wrapper + Brand Panel ==============
// fileKey: 替换为你的文件 key

const page = figma.currentPage;
page.name = 'Login Page';

const wrapper = figma.createFrame();
wrapper.name = 'Login Page';
wrapper.resize(1440, 900);
wrapper.layoutMode = 'HORIZONTAL';
wrapper.primaryAxisAlignItems = 'CENTER';
wrapper.counterAxisAlignItems = 'CENTER';
wrapper.fills = [{ type: 'SOLID', color: { r: 0.96, g: 0.97, b: 0.98 } }];
wrapper.layoutSizingHorizontal = 'FIXED';
wrapper.layoutSizingVertical = 'FIXED';

await figma.loadFontAsync({ family: 'Inter', style: 'Bold' });
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

const leftPanel = figma.createFrame();
leftPanel.name = 'Brand Panel';
leftPanel.resize(640, 900);
leftPanel.layoutMode = 'VERTICAL';
leftPanel.primaryAxisAlignItems = 'CENTER';
leftPanel.counterAxisAlignItems = 'CENTER';
leftPanel.paddingLeft = 60;
leftPanel.paddingRight = 60;
leftPanel.paddingTop = 60;
leftPanel.paddingBottom = 60;
leftPanel.itemSpacing = 24;
leftPanel.fills = [{ type: 'SOLID', color: { r: 0.23, g: 0.35, b: 0.95 } }];
wrapper.appendChild(leftPanel);
leftPanel.layoutSizingVertical = 'FILL';

const iconCircle = figma.createEllipse();
iconCircle.name = 'Brand Icon';
iconCircle.resize(80, 80);
iconCircle.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 }, opacity: 0.2 }];
leftPanel.appendChild(iconCircle);

const brandTitle = figma.createText();
brandTitle.characters = 'Welcome Back';
brandTitle.fontSize = 40;
brandTitle.fontName = { family: 'Inter', style: 'Bold' };
brandTitle.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
brandTitle.textAlignHorizontal = 'CENTER';
leftPanel.appendChild(brandTitle);

const subtitle = figma.createText();
subtitle.characters = 'Sign in to continue to your dashboard.';
subtitle.fontSize = 16;
subtitle.fontName = { family: 'Inter', style: 'Regular' };
subtitle.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 }, opacity: 0.8 }];
subtitle.textAlignHorizontal = 'CENTER';
subtitle.lineHeight = { unit: 'PIXELS', value: 24 };
subtitle.resize(460, subtitle.height);
subtitle.textAutoResize = 'HEIGHT';
leftPanel.appendChild(subtitle);

return {
  success: true,
  wrapperId: wrapper.id,
  leftPanelId: leftPanel.id,
  nextStep: 'Use wrapperId to append right panel in Step 2',
};
