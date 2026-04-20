# Atome UED Figma 素材库 — 全流程编排
# 用法: make all (完整流程) | make scan (仅增量扫描) | make test (运行测试)

.PHONY: all scan dedup classify tokens index screenshots test clean help

# 加载 .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

all: scan dedup classify tokens index ## 运行完整流程

scan: ## 增量扫描（仅更新变更文件）
	@echo "🔍 增量扫描..."
	@bash scripts/incremental-scan.sh

fetch: ## 获取全量组件列表
	@echo "📦 获取组件列表..."
	@bash scripts/fetch-components.sh

dedup: ## 组件去重分析
	@echo "🔎 组件去重分析..."
	@python3 scripts/component-dedup.py

classify: ## 分类细化
	@echo "📂 分类索引构建..."
	@python3 scripts/refine-classification.py
	@python3 scripts/build-classified-index.py

tokens: ## Token 导出（含 W3C 格式）
	@echo "🎨 Token 导出..."
	@python3 scripts/export-w3c-tokens.py

index: ## 构建统一索引
	@echo "📋 构建统一索引..."
	@node scripts/build-index.js

screenshots: ## 下载组件截图
	@echo "📸 下载截图..."
	@bash scripts/download-screenshots.sh

test: ## 运行单元测试
	@python3 -m unittest tests.test_core -v

clean: ## 清除缓存
	@rm -rf reports/.api-cache
	@echo "✅ 缓存已清除"
