import request from './request'

export const getSpots = (params) => request.get('/api/spots', { params })
export const getSpot = (id) => request.get(`/api/spots/${id}`)
export const getSpotCategories = () => request.get('/api/spots/categories')

export const getRoutes = (params) => request.get('/api/routes', { params })
export const getRoute = (id) => request.get(`/api/routes/${id}`)
export const recommendRoute = (params) => request.get('/api/routes/recommend', { params })

export const getFavorites = () => request.get('/api/favorites')
export const addFavorite = (spotId) => request.post(`/api/favorites/${spotId}`)
export const removeFavorite = (spotId) => request.delete(`/api/favorites/${spotId}`)

export const submitFeedback = (data) => request.post('/api/feedback', data)
export const getMyFeedback = () => request.get('/api/feedback/mine')

export const getFaqs = (params) => request.get('/api/faqs', { params })
export const matchFaq = (params) => request.get('/api/faqs/match', { params })

export const sendChat = (data) => request.post('/api/chat', data)
export const getChatHistory = () => request.get('/api/chat/history')
export const getChatDetail = (sessionId) => request.get(`/api/chat/history/${sessionId}`)
