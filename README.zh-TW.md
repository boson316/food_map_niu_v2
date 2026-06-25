# 校園美食地圖 v2

**Languages:** [English](README.md) · [中文](README.zh-TW.md)

> **v2 工作區** — 自 v1（`cursor/114_1_學校專案/python程式期末專案_美食系統`）複製而來。  
> **v2 雲端：** https://food-map-niu-v2.streamlit.app · **v2 repo：** https://github.com/boson316/food_map_niu_v2  
> v1 雲端：https://niu-foodmap.streamlit.app · v1 repo：https://github.com/boson316/niu-foodmap

**作者：** Boson Huang · **授權：** 專有軟體 — 見 [LICENSE](LICENSE)

> 核心演算法（`scoring.py`、`service.py`、`wheel.py`）受著作權保護；部署時會驗證檔案完整性，遭竄改則拒絕啟動。
> 若不想讓原始碼在 GitHub 上被直接閱讀，請將 repo 設為 **Private**（Streamlit Cloud 仍可部署，公開網址照常分享）。

本目錄同時保留 **project_bootstrap** 說明與本學期主題 **校園附近美食地圖**（`src/foodmap/`）。

---

## 校園附近美食地圖｜國立宜蘭大學（Mock JSON + 排序）

### 功能摘要（v2）

- 預設半徑 **1 km**、預設顯示 **300** 家；資料池 **1 km 內盡量抓滿**（加強版快取 **300** 家）。
- **美食分類**：十五類（滷味、下午茶咖啡廳、火鍋、牛排館、麵食、日式、韓式、素食蔬食、點心包子、義式披薩、百匯自助、熱炒合菜、燒腊港式、便當、炸物）+ **其他**（側欄多選；轉盤有選時自動併入「其他」）。
- **預算**：平價篩選（`price_level 1` ≈ $100–300）+ 可含未標價位。
- **營業狀態**：地圖顯示「營業中／休息中／未知」；**轉盤排除休息中**（營業時間未知仍保留）。
- 完整規格：[docs/v2-規格.md](docs/v2-規格.md)

### 功能摘要（沿用 v1）

- 預設校園中心：**國立宜蘭大學校本部**（神農路一段1號），約 `24.7464°N, 121.7457°E`。
- 依**中心緯經度**與**半徑（公里）**篩選；可設**最少評論數**。
- **排序**：`composite`（**黃氏星等 × 距離衰減**，預設）、`rating`（貝氏星等）、`huang`（黃氏星等）、`distance`（由近到遠）。
- **黃氏星等**：1～2 星低／3 星普通／4～5 星高分級 × 星分權重 × 評論量權重；`composite_score = 黃氏 × 距離衰減`。
- **離線資料**：`src/foodmap/data/sample_restaurants.json`（15 筆範例，名稱虛構）。
- **輸入防護**：自訂 JSON 上限 5 MiB、最多 10,000 筆，欄位與數值範圍驗證（見 `foodmap/validation.py`）。
- **Streamlit**：表格 + 點位圖；中心可由側欄或 `CAMPUS_LAT`／`CAMPUS_LON` 覆寫。

### 安裝與測試

```powershell
cd 校園美食地圖_v2
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
pytest -q --cov=src --cov-fail-under=70
```

### CLI

```powershell
$env:PYTHONPATH = "src"
python -m foodmap search --lat 24.7464 --lon 121.7457 --radius 1.0 --sort composite --format table
python -m foodmap search --lat 24.7464 --lon 121.7457 --food-group 火鍋類 --max-price-level 1 --format json
```

### Demo 腳本（給老師）

```powershell
cd 校園美食地圖_v2
$env:PYTHONPATH = "src"

# 1) 宜大校門口 1km 內，綜合排序
python -m foodmap search --lat 24.7464 --lon 121.7457 --radius 1.0 --sort composite

# 2) 最少評論 100 → 濾掉少評論店
python -m foodmap search --lat 24.7464 --lon 121.7457 --radius 1.0 --min-reviews 100

# 3) 半徑 5km 才出現遠距範例
python -m foodmap search --lat 24.7464 --lon 121.7457 --radius 5.0 --sort distance

# 4) 網頁版
streamlit run src/streamlit_app.py
```

### 自訂 JSON 欄位

| 欄位 | 必填 | 說明 |
|------|------|------|
| `id` | ✓ | 字串 ID |
| `name` | ✓ | 店名 |
| `lat` / `lon` | ✓ | WGS84 緯經度 |
| `rating` | ✓ | 平均星等 0～5 |
| `review_count` | ✓ | 評論數（整數 ≥0） |
| `category` | | 字串，可空 |
| `price_level` | | 1～4 或省略 |
| `food_groups` | | 字串陣列（可省略，載入時自動分類） |
| `regular_opening_hours` | | Google `periods` 物件（可省略） |
| `business_status` | | `OPERATIONAL` 等（可省略） |

`json` 輸出另含 `open_status_display`、`food_group_display`、`avg_spend_display`。

### 進階：Google Places 快取

```powershell
$env:PYTHONPATH = "src"
$env:GOOGLE_MAPS_API_KEY = "你的金鑰"
python scripts/fetch_places_to_json.py --lat 24.7464 --lon 121.7457 --radius-m 1000 --grid 6 --out data/places_cache.json
python scripts/enrich_food_groups.py data/places_cache.json
python -m foodmap search --lat 24.7464 --lon 121.7457 --radius 1.0 --data data/places_cache.json --sort huang --limit 20
streamlit run src/streamlit_app.py
```

快取檔存在時 Streamlit 會自動載入 `data/places_cache.json`（已列入 `.gitignore`）。

效能路徑：bbox 粗篩 → haversine → `heapq` top-k。

---

## project_bootstrap（範本說明）

詳見 [README.md](README.md) 英文版「project_bootstrap」章節。
