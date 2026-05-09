import http from './http'

export const userApi = {
  sendCode: (target: string, code_type: 'email' | 'phone') =>
    http.post('/users/send-code/', { target, code_type }),
  register: (data: object) => http.post('/users/register/', data),
  login: (data: object) => http.post('/users/login/', data),
  getProfile: () => http.get('/users/profile/'),
  updateProfile: (data: object) => http.patch('/users/profile/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}

export const questionnaireApi = {
  get: () => http.get('/questionnaire/'),
  patch: (answers: object) => http.patch('/questionnaire/', { answers }),
}

export const matchApi = {
  current: () => http.get('/match/current/'),
  respond: (id: number, action: 'liked' | 'passed') =>
    http.post(`/match/${id}/respond/`, { action }),
  history: () => http.get('/match/history/'),
}

export const chatApi = {
  rooms: () => http.get('/chat/rooms/'),
  messages: (roomId: number) => http.get(`/chat/rooms/${roomId}/messages/`),
  uploadImage: (roomId: number, formData: FormData) =>
    http.post(`/chat/rooms/${roomId}/upload/`, formData),
  report: (data: object) => http.post('/chat/report/', data),
  block: (userId: string) => http.post(`/chat/block/${userId}/`),
  unblock: (userId: string) => http.delete(`/chat/unblock/${userId}/`),
}

export const postsApi = {
  list: () => http.get('/posts/'),
  create: (data: { content: string; is_anonymous: boolean }) =>
    http.post('/posts/create/', data),
  like: (id: number) => http.post(`/posts/${id}/like/`),
  delete: (id: number) => http.delete(`/posts/${id}/delete/`),
}
