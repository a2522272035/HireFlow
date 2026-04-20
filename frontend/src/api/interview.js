import request from './request'

export const interviewApi = {
  // Create interview
  create(data) {
    return request.post('/v1/interviews/', data)
  },

  // Get interview by ID
  getById(id) {
    return request.get(`/v1/interviews/${id}`)
  },

  // Generate questions
  generateQuestions(id) {
    return request.post(`/v1/interviews/${id}/questions`)
  },

  // Assess answer credibility
  assessAnswer(id, data) {
    return request.post(`/v1/interviews/${id}/assess`, data)
  },

  // Update interview
  update(id, data) {
    return request.put(`/v1/interviews/${id}`, data)
  },

  // End interview
  end(id) {
    return request.post(`/v1/interviews/${id}/end`)
  },
}
