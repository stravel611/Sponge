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
        itemTableData: [],
        recordTableData: []
    },
    getters: {
        getCategoryById: (state) => (id) => {
            return state.categories[id]
        }
    },
    mutations: {
        setCategory(state, id) {
            state.current_category = id
        },
        setCategories(state, categories) {
            state.categories = categories
        },
        setTimeRange(state, times) {
            state.timeRange = times
        },
        setProceeding(state, record) {
            if (record.id == 0) {
                state.proceedingId = null
            }else {
                state.proceedingId = record.id
            }
            state.proceeding = record.start_stamp
        }
    },
    actions: {
        fetchCategory({ commit }) {
            api.get("/category").then(
                res => (commit('setCategories', res.data.data))
            )
        },
        fetchProceeding({ commit }) {
            api.get("/record/proceeding").then(
                res => (commit('setProceeding', res.data.data))
            )
        }
    },
})
