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
          
          <!-- Dashboard Title -->
          <h1 class="text-xl font-semibold text-gray-800">Home Gas Tank Monitor</h1>
          
          <!-- Last Updated -->
          <div class="text-sm text-gray-500">
            Last updated: {{ formatTime(lastUpdated) }}
            <button @click="refreshData" class="ml-2 text-blue-500 hover:text-blue-700">
              <svg class="h-4 w-4 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </div>
        </div>
      </header>
  
      <!-- Main Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-6">
        <!-- Critical Alert Banner -->
        <div v-if="alert" class="mb-6">
          <div :class="`bg-${alert.type}-50 border-l-4 border-${alert.type}-500 p-4 rounded-r-lg`">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5" :class="`text-${alert.type}-500`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div class="ml-3">
                <h3 :class="`text-sm font-medium text-${alert.type}-800`">{{ alert.title }}</h3>
                <div :class="`mt-2 text-sm text-${alert.type}-700`">
                  {{ alert.message }}
                  <button v-if="alert.action" @click="alert.action.callback" class="ml-2 px-2 py-1 text-xs rounded" :class="`bg-${alert.type}-100 text-${alert.type}-800 hover:bg-${alert.type}-200`">
                    {{ alert.action.text }}
                  </button>
                </div>
              </div>
              <button @click="dismissAlert" class="ml-auto text-gray-400 hover:text-gray-500">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
  
        <!-- Tank Status Overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <!-- Tank Level -->
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">Gas Level</h3>
              <span class="text-xs px-2 py-1 rounded-full" :class="levelStatusClass">{{ levelStatusText }}</span>
            </div>
            <div class="px-6 py-8 text-center">
              <div class="relative h-48 mx-auto" style="max-width: 200px">
                <!-- Tank visualization -->
                <div class="absolute bottom-0 left-0 right-0 bg-gray-200 rounded-t-lg" style="height: 100%">
                  <div 
                    class="absolute bottom-0 left-0 right-0 rounded-t-lg transition-all duration-500"
                    :class="levelColorClass"
                    :style="`height: ${tank.level}%`"
                  ></div>
                </div>
                <!-- Measurement markers -->
                <div class="absolute left-0 right-0 border-t border-gray-300" style="top: 25%"></div>
                <div class="absolute left-0 right-0 border-t border-gray-300" style="top: 50%"></div>
                <div class="absolute left-0 right-0 border-t border-gray-300" style="top: 75%"></div>
                <!-- Current level indicator -->
                <div class="absolute left-0 right-0 text-xs font-medium" 
                     :style="`bottom: ${tank.level}%; margin-bottom: -10px`"
                     :class="levelTextColorClass">
                  {{ tank.level }}%
                </div>
              </div>
              <div class="mt-4">
                <p class="text-3xl font-bold" :class="levelTextColorClass">{{ tank.level }}%</p>
                <p class="text-sm text-gray-500 mt-1">Estimated remaining: {{ estimatedRemaining }}</p>
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
              <button @click="showRefillModal = true" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md text-sm font-medium transition-colors">
                Schedule Refill
              </button>
            </div>
          </div>
  
          <!-- Pressure & Temperature -->
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Pressure & Temperature</h3>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between py-4">
                <div class="flex items-center">
                  <svg class="h-6 w-6 text-blue-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Pressure</p>
                    <p class="text-xl font-semibold" :class="pressureColorClass">{{ tank.pressure }} psi</p>
                    <p class="text-xs text-gray-400">Safe range: {{ safePressureRange.min }}-{{ safePressureRange.max }} psi</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs rounded-full" :class="pressureStatusClass">{{ pressureStatusText }}</span>
              </div>
              
              <div class="flex items-center justify-between py-4 border-t border-gray-100">
                <div class="flex items-center">
                  <svg class="h-6 w-6 text-orange-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Temperature</p>
                    <p class="text-xl font-semibold" :class="tempColorClass">{{ tank.temperature }}°C</p>
                    <p class="text-xs text-gray-400">Safe range: {{ safeTempRange.min }}-{{ safeTempRange.max }}°C</p>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs rounded-full" :class="tempStatusClass">{{ tempStatusText }}</span>
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
              <button @click="showSettingsModal = true" class="text-sm text-blue-600 hover:text-blue-500">
                Adjust Safety Thresholds
              </button>
            </div>
          </div>
  
          <!-- Usage Statistics -->
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Usage Statistics</h3>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div>
                  <p class="text-sm text-gray-500">Daily Usage</p>
                  <p class="text-xl font-semibold">{{ dailyUsage }}% per day</p>
                  <div class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                    <div class="bg-blue-600 h-2.5 rounded-full" :style="`width: ${Math.min(dailyUsage, 100)}%`"></div>
                  </div>
                </div>
                
                <div>
                  <p class="text-sm text-gray-500">Last Refill</p>
                  <p class="text-xl font-semibold">{{ daysSinceRefill }} days ago</p>
                  <p class="text-xs text-gray-400">{{ formatDate(tank.lastRefill) }}</p>
                </div>
                
                <div>
                  <p class="text-sm text-gray-500">Estimated Refill Date</p>
                  <p class="text-xl font-semibold">{{ estimatedRefillDate }}</p>
                  <p class="text-xs" :class="refillUrgencyClass">
                    {{ refillUrgencyText }}
                  </p>
                </div>
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
              <button @click="showUsageHistory = true" class="text-sm text-blue-600 hover:text-blue-500">
                View Detailed Usage History
              </button>
            </div>
          </div>
        </div>
  
        <!-- Consumption Chart -->
        <div class="bg-white shadow rounded-lg p-6 mb-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Consumption (Last 7 Days)</h3>
            <div class="flex space-x-2">
              <button @click="chartRange = 'week'" :class="`px-3 py-1 text-sm rounded-md ${chartRange === 'week' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`">
                Week
              </button>
              <button @click="chartRange = 'month'" :class="`px-3 py-1 text-sm rounded-md ${chartRange === 'month' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`">
                Month
              </button>
              <button @click="chartRange = 'year'" :class="`px-3 py-1 text-sm rounded-md ${chartRange === 'year' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`">
                Year
              </button>
            </div>
          </div>
          <div class="h-64">
            <!-- Chart container - in a real app you'd use a charting library here -->
            <div class="w-full h-full bg-gray-100 rounded flex items-center justify-center text-gray-400">
              <div class="text-center">
                <p class="mb-2">Gas Consumption Chart</p>
                <p class="text-sm">Showing data for last {{ chartRange }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Quick Actions -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button @click="showRefillModal = true" class="p-4 bg-white rounded-lg shadow flex flex-col items-center hover:bg-gray-50 transition-colors">
            <svg class="h-6 w-6 text-blue-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            <span class="text-sm font-medium">Order Refill</span>
          </button>
          <button @click="showTankDetails = true" class="p-4 bg-white rounded-lg shadow flex flex-col items-center hover:bg-gray-50 transition-colors">
            <svg class="h-6 w-6 text-green-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            <span class="text-sm font-medium">Tank Details</span>
          </button>
          <button @click="showAlertsSettings = true" class="p-4 bg-white rounded-lg shadow flex flex-col items-center hover:bg-gray-50 transition-colors">
            <svg class="h-6 w-6 text-yellow-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <span class="text-sm font-medium">Alert Settings</span>
          </button>
          <button @click="showSettingsModal = true" class="p-4 bg-white rounded-lg shadow flex flex-col items-center hover:bg-gray-50 transition-colors">
            <svg class="h-6 w-6 text-purple-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <span class="text-sm font-medium">Settings</span>
          </button>
        </div>
  
        <!-- Refill Modal -->
        <div v-if="showRefillModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Schedule Gas Refill</h3>
            </div>
            <div class="p-6">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Delivery Date</label>
                <input type="date" v-model="refillDate" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Delivery Time</label>
                <select v-model="refillTime" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                  <option>Morning (8am-12pm)</option>
                  <option>Afternoon (12pm-4pm)</option>
                  <option>Evening (4pm-8pm)</option>
                </select>
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Quantity (liters)</label>
                <input type="number" v-model="refillQuantity" min="10" max="100" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button @click="showRefillModal = false" class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Cancel
              </button>
              <button @click="scheduleRefill" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Schedule Refill
              </button>
            </div>
          </div>
        </div>
  
        <!-- Settings Modal -->
        <div v-if="showSettingsModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Safety Thresholds</h3>
            </div>
            <div class="p-6">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Low Level Alert (%)</label>
                <input type="number" v-model="alertThresholds.lowLevel" min="5" max="30" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Critical Level Alert (%)</label>
                <input type="number" v-model="alertThresholds.criticalLevel" min="1" max="15" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Min Pressure (psi)</label>
                <input type="number" v-model="safePressureRange.min" min="50" max="120" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Max Pressure (psi)</label>
                <input type="number" v-model="safePressureRange.max" min="130" max="200" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Min Temperature (°C)</label>
                <input type="number" v-model="safeTempRange.min" min="-10" max="10" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Max Temperature (°C)</label>
                <input type="number" v-model="safeTempRange.max" min="30" max="50" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button @click="showSettingsModal = false" class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Cancel
              </button>
              <button @click="saveSettings" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomeGasTankDashboard',
    emits: ['toggle-sidebar'],
    data() {
      return {
        lastUpdated: new Date(),
        showRefillModal: false,
        showSettingsModal: false,
        showTankDetails: false,
        showUsageHistory: false,
        showAlertsSettings: false,
        chartRange: 'week',
        refillDate: '',
        refillTime: 'Morning (8am-12pm)',
        refillQuantity: 50,
        tank: {
          level: 35,
          pressure: 120,
          temperature: 22,
          lastRefill: '2023-05-10',
          capacity: 100,
          type: 'Propane',
          serialNumber: 'HTK-2023-0425',
          installationDate: '2023-04-25'
        },
        safePressureRange: {
          min: 100,
          max: 150
        },
        safeTempRange: {
          min: 15,
          max: 30
        },
        alertThresholds: {
          lowLevel: 20,
          criticalLevel: 10
        },
        alert: null,
        usageHistory: [
          { date: '2023-06-01', level: 85, usage: 2.5 },
          { date: '2023-06-02', level: 82, usage: 3 },
          // ... more history data
        ]
      };
    },
    created() {
      this.refillDate = this.getNextAvailableDate();
      this.checkForAlerts();
      // Simulate data updates
      this.dataUpdateInterval = setInterval(this.updateTankData, 30000);
    },
    beforeDestroy() {
      clearInterval(this.dataUpdateInterval);
    },
    computed: {
      levelColorClass() {
        if (this.tank.level < this.alertThresholds.criticalLevel) return 'bg-red-500';
        if (this.tank.level < this.alertThresholds.lowLevel) return 'bg-yellow-500';
        return 'bg-green-500';
      },
      levelTextColorClass() {
        if (this.tank.level < this.alertThresholds.criticalLevel) return 'text-red-500';
        if (this.tank.level < this.alertThresholds.lowLevel) return 'text-yellow-500';
        return 'text-green-500';
      },
      levelStatusClass() {
        if (this.tank.level < this.alertThresholds.criticalLevel) return 'bg-red-100 text-red-800';
        if (this.tank.level < this.alertThresholds.lowLevel) return 'bg-yellow-100 text-yellow-800';
        return 'bg-green-100 text-green-800';
      },
      levelStatusText() {
        if (this.tank.level < this.alertThresholds.criticalLevel) return 'CRITICAL';
        if (this.tank.level < this.alertThresholds.lowLevel) return 'LOW';
        return 'NORMAL';
      },
      pressureColorClass() {
        if (this.tank.pressure < this.safePressureRange.min || this.tank.pressure > this.safePressureRange.max) 
          return 'text-red-500';
        return 'text-green-500';
      },
      pressureStatusClass() {
        if (this.tank.pressure < this.safePressureRange.min) return 'bg-red-100 text-red-800';
        if (this.tank.pressure > this.safePressureRange.max) return 'bg-red-100 text-red-800';
        return 'bg-green-100 text-green-800';
      },
      pressureStatusText() {
        if (this.tank.pressure < this.safePressureRange.min) return 'LOW';
        if (this.tank.pressure > this.safePressureRange.max) return 'HIGH';
        return 'NORMAL';
      },
      tempColorClass() {
        if (this.tank.temperature < this.safeTempRange.min || this.tank.temperature > this.safeTempRange.max) 
          return 'text-red-500';
        return 'text-green-500';
      },
      tempStatusClass() {
        if (this.tank.temperature < this.safeTempRange.min) return 'bg-blue-100 text-blue-800';
        if (this.tank.temperature > this.safeTempRange.max) return 'bg-red-100 text-red-800';
        return 'bg-green-100 text-green-800';
      },
      tempStatusText() {
        if (this.tank.temperature < this.safeTempRange.min) return 'COLD';
        if (this.tank.temperature > this.safeTempRange.max) return 'HOT';
        return 'NORMAL';
      },
      dailyUsage() {
        // Calculate average daily usage from history
        if (this.usageHistory.length < 2) return 2.5;
        const totalDays = this.daysSinceRefill;
        if (totalDays === 0) return 0;
        return ((100 - this.tank.level) / totalDays).toFixed(1);
      },
      daysSinceRefill() {
        const diff = new Date() - new Date(this.tank.lastRefill);
        return Math.floor(diff / (1000 * 60 * 60 * 24));
      },
      estimatedRemaining() {
        const days = Math.floor(this.tank.level / this.dailyUsage);
        if (days > 1) return `${days} days`;
        if (days === 1) return '1 day';
        const hours = Math.floor((this.tank.level / this.dailyUsage) * 24);
        return `${hours} hours`;
      },
      estimatedRefillDate() {
        const daysToRefill = Math.floor(this.tank.level / this.dailyUsage);
        const date = new Date();
        date.setDate(date.getDate() + daysToRefill);
        return date.toLocaleDateString();
      },
      refillUrgencyClass() {
        const daysToEmpty = this.tank.level / this.dailyUsage;
        if (daysToEmpty < 3) return 'text-red-500';
        if (daysToEmpty < 7) return 'text-yellow-500';
        return 'text-green-500';
      },
      refillUrgencyText() {
        const daysToEmpty = this.tank.level / this.dailyUsage;
        if (daysToEmpty < 3) return 'Refill urgently needed';
        if (daysToEmpty < 7) return 'Schedule refill soon';
        return 'Adequate supply';
      }
    },
    methods: {
      formatTime(date) {
        return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      },
      formatDate(dateStr) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateStr).toLocaleDateString(undefined, options);
      },
      getNextAvailableDate() {
        const date = new Date();
        date.setDate(date.getDate() + 2); // Assume 2 days lead time for delivery
        return date.toISOString().split('T')[0];
      },
      checkForAlerts() {
        // Clear any existing alert
        this.alert = null;
        
        // Check for critical level
        if (this.tank.level < this.alertThresholds.criticalLevel) {
          this.alert = {
            type: 'red',
            title: 'CRITICAL GAS LEVEL',
            message: `Your gas tank is critically low (${this.tank.level}%). Order an emergency refill immediately.`,
            action: {
              text: 'Order Now',
              callback: () => {
                this.showRefillModal = true;
                this.alert = null;
              }
            }
          };
          return;
        }
        
        // Check for low level
        if (this.tank.level < this.alertThresholds.lowLevel) {
          this.alert = {
            type: 'yellow',
            title: 'LOW GAS LEVEL',
            message: `Your gas tank is getting low (${this.tank.level}%). Consider scheduling a refill soon.`,
            action: {
              text: 'Schedule Refill',
              callback: () => {
                this.showRefillModal = true;
                this.alert = null;
              }
            }
          };
          return;
        }
        
        // Check for pressure issues
        if (this.tank.pressure < this.safePressureRange.min) {
          this.alert = {
            type: 'red',
            title: 'LOW PRESSURE WARNING',
            message: `Tank pressure is below safe threshold (${this.tank.pressure} psi). Check for leaks or contact support.`,
            action: {
              text: 'View Details',
              callback: () => {
                this.showTankDetails = true;
                this.alert = null;
              }
            }
          };
          return;
        }
        
        if (this.tank.pressure > this.safePressureRange.max) {
          this.alert = {
            type: 'red',
            title: 'HIGH PRESSURE WARNING',
            message: `Tank pressure is above safe threshold (${this.tank.pressure} psi). Move to a cooler location and contact support.`,
            action: {
              text: 'View Details',
              callback: () => {
                this.showTankDetails = true;
                this.alert = null;
              }
            }
          };
          return;
        }
        
        // Check for temperature issues
        if (this.tank.temperature > this.safeTempRange.max) {
          this.alert = {
            type: 'red',
            title: 'HIGH TEMPERATURE WARNING',
            message: `Tank temperature is above safe threshold (${this.tank.temperature}°C). Move to a cooler location immediately.`,
            action: {
              text: 'View Details',
              callback: () => {
                this.showTankDetails = true;
                this.alert = null;
              }
            }
          };
        }
      },
      dismissAlert() {
        this.alert = null;
      },
      refreshData() {
        // Simulate data refresh
        this.lastUpdated = new Date();
        this.updateTankData();
      },
      updateTankData() {
        // Simulate small changes in tank data
        const randomChange = (Math.random() - 0.5) * 2; // Between -1 and 1
        
        // Update level (slow decrease)
        this.tank.level = Math.max(0, this.tank.level - (0.1 * Math.random()));
        
        // Update pressure (small fluctuations)
        this.tank.pressure = Math.max(
          80, 
          Math.min(
            170, 
            this.tank.pressure + randomChange
          )
        );
        
        // Update temperature (affected by time of day)
        const hours = new Date().getHours();
        const tempVariation = Math.sin((hours - 12) / 24 * Math.PI) * 5; // -5 to +5 variation
        this.tank.temperature = 22 + tempVariation + (Math.random() - 0.5) * 2;
        
        // Check for new alerts
        this.checkForAlerts();
      },
      scheduleRefill() {
        // In a real app, this would send a request to your backend
        alert(`Refill scheduled for ${this.refillDate} (${this.refillTime}) - ${this.refillQuantity} liters`);
        this.showRefillModal = false;
        
        // Update last refill date (for demo purposes)
        this.tank.lastRefill = new Date().toISOString().split('T')[0];
      },
      saveSettings() {
        // In a real app, this would save to your backend
        this.showSettingsModal = false;
        this.checkForAlerts(); // Re-check alerts with new thresholds
      }
    }
  };
  </script>
  
  <style scoped>
  /* Smooth transitions for dropdowns */
  .dropdown-enter-active, .dropdown-leave-active {
    transition: all 0.2s ease;
  }
  .dropdown-enter, .dropdown-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  
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
  </style>