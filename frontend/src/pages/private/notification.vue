<template>
    <div class="flex-1 flex flex-col overflow-hidden bg-gray-50">
      <!-- Top Navigation -->
      <header class="bg-white shadow-sm z-10">
        <div class="flex items-center justify-between px-4 py-3 sm:px-6">
          <!-- Mobile menu button -->
          <button 
            @click="$emit('toggle-sidebar')"
            class="md:hidden text-gray-500 hover:text-gray-600 focus:outline-none"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          
          <!-- Page Title -->
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-800">Notifications</h1>
            <span v-if="unreadCount > 0" class="ml-2 px-2 py-0.5 text-xs rounded-full bg-red-500 text-white">
              {{ unreadCount }} new
            </span>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center space-x-2">
            <button 
              @click="markAllAsRead"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-blue-600 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Mark all as read
            </button>
            <button 
              @click="showNotificationSettings = true"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="-ml-0.5 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Settings
            </button>
          </div>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto">
        <!-- Notification Filters -->
        <div class="bg-white shadow-sm border-b border-gray-200">
          <div class="px-4 sm:px-6">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 py-3">
              <div class="flex space-x-2 overflow-x-auto pb-2 md:pb-0">
                <button 
                  v-for="filter in filters"
                  :key="filter.value"
                  @click="activeFilter = filter.value"
                  class="px-3 py-1 text-sm rounded-md whitespace-nowrap"
                  :class="{
                    'bg-blue-100 text-blue-800': activeFilter === filter.value,
                    'bg-gray-100 text-gray-800 hover:bg-gray-200': activeFilter !== filter.value
                  }"
                >
                  {{ filter.label }}
                  <span v-if="filter.count" class="ml-1 px-1.5 py-0.5 text-xs rounded-full" 
                    :class="{
                      'bg-blue-200 text-blue-800': activeFilter === filter.value,
                      'bg-gray-200 text-gray-800': activeFilter !== filter.value
                    }">
                    {{ filter.count }}
                  </span>
                </button>
              </div>
              
              <div class="flex items-center">
                <label for="sort" class="mr-2 text-sm text-gray-600">Sort by:</label>
                <select 
                  id="sort"
                  v-model="sortBy"
                  class="block w-full pl-3 pr-10 py-1.5 text-sm border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-md"
                >
                  <option value="newest">Newest first</option>
                  <option value="oldest">Oldest first</option>
                  <option value="priority">Priority</option>
                </select>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Notifications List -->
        <div class="divide-y divide-gray-200">
          <div v-for="notification in filteredNotifications" :key="notification.id" 
            class="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors duration-150"
            :class="{
              'bg-blue-50': notification.unread,
              'border-l-4 border-blue-500': notification.unread && notification.priority === 'high',
              'border-l-4 border-yellow-500': notification.unread && notification.priority === 'medium',
              'border-l-4 border-gray-300': notification.unread && notification.priority === 'low'
            }">
            <div class="flex items-start">
              <!-- Notification Icon -->
              <div class="flex-shrink-0 pt-1">
                <div class="h-8 w-8 rounded-full flex items-center justify-center"
                  :class="{
                    'bg-red-100 text-red-600': notification.type === 'alert',
                    'bg-blue-100 text-blue-600': notification.type === 'system',
                    'bg-green-100 text-green-600': notification.type === 'success',
                    'bg-yellow-100 text-yellow-600': notification.type === 'warning'
                  }">
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="notification.type === 'alert'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    <path v-if="notification.type === 'system'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path v-if="notification.type === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    <path v-if="notification.type === 'warning'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
              </div>
              
              <!-- Notification Content -->
              <div class="ml-3 flex-1 min-w-0">
                <div class="flex justify-between">
                  <p class="text-sm font-medium text-gray-900">
                    {{ notification.title }}
                    <span v-if="notification.unread" class="ml-1 inline-block h-2 w-2 rounded-full bg-blue-500"></span>
                  </p>
                  <div class="text-xs text-gray-500">
                    {{ formatTime(notification.timestamp) }}
                  </div>
                </div>
                <p class="text-sm text-gray-600 mt-1">
                  {{ notification.message }}
                </p>
                
                <!-- Notification Actions -->
                <div class="mt-2 flex space-x-3">
                  <button 
                    v-if="notification.unread"
                    @click="markAsRead(notification)"
                    class="text-xs text-blue-600 hover:text-blue-800"
                  >
                    Mark as read
                  </button>
                  <button 
                    v-if="notification.action"
                    @click="handleAction(notification)"
                    class="text-xs px-2 py-1 rounded border border-gray-300 text-gray-600 hover:bg-gray-100"
                  >
                    {{ notification.action.label }}
                  </button>
                  <button 
                    @click="dismissNotification(notification)"
                    class="text-xs text-gray-500 hover:text-gray-700 ml-auto"
                  >
                    Dismiss
                  </button>
                </div>
                
                <!-- Additional Context -->
                <div v-if="notification.context" class="mt-2 text-xs text-gray-500">
                  <span v-if="notification.context.tank">Tank #{{ notification.context.tank }}</span>
                  <span v-if="notification.context.sensor" class="ml-2">Sensor: {{ notification.context.sensor }}</span>
                  <span v-if="notification.context.value" class="ml-2">Value: {{ notification.context.value }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" class="px-4 py-12 sm:px-6 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No notifications</h3>
            <p class="mt-1 text-sm text-gray-500">
              {{ activeFilter === 'all' ? "You're all caught up!" : `No ${activeFilter} notifications` }}
            </p>
            <div class="mt-6">
              <button 
                @click="activeFilter = 'all'"
                type="button"
                class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                View all notifications
              </button>
            </div>
          </div>
        </div>
      </main>
  
      <!-- Notification Settings Modal -->
      <div v-if="showNotificationSettings" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Notification Settings</h3>
          </div>
          <div class="p-6">
            <div class="space-y-6">
              <!-- Notification Preferences -->
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-3">Notification Preferences</h4>
                <div class="space-y-4">
                  <div class="flex items-start">
                    <div class="flex items-center h-5">
                      <input 
                        id="email-notifications" 
                        v-model="settings.emailEnabled" 
                        type="checkbox" 
                        class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                      >
                    </div>
                    <div class="ml-3 text-sm">
                      <label for="email-notifications" class="font-medium text-gray-700">Email Notifications</label>
                      <p class="text-gray-500">Receive notifications via email</p>
                    </div>
                  </div>
                  
                  <div class="flex items-start">
                    <div class="flex items-center h-5">
                      <input 
                        id="push-notifications" 
                        v-model="settings.pushEnabled" 
                        type="checkbox" 
                        class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                      >
                    </div>
                    <div class="ml-3 text-sm">
                      <label for="push-notifications" class="font-medium text-gray-700">Push Notifications</label>
                      <p class="text-gray-500">Receive notifications on your devices</p>
                    </div>
                  </div>
                  
                  <div class="flex items-start">
                    <div class="flex items-center h-5">
                      <input 
                        id="sms-notifications" 
                        v-model="settings.smsEnabled" 
                        type="checkbox" 
                        class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded"
                      >
                    </div>
                    <div class="ml-3 text-sm">
                      <label for="sms-notifications" class="font-medium text-gray-700">SMS Notifications</label>
                      <p class="text-gray-500">Receive critical alerts via text message</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Alert Thresholds -->
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-3">Alert Thresholds</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label for="critical-alerts" class="block text-sm font-medium text-gray-700 mb-1">Critical Alerts</label>
                    <select 
                      id="critical-alerts" 
                      v-model="settings.criticalAlerts" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="all">All critical alerts</option>
                      <option value="system">System alerts only</option>
                      <option value="none">None</option>
                    </select>
                  </div>
                  <div>
                    <label for="warning-alerts" class="block text-sm font-medium text-gray-700 mb-1">Warning Alerts</label>
                    <select 
                      id="warning-alerts" 
                      v-model="settings.warningAlerts" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="all">All warnings</option>
                      <option value="important">Important only</option>
                      <option value="none">None</option>
                    </select>
                  </div>
                  <div>
                    <label for="info-alerts" class="block text-sm font-medium text-gray-700 mb-1">Info Alerts</label>
                    <select 
                      id="info-alerts" 
                      v-model="settings.infoAlerts" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="important">Important only</option>
                      <option value="none">None</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <!-- Quiet Hours -->
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-3">Quiet Hours</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label for="quiet-start" class="block text-sm font-medium text-gray-700 mb-1">Start Time</label>
                    <select 
                      id="quiet-start" 
                      v-model="settings.quietStart" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option v-for="hour in hours" :key="'start-'+hour.value" :value="hour.value">
                        {{ hour.label }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label for="quiet-end" class="block text-sm font-medium text-gray-700 mb-1">End Time</label>
                    <select 
                      id="quiet-end" 
                      v-model="settings.quietEnd" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option v-for="hour in hours" :key="'end-'+hour.value" :value="hour.value">
                        {{ hour.label }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
            <button 
              @click="showNotificationSettings = false"
              class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button 
              @click="saveNotificationSettings"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotificationsView',
    emits: ['toggle-sidebar'],
    data() {
      return {
        activeFilter: 'unread',
        sortBy: 'newest',
        showNotificationSettings: false,
        hours: [
          { value: 22, label: '10:00 PM' },
          { value: 23, label: '11:00 PM' },
          { value: 0, label: '12:00 AM' },
          { value: 1, label: '1:00 AM' },
          { value: 2, label: '2:00 AM' },
          { value: 3, label: '3:00 AM' },
          { value: 4, label: '4:00 AM' },
          { value: 5, label: '5:00 AM' },
          { value: 6, label: '6:00 AM' }
        ],
        filters: [
          { value: 'all', label: 'All', count: null },
          { value: 'unread', label: 'Unread', count: null },
          { value: 'alerts', label: 'Alerts', count: null },
          { value: 'system', label: 'System', count: null },
          { value: 'tanks', label: 'Tanks', count: null }
        ],
        settings: {
          emailEnabled: true,
          pushEnabled: true,
          smsEnabled: false,
          criticalAlerts: 'all',
          warningAlerts: 'all',
          infoAlerts: 'important',
          quietStart: 22,
          quietEnd: 6
        },
        notifications: [
          {
            id: 1,
            title: 'Low gas level detected',
            message: 'Tank #3 has reached 15% capacity. Consider scheduling a refill soon.',
            type: 'alert',
            priority: 'high',
            unread: true,
            timestamp: '2023-06-15T14:32:00',
            context: {
              tank: 3,
              sensor: 'Level Sensor',
              value: '15%'
            },
            action: {
              label: 'Schedule Refill',
              callback: () => console.log('Schedule refill for tank 3')
            }
          },
          {
            id: 2,
            title: 'System update available',
            message: 'A new version (v2.1.3) of GasTrack Pro is available for installation.',
            type: 'system',
            priority: 'medium',
            unread: true,
            timestamp: '2023-06-15T10:15:00',
            action: {
              label: 'View Details',
              callback: () => console.log('View update details')
            }
          },
          {
            id: 3,
            title: 'Pressure warning',
            message: 'Tank #1 pressure is above normal threshold (165 psi).',
            type: 'warning',
            priority: 'high',
            unread: false,
            timestamp: '2023-06-14T18:45:00',
            context: {
              tank: 1,
              sensor: 'Pressure Sensor',
              value: '165 psi'
            }
          },
          {
            id: 4,
            title: 'Temperature normal',
            message: 'Tank #2 temperature has returned to normal range (22°C).',
            type: 'success',
            priority: 'low',
            unread: false,
            timestamp: '2023-06-14T12:30:00',
            context: {
              tank: 2,
              sensor: 'Temp Sensor',
              value: '22°C'
            }
          },
          {
            id: 5,
            title: 'New user added',
            message: 'Michael Brown has been added to your organization with Viewer access.',
            type: 'system',
            priority: 'low',
            unread: false,
            timestamp: '2023-06-13T09:10:00'
          },
          {
            id: 6,
            title: 'Critical gas level',
            message: 'Tank #4 has reached 8% capacity. Immediate refill required!',
            type: 'alert',
            priority: 'high',
            unread: true,
            timestamp: '2023-06-15T16:20:00',
            context: {
              tank: 4,
              sensor: 'Level Sensor',
              value: '8%'
            },
            action: {
              label: 'Emergency Refill',
              callback: () => console.log('Emergency refill for tank 4')
            }
          }
        ]
      }
    },
    computed: {
      filteredNotifications() {
        let filtered = [...this.notifications];
        
        // Apply filter
        switch (this.activeFilter) {
          case 'unread':
            filtered = filtered.filter(n => n.unread);
            break;
          case 'alerts':
            filtered = filtered.filter(n => n.type === 'alert');
            break;
          case 'system':
            filtered = filtered.filter(n => n.type === 'system');
            break;
          case 'tanks':
            filtered = filtered.filter(n => n.context && n.context.tank);
            break;
          // 'all' shows everything
        }
        
        // Apply sorting
        switch (this.sortBy) {
          case 'newest':
            filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            break;
          case 'oldest':
            filtered.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            break;
          case 'priority':
            const priorityOrder = { 'high': 1, 'medium': 2, 'low': 3 };
            filtered.sort((a, b) => {
              if (priorityOrder[a.priority] === priorityOrder[b.priority]) {
                return new Date(b.timestamp) - new Date(a.timestamp);
              }
              return priorityOrder[a.priority] - priorityOrder[b.priority];
            });
            break;
        }
        
        return filtered;
      },
      unreadCount() {
        return this.notifications.filter(n => n.unread).length;
      }
    },
    created() {
      // Update filter counts
      this.updateFilterCounts();
    },
    methods: {
      formatTime(timestamp) {
        const now = new Date();
        const date = new Date(timestamp);
        const diffHours = Math.floor((now - date) / (1000 * 60 * 60));
        
        if (diffHours < 1) {
          const diffMinutes = Math.floor((now - date) / (1000 * 60));
          return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''} ago`;
        }
        if (diffHours < 24) {
          return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
        }
        
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      },
      markAsRead(notification) {
        notification.unread = false;
        this.updateFilterCounts();
      },
      markAllAsRead() {
        this.notifications.forEach(n => n.unread = false);
        this.updateFilterCounts();
      },
      dismissNotification(notification) {
        const index = this.notifications.findIndex(n => n.id === notification.id);
        if (index !== -1) {
          this.notifications.splice(index, 1);
        }
        this.updateFilterCounts();
      },
      handleAction(notification) {
        if (notification.action && notification.action.callback) {
          notification.action.callback();
        }
        if (notification.unread) {
          this.markAsRead(notification);
        }
      },
      updateFilterCounts() {
        this.filters = this.filters.map(filter => {
          let count;
          switch (filter.value) {
            case 'unread':
              count = this.notifications.filter(n => n.unread).length;
              break;
            case 'alerts':
              count = this.notifications.filter(n => n.type === 'alert').length;
              break;
            case 'system':
              count = this.notifications.filter(n => n.type === 'system').length;
              break;
            case 'tanks':
              count = this.notifications.filter(n => n.context && n.context.tank).length;
              break;
            default:
              count = null;
          }
          return { ...filter, count };
        });
      },
      saveNotificationSettings() {
        // In a real app, this would save to your backend
        console.log('Notification settings saved:', this.settings);
        this.showNotificationSettings = false;
      }
    }
  }
  </script>
  
  <style scoped>
  /* Custom scrollbar for main content */
  main::-webkit-scrollbar {
    width: 8px;
  }
  main::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
  }
  main::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }
  main::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.2);
  }
  
  /* Modal transitions */
  .modal-enter-active, .modal-leave-active {
    transition: opacity 0.3s ease;
  }
  .modal-enter, .modal-leave-to {
    opacity: 0;
  }
  
  /* Notification priority indicators */
  .border-l-4 {
    transition: border-color 0.2s ease;
  }
  
  /* Button transitions */
  button {
    transition: all 0.2s ease;
  }
  </style>