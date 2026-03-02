<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    title="导入Excel"
    width="500px"
  >
    <el-form label-width="100px">
      <el-form-item label="导入模式" required>
        <el-radio-group v-model="importMode">
          <el-radio label="append">追加（添加记录）</el-radio>
          <el-radio label="update">更新（更新匹配记录）</el-radio>
          <el-radio label="upsert">追加或更新</el-radio>
          <el-radio label="replace">替换（清空后导入）</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="选择文件" required>
        <el-upload
          ref="uploadRef"
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          accept=".xlsx,.xls"
        >
          <el-button type="primary">
            <el-icon><Upload /></el-icon>选择文件
          </el-button>
          <template #tip>
            <div class="upload-tip">
              支持 .xlsx, .xls 格式，必须包含"收费项目编码"和"项目名称"列
            </div>
          </template>
        </el-upload>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="uploading">确定导入</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { excelApi } from '../api'

const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['update:visible', 'success'])

const uploadRef = ref()
const importMode = ref('append')
const selectedFile = ref(null)
const uploading = ref(false)

const handleFileChange = (file) => {
  selectedFile.value = file.raw
}

const handleCancel = () => {
  selectedFile.value = null
  importMode.value = 'append'
  uploadRef.value?.clearFiles()
  emit('update:visible', false)
}

const handleSubmit = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }

  uploading.value = true
  try {
    const res = await excelApi.import(selectedFile.value, importMode.value)
    const msg = [`导入完成`]
    if (res.inserted) msg.push(`新增: ${res.inserted} 条`)
    if (res.updated) msg.push(`更新: ${res.updated} 条`)
    if (res.errors?.length) {
      msg.push(`错误: ${res.errors.length} 条`)
      console.error('导入错误:', res.errors)
    }
    ElMessage.success(msg.join('，'))
    emit('success')
    handleCancel()
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
</style>
