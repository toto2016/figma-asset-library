/**
 * Figma 轻量元数据提取脚本
 * 用于快速筛选：仅提取页面列表和组件数量概览
 * 适合第一阶段快速扫描，判断文件是否值得深度提取
 *
 * 注意：此脚本也可以通过 get_metadata 替代
 * 但 get_metadata 返回 XML 格式，此脚本返回结构化 JSON
 */

const result = {
  pages: [],
  hasComponents: false,
  hasVariables: false,
  hasStyles: false,
  summary: {}
};

let totalComponents = 0;
let totalComponentSets = 0;
let totalFrames = 0;

for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);

  let compCount = 0;
  let compSetCount = 0;
  page.findAll(n => {
    if (n.type === 'COMPONENT') compCount++;
    if (n.type === 'COMPONENT_SET') compSetCount++;
    return false;
  });

  totalComponents += compCount;
  totalComponentSets += compSetCount;
  totalFrames += page.children.length;

  result.pages.push({
    name: page.name,
    id: page.id,
    childCount: page.children.length,
    componentCount: compCount,
    componentSetCount: compSetCount,
    topLevelNames: page.children.slice(0, 10).map(c => c.name)
  });
}

const collections = await figma.variables.getLocalVariableCollectionsAsync();
const textStyles = await figma.getLocalTextStylesAsync();
const effectStyles = await figma.getLocalEffectStylesAsync();

result.hasComponents = totalComponents > 0 || totalComponentSets > 0;
result.hasVariables = collections.length > 0;
result.hasStyles = textStyles.length > 0 || effectStyles.length > 0;

result.summary = {
  pageCount: result.pages.length,
  totalComponents: totalComponents,
  totalComponentSets: totalComponentSets,
  totalFrames: totalFrames,
  variableCollections: collections.length,
  textStyles: textStyles.length,
  effectStyles: effectStyles.length,
  worthDeepExtract: totalComponents > 0 || totalComponentSets > 0
    || collections.length > 0 || textStyles.length > 0
};

return result;
