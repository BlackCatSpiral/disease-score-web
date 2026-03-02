<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    :title="isEdit ? '编辑记录' : '新增记录'"
    width="500px"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="收费分类" prop="charge_category">
        <el-input v-model="form.charge_category" placeholder="请输入收费分类" />
      </el-form-item>

      <el-form-item label="收费项目编码" prop="charge_item_code">
        <el-input v-model="form.charge_item_code" placeholder="请输入收费项目编码" />
      </el-form-item>

      <el-form-item label="项目名称" prop="item_name">
        <el-input v-model="form.item_name" placeholder="请输入项目名称" />
      </el-form-item>

      <el-form-item label="省份" prop="province">
        <el-input v-model="form.province" placeholder="请输入省份" />
      </el-form-item>

      <el-form-item label="城市" prop="city">
        <el-input v-model="form.city" placeholder="请输入城市" />
      </el-form-item>

      <el-form-item label="原价" prop="original_price">
        <el-input-number v-model="form.original_price" :precision="2" :min="0" style="width: 100%" />
      </el-form-item>

      <el-form-item label="折扣价" prop="discount_price">
        <el-input-number v-model="form.discount_price" :precision="2" :min="0" style="width: 100%" />
      </el-form-item>

      <el-form-item label="项目分值" prop="project_score">
        <el-input-number v-model="form.project_score" :precision="2" style="width: 100%" />
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input v-model="form.remark" type="textarea" rows="3" placeholder="请输入备注" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { recordApi } from '../api'

const props = defineProps({
  visible: Boolean,
  record: Object
})

const emit = defineEmits(['update:visible', 'success'])

const formRef = ref()
const submitting = ref(false)

const isEdit = computed(() => !!props.record)

const defaultForm = {
  charge_category: '',
  charge_item_code: '',
  item_name: '',
  province: '',
  city: '',
  original_price: null,
  discount_price: null,
  project_score: null,
  remark: ''
}

const form = ref({ ...defaultForm })

const rules = {
  charge_item_code: [
    { required: true, message: '请输入收费项目编码', trigger: 'blur' }
  ],
  item_name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ]
}

// 监听record变化
watch(() => props.record, (val) => {
  if (val) {
    form.value = { ...val }
  } else {
    form.value = { ...defaultForm }
  }
}, { immediate: true })

const handleCancel = () => {
  emit('update:visible', false)
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (isEdit.value) {
      await recordApi.update(props.record.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await recordApi.create(form.value)
      ElMessage.success('创建成功')
    }
    emit('success')
    emit('update:visible', false)
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    submitting.value = false
  }
}
</script>
