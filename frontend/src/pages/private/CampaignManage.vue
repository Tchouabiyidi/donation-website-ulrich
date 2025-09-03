<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold">Manage Campaigns</h1>
        <p class="text-gray-400">Search, filter, and manage all campaigns</p>
      </div>
      <router-link to="/admin/campaigns/create" class="px-3 py-2 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-600/30 hover:bg-yellow-500/20 text-sm">New Campaign</router-link>
    </div>

    <!-- Toolbar -->
    <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4 mb-4 grid grid-cols-1 md:grid-cols-5 gap-3">
      <input v-model="query" type="text" placeholder="Search by title or owner" class="md:col-span-2 bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm placeholder-gray-500" />
      <select v-model="status" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="all">All Statuses</option>
        <option value="active">Active</option>
        <option value="draft">Draft</option>
        <option value="completed">Completed</option>
        <option value="archived">Archived</option>
      </select>
      <select v-model="category" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="all">All Categories</option>
        <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
      </select>
      <select v-model="sortBy" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="date">Sort: Newest</option>
        <option value="amount">Sort: Amount Raised</option>
        <option value="progress">Sort: Progress</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-gray-900/60 border border-gray-800 rounded-lg overflow-x-auto">
      <table class="min-w-full text-sm">
        <thead class="bg-yellow-600 text-gray-300">
          <tr>
            <th class="text-left px-4 py-2">Campaign</th>
            <th class="text-left px-4 py-2">Owner</th>
            <th class="text-right px-4 py-2">Raised</th>
            <th class="text-center px-4 py-2">Progress</th>
            <th class="text-center px-4 py-2">Status</th>
            <th class="text-right px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in paged" :key="c.id" class="border-t border-gray-800 hover:bg-gray-800/40">
            <td class="px-4 py-3">
              <div class="font-medium">{{ c.title }}</div>
              <div class="text-xs text-gray-400">{{ c.category }}</div>
            </td>
            <td class="px-4 py-3">{{ c.owner }}</td>
            <td class="px-4 py-3 text-right">XAF {{ c.raised.toLocaleString() }} / XAF {{ c.goal.toLocaleString() }}</td>
            <td class="px-4 py-3 text-center">
              <div class="w-32 h-2 bg-gray-800 rounded overflow-hidden inline-block align-middle">
                <div class="h-full bg-yellow-500" :style="{ width: Math.min(100, Math.round((c.raised/c.goal)*100)) + '%' }"></div>
              </div>
              <span class="ml-2 text-xs text-gray-300">{{ Math.min(100, Math.round((c.raised/c.goal)*100)) }}%</span>
            </td>
            <td class="px-4 py-3 text-center">
              <span :class="statusClass(c.status)" class="px-2 py-1 rounded text-xs border">{{ c.status }}</span>
            </td>
            <td class="px-4 py-3 text-right">
              <div class="inline-flex gap-2">
                <button @click="view(c)" class="text-xs px-2 py-1 border border-gray-700 rounded hover:bg-gray-800/60">View</button>
                <button @click="edit(c)" class="text-xs px-2 py-1 border border-gray-700 rounded hover:bg-gray-800/60">Edit</button>
                <button @click="toggleArchive(c)" class="text-xs px-2 py-1 border border-yellow-700 text-yellow-300 rounded hover:bg-yellow-500/10">{{ c.status === 'archived' ? 'Unarchive' : 'Archive' }}</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
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
import { useRouter } from 'vue-router'

const router = useRouter()

const categories = ['Health', 'Education', 'Emergency', 'Environment', 'Community']
const data = reactive([
  { id: 1, title: 'Clean Water for All', owner: 'Charity A', category: 'Health', goal: 50000, raised: 38420, status: 'active', createdAt: '2025-08-10' },
  { id: 2, title: 'Education First', owner: 'Charity B', category: 'Education', goal: 80000, raised: 64210, status: 'active', createdAt: '2025-08-01' },
  { id: 3, title: 'Relief Fund', owner: 'Relief Org', category: 'Emergency', goal: 60000, raised: 59000, status: 'completed', createdAt: '2025-07-20' },
  { id: 4, title: 'Tree Planting', owner: 'Green World', category: 'Environment', goal: 30000, raised: 21230, status: 'draft', createdAt: '2025-08-12' },
  { id: 5, title: 'Community Kitchen', owner: 'Local Helpers', category: 'Community', goal: 25000, raised: 11200, status: 'archived', createdAt: '2025-06-11' },
  { id: 6, title: 'Scholarship Drive', owner: 'Schools United', category: 'Education', goal: 40000, raised: 28800, status: 'active', createdAt: '2025-08-14' },
])

const query = ref('')
const status = ref('all')
const category = ref('all')
const sortBy = ref('date')

const filtered = computed(() => {
  let arr = data.filter(c =>
    (!query.value || c.title.toLowerCase().includes(query.value.toLowerCase()) || c.owner.toLowerCase().includes(query.value.toLowerCase())) &&
    (status.value === 'all' || c.status === status.value) &&
    (category.value === 'all' || c.category === category.value)
  )
  if (sortBy.value === 'amount') arr.sort((a,b) => b.raised - a.raised)
  else if (sortBy.value === 'progress') arr.sort((a,b) => (b.raised/b.goal) - (a.raised/a.goal))
  else arr.sort((a,b) => new Date(b.createdAt) - new Date(a.createdAt))
  return arr
})

const page = ref(1)
const pageSize = ref(5)
const start = computed(() => (page.value - 1) * pageSize.value)
const end = computed(() => page.value * pageSize.value)
const paged = computed(() => filtered.value.slice(start.value, end.value))

function statusClass(s) {
  if (s === 'active') return 'bg-green-500/10 text-green-400 border-green-500/30'
  if (s === 'completed') return 'bg-blue-500/10 text-blue-400 border-blue-500/30'
  if (s === 'draft') return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30'
  if (s === 'archived') return 'bg-gray-500/10 text-gray-300 border-gray-500/30'
  return 'bg-gray-500/10 text-gray-300 border-gray-500/30'
}

function view(c) {
  console.log('view', c)
}

function edit(c) {
  router.push({ path: '/admin/campaigns/create', query: { from: 'manage', id: c.id } })
}

function toggleArchive(c) {
  if (c.status === 'archived') c.status = 'active'
  else c.status = 'archived'
}
</script>

<style scoped>
</style>