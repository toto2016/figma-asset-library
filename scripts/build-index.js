#!/usr/bin/env node
// 构建全量统一索引: catalog/assets.json
// 用法: node scripts/build-index.js

const fs = require('fs');
const path = require('path');

const SCAN_DIR = 'reports/extractions/scans';
const DEEP_DIR = 'reports/extractions/deep';
const OUTPUT = 'catalog/assets.json';

function loadScans() {
  const files = fs.readdirSync(SCAN_DIR).filter(f => f.endsWith('-scan.json'));
  const allFiles = [];

  for (const scanFile of files) {
    const data = JSON.parse(fs.readFileSync(path.join(SCAN_DIR, scanFile), 'utf8'));
    const project = data.project || data.projectName || 'unknown';

    for (const file of data.files) {
      const deepPath = path.join(DEEP_DIR, `${file.fileKey}.json`);
      const hasDeep = fs.existsSync(deepPath);

      allFiles.push({
        fileKey: file.fileKey,
        fileName: file.fileName,
        project,
        projectName: file.projectName || data.projectName,
        lastModified: file.lastModified,
        pageCount: file.summary.pageCount,
        publishedComponents: file.summary.publishedComponents,
        publishedStyles: file.summary.publishedStyles,
        isHighValue: file.summary.worthDeepExtract,
        hasDeepExtraction: hasDeep,
        pages: file.pages.map(p => ({ name: p.name, id: p.id, childCount: p.childCount })),
        componentGroups: Object.keys(file.componentGroups || {}).map(g => ({
          group: g,
          count: (file.componentGroups[g] || []).length
        })),
        styleGroups: Object.keys(file.styleGroups || {}).map(g => ({
          type: g,
          count: (file.styleGroups[g] || []).length
        }))
      });
    }
  }

  return allFiles;
}

function buildSummary(allFiles) {
  const byProject = {};
  for (const f of allFiles) {
    if (!byProject[f.project]) {
      byProject[f.project] = { projectName: f.projectName, files: 0, components: 0, styles: 0, highValue: 0 };
    }
    byProject[f.project].files++;
    byProject[f.project].components += f.publishedComponents;
    byProject[f.project].styles += f.publishedStyles;
    if (f.isHighValue) byProject[f.project].highValue++;
  }

  return {
    totalFiles: allFiles.length,
    totalComponents: allFiles.reduce((s, f) => s + f.publishedComponents, 0),
    totalStyles: allFiles.reduce((s, f) => s + f.publishedStyles, 0),
    highValueFiles: allFiles.filter(f => f.isHighValue).length,
    deepExtracted: allFiles.filter(f => f.hasDeepExtraction).length,
    byProject
  };
}

function buildComponentIndex(allFiles) {
  const components = [];
  for (const f of allFiles) {
    for (const g of f.componentGroups) {
      if (g.count > 0) {
        components.push({
          fileKey: f.fileKey,
          fileName: f.fileName,
          project: f.project,
          group: g.group,
          count: g.count
        });
      }
    }
  }
  return components.sort((a, b) => b.count - a.count);
}

// 执行
const allFiles = loadScans();
const summary = buildSummary(allFiles);
const componentIndex = buildComponentIndex(allFiles);

const index = {
  generatedAt: new Date().toISOString(),
  summary,
  componentIndex: componentIndex.slice(0, 100),
  highValueFiles: allFiles
    .filter(f => f.isHighValue)
    .sort((a, b) => (b.publishedComponents + b.publishedStyles) - (a.publishedComponents + a.publishedStyles)),
  allFiles: allFiles.sort((a, b) => (b.publishedComponents + b.publishedStyles) - (a.publishedComponents + a.publishedStyles))
};

fs.mkdirSync('catalog', { recursive: true });
fs.writeFileSync(OUTPUT, JSON.stringify(index, null, 2));

console.log(`✅ 索引已生成: ${OUTPUT}`);
console.log(`   文件: ${summary.totalFiles}`);
console.log(`   组件: ${summary.totalComponents}`);
console.log(`   样式: ${summary.totalStyles}`);
console.log(`   高价值: ${summary.highValueFiles}`);
console.log(`   深度提取: ${summary.deepExtracted}`);
