// /src/utils/http.js
import axios from 'axios'

const httpInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 5000,
    
})

httpInstance.interceptors.request.use(function (config) {
    return config;
  }, function (error) {
    return Promise.reject(error);
  });

// 添加响应拦截器
httpInstance.interceptors.response.use(function (response) {
    return response;
  }, function (error) {
    return Promise.reject(error);
  });

export default httpInstance