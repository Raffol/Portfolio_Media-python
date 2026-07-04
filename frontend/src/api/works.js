import client from './client'

export const getWorks = (params = {}) =>
  client.get('/works/', { params }).then((r) => r.data)

export const getWork = (slug) =>
  client.get(`/works/${slug}/`).then((r) => r.data)

export const getCategories = () =>
  client.get('/categories/').then((r) => r.data)
