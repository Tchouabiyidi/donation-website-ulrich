<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold">Manage Notifications</h1>
        <p class="text-gray-400">Templates, broadcasts and delivery channels</p>
      </div>
      <button @click="openCreate()" class="px-3 py-2 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-600/30 hover:bg-yellow-500/20 text-sm">New Template</button>
    </div>

    <!-- Toolbar -->
    <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4 mb-4 grid grid-cols-1 md:grid-cols-4 gap-3">
      <input v-model="query" type="text" placeholder="Search by name or subject" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm placeholder-gray-500" />
      <select v-model="channel" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="all">All Channels</option>
        <option value="email">Email</option>
        <option value="sms">SMS</option>
        <option value="push">Push</option>
      </select>
      <select v-model="sortBy" class="bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
        <option value="updated">Sort: Last Updated</option>
        <option value="name">Sort: Name</option>
      </select>
      <div class="flex items-center gap-3">
        <label class="inline-flex items-center gap-2 text-sm text-gray-300"><input type="checkbox" v-model="onlyActive" class="accent-yellow-500"/> Active only</label>
      </div>
    </div>

    <!-- Templates List -->
    <div class="bg-gray-900/60 border border-gray-800 rounded-lg overflow-x-auto">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-900/60 text-gray-300">
          <tr>
            <th class="text-left px-4 py-2">Name</th>
            <th class="text-left px-4 py-2">Subject</th>
            <th class="text-center px-4 py-2">Channel</th>
            <th class="text-center px-4 py-2">Active</th>
            <th class="text-right px-4 py-2">Updated</th>
            <th class="text-right px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in filtered" :key="t.id" class="border-t border-gray-800 hover:bg-gray-800/40">
            <td class="px-4 py-3">
              <div class="font-medium">{{ t.name }}</div>
              <div class="text-xs text-gray-400">{{ t.key }}</div>
            </td>
            <td class="px-4 py-3">{{ t.subject }}</td>
            <td class="px-4 py-3 text-center"><span class="px-2 py-1 text-xs border rounded" :class="channelClass(t.channel)">{{ t.channel }}</span></td>
            <td class="px-4 py-3 text-center">
              <button @click="toggleActive(t)" :class="t.active ? 'bg-green-500/10 text-green-400 border-green-500/30' : 'bg-gray-700/50 text-gray-300 border-gray-600'" class="px-2 py-1 rounded text-xs border">{{ t.active ? 'Active' : 'Inactive' }}</button>
            </td>
            <td class="px-4 py-3 text-right">{{ formatDate(t.updatedAt) }}</td>
            <td class="px-4 py-3 text-right">
              <div class="inline-flex gap-2">
                <button @click="edit(t)" class="text-xs px-2 py-1 border border-gray-700 rounded hover:bg-gray-800/60">Edit</button>
                <button @click="sendTest(t)" class="text-xs px-2 py-1 border border-gray-700 rounded hover:bg-gray-800/60">Send Test</button>
                <button @click="broadcast(t)" class="text-xs px-2 py-1 border border-yellow-700 text-yellow-300 rounded hover:bg-yellow-500/10">Broadcast</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-3xl bg-gray-900 border border-gray-800 rounded-lg">
        <div class="p-4 border-b border-gray-800 flex items-center justify-between">
          <h3 class="font-semibold">{{ current?.id ? 'Edit Template' : 'Create Template' }}</h3>
          <button @click="closeModal" class="text-gray-400 hover:text-white">✕</button>
        </div>
        <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-3">
            <div>
              <label class="block text-sm text-gray-300 mb-1">Name</label>
              <input v-model="form.name" type="text" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm text-gray-300 mb-1">Key</label>
              <input v-model="form.key" type="text" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm text-gray-300 mb-1">Channel</label>
              <select v-model="form.channel" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
                <option value="email">Email</option>
                <option value="sms">SMS</option>
                <option value="push">Push</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-gray-300 mb-1">Subject</label>
              <input v-model="form.subject" type="text" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
            </div>
            <div class="flex items-center gap-2">
              <input v-model="form.active" type="checkbox" class="accent-yellow-500" />
              <span class="text-sm text-gray-300">Active</span>
            </div>
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">Body</label>
            <textarea v-model="form.body" rows="12" class="w-full h-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm"></textarea>
          </div>
        </div>
        <div class="p-4 border-t border-gray-800 flex items-center justify-end gap-2">
          <button @click="closeModal" class="px-3 py-2 rounded border border-gray-700 hover:bg-gray-800/60 text-sm">Cancel</button>
          <button @click="saveTemplate" class="px-3 py-2 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-600/30 hover:bg-yellow-500/20 text-sm">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

