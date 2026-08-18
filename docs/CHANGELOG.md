# 更新日誌 / Changelog

**Languages:** 本檔繁中為主 · English summaries inline where noted

---

## 2026-08-18 — 轉盤優先 pin 擴充至 14 家

### 摘要

轉盤優先納入店家由 **4 家 → 14 家**（保留原 4 家 + 圖片清單 10 家）。離線快取 **303 → 306** 家；其中 3 家經 `add_user_favorite_places.py` 手動 merge，其餘 7 家已在快取中僅新增 pin。

### 變更檔案

| 檔案 | 說明 |
|------|------|
| `data/user_favorites.json` | 新增 10 個 `place_ids`（共 14） |
| `scripts/add_user_favorite_places.py` | 補 3 家不在快取的店家資料 |
| `data/places_cache.public.json` | 雲端 demo 快取同步至 306 家 |
| `data/places_cache.json` | 本機快取（`.gitignore`，不 commit） |

### 14 家轉盤 pin 清單

| # | 顯示／圖片名稱 | 快取店名 | 來源 |
|---|----------------|----------|------|
| 1 | 巧食坊 | 巧食坊宜大店 | 原 pin |
| 2 | 甜屋 | 甜屋義大利麵 | 原 pin |
| 3 | 布麥加 | 布麥加 | 原 pin |
| 4 | 鴨米 | 鴨米港式燒臘便當 | 原 pin |
| 5 | 林聚裡臭臭鍋 | 林聚裡臭臭鍋 | 快取已有，僅 pin |
| 6 | 嗅香臭臭鍋 | 嗅香臭臭鍋 | **手動 merge** |
| 7 | 又見麵拉麵 | 又見麵拉麵 | **手動 merge** |
| 8 | 上野烤肉飯 | 上野烤肉飯-宜蘭店 | 快取已有，僅 pin |
| 9 | 紅牛鐵板燒 | 紅牛鐵板燒 | **手動 merge** |
| 10 | 好食麵舖 | 好食糆舖.火鍋 | 快取已有；Google 正式名 |
| 11 | 非凡豆漿 | 非凡豆漿 | 快取已有，僅 pin |
| 12 | 火生餛飩 | 火生餛飩麵店 | 快取已有，僅 pin |
| 13 | 歡喜堂 | 歡喜堂 便當-快餐 | 快取已有，僅 pin |
| 14 | 老仙覺 | 老先覺麻辣鍋(蔬食吃到飽)-宜蘭宜中店 | 快取已有；Google 正式名 |

### 行為說明

- 轉盤在**營業中**且通過正餐／分類篩選時，會**優先**納入上述 14 家（見 `data/user_favorites.json` → `streamlit_app._load_wheel_pins`）。
- **休息中**的 pin 店仍會被排除（與既有轉盤規則一致）。

### 驗證

```powershell
cd c:\Users\User\Documents\code\校園美食地圖_v2
$env:PYTHONPATH = "src"
pytest -q --cov=src --cov-fail-under=70
```

結果：**117 passed**，coverage **84%**（exit 0）。

### 風險與後續

- 3 家手動 merge 的評分／座標來自公開來源彙整，**非即時 Google API**；有 `GOOGLE_MAPS_API_KEY` 時可重跑 `fetch_places_to_json.py` 校正後再 `add_user_favorite_places.py` 與 `Copy-Item` 同步 public 快取。
- 更新本機 `places_cache.json` 後，部署前須同步 `data/places_cache.public.json` 再 push。

### 相關指令（有 API key 時校正快取）

```powershell
cd c:\Users\User\Documents\code\校園美食地圖_v2
$env:PYTHONPATH = "src"
$env:GOOGLE_MAPS_API_KEY = "你的金鑰"
$env:GOOGLE_PLACES_TIMEOUT_S = "60"
python scripts/fetch_places_to_json.py --lat 24.7464 --lon 121.7457 --radius-m 1000 --grid 6 --out data/places_cache.json
python scripts/enrich_food_groups.py data/places_cache.json
python scripts/add_user_favorite_places.py
Copy-Item data/places_cache.json data/places_cache.public.json -Force
```

---

## Earlier releases

| 日期 | 摘要 | 詳見 |
|------|------|------|
| 2026-06-25 | v2 上線：300 家快取、15 類、轉盤 Top 40 | [v2-上線與變更總結.md](v2-上線與變更總結.md) |
| 2026-06-26 | 轉盤 pin 4 家、移除常去 UI | Git `8bc4c6c` 等 |

---

*Last updated: 2026-08-18*
