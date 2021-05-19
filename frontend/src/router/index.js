import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(VueRouter)
Vue.use(ElementUI)

import login from '../views/login'
import register from '../views/register'
import userCenter from "../views/userCenter";
import watchLive from "../views/watchLive";
import fittingRoom from "../views/fittingRoom";
import live from "../views/live";
import test from "../views/test";
import fa from "element-ui/src/locale/lang/fa";

const routes = [
    {
        path: '/login',
        name: 'login',
        component: login,
        beforeEnter (to, from, next){
            if(from.path === "/register" ||from.path === "/" ) next()
            else next(false)
        }
    },
    {
        path: '/register',
        name: 'register',
        component: register,
        beforeEnter (to, from, next){
            if(from.path === "/login" ||from.path === "/") next()
            else next(false)
        }
    },
    {
        path: '/userCenter',
        name: "userCenter",
        component: userCenter,
        props: true
    },
    {
        path: '/watchLive',
        name: 'watchLive',
        component: watchLive,
    },
    {
        path: '/fittingRoom',
        name: 'fittingRoom',
        component: fittingRoom,
    },
    {
        path: '/live',
        name: 'live',
        component: live,
    },
    {
        path: '/test',
        name: 'test',
        component: test,
    }
]

const router =new VueRouter({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes
})

export default router