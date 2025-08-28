<template>
  <div class="min-h-screen bg-black text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-extrabold tracking-tight">Manage Accounts</h1>
        <p class="text-gray-400 mt-1">Create, assign roles, and manage user access.</p>
      </div>

      <!-- Toolbar -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-4 mb-6">
        <div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center">
          <div class="flex-1">
            <div class="relative">
              <input v-model="query" type="text" placeholder="Search by name or email" class="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-3 py-2 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500/60" />
              <svg class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M10 18a8 8 0 110-16 8 8 0 010 16z"/></svg>
            </div>
          </div>
          <select v-model="roleFilter" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
            <option value="all">All roles</option>
            <option value="admin">Admin</option>
            <option value="campaignOrganizer">Campaign Organizer</option>
            <option value="donor">Donor</option>
          </select>
          <button @click="openInvite" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold shadow hover:opacity-95">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            Invite User
          </button>
          <button @click="resetFilters" class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">Reset</button>
        </div>
      </div>

      <!-- Table -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-xl overflow-hidden">
        <div class="px-5 py-4 border-b border-gray-800 flex items-center justify-between">
          <h2 class="text-lg font-semibold">Users</h2>
          <span class="text-sm text-gray-400">{{ filtered.length }} users</span>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="text-left text-gray-300">
                <th class="py-3 px-5">Name</th>
                <th class="py-3 px-5">Email</th>
                <th class="py-3 px-5">Role</th>
                <th class="py-3 px-5">Status</th>
                <th class="py-3 px-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in filtered" :key="u.id" class="border-t border-gray-800 hover:bg-gray-800/40">
                <td class="py-3 px-5">
                  <div class="font-semibold">{{ u.name }}</div>
                  <div class="text-xs text-gray-500">ID: {{ u.id }}</div>
                </td>
                <td class="py-3 px-5">{{ u.email }}</td>
                <td class="py-3 px-5">
                  <select v-model="u.role" @change="changeRole(u)" class="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-gray-200">
                    <option value="admin">Admin</option>
                    <option value="campaignOrganizer">Campaign Organizer</option>
                    <option value="donor">Donor</option>
                  </select>
                </td>
                <td class="py-3 px-5">
                  <span class="text-xs px-2 py-0.5 rounded-full border"
                        :class="u.active ? 'bg-green-900/40 text-green-300 border-green-800' : 'bg-red-900/40 text-red-300 border-red-800'">
                    {{ u.active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="py-3 px-5 text-right">
                  <div class="inline-flex gap-2">
                    <button @click="toggleActive(u)" class="text-xs px-3 py-1.5 rounded border border-gray-700 text-gray-300 hover:bg-gray-700">
                      {{ u.active ? 'Deactivate' : 'Activate' }}
                    </button>
                    <button @click="resetPassword(u)" class="text-xs px-3 py-1.5 rounded border border-gray-700 text-gray-300 hover:bg-gray-700">Reset Password</button>
                    <button @click="deleteUser(u)" class="text-xs px-3 py-1.5 rounded border border-red-700 text-red-300 hover:bg-red-900/30">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Invite Modal (stub) -->
      <div v-if="showInvite" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black/60" @click="showInvite = false"></div>
        <div class="relative bg-gray-900 border border-gray-800 rounded-xl p-6 w-full max-w-md">
          <h3 class="text-lg font-semibold mb-4">Invite New User</h3>
          <div class="space-y-3">
            <input v-model="invite.email" type="email" placeholder="Email" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
            <select v-model="invite.role" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200">
              <option value="campaignOrganizer">Campaign Organizer</option>
              <option value="donor">Donor</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="mt-5 flex justify-end gap-2">
            <button class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800" @click="showInvite=false">Cancel</button>
            <button class="px-4 py-2 rounded-lg bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold" @click="sendInvite">Send Invite</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, onMounted } from 'vue'
import api from '../../lib/api'

const users = ref([])
const loading = ref(false)
const error = ref('')

const query = ref('')
const roleFilter = ref('all')
const showInvite = ref(false)
const invite = reactive({ email: '', role: 'campaignOrganizer' })

const filtered = computed(() => {
  // Map to include a display name and normalized fields
  let list = users.value.map(u => ({
    ...u,
    name: `${u.first_name || ''} ${u.last_name || ''}`.trim() || (u.email?.split('@')[0] || 'User'),
    active: u.is_active,
  }))
  const q = query.value.trim().toLowerCase()
  if (q) {
    list = list.filter(u =>
      u.name.toLowerCase().includes(q) ||
      u.email.toLowerCase().includes(q)
    )
  }
  if (roleFilter.value !== 'all') list = list.filter(u => u.role === roleFilter.value)
  return list
})

function resetFilters() {
  query.value = ''
  roleFilter.value = 'all'
}

function changeRole(user) {
  // Stub: integrate with backend
  console.log('Role changed', user.id, '->', user.role)
}

async function toggleActive(user) {
  const original = !!user.active
  const desired = !original
  // Optimistic UI update
  user.active = desired
  try {
    await api.patch(`/users/${user.id}/suspend/`, { is_active: desired })
    // Reflect in base list (users.value contains backend objects)
    users.value = users.value.map(u => u.id === user.id ? { ...u, is_active: desired } : u)
  } catch (e) {
    // Revert UI on failure
    user.active = original
    console.error('Failed to change active state', e?.response?.data || e)
    alert(e?.response?.data?.detail || e?.response?.data?.message || e?.message || 'Operation failed')
  }
}

function resetPassword(user) {
  // Stub: trigger password reset flow
  alert(`Password reset link sent to ${user.email}`)
}

function openInvite() { showInvite.value = true }
function sendInvite() {
  if (!invite.email) return
  // Stub: send invite to backend
  users.value.push({ id: `USR-${String(users.value.length + 1).padStart(3,'0')}`, name: invite.email.split('@')[0], email: invite.email, role: invite.role, active: true })
  invite.email = ''
  invite.role = 'campaignOrganizer'
  showInvite.value = false
}

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/users/')
    users.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Failed to fetch users', e?.response?.data || e)
    error.value = e?.response?.data?.detail || e?.message || 'Failed to load users'
  } finally {
    loading.value = false
  }
}

async function deleteUser(user) {
  if (!confirm(`Delete user ${user.email}? This cannot be undone.`)) return
  try {
    await api.delete(`/users/${user.id}/`)
    users.value = users.value.filter(u => u.id !== user.id)
  } catch (e) {
    console.error('Failed to delete user', e?.response?.data || e)
    alert(e?.response?.data?.detail || e?.response?.data?.message || e?.message || 'Delete failed')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
table thead th { border-bottom: 1px solid rgba(75,85,99,0.5); }
</style>