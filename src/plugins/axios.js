"use strict";

import Vue from 'vue';
import axios from "axios";
import { Message } from 'element-ui'

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

let config = {
  // baseURL: process.env.baseURL || process.env.apiUrl || ""
  baseURL: 'http://localhost:5000/api/v1'
  // timeout: 60 * 1000, // Timeout
  // withCredentials: true, // Check cross-site Access-Control
};

const ShowError = () => {
  Message({
    type: 'error',
    message: '出错了！',
    duration: 2000
  })
}

export const api = axios.create(config);

api.interceptors.request.use(
  function (config) {
    // Do something before request is sent
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add a response interceptor
api.interceptors.response.use(
  function (response) {
    // Do something with response data
    return response;
  },
  function (error) {
    // Do something with response error
    ShowError()
    return Promise.reject(error);
  }
);

Plugin.install = function (Vue, options) {
  Vue.axios = api;
  window.axios = api;
  Object.defineProperties(Vue.prototype, {
    axios: {
      get() {
        return api;
      }
    },
    $axios: {
      get() {
        return api;
      }
    },
  });
};

Vue.use(Plugin)

export default Plugin;
