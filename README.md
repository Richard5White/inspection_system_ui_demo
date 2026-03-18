# 检测数据分析系统接口文档

# 1 接口设计概述

本系统用于对元器件检测数据进行统一管理和分析，包括检测数据的结构化存储、统计分析以及可视化展示。

------------------------------------------------------------------------

# 2 接口通用规范

## 2.1 接口前缀

    /api/v1

## 2.2 请求格式

    Content-Type: application/json

## 2.3 时间格式

    YYYY-MM-DD HH:mm:ss

## 2.4 通用返回结构

``` json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

# 3 基础数据接口

## 3.1 获取厂家列表

### 接口说明

该接口用于获取系统中已录入的厂家信息列表。厂家信息属于系统基础数据，在产品型号管理、检测批次创建以及数据查询等功能中都会使用到。

前端页面通常在加载筛选条件或查看检测批次时调用该接口获取厂家列表。

### 请求方式

```
GET /api/v1/manufacturers
```

### 请求参数

| 字段    | 类型   | 参数说明                     | 是否必填 |
| ------- | ------ | ---------------------------- | -------- |
| keyword | string | 厂家名称关键词，用于模糊查询 | 否       |

### 返回参数说明

| 字段             | 类型   | 说明     |
| ---------------- | ------ | -------- |
| manufacturerId   | string | 厂家ID   |
| manufacturerName | string | 厂家名称 |

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "manufacturerId": "manufacturer_001",
      "manufacturerName": "某电子科技有限公司"
    },
    {
      "manufacturerId": "manufacturer_002",
      "manufacturerName": "某半导体制造有限公司"
    }
  ]
}
```

## 3.2 获取产品型号列表

### 接口说明

该接口用于查询系统中已录入的产品型号信息。

产品型号通常与厂家存在关联关系，因此接口支持按照厂家进行筛选。

同时接口采用分页方式返回结果，方便前端进行列表展示和数据管理。

### 请求方式

```
GET /api/v1/products
```

### 请求参数

| 字段           | 类型   | 参数说明              | 是否必填 |
| -------------- | ------ | --------------------- | -------- |
| manufacturerId | string | 厂家ID                | 否       |
| keyword        | string | 产品型号关键词        | 否       |
| page           | int    | 页码，默认值为 1      | 否       |
| pageSize       | int    | 每页数量，默认值为 10 | 否       |

### 返回参数说明

**Products**

| 字段     | 类型  | 说明     |
| -------- | ----- | -------- |
| Products | array | 产品列表 |
| total    | int   | 总记录数 |
| page     | int   | 当前页码 |
| pageSize | int   | 每页数量 |

**Product**

| 字段             | 类型   | 说明                         |
| ---------------- | ------ | ---------------------------- |
| productId        | string | 产品ID                       |
| productModel     | string | 产品型号                     |
| productType      | string | 产品类型，如二极管、三极管等 |
| manufacturerId   | string | 厂家ID                       |
| manufacturerName | string | 厂家名称                     |

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "products": [
      {
        "productId": "prod_001",
        "productModel": "1N4148",
        "productType": "二极管",
        "manufacturerId": "manufacturer_001",
        "manufacturerName": "某电子科技有限公司"
      },
      {
        "productId": "prod_002",
        "productModel": "SS14",
        "productType": "肖特基二极管",
        "manufacturerId": "manufacturer_001",
        "manufacturerName": "某电子科技有限公司"
      }
    ],
    "total": 2,
    "page": 1,
    "pageSize": 10
  }
}
```

## 3.3 获取指定产品的检测指标

### 接口说明

该接口用于获取指定产品型号对应的检测指标信息。

例如稳定电压、稳定电流等。

### 请求方式

```
GET /api/v1/indicators
```

### 请求参数

| 字段      | 类型   | 参数说明 | 是否必填 |
| --------- | ------ | -------- | -------- |
| productId | string | 产品ID   | 是       |

### 返回参数说明

| 字段          | 类型   | 说明     |
| ------------- | ------ | -------- |
| indicatorId   | string | 指标ID   |
| indicatorName | string | 指标名称 |
| unit          | string | 单位     |
| upperLimit    | number | 指标上限 |
| lowerLimit    | number | 指标下限 |

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "indicatorId": "ind_001",
      "indicatorName": "稳定电压",
      "unit": "V",
      "upperLimit": 1.0,
      "lowerLimit": 0.0
    },
    {
      "indicatorId": "ind_002",
      "indicatorName": "稳定电流",
      "unit": "mA",
      "upperLimit": 10.0,
      "lowerLimit": 0.0
    }
  ]
}
```

