// /src/apis/register.js
// 注册接口
import httpInstance from '@/utils/http.js'

export function register(data) {
  return httpInstance({
    url: '/register',
    method: 'post',
    data
  })
}