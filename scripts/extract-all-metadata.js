/**
 * Figma 全量元数据提取脚本（深度版）
 * 用于 use_figma 工具的 code 参数
 * 一次调用提取一个文件的所有设计资产元数据
 *
 * 提取内容：页面、组件、变量、样式、顶层 frame
 * 返回：结构化 JSON
 */

const result = {
  extractedAt: new Date().toISOString(),
  pages: [],
  components: [],
  componentSets: [],
  localVariableCollections: [],
  textStyles: [],
  effectStyles: [],
  topLevelFrames: [],
  summary: {}
};

for (const page of figma.root.children) {
  await figma.setCurrentPageAsync(page);

  const pageData = {
    name: page.name,
    id: page.id,
    childCount: page.children.length,
    topLevelNodes: []
  };

  for (const child of page.children) {
    const nodeInfo = {
      name: child.name,
      id: child.id,
      type: child.type,
      width: Math.round(child.width),
      height: Math.round(child.height)
    };

    if (child.type === 'COMPONENT') {
      result.components.push({
        name: child.name,
        id: child.id,
        key: child.key,
        page: page.name,
        width: Math.round(child.width),
        height: Math.round(child.height),
        description: child.description || ''
      });
    }

    if (child.type === 'COMPONENT_SET') {
      const variants = child.children
        .filter(c => c.type === 'COMPONENT')
        .map(c => ({ name: c.name, id: c.id, key: c.key }));
      result.componentSets.push({
        name: child.name,
        id: child.id,
        key: child.key,
        page: page.name,
        variantCount: variants.length,
        variants: variants.slice(0, 20),
        description: child.description || ''
      });
    }

    if (child.type === 'FRAME' || child.type === 'SECTION') {
      const nestedComps = [];
      child.findAll(n => {
        if (n.type === 'COMPONENT' || n.type === 'COMPONENT_SET') {
          nestedComps.push({
            name: n.name,
            id: n.id,
            type: n.type,
            key: n.key
          });
        }
        return false;
      });

      nodeInfo.nestedComponentCount = nestedComps.length;
      if (nestedComps.length > 0) {
        nodeInfo.nestedComponents = nestedComps.slice(0, 30);
      }

      result.components.push(
        ...nestedComps
          .filter(c => c.type === 'COMPONENT')
          .map(c => ({ ...c, page: page.name }))
      );
      result.componentSets.push(
        ...nestedComps
          .filter(c => c.type === 'COMPONENT_SET')
          .map(c => ({ ...c, page: page.name }))
      );
    }

    pageData.topLevelNodes.push(nodeInfo);
  }

  result.pages.push(pageData);
}

const collections = await figma.variables.getLocalVariableCollectionsAsync();
for (const col of collections) {
  const vars = [];
  for (const varId of col.variableIds.slice(0, 50)) {
    const v = await figma.variables.getVariableByIdAsync(varId);
    if (v) {
      vars.push({
        name: v.name,
        id: v.id,
        type: v.resolvedType,
        scopes: v.scopes
      });
    }
  }
  result.localVariableCollections.push({
    name: col.name,
    id: col.id,
    modes: col.modes.map(m => m.name),
    variableCount: col.variableIds.length,
    variables: vars
  });
}

const textStylesList = await figma.getLocalTextStylesAsync();
result.textStyles = textStylesList.slice(0, 50).map(s => ({
  name: s.name,
  id: s.id,
  key: s.key,
  fontSize: s.fontSize,
  fontName: s.fontName
}));

const effectStylesList = await figma.getLocalEffectStylesAsync();
result.effectStyles = effectStylesList.slice(0, 30).map(s => ({
  name: s.name,
  id: s.id,
  key: s.key
}));

const uniqueComps = new Map();
for (const c of result.components) {
  if (!uniqueComps.has(c.id)) uniqueComps.set(c.id, c);
}
result.components = [...uniqueComps.values()];

const uniqueSets = new Map();
for (const c of result.componentSets) {
  if (!uniqueSets.has(c.id)) uniqueSets.set(c.id, c);
}
result.componentSets = [...uniqueSets.values()];

result.summary = {
  pageCount: result.pages.length,
  componentCount: result.components.length,
  componentSetCount: result.componentSets.length,
  variableCollectionCount: result.localVariableCollections.length,
  totalVariableCount: result.localVariableCollections
    .reduce((sum, c) => sum + c.variableCount, 0),
  textStyleCount: result.textStyles.length,
  effectStyleCount: result.effectStyles.length
};

return result;
