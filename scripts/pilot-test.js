/**
 * Pilot 权限测试脚本
 * 用于验证 View 权限是否能通过 use_figma 读取组织文件
 *
 * 使用方式：
 * 1. 先用 whoami 确认升级后的席位类型
 * 2. 用 get_metadata 测试文件读取（nodeId: "0:1"）
 * 3. 用此脚本测试 use_figma 执行能力
 *
 * 此脚本是纯只读操作，不会修改文件内容
 */

const pages = figma.root.children.map(p => ({
  name: p.name,
  id: p.id,
  childCount: p.children.length
}));

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const textStyles = await figma.getLocalTextStylesAsync();

return {
  test: 'pilot-permission-check',
  success: true,
  fileInfo: {
    pageCount: pages.length,
    pages: pages,
    variableCollections: collections.length,
    textStyles: textStyles.length
  },
  message: 'View 权限下 use_figma 只读操作正常'
};
