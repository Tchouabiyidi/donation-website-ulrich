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
          <h1 class="text-xl font-semibold text-gray-800">User Management</h1>
          
          <!-- Actions -->
          <div class="flex items-center space-x-2">
            <button 
              @click="showInviteModal = true"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="-ml-0.5 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
              Invite User
            </button>
          </div>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-4 sm:p-6">
        <!-- User Search and Filters -->
        <div class="mb-6 bg-white shadow rounded-lg p-4">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <!-- Search -->
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </div>
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Search users by name or email"
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
            </div>
            
            <!-- Filters -->
            <div class="flex items-center space-x-2">
              <select 
                v-model="roleFilter"
                class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="">All Roles</option>
                <option v-for="role in availableRoles" :key="role.value" :value="role.value">{{ role.label }}</option>
              </select>
              
              <select 
                v-model="statusFilter"
                class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="">All Statuses</option>
                <option value="active">Active</option>
                <option value="pending">Pending</option>
                <option value="suspended">Suspended</option>
              </select>
            </div>
          </div>
        </div>
  
        <!-- Users Table -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Role
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Active
                  </th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="user in paginatedUsers" :key="user.id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10">
                        <img class="h-10 w-10 rounded-full" :src="user.avatar" :alt="user.name">
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ user.name }}</div>
                        <div class="text-sm text-gray-500">{{ user.email }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ formatRole(user.role) }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="statusClass(user.status)">
                      {{ formatStatus(user.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatLastActive(user.lastActive) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      @click="editUser(user)"
                      class="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Edit
                    </button>
                    <button 
                      @click="confirmUserAction(user, user.status === 'active' ? 'suspend' : 'activate')"
                      class="text-yellow-600 hover:text-yellow-900 mr-3"
                    >
                      {{ user.status === 'active' ? 'Suspend' : 'Activate' }}
                    </button>
                    <button 
                      @click="confirmUserAction(user, 'delete')"
                      class="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">
                    No users found matching your criteria
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Pagination -->
          <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div class="flex-1 flex justify-between sm:hidden">
              <button 
                @click="currentPage = Math.max(1, currentPage - 1)"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Previous
              </button>
              <button 
                @click="currentPage = Math.min(totalPages, currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Next
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Showing <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> to <span class="font-medium">{{ Math.min(currentPage * pageSize, filteredUsers.length) }}</span> of <span class="font-medium">{{ filteredUsers.length }}</span> users
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button 
                    @click="currentPage = Math.max(1, currentPage - 1)"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Previous</span>
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                  </button>
                  <button 
                    v-for="page in visiblePages"
                    :key="page"
                    @click="currentPage = page"
                    :class="{
                      'z-10 bg-blue-50 border-blue-500 text-blue-600': currentPage === page,
                      'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': currentPage !== page
                    }"
                    class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                  >
                    {{ page }}
                  </button>
                  <button 
                    @click="currentPage = Math.min(totalPages, currentPage + 1)"
                    :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span class="sr-only">Next</span>
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Invite User Modal -->
        <div v-if="showInviteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Invite New User</h3>
            </div>
            <div class="p-6">
              <div class="mb-4">
                <label for="invite-email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                <input 
                  type="email" 
                  id="invite-email" 
                  v-model="inviteEmail"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="user@example.cm"
                >
              </div>
              <div class="mb-4">
                <label for="invite-role" class="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select 
                  id="invite-role" 
                  v-model="inviteRole"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option v-for="role in availableRoles" :key="role.value" :value="role.value">{{ role.label }}</option>
                </select>
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button 
                @click="showInviteModal = false"
                class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button 
                @click="sendInvite"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Send Invitation
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit User Modal -->
        <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Edit User</h3>
            </div>
            <div class="p-6">
              <div class="mb-4">
                <label for="edit-name" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input 
                  type="text" 
                  id="edit-name" 
                  v-model="editingUser.name"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
              </div>
              <div class="mb-4">
                <label for="edit-email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                <input 
                  type="email" 
                  id="edit-email" 
                  v-model="editingUser.email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
              </div>
              <div class="mb-4">
                <label for="edit-role" class="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select 
                  id="edit-role" 
                  v-model="editingUser.role"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option v-for="role in availableRoles" :key="role.value" :value="role.value">{{ role.label }}</option>
                </select>
              </div>
              <div class="mb-4">
                <label for="edit-status" class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select 
                  id="edit-status" 
                  v-model="editingUser.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="active">Active</option>
                  <option value="pending">Pending</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button 
                @click="showEditModal = false"
                class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button 
                @click="saveUser"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
  
        <!-- Confirmation Modal -->
        <div v-if="showConfirmModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">{{ confirmTitle }}</h3>
            </div>
            <div class="p-6">
              <p class="text-gray-700">{{ confirmMessage }}</p>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button 
                @click="showConfirmModal = false"
                class="mr-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button 
                @click="executeUserAction"
                :class="{
                  'bg-red-600 hover:bg-red-700': confirmAction === 'delete',
                  'bg-yellow-600 hover:bg-yellow-700': confirmAction === 'suspend',
                  'bg-green-600 hover:bg-green-700': confirmAction === 'activate'
                }"
                class="px-4 py-2 text-sm font-medium text-white border border-transparent rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                {{ confirmButtonText }}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserManagement',
    emits: ['toggle-sidebar'],
    data() {
      return {
        searchQuery: '',
        roleFilter: '',
        statusFilter: '',
        currentPage: 1,
        pageSize: 10,
        showInviteModal: false,
        showEditModal: false,
        showConfirmModal: false,
        inviteEmail: '',
        inviteRole: 'user',
        editingUser: null,
        confirmAction: '',
        confirmUser: null,
        availableRoles: [
          { value: 'admin', label: 'Administrator' },
          { value: 'manager', label: 'Manager' },
          { value: 'user', label: 'Standard User' },
          { value: 'viewer', label: 'Viewer' }
        ],
        users: [
          {
            id: 1,
            name: 'John Smith',
            email: 'john.smith@example.cm',
            avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
            role: 'admin',
            status: 'active',
            lastActive: '2023-06-15T14:32:00'
          },
          {
            id: 2,
            name: 'Sarah Johnson',
            email: 'sarah.j@example.cm',
            avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
            role: 'manager',
            status: 'active',
            lastActive: '2023-06-14T09:15:00'
          },
          {
            id: 3,
            name: 'Michael Brown',
            email: 'michael.b@example.cm',
            avatar: 'https://randomuser.me/api/portraits/men/22.jpg',
            role: 'user',
            status: 'pending',
            lastActive: null
          },
          {
            id: 4,
            name: 'Emily Davis',
            email: 'emily.d@example.cm',
            avatar: 'https://randomuser.me/api/portraits/women/33.jpg',
            role: 'viewer',
            status: 'suspended',
            lastActive: '2023-05-30T16:45:00'
          },
          {
            id: 5,
            name: 'Robert Wilson',
            email: 'robert.w@example.cm',
            avatar: 'https://randomuser.me/api/portraits/men/55.jpg',
            role: 'user',
            status: 'active',
            lastActive: '2023-06-15T11:20:00'
          }
        ]
      }
    },
    computed: {
      filteredUsers() {
        return this.users.filter(user => {
          const matchesSearch = this.searchQuery === '' || 
            user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
            user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
          
          const matchesRole = this.roleFilter === '' || user.role === this.roleFilter;
          const matchesStatus = this.statusFilter === '' || user.status === this.statusFilter;
          
          return matchesSearch && matchesRole && matchesStatus;
        });
      },
      paginatedUsers() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredUsers.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredUsers.length / this.pageSize);
      },
      visiblePages() {
        const pages = [];
        const maxVisible = 5;
        let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        let end = Math.min(this.totalPages, start + maxVisible - 1);
        
        if (end - start < maxVisible - 1) {
          start = Math.max(1, end - maxVisible + 1);
        }
        
        for (let i = start; i <= end; i++) {
          pages.push(i);
        }
        
        return pages;
      },
      confirmTitle() {
        switch (this.confirmAction) {
          case 'delete':
            return 'Delete User';
          case 'suspend':
            return 'Suspend User';
          case 'activate':
            return 'Activate User';
          default:
            return 'Confirm Action';
        }
      },
      confirmMessage() {
        if (!this.confirmUser) return '';
        
        switch (this.confirmAction) {
          case 'delete':
            return `Are you sure you want to permanently delete ${this.confirmUser.name}? This action cannot be undone.`;
          case 'suspend':
            return `Are you sure you want to suspend ${this.confirmUser.name}? They will no longer be able to access the system.`;
          case 'activate':
            return `Are you sure you want to activate ${this.confirmUser.name}? They will regain access to the system.`;
          default:
            return 'Are you sure you want to perform this action?';
        }
      },
      confirmButtonText() {
        switch (this.confirmAction) {
          case 'delete':
            return 'Delete User';
          case 'suspend':
            return 'Suspend User';
          case 'activate':
            return 'Activate User';
          default:
            return 'Confirm';
        }
      }
    },
    methods: {
      formatRole(role) {
        const found = this.availableRoles.find(r => r.value === role);
        return found ? found.label : role;
      },
      formatStatus(status) {
        switch (status) {
          case 'active': return 'Active';
          case 'pending': return 'Pending';
          case 'suspended': return 'Suspended';
          default: return status;
        }
      },
      statusClass(status) {
        switch (status) {
          case 'active': return 'bg-green-100 text-green-800';
          case 'pending': return 'bg-yellow-100 text-yellow-800';
          case 'suspended': return 'bg-red-100 text-red-800';
          default: return 'bg-gray-100 text-gray-800';
        }
      },
      formatLastActive(date) {
        if (!date) return 'Never';
        
        const now = new Date();
        const lastActive = new Date(date);
        const diffDays = Math.floor((now - lastActive) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        
        return lastActive.toLocaleDateString();
      },
      editUser(user) {
        this.editingUser = { ...user };
        this.showEditModal = true;
      },
      saveUser() {
        // In a real app, this would update the user in your backend
        const index = this.users.findIndex(u => u.id === this.editingUser.id);
        if (index !== -1) {
          this.users[index] = { ...this.editingUser };
        }
        this.showEditModal = false;
      },
      confirmUserAction(user, action) {
        this.confirmUser = user;
        this.confirmAction = action;
        this.showConfirmModal = true;
      },
      executeUserAction() {
        // In a real app, this would call your backend API
        const index = this.users.findIndex(u => u.id === this.confirmUser.id);
        if (index !== -1) {
          switch (this.confirmAction) {
            case 'delete':
              this.users.splice(index, 1);
              break;
            case 'suspend':
              this.users[index].status = 'suspended';
              break;
            case 'activate':
              this.users[index].status = 'active';
              this.users[index].lastActive = new Date().toISOString();
              break;
          }
        }
        this.showConfirmModal = false;
      },
      sendInvite() {
        // In a real app, this would send an invitation via your backend
        const newUser = {
          id: Math.max(...this.users.map(u => u.id)) + 1,
          name: this.inviteEmail.split('@')[0],
          email: this.inviteEmail,
          avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(this.inviteEmail.split('@')[0])}&background=random`,
          role: this.inviteRole,
          status: 'pending',
          lastActive: null
        };
        
        this.users.push(newUser);
        this.showInviteModal = false;
        this.inviteEmail = '';
        this.inviteRole = 'user';
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
  
  /* Table row hover effect */
  tbody tr {
    transition: background-color 0.2s ease;
  }
  tbody tr:hover {
    background-color: rgba(243, 244, 246, 0.5);
  }
  
  /* Button transitions */
  button {
    transition: all 0.2s ease;
  }
  </style>