import request from './request'

export const resumeApi = {
  // Upload resume
  upload(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/v1/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Get resume by ID
  getById(id) {
    return request.get(`/v1/resumes/${id}`)
  },

  // Analyze resume gaps
  analyzeGaps(id) {
    return request.get(`/v1/resumes/${id}/gaps`)
  },

  // Update resume
  update(id, data) {
    return request.put(`/v1/resumes/${id}`, data)
  },

  // Delete resume
  delete(id) {
    return request.delete(`/v1/resumes/${id}`)
  },
}
