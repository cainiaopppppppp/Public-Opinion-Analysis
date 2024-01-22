// /src/apis/login.js
// 登录接口
import httpInstance from '@/utils/http.js'

export function login(data) {
  return httpInstance({
    url: '/login', 
    method: 'post',
    data
  })
}