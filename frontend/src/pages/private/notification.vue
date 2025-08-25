<template>
  <div class="min-h-screen bg-black text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-extrabold tracking-tight">Notifications Center</h1>
        <p class="text-gray-400 mt-1">Review, manage, and act on system notifications.</p>
      </div>

      <!-- Toolbar -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-4 mb-6">
        <div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center">
          <div class="flex-1">
            <div class="relative">
              <input v-model="query" type="text" placeholder="Search notifications"
                class="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-3 py-2 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500/60" />
              <svg class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M10 18a8 8 0 110-16 8 8 0 010 16z"/></svg>
            </div>
          </div>

          <select v-model="typeFilter" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="all">All types</option>
            <option value="info">Info</option>
            <option value="success">Success</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>

          <select v-model="statusFilter" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="all">All statuses</option>
            <option value="unread">Unread</option>
            <option value="read">Read</option>
          </select>

          <select v-model="sortBy" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="date_desc">Newest first</option>
            <option value="date_asc">Oldest first</option>
          </select>

          <div class="flex gap-2">
            <button @click="markAllRead" class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">Mark all read</button>
            <button @click="clearAll" class="px-4 py-2 rounded-lg bg-red-600/80 hover:bg-red-600 text-white">Clear all</button>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- List -->
        <div class="lg:col-span-2 bg-gray-900/60 border border-gray-800 rounded-xl overflow-hidden">
          <div class="border-b border-gray-800 px-4 py-3 flex items-center justify-between">
            <h2 class="font-semibold text-gray-200">Notifications</h2>
            <span class="text-xs text-gray-400">{{ filteredNotifications.length }} results</span>
          </div>

          <ul role="list" class="divide-y divide-gray-800">
            <li v-for="n in filteredNotifications" :key="n.id"
                class="p-4 hover:bg-gray-800/50 cursor-pointer flex gap-4"
                @click="select(n)"
                :class="{ 'bg-gray-800/40': selected && selected.id === n.id }">
              <div class="pt-1">
                <span class="inline-flex items-center text-xs font-medium px-2 py-0.5 rounded-full border"
                  :class="typeBadgeClass(n.type)">{{ n.type }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <p class="font-semibold text-gray-100 truncate">{{ n.title }}</p>
                  <span v-if="!n.read" class="inline-block w-2 h-2 rounded-full bg-yellow-400" title="Unread"></span>
                </div>
                <p class="text-sm text-gray-400 line-clamp-1">{{ n.message }}</p>
                <div class="mt-1 text-xs text-gray-500">{{ formatDate(n.createdAt) }} • {{ n.actor }}</div>
              </div>
              <div class="flex items-center gap-2">
                <button @click.stop="toggleRead(n)" class="text-xs px-3 py-1 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">
                  {{ n.read ? 'Mark unread' : 'Mark read' }}
                </button>
                <button @click.stop="removeOne(n)" class="text-xs px-3 py-1 rounded-lg border border-red-700 text-red-300 hover:bg-red-700/20">Remove</button>
              </div>
            </li>
          </ul>
        </div>

        <!-- Detail Panel -->
        <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-4">
          <h3 class="font-semibold text-gray-200 mb-3">Details</h3>
          <div v-if="selected" class="space-y-3">
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center text-xs font-medium px-2 py-0.5 rounded-full border" :class="typeBadgeClass(selected.type)">{{ selected.type }}</span>
              <span class="text-xs text-gray-500">{{ formatDate(selected.createdAt) }}</span>
            </div>
            <h4 class="text-lg font-bold text-white">{{ selected.title }}</h4>
            <p class="text-gray-300">{{ selected.message }}</p>
            <div class="text-sm text-gray-400">From: {{ selected.actor }}</div>
            <div v-if="selected.link" class="pt-2">
              <a :href="selected.link" class="text-yellow-400 hover:underline" target="_blank" rel="noopener">Open related item</a>
            </div>
            <div class="flex gap-2 pt-2">
              <button @click="toggleRead(selected)" class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">{{ selected.read ? 'Mark unread' : 'Mark read' }}</button>
              <button @click="removeOne(selected)" class="px-4 py-2 rounded-lg bg-red-600/80 hover:bg-red-600 text-white">Remove</button>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">Select a notification to view details.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../../lib/api'

// Filters
const query = ref('');
const typeFilter = ref('all'); // all | info | success | warning | error
const statusFilter = ref('all'); // all | read | unread
const sortBy = ref('date_desc'); // date_desc | date_asc

// Notifications from backend
const notifications = ref([])
const loading = ref(false)
const error = ref('')

const selected = ref(null);

const filteredNotifications = computed(() => {
  let items = [...notifications.value];

  if (query.value.trim()) {
    const q = query.value.toLowerCase();
    items = items.filter(n =>
      n.title.toLowerCase().includes(q) ||
      n.message.toLowerCase().includes(q) ||
      n.actor.toLowerCase().includes(q)
    );
  }

  if (typeFilter.value !== 'all') {
    items = items.filter(n => n.type === typeFilter.value);
  }

  if (statusFilter.value !== 'all') {
    items = items.filter(n => (statusFilter.value === 'read' ? n.read : !n.read));
  }

  items.sort((a, b) => sortBy.value === 'date_desc'
    ? b.createdAt - a.createdAt
    : a.createdAt - b.createdAt
  );

  return items;
});

function select(n) {
  selected.value = n;
}

async function toggleRead(n) {
  try {
    const desired = !n.read
    await api.patch(`/notifications/${n.id}/toggle-read/`, { is_read: desired })
    n.read = desired
  } catch (e) {
    console.error('Failed to toggle read', e?.response?.data || e)
    alert('Failed to update notification status')
  }
}

function markAllRead() {
  // Optimistic: update UI and fire requests
  notifications.value.forEach(async n => {
    if (!n.read) {
      n.read = true
      try { await api.patch(`/notifications/${n.id}/toggle-read/`, { is_read: true }) } catch (_) {}
    }
  })
}

function clearAll() {
  if (confirm('Clear all notifications? This cannot be undone.')) {
    const ids = notifications.value.map(n => n.id)
    notifications.value = []
    selected.value = null
    // Fire and forget deletes
    ids.forEach(async id => { try { await api.delete(`/notifications/${id}/`) } catch (_) {} })
  }
}

function removeOne(n) {
  notifications.value = notifications.value.filter(x => x.id !== n.id);
  if (selected.value && selected.value.id === n.id) {
    selected.value = null;
  }
  // Delete on backend
  api.delete(`/notifications/${n.id}/`).catch(() => {})
}

function typeBadgeClass(t) {
  switch (t) {
    case 'success': return 'bg-green-900/40 text-green-300 border-green-700';
    case 'warning': return 'bg-yellow-900/40 text-yellow-300 border-yellow-700';
    case 'error':   return 'bg-red-900/40 text-red-300 border-red-700';
    default:        return 'bg-blue-900/40 text-blue-300 border-blue-700';
  }
}

function formatDate(d) {
  try {
    return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(d);
  } catch {
    return String(d);
  }
}

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/notifications/')
    notifications.value = (data || []).map(x => ({
      id: x.id,
      title: x.message?.slice(0, 40) || 'Notification',
      message: x.message || '',
      type: 'info',
      createdAt: new Date(x.created_at),
      read: !!x.is_read,
      actor: x.sender_email || 'System',
      link: null,
    }))
  } catch (e) {
    console.error('Failed to load notifications', e?.response?.data || e)
    error.value = e?.response?.data?.detail || 'Failed to load notifications.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* Fade animation for notification */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Enhanced focus styles */
button:focus {
  outline-offset: 2px;
}
</style>