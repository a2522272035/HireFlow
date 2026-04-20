import request from './request'

export const policyApi = {
  // Upload policy document
  upload(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/v1/policies/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Query policy documents
  query(data) {
    return request.post('/v1/policies/query', data)
  },

  // List all documents
  list(params) {
    return request.get('/v1/policies/documents', { params })
  },

  // Get document by ID
  getById(id) {
    return request.get(`/v1/policies/documents/${id}`)
  },

  // Delete document
  delete(id) {
    return request.delete(`/v1/policies/documents/${id}`)
  },

  // Update document
  update(id, data) {
    return request.put(`/v1/policies/documents/${id}`, data)
  },
}
