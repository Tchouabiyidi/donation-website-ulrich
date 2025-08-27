<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold">Admin Statistics</h1>
        <p class="text-gray-400">Platform-wide analytics and insights</p>
      </div>
      <div class="flex gap-3">
        <select v-model="filters.range" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="ytd">Year to date</option>
        </select>
        <select v-model="filters.groupBy" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
          <option value="day">Group: Day</option>
          <option value="week">Group: Week</option>
          <option value="month">Group: Month</option>
        </select>
        <button @click="refresh()" class="px-3 py-2 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-600/30 hover:bg-yellow-500/20 text-sm">Refresh</button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="text-gray-400 text-xs">Total Donations</div>
        <div class="text-2xl font-semibold mt-1">XAF {{ kpis.totalDonations.toLocaleString() }}</div>
        <div class="text-xs mt-2" :class="kpis.trendDonations >= 0 ? 'text-green-400' : 'text-red-400'">
          {{ kpis.trendDonations >= 0 ? '+' : '' }}{{ kpis.trendDonations.toFixed(1) }}% vs prev
        </div>
      </div>
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="text-gray-400 text-xs">Active Campaigns</div>
        <div class="text-2xl font-semibold mt-1">{{ kpis.activeCampaigns }}</div>
        <div class="text-xs mt-2" :class="kpis.trendCampaigns >= 0 ? 'text-green-400' : 'text-red-400'">
          {{ kpis.trendCampaigns >= 0 ? '+' : '' }}{{ kpis.trendCampaigns.toFixed(1) }}% vs prev
        </div>
      </div>
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="text-gray-400 text-xs">Avg. Donation</div>
        <div class="text-2xl font-semibold mt-1">XAF {{ Math.round(kpis.avgDonation).toLocaleString() }}</div>
        <div class="text-xs mt-2 text-gray-400">{{ kpis.totalDonationsCount }} donations</div>
      </div>
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="text-gray-400 text-xs">New Users</div>
        <div class="text-2xl font-semibold mt-1">{{ kpis.newUsers }}</div>
        <div class="text-xs mt-2" :class="kpis.trendUsers >= 0 ? 'text-green-400' : 'text-red-400'">
          {{ kpis.trendUsers >= 0 ? '+' : '' }}{{ kpis.trendUsers.toFixed(1) }}% vs prev
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- Mock Line Chart -->
      <div class="xl:col-span-2 bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold">Donations Over Time</h2>
          <div class="text-gray-400 text-xs">Mock chart</div>
        </div>
        <div class="h-56 bg-gradient-to-b from-gray-800/60 to-gray-900/40 rounded flex items-end gap-1 p-3">
          <div v-for="(v, idx) in series" :key="idx" class="bg-yellow-500/60 hover:bg-yellow-400/70 transition-colors rounded-t" :style="{ height: v + 'px', width: barWidth }" />
        </div>
      </div>

      <!-- Top Campaigns -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold">Top Campaigns</h2>
          <button @click="shuffle()" class="text-xs text-gray-400 hover:text-yellow-400">Shuffle</button>
        </div>
        <ul class="space-y-3">
          <li v-for="c in topCampaigns" :key="c.id" class="flex items-center justify-between">
            <div>
              <div class="font-medium">{{ c.name }}</div>
              <div class="text-xs text-gray-400">{{ c.category }}</div>
            </div>
            <div class="text-right">
              <div class="font-semibold">XAF {{ c.raised.toLocaleString() }}</div>
              <div class="text-xs text-gray-400">{{ Math.round((c.raised / c.goal) * 100) }}% of XAF {{ c.goal.toLocaleString() }}</div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Recent Donations Table -->
    <div class="mt-6 bg-gray-900/60 border border-gray-800 rounded-lg">
      <div class="p-4 border-b border-gray-800 flex items-center justify-between">
        <h2 class="font-semibold">Recent Donations</h2>
        <div class="text-xs text-gray-400">Showing {{ donations.length }} items</div>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-900/60 text-gray-300">
            <tr>
              <th class="text-left px-4 py-2">Donor</th>
              <th class="text-left px-4 py-2">Campaign</th>
              <th class="text-right px-4 py-2">Amount</th>
              <th class="text-right px-4 py-2">Date</th>
              <th class="text-center px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in donations" :key="d.id" class="border-t border-gray-800 hover:bg-gray-800/40">
              <td class="px-4 py-2">{{ d.donor }}</td>
              <td class="px-4 py-2">{{ d.campaign }}</td>
              <td class="px-4 py-2 text-right">XAF {{ Math.round(d.amount).toLocaleString() }}</td>
              <td class="px-4 py-2 text-right">{{ formatDate(d.date) }}</td>
              <td class="px-4 py-2 text-center">
                <span :class="statusClass(d.status)" class="px-2 py-1 rounded text-xs border">{{ d.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'

const filters = reactive({ range: '30d', groupBy: 'week' })

const kpis = reactive({
  totalDonations: 128450,
  totalDonationsCount: 2340,
  activeCampaigns: 42,
  avgDonation: 54.86,
  newUsers: 312,
  trendDonations: 8.4,
  trendCampaigns: 2.1,
  trendUsers: -1.7,
})

// Mock series heights for a bar chart
const series = computed(() => {
  const base = filters.groupBy === 'day' ? 24 : filters.groupBy === 'week' ? 12 : 8
  const arr = Array.from({ length: base }, (_, i) => 20 + Math.round(Math.abs(Math.sin(i + seed())) * 120))
  return arr
})
const barWidth = computed(() => `${Math.max(6, Math.floor(600 / series.value.length))}px`)

function seed() {
  // simple pseudo randomness based on range
  return filters.range === '7d' ? 1 : filters.range === '30d' ? 2 : filters.range === '90d' ? 3 : 4
}

const topCampaigns = reactive([
  { id: 1, name: 'Clean Water for All', category: 'Health', goal: 50000, raised: 38420 },
  { id: 2, name: 'Education First', category: 'Education', goal: 80000, raised: 64210 },
  { id: 3, name: 'Relief Fund', category: 'Emergency', goal: 60000, raised: 59000 },
  { id: 4, name: 'Tree Planting', category: 'Environment', goal: 30000, raised: 21230 },
])

const donations = reactive([
  { id: 1, donor: 'Alice Johnson', campaign: 'Clean Water for All', amount: 120.5, date: '2025-08-18', status: 'completed' },
  { id: 2, donor: 'Bob Smith', campaign: 'Education First', amount: 75, date: '2025-08-18', status: 'completed' },
  { id: 3, donor: 'Cynthia Ray', campaign: 'Relief Fund', amount: 300, date: '2025-08-17', status: 'pending' },
  { id: 4, donor: 'David Kim', campaign: 'Tree Planting', amount: 45, date: '2025-08-16', status: 'refunded' },
  { id: 5, donor: 'Emma Stone', campaign: 'Clean Water for All', amount: 220, date: '2025-08-15', status: 'completed' },
])

function statusClass(s) {
  if (s === 'completed') return 'bg-green-500/10 text-green-400 border-green-500/30'
  if (s === 'pending') return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30'
  return 'bg-red-500/10 text-red-400 border-red-500/30'
}

function formatDate(d) {
  const dt = new Date(d)
  return dt.toLocaleDateString()
}

function refresh() {
  // Stub: in real app, fetch KPIs and series by filters
  console.log('Refresh analytics with', { ...filters })
}

function shuffle() {
  topCampaigns.sort(() => Math.random() - 0.5)
}
</script>

<style scoped>
</style>
