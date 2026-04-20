import request from './request'

export const reportApi = {
  // List reports
  list(params) {
    return request.get('/v1/reports/', { params })
  },

  // Get report by ID
  getById(id) {
    return request.get(`/v1/reports/${id}`)
  },

  // Generate report
  generate(interviewId) {
    return request.post(`/v1/reports/generate/${interviewId}`)
  },

  // Export report
  export(id, format = 'pdf') {
    return request.get(`/v1/reports/${id}/export`, {
      params: { format },
      responseType: 'blob',
    })
  },
}
