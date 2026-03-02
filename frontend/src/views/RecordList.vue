<template>
  <div class="app-container">
    <!-- 顶部工具栏 -->
    <el-card class="toolbar-card" shadow="never">
      <el-row :gutter="10" align="middle">
        <el-col :span="16">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增
          </el-button>
          <el-button @click="handleImport">
            <el-icon><Upload /></el-icon>导入Excel
          </el-button>
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>导出Excel
          </el-button>
          <el-button type="danger" @click="handleBatchDelete" :disabled="!selectedRows.length">
            <el-icon><Delete /></el-icon>删除
          </el-button>
        </el-col>
        <el-col :span="8">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索：分类/编码/名称/省份/城市"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        :data="tableData"
        v-loading="loading"
        @selection-change="handleSelectionChange"
        stripe
        border
        height="calc(100vh - 250px)"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="charge_category" label="收费分类" width="100" />
        <el-table-column prop="charge_item_code" label="收费项目编码" width="120" />
        <el-table-column prop="item_name" label="项目名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="province" label="省份" width="80" />
        <el-table-column prop="city" label="城市" width="80" />
        <el-table-column prop="original_price" label="原价" width="80" align="right">
          <template #default="{ row }">
            {{ row.original_price?.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="discount_price" label="折扣价" width="80" align="right">
          <template #default="{ row }">
            {{ row.discount_price?.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="project_score" label="项目分值" width="80" align="right" />
        <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100, 200]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        class="pagination"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <RecordDialog
      v-model:visible="dialogVisible"
      :record="currentRecord"
      @success="handleSuccess"
    />

    <!-- 导入对话框 -->
    <ImportDialog
      v-model:visible="importVisible"
      @success="handleSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { recordApi, excelApi } from '../api'
import RecordDialog from '../components/RecordDialog.vue'
import ImportDialog from '../components/ImportDialog.vue'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(50)
const searchKeyword = ref('')
const selectedRows = ref([])
const dialogVisible = ref(false)
const importVisible = ref(false)
const currentRecord = ref(null)

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await recordApi.getList({
      keyword: searchKeyword.value,
      page: page.value,
      page_size: pageSize.value
    })
    tableData.value = res.data
    total.value = res.total
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  fetchData()
}

// 分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchData()
}

const handlePageChange = (val) => {
  page.value = val
  fetchData()
}

// 选择
const handleSelectionChange = (val) => {
  selectedRows.value = val
}

// 新增
const handleAdd = () => {
  currentRecord.value = null
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  currentRecord.value = row
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该记录吗？', '提示', {
      type: 'warning'
    })
    await recordApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
      type: 'warning'
    })
    for (const row of selectedRows.value) {
      await recordApi.delete(row.id)
    }
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

// 导入
const handleImport = () => {
  importVisible.value = true
}

// 导出
const handleExport = () => {
  excelApi.export(searchKeyword.value)
  ElMessage.success('开始下载')
}

// 成功回调
const handleSuccess = () => {
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.toolbar-card {
  margin-bottom: 15px;
}

.table-card {
  margin-bottom: 15px;
}

.pagination {
  margin-top: 15px;
  justify-content: flex-end;
}
</style>
