/**
 * 扫描结果处理器
 * 将 use_figma 返回的原始数据转化为标准索引格式
 *
 * 用法（Node.js）:
 *   node scripts/process-scan-result.js <fileKey> <projectName> <scanType>
 *
 * 也可作为模块导入：
 *   const { processLiteScan, processDeepScan } = require('./process-scan-result');
 */

function processLiteScan(rawResult, fileKey, fileName, projectName, priority) {
  return {
    fileKey,
    fileName,
    projectName,
    priority,
    extractedAt: new Date().toISOString(),
    scanType: 'lite',
    summary: rawResult.summary,
    pages: rawResult.pages,
    components: [],
    variables: [],
    styles: { text: [], effect: [] }
  };
}

function processDeepScan(rawResult, fileKey, fileName, projectName, priority) {
  const components = [
    ...rawResult.components.map(c => ({ ...c, type: 'COMPONENT', tags: {} })),
    ...rawResult.componentSets.map(c => ({ ...c, type: 'COMPONENT_SET', tags: {} }))
  ];

  const variables = [];
  for (const col of rawResult.localVariableCollections || []) {
    for (const v of col.variables || []) {
      variables.push({
        collectionName: col.name,
        name: v.name,
        id: v.id,
        type: v.type,
        scopes: v.scopes || []
      });
    }
  }

  return {
    fileKey,
    fileName,
    projectName,
    priority,
    extractedAt: rawResult.extractedAt || new Date().toISOString(),
    scanType: 'deep',
    summary: rawResult.summary,
    pages: rawResult.pages,
    components,
    variables,
    styles: {
      text: rawResult.textStyles || [],
      effect: rawResult.effectStyles || []
    }
  };
}

function mergeIntoAssetIndex(assetIndex, fileIndex) {
  const existing = assetIndex.findIndex(f => f.fileKey === fileIndex.fileKey);
  if (existing >= 0) {
    assetIndex[existing] = fileIndex;
  } else {
    assetIndex.push(fileIndex);
  }
  return assetIndex;
}

function generateSummaryReport(assetIndex) {
  const byProject = {};
  let totalComponents = 0;
  let totalVariables = 0;
  let totalFiles = assetIndex.length;

  for (const file of assetIndex) {
    const proj = file.projectName || 'unknown';
    if (!byProject[proj]) {
      byProject[proj] = { files: 0, components: 0, variables: 0 };
    }
    byProject[proj].files++;
    byProject[proj].components += file.components.length;
    byProject[proj].variables += file.variables.length;
    totalComponents += file.components.length;
    totalVariables += file.variables.length;
  }

  return {
    generatedAt: new Date().toISOString(),
    totalFiles,
    totalComponents,
    totalVariables,
    byProject
  };
}

if (typeof module !== 'undefined') {
  module.exports = {
    processLiteScan,
    processDeepScan,
    mergeIntoAssetIndex,
    generateSummaryReport
  };
}