const items = reactive([
  { id: 1, key: 'donation_receipt', name: 'Donation Receipt', subject: 'Thank you for your donation', channel: 'email', active: true, updatedAt: '2025-08-18', body: 'Hello {{name}}, thanks...' },
  { id: 2, key: 'campaign_approved', name: 'Campaign Approved', subject: 'Your campaign is live!', channel: 'email', active: true, updatedAt: '2025-08-16', body: 'Congrats...' },
  { id: 3, key: 'weekly_digest', name: 'Weekly Digest', subject: 'Your weekly update', channel: 'email', active: false, updatedAt: '2025-08-10', body: 'This week...' },
  { id: 4, key: 'donation_update', name: 'Donation Update', subject: 'A campaign you follow has news', channel: 'push', active: true, updatedAt: '2025-08-14', body: 'Update...' },
  { id: 5, key: 'otp_code', name: 'OTP Code', subject: 'Your verification code', channel: 'sms', active: true, updatedAt: '2025-08-12', body: 'Code: {{code}}' },
])

const query = ref('')
const channel = ref('all')
const sortBy = ref('updated')
const onlyActive = ref(false)

const filtered = computed(() => {
  let arr = items.filter(t =>
    (!query.value || t.name.toLowerCase().includes(query.value.toLowerCase()) || t.subject.toLowerCase().includes(query.value.toLowerCase())) &&
    (channel.value === 'all' || t.channel === channel.value) &&
    (!onlyActive.value || t.active)
  )
  if (sortBy.value === 'name') arr.sort((a,b) => a.name.localeCompare(b.name))
  else arr.sort((a,b) => new Date(b.updatedAt) - new Date(a.updatedAt))
  return arr
})

const showModal = ref(false)
const current = ref(null)
const form = reactive({ id: null, key: '', name: '', subject: '', channel: 'email', active: true, body: '' })

function openCreate() {
  current.value = null
  Object.assign(form, { id: null, key: '', name: '', subject: '', channel: 'email', active: true, body: '' })
  showModal.value = true
}

function edit(t) {
  current.value = t
  Object.assign(form, JSON.parse(JSON.stringify(t)))
  showModal.value = true
}

function saveTemplate() {
  if (!form.name || !form.key) { alert('Name and Key are required'); return }
  if (current.value) {
    Object.assign(current.value, JSON.parse(JSON.stringify(form)))
    current.value.updatedAt = new Date().toISOString().slice(0,10)
  } else {
    items.push({ ...JSON.parse(JSON.stringify(form)), id: Date.now(), updatedAt: new Date().toISOString().slice(0,10) })
  }
  closeModal()
}

function closeModal() { showModal.value = false }

function toggleActive(t) { t.active = !t.active }

function sendTest(t) {
  alert(`Sent test ${t.channel.toUpperCase()} using template: ${t.name}`)
}

function broadcast(t) {
  const when = prompt('Broadcast now? Enter schedule ISO string or leave blank for immediate send (stub).')
  console.log('broadcast', { template: t.key, schedule: when || 'now' })
  alert('Broadcast scheduled (stub).')
}

function channelClass(c) {
  if (c === 'email') return 'bg-blue-500/10 text-blue-300 border-blue-500/30'
  if (c === 'sms') return 'bg-green-500/10 text-green-300 border-green-500/30'
  return 'bg-yellow-500/10 text-yellow-300 border-yellow-500/30'
}

function formatDate(d) { return new Date(d).toLocaleDateString() }
</script>

<style scoped>
</style>