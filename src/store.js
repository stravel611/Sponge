import Vue from 'vue'
import Vuex from 'vuex'
import { api } from './plugins/axios'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        categories: [],         // 分类
        current_category: null, // 当前显示的分类的 id
        proceeding: null,       // 进行中的项目(timestamp)
        proceedingId: null,     // 进行中的项目的 id
        timeRange: [0, 0],      // 当前选择的时间范围(timestamp)
    },
    getters: {
        // 根据 id 获取分类名称
        getCategoryById: (state) => (id) => {
            return state.categories[id]
        }
    },
    mutations: {
        // 设置当前分类，0 代表所有分类
        setCategory(state, id) {
            state.current_category = id
        },
        // 设置分类数据集
        setCategories(state, categories) {
            state.categories = categories
        },
        // 设置记录查询时间范围
        setTimeRange(state, times) {
            state.timeRange = times
        },
        // 设置当前记录进行状态， null 代表没有进行中的记录
        setProceeding(state, record) {
            if (record.id == 0) {
                state.proceedingId = null
            } else {
                state.proceedingId = record.id
            }
            state.proceeding = record.start_stamp
        }
    },
    actions: {
        // 从服务器获取所有分类
        fetchCategory({ commit }) {
            api.get("/category").then(
                res => (commit('setCategories', res.data.data))
            )
        },
        // 从服务器获取记录进行状态
        fetchProceeding({ commit }) {
            api.get("/record/proceeding").then(
                res => (commit('setProceeding', res.data.data))
            )
        }
    },
})