# 4 检测批次接口

## 4.1 查询批次列表

### 接口说明

该接口用于查询系统中的某个厂家某个产品的检测批次信息。

**仅包含检测批次信息，不包含具体的检测数据。**

支持根据厂家、产品型号、批次编号以及数据来源类型进行筛选，并通过分页方式返回结果。

### 请求方式

```
GET /api/v1/batches
```

### 请求参数

| 字段           | 类型   | 参数说明                   | 是否必填 |
| -------------- | ------ | -------------------------- | -------- |
| manufacturerId | string | 厂家ID                     | 否       |
| productId      | string | 产品ID                     | 否       |
| batchNo        | string | 批次编号，支持模糊查询     | 否       |
| sourceType     | string | 数据来源类型，如一筛、二筛 | 否       |
| page           | int    | 页码，默认值为 1           | 否       |
| pageSize       | int    | 每页数量，默认值为 10      | 否       |

### 返回参数说明

**Batches**

| 字段     | 类型  | 说明     |
| -------- | ----- | -------- |
| batches  | array | 批次列表 |
| total    | int   | 总记录数 |
| page     | int   | 当前页码 |
| pageSize | int   | 每页数量 |

**Batch**

| 字段             | 类型   | 说明         |
| ---------------- | ------ | ------------ |
| batchId          | string | 批次ID       |
| batchNo          | string | 批次编号     |
| manufacturerId   | string | 厂家ID       |
| manufacturerName | string | 厂家名称     |
| productId        | string | 产品ID       |
| productModel     | string | 产品型号     |
| sourceType       | string | 数据来源类型 |
| productionDate   | string | 生产日期     |
| inspectionDate   | string | 检测日期     |
| sampleCount      | int    | 样品数量     |
| remark           | string | 备注信息     |

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "batches": [
      {
        "batchId": "batch_001",
        "batchNo": "B20260121001",
        "manufacturerId": "manufacturer_001",
        "manufacturerName": "某电子科技有限公司",
        "productId": "prod_001",
        "productModel": "1N4148",
        "sourceType": "一筛",
        "productionDate": "2026-01-15",
        "inspectionDate": "2026-01-21",
        "sampleCount": 500,
        "remark": "代表性批次样本"
      }
    ],
    "total": 1,
    "page": 1,
    "pageSize": 10
  }
}
```

## 4.2 查询批次详情

### 接口说明

该接口用于获取指定检测批次的详细信息。

### 请求方式

```
GET /api/v1/batches/{batchId}
```

### 路径参数

| 字段    | 类型   | 参数说明 | 是否必填 |
| ------- | ------ | -------- | -------- |
| batchId | string | 批次ID   | 是       |

### 返回参数说明

| 字段             | 类型   | 说明         |
| ---------------- | ------ | ------------ |
| batchId          | string | 批次ID       |
| batchNo          | string | 批次编号     |
| manufacturerId   | string | 厂家ID       |
| manufacturerName | string | 厂家名称     |
| productId        | string | 产品ID       |
| productModel     | string | 产品型号     |
| productType      | string | 产品类型     |
| sourceType       | string | 数据来源类型 |
| productionDate   | string | 生产日期     |
| inspectionDate   | string | 检测日期     |
| sampleCount      | int    | 样品数量     |
| remark           | string | 备注         |
| createdAt        | string | 创建时间     |
| updatedAt        | string | 更新时间     |

### 返回示例

```
{
  "code": 0,
  "message": "success",
  "data": {
    "batchId": "batch_001",
    "batchNo": "B20260121001",
    "manufacturerId": "manufacturer_001",
    "manufacturerName": "某电子科技有限公司",
    "productId": "prod_001",
    "productModel": "1N4148",
    "productType": "二极管",
    "sourceType": "一筛",
    "productionDate": "2026-01-15",
    "inspectionDate": "2026-01-21",
    "sampleCount": 500,
    "remark": "代表性批次样本",
    "createdAt": "2026-01-21 10:00:00",
    "updatedAt": "2026-01-21 10:30:00"
  }
}
```

------

# 5 检测记录接口

## 5.1 查询某个批次的所有检测数据

### 接口说明

该接口用于查询指定检测批次的检测记录数据。

检测记录表示某个样品在某个检测指标下的检测结果。一个检测批次通常会包含多个样品，每个样品又对应多个检测指标。因此，该接口返回的数据将按照 **样品（Sample）进行分组**，每个样品包含其对应的多个检测结果。

------

### 请求方式

```
GET /api/v1/records
```

------

### 请求参数

| 字段    | 类型   | 参数说明   | 是否必填 |
| ------- | ------ | ---------- | -------- |
| batchId | string | 检测批次ID | 是       |

------

### 返回参数说明

**RecordsResponse**

| 字段    | 类型   | 说明         |
| ------- | ------ | ------------ |
| batchId | string | 检测批次ID   |
| samples | array  | 样品检测数据 |

------

**Sample**

| 字段     | 类型   | 说明                 |
| -------- | ------ | -------------------- |
| sampleNo | string | 样品编号             |
| results  | array  | 该样品对应的检测结果 |

------

**Result**

| 字段          | 类型   | 说明         |
| ------------- | ------ | ------------ |
| indicatorId   | string | 检测指标ID   |
| indicatorName | string | 检测指标名称 |
| value         | number | 检测值       |
| unit          | string | 单位         |

------

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "batchId": "batch_001",
    "samples": [
      {
        "sampleNo": "S001",
        "results": [
          {
            "indicatorId": "ind_001",
            "indicatorName": "稳定电压",
            "value": 0.16,
            "unit": "V"
          },
          {
            "indicatorId": "ind_002",
            "indicatorName": "稳定电流",
            "value": 1.2,
            "unit": "mA"
          }
        ]
      },
      {
        "sampleNo": "S002",
        "results": [
          {
            "indicatorId": "ind_001",
            "indicatorName": "稳定电压",
            "value": 0.15,
            "unit": "V"
          },
          {
            "indicatorId": "ind_002",
            "indicatorName": "稳定电流",
            "value": 1.3,
            "unit": "mA"
          }
        ]
      }
    ]
  }
}
```

