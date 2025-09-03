<template>
  <div class="min-h-screen  text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-extrabold tracking-tight">Campaign Verification</h1>
        <p class="text-gray-400 mt-1">Review submissions and approve or reject campaigns.</p>
      </div>

      <!-- Toolbar -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-4 mb-6">
        <div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center">
          <div class="flex-1">
            <div class="relative">
              <input v-model="query" type="text" placeholder="Search by title, organizer, or ID" class="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-3 py-2 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500/60" />
              <svg class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M10 18a8 8 0 110-16 8 8 0 010 16z"/></svg>
            </div>
          </div>
          <select v-model="statusFilter" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="all">All statuses</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>
          <select v-model="sortBy" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="date">Newest</option>
            <option value="title">Title</option>
            <option value="amount">Goal Amount</option>
          </select>
          <button @click="resetFilters" class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">Reset</button>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- List -->
        <div class="lg:col-span-2 bg-gray-900/60 border border-gray-800 rounded-xl">
          <div class="px-5 py-4 border-b border-gray-800 flex items-center justify-between">
            <h2 class="text-lg font-semibold">Submissions</h2>
            <span class="text-sm text-gray-400">{{ filtered.length }} items</span>
          </div>
          <ul class="divide-y divide-gray-800">
            <li v-for="c in filtered" :key="c.id" @click="select(c)" class="px-5 py-4 cursor-pointer hover:bg-gray-800/40"
                :class="selected && selected.id === c.id ? 'bg-gray-800/60' : ''">
              <div class="flex items-start justify-between">
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="font-semibold">{{ c.title }}</h3>
                    <span class="text-xs px-2 py-0.5 rounded-full border"
                          :class="badgeClass(c.status)">{{ c.status }}</span>
                  </div>
                  <p class="text-sm text-gray-400">by {{ c.organizer }} • Goal: {{ currency(c.goal) }}</p>
                  <p class="text-xs text-gray-500">ID: {{ c.id }} • Submitted {{ formatDate(c.submittedAt) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm text-gray-300">Raised: {{ currency(c.raised) }}</p>
                  <p class="text-xs text-gray-500">{{ c.donors }} donors</p>
                </div>
              </div>
            </li>
          </ul>
          <div v-if="!filtered.length" class="px-5 py-8 text-center text-gray-500">No campaigns match your filters.</div>
        </div>

        <!-- Details -->
        <div class="bg-gray-900/60 border border-gray-800 rounded-xl">
          <div class="px-5 py-4 border-b border-gray-800 flex items-center justify-between">
            <h2 class="text-lg font-semibold">Details</h2>
            <span v-if="selected" class="text-xs px-2 py-0.5 rounded-full border" :class="badgeClass(selected.status)">{{ selected.status }}</span>
          </div>
          <div class="p-5" v-if="selected">
            <h3 class="text-xl font-bold mb-1">{{ selected.title }}</h3>
            <p class="text-gray-400 mb-4">by {{ selected.organizer }} • {{ selected.category }}</p>

            <div class="grid grid-cols-2 gap-4 mb-4">
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Goal</p>
                <p class="text-lg font-semibold">{{ currency(selected.goal) }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Raised</p>
                <p class="text-lg font-semibold">{{ currency(selected.raised) }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Donors</p>
                <p class="text-lg font-semibold">{{ selected.donors }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Submitted</p>
                <p class="text-lg font-semibold">{{ formatDate(selected.submittedAt) }}</p>
              </div>
            </div>

            <div class="mb-4">
              <p class="text-sm text-gray-300 mb-2">Description</p>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-200 leading-relaxed max-h-40 overflow-auto">
                {{ selected.description }}
              </div>
            </div>

            <div class="mb-4">
              <p class="text-sm text-gray-300 mb-2">Uploaded Documents</p>
              <ul class="space-y-2">
                <li v-for="doc in selected.documents" :key="doc.name" class="flex items-center justify-between p-2 bg-gray-800 border border-gray-700 rounded-lg">
                  <span class="text-sm text-gray-300">{{ doc.name }}</span>
                  <button class="text-xs px-2 py-1 rounded border border-gray-700 text-gray-300 hover:bg-gray-700" @click="viewDoc(doc)">View</button>
                </li>
              </ul>
            </div>

            <div class="flex items-center gap-3">
              <button @click="approve(selected)" :disabled="selected.status==='approved'" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500 text-black font-semibold shadow disabled:opacity-50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                Approve
              </button>
              <button @click="reject(selected)" :disabled="selected.status==='rejected'" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-red-500 text-black font-semibold shadow disabled:opacity-50">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                Reject
              </button>
            </div>
          </div>
          <div v-else class="p-5 text-gray-500">Select a campaign to review.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import api from '../../lib/api'

const submissions = ref([])
const loading = ref(false)
const error = ref('')

const selected = ref(null)
const query = ref('')
const statusFilter = ref('pending')
const sortBy = ref('date')

onMounted(async () => {
  await fetchPending()
})

async function fetchPending() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/campaigns/pending/')
    // Map backend fields to UI model
    submissions.value = (data || []).map(c => ({
      id: c.id,
      title: c.title,
      organizer: String(c.organizer),
      category: '',
      goal: Number(c.target_amount || 0),
      raised: 0,
      donors: 0,
      status: c.is_validated ? 'approved' : 'pending',
      submittedAt: c.created_at,
      description: c.description || '',
      documents: [],
    }))
    selected.value = submissions.value[0] || null
  } catch (e) {
    console.error('Failed to load pending campaigns', e?.response?.data || e)
    error.value = e?.response?.data?.detail || 'Failed to load pending campaigns.'
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  let list = submissions.value

  // search
  const q = query.value.trim().toLowerCase()
  if (q) {
    list = list.filter(c =>
      c.title.toLowerCase().includes(q) ||
      c.organizer.toLowerCase().includes(q) ||
      String(c.id).toLowerCase().includes(q)
    )
  }

  // status
  if (statusFilter.value !== 'all') {
    list = list.filter(c => c.status === statusFilter.value)
  }

  // sort
  list = [...list]
  if (sortBy.value === 'title') list.sort((a,b) => a.title.localeCompare(b.title))
  else if (sortBy.value === 'amount') list.sort((a,b) => b.goal - a.goal)
  else list.sort((a,b) => new Date(b.submittedAt) - new Date(a.submittedAt))

  return list
})

function select(c) { selected.value = c }
function resetFilters() {
  query.value = ''
  statusFilter.value = 'pending'
  sortBy.value = 'date'
}

async function approve(c) {
  if (!c) return
  try {
    await api.patch(`/campaigns/${c.id}/validate/`)
    c.status = 'approved'
  } catch (e) {
    alert('Failed to approve campaign')
    console.error(e?.response?.data || e)
  }
}
function reject(c) {
  if (!c) return
  // No backend reject endpoint yet; stub UI change only
  c.status = 'rejected'
}

function viewDoc(doc) {
  // Stub: open a preview later; for now, download prompt using a Blob stub
  const blob = new Blob([`Preview not implemented for ${doc.name}.`], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = doc.name
  a.click()
  URL.revokeObjectURL(url)
}

function badgeClass(status) {
  if (status === 'approved') return 'bg-green-900/40 text-green-300 border-green-800'
  if (status === 'rejected') return 'bg-red-900/40 text-red-300 border-red-800'
  return 'bg-yellow-900/40 text-yellow-300 border-yellow-800'
}

function currency(value) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XAF', maximumFractionDigits: 0 }).format(value || 0)
  } catch {
    return `XAF ${Number(value || 0).toLocaleString()}`
  }
}

function formatDate(value) {
  try {
    const d = new Date(value)
    if (isNaN(d.getTime())) return String(value)
    return d.toLocaleDateString()
  } catch (e) {
    return String(value)
  }
}

// Initialize selection to first filtered item (if any)
select(filtered.value[0] || null)
</script>

<style scoped>
/* Subtle list dividers to match dark theme */
.divide-gray-800 > :not([hidden]) ~ :not([hidden]) {
  border-color: rgba(31, 41, 55, 1);
}
</style>