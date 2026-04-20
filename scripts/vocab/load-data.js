const fs = require('fs');
const path = require('path');

const CATALOG_DIR = 'catalog/classified';

function loadCategoryFile(dimension, value) {
  const file = path.join(CATALOG_DIR, dimension, `${value}.json`);
  if (!fs.existsSync(file)) return [];
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  return data.items || [];
}

function listCategoryValues(dimension) {
  const dir = path.join(CATALOG_DIR, dimension);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.json'))
    .map(f => f.replace(/\.json$/, ''))
    .sort();
}

function filterDesignOps(items) {
  return items.filter(it => it.system === 'DesignOps');
}

function groupByFileAndName(items) {
  const groups = new Map();
  for (const it of items) {
    const key = `${it.file}\u0000${it.name}`;
    if (!groups.has(key)) {
      groups.set(key, {
        file: it.file,
        name: it.name,
        platform: it.platform,
        module: it.module,
        variants: []
      });
    }
    groups.get(key).variants.push({ key: it.key });
  }
  return [...groups.values()].sort((a, b) => {
    if (a.file !== b.file) return a.file.localeCompare(b.file);
    return a.name.localeCompare(b.name);
  });
}

module.exports = {
  loadCategoryFile,
  listCategoryValues,
  filterDesignOps,
  groupByFileAndName,
  CATALOG_DIR
};