# 6 数据分析接口

## 6.1 批次指标统计接口

### 接口说明

该接口用于对指定检测批次中的某个检测指标进行统计分析，例如平均值、最大值、最小值以及标准差等统计指标。

------

### 请求方式

```
GET /api/v1/analysis
```

------

### 请求参数

| 字段        | 类型   | 参数说明   | 是否必填 |
| ----------- | ------ | ---------- | -------- |
| batchId     | string | 检测批次ID | 是       |
| indicatorId | string | 检测指标ID | 是       |

------

### 返回参数说明

| 字段          | 类型   | 说明         |
| ------------- | ------ | ------------ |
| batchId       | string | 批次ID       |
| indicatorId   | string | 检测指标ID   |
| indicatorName | string | 检测指标名称 |
| mean          | number | 平均值       |
| max           | number | 最大值       |
| min           | number | 最小值       |
| std           | number | 标准差       |
| sampleCount   | int    | 样本数量     |

------

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "batchId": "batch_001",
    "indicatorId": "ind_001",
    "indicatorName": "稳定电压",
    "mean": 0.15,
    "max": 0.60,
    "min": 0.14,
    "std": 0.03,
    "sampleCount": 500
  }
}
```

## 6.2 批次指标统计接口(细化到统计方式)(待定)

# 7 首页可视化接口

## 7.1 首页概览接口

### 接口说明

该接口用于获取系统整体数据统计信息，用于展示系统当前的数据规模与运行情况。

接口返回的信息包括系统中已录入的厂家数量、产品型号数量、检测批次数量以及检测记录总数等统计指标。前端首页通常通过调用该接口获取系统整体数据，并用于展示首页仪表盘（Dashboard）中的统计卡片或概览信息。

通过该接口，用户可以快速了解系统当前的数据接入情况以及检测数据规模，为后续数据分析和异常检测提供整体视角。

------

### 请求方式

```
GET /api/v1/dashboard/overview
```

------

### 请求参数

无

------

### 返回参数说明

| 字段              | 类型 | 说明                 |
| ----------------- | ---- | -------------------- |
| manufacturerCount | int  | 系统中厂家数量       |
| productCount      | int  | 系统中产品型号数量   |
| batchCount        | int  | 检测批次数量         |
| recordCount       | int  | 检测记录总数         |
| anomalyBatchCount | int  | 检测到异常的批次数量 |

------

### 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "manufacturerCount": 3,
    "productCount": 12,
    "batchCount": 86,
    "recordCount": 152340,
    "anomalyBatchCount": 5
  }
}
```
