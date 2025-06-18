import { createRouter, createWebHistory } from 'vue-router';
import DefaultLayout from '../layouts/Defaultlayout.vue';
import Dashboard from '../pages/private/dashboard.vue';
import GasTank from '../pages/private/GasTank.vue';
import usermanagmment from '../pages/private/Usermanagment.vue'
import Analytics from '../pages/private/Analitics.vue'; // Assuming the file is actually spelled Analitics.vue
import systemsetting from '../pages/private/Systemsetting.vue'
import notification from '../pages/private/notification.vue'
import PublicLayout from '../layouts/PublicLayout.vue';
import landing from '../pages/public/Landing.vue'
import about from '../pages/public/About.vue' 
import signup from '../pages/public/signup.vue'
import login from '../pages/public/Login.vue'
import contact from "../pages/public/Contact.vue"
import  Features  from '../pages/public/Features.vue';
import pricing from "../pages/public/Pricing.vue"
const routes = [
  {
    path: '/admin',
    component: DefaultLayout,
    children: [
      {
        path: '', // Default child route
        name: 'dashboard',
        component: Dashboard,
      },
      {
        path: 'analytics',
        name: 'analytics',
        component: Analytics,
      },
      {
        path: 'tanks',
        name: 'tanks',
        component: GasTank,
      },
      {
        path: 'settings',
        name: 'Setting',
        component: systemsetting,
      },
      {
        path: '/users',
        name: '/users',
        component: usermanagmment,
      },
      {
        path: '/alerts',
        name: '/alerts',
        component: notification
      },
    ],
  },
  {
    path:"/",
    component:PublicLayout ,
    children:[
      {
        path: '',
        name: 'landing',
        component: landing
      },
      {
        path:'/about',
        name: '/about',
        component: about,
      },
      {
        path:'/register',
        name: 'signup',
        component: signup,
      },
      {
        path:'/login',
        name: 'login',
        component:login,
      },
      {
        path:"/contact",
        name:"contact",
        component: contact,
      },
      {
        path:"/features",
        name:"features",
        component: Features,
      },
      {
        path:"/pricing",
        name:"pricing",
        component: pricing,
      },
    ],
  },


];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
