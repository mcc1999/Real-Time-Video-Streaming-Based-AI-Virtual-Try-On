import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        humanImageName:'',
        clothObjectKey:'',
        liveInfo: {},
    },
    mutations: {
        humanImageNameChange(state, newName){
            state.humanImageName = newName
        },
        changeClothObjectKey(state, newKey){
            state.clothObjectKey = newKey
        },
        changeLiveInfo(state, newLiveInfo){
            state.liveInfo = Object.assign(newLiveInfo)
        }
    },
    actions: {
    },
    modules: {
    }
})
