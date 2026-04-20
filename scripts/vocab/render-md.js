const TYPE_LABELS = {
  button: '按钮 Button', input: '输入 Input', avatar: '头像 Avatar',
  badge: '徽标 Badge', card: '卡片 Card', divider: '分割线 Divider',
  flag: '国旗 Flag', form: '表单 Form', icon: '图标 Icon',
  image: '图片 Image', list: '列表 List', loading: '加载 Loading',
  logo: '品牌标识 Logo', modal: '弹窗 Modal', navigation: '导航 Navigation',
  progress: '进度 Progress', toast: '提示 Toast', toggle: '开关 Toggle',
  tooltip: '气泡提示 Tooltip', typography: '排版 Typography',
  voucher: '优惠券 Voucher', other: '其他 Other'
};

const MODULE_LABELS = {
  general: '通用 General', home: '首页 Home', kyc: 'KYC 实名',
  loan: '贷款 Loan', merchant: '商户 Merchant', notification: '通知 Notification',
  onboarding: '新手引导 Onboarding', payment: '支付 Payment',
  profile: '个人中心 Profile', voucher: '优惠券 Voucher'
};

function header(title, subtitle, breadcrumb) {
  const lines = [`# ${title}`, ''];
  if (breadcrumb) lines.push(`> ${breadcrumb}`, '');
  if (subtitle) lines.push(subtitle, '');
  lines.push('---', '');
  return lines.join('\n');
}

function compactRow(g) {
  const firstKey = g.variants[0] ? g.variants[0].key : '';
  const more = g.variants.length > 1 ? ` _+${g.variants.length - 1}_` : '';
  return `| \`${g.name}\` | ${g.variants.length} | ${g.platform} | \`${firstKey}\`${more} |\n`;
}

function statsBlock(groupCount, total, fileCount) {
  return [
    '## 统计', '',
    `- 组件集：**${groupCount}**`,
    `- 变体总数：**${total}**`,
    `- 来源库：**${fileCount}**`,
    '', ''
  ].join('\n');
}

const MAX_LINES = 180;

