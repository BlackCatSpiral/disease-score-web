import api from './request'

export const recordApi = {
  // 获取列表
  getList: (params) => api.get('/records/', { params }),
  
  // 获取单条
  getById: (id) => api.get(`/records/${id}`),
  
  // 创建
  create: (data) => api.post('/records/', data),
  
  // 更新
  update: (id, data) => api.put(`/records/${id}`, data),
  
  // 删除
  delete: (id) => api.delete(`/records/${id}`)
}

export const excelApi = {
  // 导入
  import: (file, mode) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/excel/import?mode=${mode}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // 导出
  export: (keyword) => {
    const params = keyword ? `?keyword=${encodeURIComponent(keyword)}` : ''
    window.open(`http://localhost:8000/excel/export${params}`)
  }
}
