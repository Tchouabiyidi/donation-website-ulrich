<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Donation Tracking</h1>
      <p class="text-gray-400">Search, filter, and inspect donation records</p>
    </div>

    <!-- Filters -->
    <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4 mb-4 grid grid-cols-1 md:grid-cols-6 gap-3">
      <input v-model="query" type="text" placeholder="Search donor, campaign, or ref" class="md:col-span-2 bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm placeholder-gray-500" />
      <input v-model="from" type="date" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
      <input v-model="to" type="date" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
      <select v-model="status" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="all">All Statuses</option>
        <option value="completed">Completed</option>
        <option value="pending">Pending</option>
        <option value="refunded">Refunded</option>
        <option value="failed">Failed</option>
      </select>
      <select v-model="method" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="all">All Methods</option>
        <option value="card">Card</option>
        <option value="bank">Bank</option>
        <option value="wallet">Wallet</option>
        <option value="crypto">Crypto</option>
      </select>
    </div>

    <!-- Table and Detail -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <div class="xl:col-span-2 bg-gray-900/60 border border-gray-800 rounded-lg overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-900/60 text-gray-300">
            <tr>
              <th class="text-left px-4 py-2">Donor</th>
              <th class="text-left px-4 py-2">Campaign</th>
              <th class="text-right px-4 py-2">Amount</th>
              <th class="text-right px-4 py-2">Date</th>
              <th class="text-center px-4 py-2">Method</th>
              <th class="text-center px-4 py-2">Status</th>
              <th class="text-right px-4 py-2">Ref</th>
              <th class="text-right px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in paged" :key="d.id" class="border-t border-gray-800 hover:bg-gray-800/40">
              <td class="px-4 py-2">
                <div class="font-medium">{{ d.donor }}</div>
                <div class="text-xs text-gray-400">{{ d.email }}</div>
              </td>
              <td class="px-4 py-2">{{ d.campaign }}</td>
              <td class="px-4 py-2 text-right">${{ d.amount.toFixed(2) }}</td>
              <td class="px-4 py-2 text-right">{{ formatDate(d.date) }}</td>
              <td class="px-4 py-2 text-center">
                <span class="px-2 py-1 rounded text-xs border" :class="methodClass(d.method)">{{ d.method }}</span>
              </td>
              <td class="px-4 py-2 text-center">
                <span class="px-2 py-1 rounded text-xs border" :class="statusClass(d.status)">{{ d.status }}</span>
              </td>
              <td class="px-4 py-2 text-right">{{ d.reference }}</td>
              <td class="px-4 py-2 text-right">
                <button @click="select(d)" class="text-xs px-2 py-1 border border-gray-700 rounded hover:bg-gray-800/60">Details</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Detail Panel -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4" v-if="selected">
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-semibold">Donation Details</h2>
          <button @click="selected=null" class="text-gray-400 hover:text-white">✕</button>
        </div>
        <div class="text-sm space-y-2">
          <div class="flex justify-between"><span class="text-gray-400">Reference</span><span class="font-mono">{{ selected.reference }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Donor</span><span>{{ selected.donor }} • {{ selected.email }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Campaign</span><span>{{ selected.campaign }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Amount</span><span>${{ selected.amount.toFixed(2) }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Date</span><span>{{ formatDate(selected.date) }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Method</span><span class="px-2 py-0.5 rounded text-xs border" :class="methodClass(selected.method)">{{ selected.method }}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Status</span><span class="px-2 py-0.5 rounded text-xs border" :class="statusClass(selected.status)">{{ selected.status }}</span></div>
        </div>
        <div class="mt-4 flex gap-2">
          <button @click="resendReceipt(selected)" class="px-3 py-2 rounded border border-gray-700 hover:bg-gray-800/60 text-sm">Resend Receipt</button>
          <button v-if="selected.status==='completed'" @click="refund(selected)" class="px-3 py-2 rounded border border-red-700 text-red-300 hover:bg-red-500/10 text-sm">Refund</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between text-sm text-gray-400 mt-4">
      <div>Showing {{ start + 1 }}–{{ Math.min(end, filtered.length) }} of {{ filtered.length }}</div>
      <div class="flex gap-2">
        <button :disabled="page===1" @click="page--" class="px-2 py-1 border border-gray-800 rounded disabled:opacity-40">Prev</button>
        <button :disabled="end>=filtered.length" @click="page++" class="px-2 py-1 border border-gray-800 rounded disabled:opacity-40">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

const data = reactive([
  { id: 1, donor: 'Alice Johnson', email: 'alice@example.com', campaign: 'Clean Water for All', amount: 120.5, date: '2025-08-18', status: 'completed', method: 'card', reference: 'DON-73A9' },
  { id: 2, donor: 'Bob Smith', email: 'bob@example.com', campaign: 'Education First', amount: 75, date: '2025-08-18', status: 'completed', method: 'bank', reference: 'DON-019B' },
  { id: 3, donor: 'Cynthia Ray', email: 'cynthia@example.com', campaign: 'Relief Fund', amount: 300, date: '2025-08-17', status: 'pending', method: 'card', reference: 'DON-88KF' },
  { id: 4, donor: 'David Kim', email: 'david@example.com', campaign: 'Tree Planting', amount: 45, date: '2025-08-16', status: 'refunded', method: 'wallet', reference: 'DON-55MD' },
  { id: 5, donor: 'Emma Stone', email: 'emma@example.com', campaign: 'Clean Water for All', amount: 220, date: '2025-08-15', status: 'failed', method: 'crypto', reference: 'DON-234Z' },
  { id: 6, donor: 'Fred Moore', email: 'fred@example.com', campaign: 'Scholarship Drive', amount: 130, date: '2025-08-14', status: 'completed', method: 'card', reference: 'DON-77QQ' },
])

const query = ref('')
const from = ref('')
const to = ref('')
const status = ref('all')
const method = ref('all')
const selected = ref(null)

const filtered = computed(() => {
  let arr = data.filter(d => {
    const q = query.value.toLowerCase()
    const inText = !q || d.donor.toLowerCase().includes(q) || d.campaign.toLowerCase().includes(q) || d.reference.toLowerCase().includes(q)
    const inStatus = status.value === 'all' || d.status === status.value
    const inMethod = method.value === 'all' || d.method === method.value
    const date = new Date(d.date)
    const after = !from.value || date >= new Date(from.value)
    const before = !to.value || date <= new Date(to.value)
    return inText && inStatus && inMethod && after && before
  })
  arr.sort((a,b) => new Date(b.date) - new Date(a.date))
  return arr
})

const page = ref(1)
const pageSize = ref(8)
const start = computed(() => (page.value - 1) * pageSize.value)
const end = computed(() => page.value * pageSize.value)
const paged = computed(() => filtered.value.slice(start.value, end.value))

function select(d) { selected.value = d }

function methodClass(m) {
  if (m === 'card') return 'bg-blue-500/10 text-blue-300 border-blue-500/30'
  if (m === 'bank') return 'bg-purple-500/10 text-purple-300 border-purple-500/30'
  if (m === 'wallet') return 'bg-green-500/10 text-green-300 border-green-500/30'
  return 'bg-yellow-500/10 text-yellow-300 border-yellow-500/30'
}

function statusClass(s) {
  if (s === 'completed') return 'bg-green-500/10 text-green-400 border-green-500/30'
  if (s === 'pending') return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30'
  if (s === 'refunded') return 'bg-blue-500/10 text-blue-400 border-blue-500/30'
  return 'bg-red-500/10 text-red-400 border-red-500/30'
}

function formatDate(d) { return new Date(d).toLocaleDateString() }

function resendReceipt(d) { alert(`Resent receipt to ${d.email} (stub)`) }
function refund(d) { alert(`Refund initiated for ${d.reference} (stub)`) }
</script>

<style scoped>
</style>