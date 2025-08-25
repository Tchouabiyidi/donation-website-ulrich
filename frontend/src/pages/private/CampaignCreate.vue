<template>
  <div class="min-h-screen text-white pt-20 px-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold">Create Fundraising Campaign</h1>
        <p class="text-gray-400">Fill details and preview before publishing</p>
      </div>
      <div class="flex gap-2">
        <button @click="saveDraft" class="px-3 py-2 rounded border border-gray-700 hover:bg-gray-800/60 text-sm">Save Draft</button>
        <button @click="submitCampaign" class="px-3 py-2 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-600/30 hover:bg-yellow-500/20 text-sm">Publish</button>
      </div>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- Form -->
      <form @submit.prevent class="xl:col-span-2 bg-gray-900/60 border border-gray-800 rounded-lg p-4 space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-300 mb-1">Title</label>
            <input v-model="form.title" type="text" placeholder="Campaign title" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm placeholder-gray-500" />
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">Category</label>
            <select v-model="form.category" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm">
              <option disabled value="">Select a category</option>
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm text-gray-300 mb-1">Goal Amount (USD)</label>
            <input v-model.number="form.goal" type="number" min="0" step="1" placeholder="50000" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">Start Date</label>
            <input v-model="form.startDate" type="date" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">End Date</label>
            <input v-model="form.endDate" type="date" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-300 mb-1">Location</label>
            <input v-model="form.location" type="text" placeholder="City, Country" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">Cover Image</label>
            <input @change="onFile" type="file" accept="image/*" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm file:mr-3 file:px-3 file:py-2 file:border-0 file:bg-gray-800 file:text-gray-300" />
          </div>
        </div>

        <div>
          <label class="block text-sm text-gray-300 mb-1">Short Summary</label>
          <input v-model="form.summary" type="text" maxlength="160" placeholder="One-liner that explains the campaign" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
          <div class="text-xs text-gray-500 mt-1">{{ form.summary.length }}/160</div>
        </div>

        <div>
          <label class="block text-sm text-gray-300 mb-1">Story / Description</label>
          <textarea v-model="form.description" rows="6" placeholder="Tell the story and why support is needed" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm"></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm text-gray-300 mb-1">Tags</label>
            <input v-model="tagInput" @keydown.enter.prevent="addTag" type="text" placeholder="Press Enter to add" class="w-full bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
            <div class="mt-2 flex flex-wrap gap-2">
              <span v-for="(t, i) in form.tags" :key="i" class="px-2 py-1 text-xs bg-gray-800 border border-gray-700 rounded">{{ t }} <button @click="removeTag(i)" class="ml-1 text-gray-400 hover:text-red-400">×</button></span>
            </div>
          </div>
          <div>
            <label class="block text-sm text-gray-300 mb-1">Suggested Donation Amounts</label>
            <div class="flex gap-2">
              <input v-model.number="suggest" type="number" min="1" class="w-28 bg-gray-900/70 border border-gray-800 rounded px-3 py-2 text-sm" />
              <button @click="addSuggest" type="button" class="px-3 py-2 rounded border border-gray-700 hover:bg-gray-800/60 text-sm">Add</button>
            </div>
            <div class="mt-2 flex flex-wrap gap-2">
              <span v-for="(s, i) in form.suggested" :key="i" class="px-2 py-1 text-xs bg-gray-800 border border-gray-700 rounded">${{ s }} <button @click="removeSuggest(i)" class="ml-1 text-gray-400 hover:text-red-400">×</button></span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-4 pt-2">
          <label class="inline-flex items-center gap-2 text-sm text-gray-300">
            <input v-model="form.allowComments" type="checkbox" class="accent-yellow-500" /> Allow comments
          </label>
          <label class="inline-flex items-center gap-2 text-sm text-gray-300">
            <input v-model="form.featured" type="checkbox" class="accent-yellow-500" /> Feature on landing
          </label>
        </div>
      </form>

      <!-- Preview -->
      <div class="bg-gray-900/60 border border-gray-800 rounded-lg p-4">
        <h2 class="font-semibold mb-3">Live Preview</h2>
        <div class="rounded-lg overflow-hidden border border-gray-800 bg-gray-950">
          <div class="h-40 bg-gray-800/60 flex items-center justify-center text-gray-500" :style="coverStyle">Cover image</div>
          <div class="p-4">
            <div class="text-xs text-gray-400">{{ form.category || '—' }}</div>
            <div class="text-lg font-semibold">{{ form.title || 'Untitled Campaign' }}</div>
            <div class="text-sm text-gray-300 mt-1">{{ form.summary || 'Summary will appear here' }}</div>
            <div class="mt-3">
              <div class="w-full h-2 bg-gray-800 rounded overflow-hidden">
                <div class="h-full bg-yellow-500" :style="{ width: progress + '%' }"></div>
              </div>
              <div class="flex items-center justify-between text-xs text-gray-400 mt-1">
                <div>${{ raised.toLocaleString() }} raised of ${{ (form.goal || 0).toLocaleString() }}</div>
                <div>{{ progress }}%</div>
              </div>
            </div>
            <div class="mt-3 flex flex-wrap gap-2">
              <span v-for="(t, i) in form.tags" :key="i" class="px-2 py-1 text-xs bg-gray-800 border border-gray-700 rounded">#{{ t }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import api from '../../lib/api'

