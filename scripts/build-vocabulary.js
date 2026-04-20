#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  loadCategoryFile, listCategoryValues, filterDesignOps, groupByFileAndName
} = require('./vocab/load-data');
const {
  TYPE_LABELS, MODULE_LABELS,
  renderTypeOrModulePage, renderIndex, renderIconsPage, renderDataJson
} = require('./vocab/render-md');

const OUT_DIR = 'docs/vocabulary';
const DATA_JSON = 'catalog/vocabulary-data.json';
const ICON_CHUNK = 30;

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function writeMd(rel, content) {
  const full = path.join(OUT_DIR, rel);
  ensureDir(path.dirname(full));
  fs.writeFileSync(full, content);
  return rel;
}

function buildKind(kind, labels, dataAccumulator) {
  const dimension = kind === 'type' ? 'by-type' : 'by-module';
  const values = listCategoryValues(dimension);
  const entries = [];
  const written = [];
  for (const value of values) {
    if (!labels[value]) continue;
    if (kind === 'type' && value === 'icon') continue;
    const items = filterDesignOps(loadCategoryFile(dimension, value));
    if (items.length === 0) continue;
    const groups = groupByFileAndName(items);
    const total = items.length;
    const byFile = {};
    for (const g of groups) {
      if (!byFile[g.file]) byFile[g.file] = [];
      byFile[g.file].push(g);
    }
    const result = renderTypeOrModulePage({
      kind, value, label: labels[value], groups, total, byFile
    });
    written.push(writeMd(path.join(dimension, `${value}.md`), result.main));
    for (const sub of result.sub) {
      written.push(writeMd(
        path.join(dimension, value, `${sub.fileSlug}.md`), sub.content
      ));
    }
    entries.push({ value, groupCount: groups.length, variantCount: total });
    dataAccumulator[dimension][value] = groups;
  }
  entries.sort((a, b) => b.variantCount - a.variantCount);
  written.push(writeMd(path.join(dimension, 'README.md'), renderIndex({ kind, entries })));
  return { written, entries };
}

function buildIcons(dataAccumulator) {
  const items = filterDesignOps(loadCategoryFile('by-type', 'icon'));
  const grouped = new Map();
  for (const it of items) {
    const k = `${it.file}\u0000${it.name}`;
    if (!grouped.has(k)) grouped.set(k, { name: it.name, file: it.file, keys: [] });
    grouped.get(k).keys.push(it.key);
  }
  const aggregated = [...grouped.values()].sort((a, b) => a.name.localeCompare(b.name));
  const view = aggregated.map(g => ({
    name: g.name, file: g.file, key: g.keys[0], variantCount: g.keys.length
  }));
  const result = renderIconsPage(view, ICON_CHUNK);
  const written = [writeMd('icons/README.md', result.main)];
  for (const sub of result.sub) {
    written.push(writeMd(
      path.join('icons', 'by-letter', `${sub.letterSlug}.md`), sub.content
    ));
  }
  dataAccumulator.icons = aggregated;
  return { written, totalRecords: items.length, uniqueIcons: aggregated.length, mode: result.mode };
}

function main() {
  ensureDir(OUT_DIR);
  const dataAccumulator = { 'by-type': {}, 'by-module': {}, icons: [] };
  const typeBuild = buildKind('type', TYPE_LABELS, dataAccumulator);
  const moduleBuild = buildKind('module', MODULE_LABELS, dataAccumulator);
  const iconBuild = buildIcons(dataAccumulator);

  ensureDir(path.dirname(DATA_JSON));
  fs.writeFileSync(DATA_JSON, renderDataJson({
    generatedAt: new Date().toISOString(),
    source: 'catalog/classified, system=DesignOps',
    ...dataAccumulator
  }));

  const summary = {
    generatedAt: new Date().toISOString(),
    byType: { files: typeBuild.written.length, entries: typeBuild.entries },
    byModule: { files: moduleBuild.written.length, entries: moduleBuild.entries },
    icons: { totalRecords: iconBuild.totalRecords, uniqueIcons: iconBuild.uniqueIcons, files: iconBuild.written.length, mode: iconBuild.mode }
  };
  fs.writeFileSync('docs/vocabulary/.build-summary.json', JSON.stringify(summary, null, 2));

  console.log(`✓ by-type: ${typeBuild.written.length} 个 markdown`);
  console.log(`✓ by-module: ${moduleBuild.written.length} 个 markdown`);
  console.log(`✓ icons: ${iconBuild.uniqueIcons} 唯一图标 / ${iconBuild.totalRecords} 变体 (${iconBuild.written.length} 文件)`);
  console.log(`✓ 完整数据: ${DATA_JSON}`);
}

main();