function fileSlug(file) {
  return file.replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function compactTableHeadRel(jsonPathRel) {
  return [
    `| 组件集 | 变体 | 平台 | 首个变体 Key（更多见 [完整数据](${jsonPathRel})） |`,
    '|--------|------|------|----------------------------------------------------|'
  ].join('\n') + '\n';
}

function buildFlat({ kind, value, label, groups, total, byFile }) {
  const breadcrumb = `[词汇表](../../design-vocabulary.md) › [按${kind === 'type' ? '类型' : '模块'}](README.md) › ${label}`;
  let out = header(label, `DesignOps 库内 \`${kind === 'type' ? 'uiType' : 'module'} = ${value}\` 的全部组件，按来源库分节列出。`, breadcrumb);
  out += statsBlock(groups.length, total, Object.keys(byFile).length);
  for (const file of Object.keys(byFile).sort()) {
    out += `## ${file}\n\n` + compactTableHeadRel('../../../catalog/vocabulary-data.json');
    for (const g of byFile[file]) out += compactRow(g);
    out += '\n';
  }
  return out;
}

function buildIndex({ kind, value, label, groups, total, byFile }) {
  const breadcrumb = `[词汇表](../../design-vocabulary.md) › [按${kind === 'type' ? '类型' : '模块'}](README.md) › ${label}`;
  let out = header(label, `数据较多，已按来源库拆分到子文件。`, breadcrumb);
  out += statsBlock(groups.length, total, Object.keys(byFile).length);
  out += '## 按来源库分页\n\n| 来源库 | 组件集 | 变体 | 文档 |\n|--------|--------|------|------|\n';
  for (const file of Object.keys(byFile).sort()) {
    const g = byFile[file];
    const v = g.reduce((s, x) => s + x.variants.length, 0);
    out += `| ${file} | ${g.length} | ${v} | [${fileSlug(file)}.md](${value}/${fileSlug(file)}.md) |\n`;
  }
  return out;
}

function buildSub({ kind, value, label, file, groups }) {
  const breadcrumb = `[词汇表](../../../design-vocabulary.md) › [按${kind === 'type' ? '类型' : '模块'}](../README.md) › [${label}](../${value}.md) › ${file}`;
  const total = groups.reduce((s, g) => s + g.variants.length, 0);
  let out = header(`${label} · ${file}`, `共 ${groups.length} 个组件集 / ${total} 个变体。`, breadcrumb);
  out += compactTableHeadRel('../../../../catalog/vocabulary-data.json');
  for (const g of groups) out += compactRow(g);
  return out;
}

function renderTypeOrModulePage(opts) {
  const flat = buildFlat(opts);
  if (flat.split('\n').length <= MAX_LINES) {
    return { mode: 'flat', main: flat, sub: [] };
  }
  const main = buildIndex(opts);
  const sub = Object.keys(opts.byFile).sort().map(file => ({
    fileSlug: fileSlug(file),
    content: buildSub({ ...opts, file, groups: opts.byFile[file] })
  }));
  return { mode: 'split', main, sub };
}

function renderIndex({ kind, entries }) {
  const labels = kind === 'type' ? TYPE_LABELS : MODULE_LABELS;
  const breadcrumb = `[词汇表](../../design-vocabulary.md) › 按${kind === 'type' ? '类型' : '模块'}`;
  let out = header(
    kind === 'type' ? '按 UI 类型索引' : '按业务模块索引',
    `DesignOps 库（1,588 组件）的${kind === 'type' ? '类型' : '模块'}维度索引。`,
    breadcrumb
  );
  out += '| 类目 | 组件集 | 变体 | 文档 |\n|------|--------|------|------|\n';
  for (const e of entries) {
    const lbl = labels[e.value] || e.value;
    out += `| ${lbl} | ${e.groupCount} | ${e.variantCount} | [${e.value}.md](${e.value}.md) |\n`;
  }
  return out;
}

function renderIconsPage(icons, chunkSize) {
  const breadcrumb = `[词汇表](../../design-vocabulary.md) › 图标`;
  const headRow = '| 图标名 | 变体 | 首个 Key | 来源库 |\n|--------|------|---------|--------|\n';
  const rowFor = ic => `| \`${ic.name}\` | ${ic.variantCount} | \`${ic.key}\` | ${ic.file} |\n`;
  if (icons.length <= chunkSize) {
    let out = header('图标完整清单', `DesignOps Icon Library 共 ${icons.length} 个唯一图标（按名称去重），变体 keys 详见 [完整数据](../../catalog/vocabulary-data.json)。`, breadcrumb);
    out += headRow;
    for (const ic of icons) out += rowFor(ic);
    return { mode: 'flat', main: out, sub: [] };
  }
  const chunks = {};
  for (const ic of icons) {
    const first = (ic.name || '?').replace(/^icon\./, '').charAt(0).toUpperCase() || '#';
    const k = /[A-Z]/.test(first) ? first : '#';
    if (!chunks[k]) chunks[k] = [];
    chunks[k].push(ic);
  }
  let out = header('图标索引', `DesignOps Icon Library 共 ${icons.length} 个唯一图标，按首字母分组。变体 keys 详见 [完整数据](../../catalog/vocabulary-data.json)。`, breadcrumb);
  out += '| 首字母 | 数量 | 文档 |\n|--------|------|------|\n';
  for (const k of Object.keys(chunks).sort()) {
    out += `| ${k} | ${chunks[k].length} | [${k.toLowerCase()}.md](by-letter/${k.toLowerCase()}.md) |\n`;
  }
  const sub = Object.keys(chunks).sort().map(k => {
    let body = `# 图标 · ${k}\n\n> [词汇表](../../../design-vocabulary.md) › [图标](../README.md) › ${k}\n\n共 ${chunks[k].length} 个。\n\n---\n\n` + headRow;
    for (const ic of chunks[k]) body += rowFor(ic);
    return { letterSlug: k.toLowerCase(), content: body };
  });
  return { mode: 'split', main: out, sub };
}

function renderDataJson(allByDimension) {
  return JSON.stringify(allByDimension, null, 2);
}

module.exports = {
  TYPE_LABELS, MODULE_LABELS,
  renderTypeOrModulePage, renderIndex, renderIconsPage, renderDataJson
};
