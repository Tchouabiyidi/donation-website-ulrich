import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/user'
import DefaultLayout from '../layouts/Defaultlayout.vue';
import PublicLayout from '../layouts/PublicLayout.vue';

import donate from '../pages/private/donate.vue';
import history from '../pages/private/history.vue';
import notification from '../pages/private/notification.vue';
import search_campaign from '../pages/private/search_campaign.vue'; // Assuming the file is actually spelled Analitics.vue
import systemsetting from '../pages/private/Systemsetting.vue';
import usermanagmment from '../pages/private/Usermanagment.vue';
import CampaignCreate from '../pages/private/CampaignCreate.vue';
import CampaignManage from '../pages/private/CampaignManage.vue';
import DonationTrack from '../pages/private/DonationTrack.vue';
import NotificationManage from '../pages/private/NotificationManage.vue';
import ReportGenerate from '../pages/private/ReportGenerate.vue';
import AdminAccounts from '../pages/private/AdminAccounts.vue';
import AdminCampaignVerify from '../pages/private/AdminCampaignVerify.vue';
import AdminStatistics from '../pages/private/AdminStatistics.vue';
import about from '../pages/public/About.vue';
import contact from "../pages/public/Contact.vue";

import landing from '../pages/public/Landing.vue';
import login from '../pages/public/Login.vue';
import signup from '../pages/public/signup.vue';
import impact from "../pages/public/story.vue";
const routes = [
  {
    path: '/admin',
    component: DefaultLayout,
    children: [
      {
        path: '',
        redirect: 'campaigns/search',
      },
     
      {
        path: 'campaigns/search',
        name: 'search',
        component: search_campaign,
        meta: { roles: ['donor', 'campaign_manager', 'superadmin'] },
      },
      // Donor
      {
        path: 'donate',
        name: 'donate',
        component: donate,
        meta: { roles: ['donor', 'campaign_manager', 'superadmin'] },
      },
      {
        path:'donations/history',
        name:'history',
        component:history,
        meta: { roles: ['donor', 'campaign_manager', 'superadmin'] },
      },
      // Campaign Organizer
      {
        path: 'campaigns/create',
        name: 'campaign-create',
        component: CampaignCreate,
        meta: { roles: ['campaign_manager', 'superadmin'] },
      },
      {
        path: 'campaigns/manage',
        name: 'campaign-manage',
        component: CampaignManage,
        meta: { roles: ['campaign_manager', 'superadmin'] },
      },
      {
        path: 'donations/track',
        name: 'donation-track',
        component: DonationTrack,
        meta: { roles: ['campaign_manager', 'superadmin'] },
      },
      {
        path: 'notifications/manage',
        name: 'notifications-manage',
        component: NotificationManage,
        meta: { roles: ['campaign_manager', 'superadmin'] },
      },
      {
        path: 'reports/generate',
        name: 'reports-generate',
        component: ReportGenerate,
        meta: { roles: ['campaign_manager', 'superadmin'] },
      },
      // Admin
      {
        path: 'accounts',
        name: 'admin-accounts',
        component: AdminAccounts,
        meta: { roles: ['superadmin'] },
      },
      {
        path: 'campaigns/verify',
        name: 'admin-campaign-verify',
        component: AdminCampaignVerify,
        meta: { roles: ['superadmin'] },
      },
      {
        path: 'statistics',
        name: 'admin-statistics',
        component: AdminStatistics,
        meta: { roles: ['superadmin'] },
      },
      {
        path: 'settings',
        name: 'Setting',
        component: systemsetting,
        meta: { roles: ['superadmin'] },
      },
      {
        path: 'users',
        name: 'users',
        component: usermanagmment,
        meta: { roles: ['superadmin'] },
      },
      {
        path: 'notifications',
        name: 'alerts',
        component: notification,
        meta: { roles: ['donor', 'campaign_manager', 'superadmin'] },
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
        path:'/signup',
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
        path:"/impact",
        name:"impact",
        component: impact,
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

// Role home helper
function roleHome(role) {
  if (role === 'superadmin') return { path: '/admin/accounts' };
  if (role === 'campaign_manager') return { path: '/admin/campaigns/manage' };
  // donor and default
  return { path: '/admin/campaigns/search' };
}

// Global navigation guard for auth + role-based access
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthed = !!userStore.token || !!userStore.user;

  // If trying to access admin area
  if (to.path.startsWith('/admin')) {
    if (!isAuthed) {
      return next({ name: 'login', query: { redirect: to.fullPath } });
    }
    const role = userStore.user?.role;
    // Check role permissions defined in route meta
    const allowed = to.matched.some(r => !r.meta?.roles || r.meta.roles.includes(role));
    if (!allowed) {
      return next(roleHome(role));
    }
  }

  // Prevent logged-in users from visiting login/signup
  if ((to.name === 'login' || to.name === 'signup') && isAuthed) {
    return next(roleHome(userStore.user?.role));
  }

  next();
});

export default router;
