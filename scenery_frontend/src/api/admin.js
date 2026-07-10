import request from './request'

export const adminUsers = (params) => request.get('/api/admin/users', { params })
export const updateUserStatus = (id, data) => request.put(`/api/admin/users/${id}/status`, data)
export const updateUserRole = (id, data) => request.put(`/api/admin/users/${id}/role`, data)

export const adminSpots = (params) => request.get('/api/admin/spots', { params })
export const createSpot = (data) => request.post('/api/admin/spots', data)
export const updateSpot = (id, data) => request.put(`/api/admin/spots/${id}`, data)
export const deleteSpot = (id) => request.delete(`/api/admin/spots/${id}`)

export const adminRoutes = (params) => request.get('/api/admin/routes', { params })
export const createRoute = (data) => request.post('/api/admin/routes', data)
export const updateRoute = (id, data) => request.put(`/api/admin/routes/${id}`, data)
export const deleteRoute = (id) => request.delete(`/api/admin/routes/${id}`)

export const adminFaqs = (params) => request.get('/api/admin/faqs', { params })
export const createFaq = (data) => request.post('/api/admin/faqs', data)
export const updateFaq = (id, data) => request.put(`/api/admin/faqs/${id}`, data)
export const deleteFaq = (id) => request.delete(`/api/admin/faqs/${id}`)

export const adminFeedbacks = (params) => request.get('/api/admin/feedbacks', { params })
export const updateFeedback = (id, data) => request.put(`/api/admin/feedbacks/${id}`, data)
export const feedbackStats = () => request.get('/api/admin/feedbacks/stats')

export const adminChats = (params) => request.get('/api/admin/chat-records', { params })