const categories = ['Health', 'Education', 'Emergency', 'Environment', 'Community']

const form = reactive({
  title: '',
  category: '',
  goal: 0,
  startDate: '',
  endDate: '',
  beneficiary: '',
  location: '',
  summary: '',
  description: '',
  cover: '', // data URL
  tags: [],
  suggested: [10, 25, 50],
  allowComments: true,
  featured: false,
})

const tagInput = ref('')
const suggest = ref(25)
const raised = ref(0)

const progress = computed(() => {
  if (!form.goal) return 0
  return Math.min(100, Math.round((raised.value / form.goal) * 100))
})

const coverStyle = computed(() => form.cover ? { backgroundImage: `url(${form.cover})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {})

function onFile(e) {
  const file = e.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { form.cover = reader.result }
  reader.readAsDataURL(file)
}

function addTag() {
  const v = tagInput.value.trim()
  if (!v) return
  form.tags.push(v)
  tagInput.value = ''
}

function removeTag(i) {
  form.tags.splice(i, 1)
}

function addSuggest() {
  if (!suggest.value || suggest.value <= 0) return
  form.suggested.push(Math.round(suggest.value))
  suggest.value = 25
}

function removeSuggest(i) {
  form.suggested.splice(i, 1)
}

function validate() {
  const errors = []
  if (!form.title) errors.push('Title is required')
  if (!form.goal || form.goal <= 0) errors.push('Goal must be greater than 0')
  if (!form.startDate) errors.push('Start date is required')
  if (!form.endDate) errors.push('End date is required')
  if (form.startDate && form.endDate && form.endDate < form.startDate) errors.push('End date must be after start date')
  return errors
}

function saveDraft() {
  console.log('save draft', JSON.parse(JSON.stringify(form)))
  alert('Draft saved locally (stub).')
}

async function submitCampaign() {
  const errors = validate()
  if (errors.length) {
    alert('Please fix:\n- ' + errors.join('\n- '))
    return
  }
  try {
    const payload = {
      title: form.title,
      description: form.description || form.summary || '',
      target_amount: String(form.goal || 0),
      start_date: form.startDate || new Date().toISOString().slice(0, 10),
      end_date: form.endDate || form.startDate || new Date().toISOString().slice(0, 10),
    }
    const { data } = await api.post('/campaigns/', payload)
    console.log('Campaign created:', data)
    alert('Campaign submitted successfully and pending validation!')
  } catch (e) {
    console.error('Campaign creation failed:', e?.response?.data || e)
    const msg = e?.response?.data?.message || 'Failed to submit campaign.'
    const errs = e?.response?.data?.errors
    if (errs && typeof errs === 'object') {
      try {
        alert(msg + '\n' + Object.entries(errs).map(([k,v]) => `- ${k}: ${Array.isArray(v)?v.join(', '):v}`).join('\n'))
      } catch {
        alert(msg)
      }
    } else {
      alert(msg)
    }
  }
}
</script>

<style scoped>
</style>
