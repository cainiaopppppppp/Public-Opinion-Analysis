// /src/apis/forget.js

import httpInstance from '@/utils/http'

// 发送重置密码邮件
// export function sendResetEmail(email) {
//   return httpInstance({
//     url: '/password/reset',
//     method: 'post',
//     data: {
//       email
//     }
//   })
// }

// 重置密码
export function resetPassword(data) {
  return httpInstance({
    url: '/forget',
    method: 'post',
    data 
  })
}