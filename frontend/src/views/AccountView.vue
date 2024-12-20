<template>
    <div class="account-view">
        <h2 class="title">Account Settings</h2>
        <div class="profile-section">
            <img class="avatar" :src="userAvatar" alt="User Avatar" />
            <div class="profile-details">
                <p class="username">{{ user.username }}</p>
                <a class="logout-link" @click.prevent="logout">Logout</a>
            </div>
        </div>
        <div class="membership-info">
            <p><strong>Member since</strong></p>
            <p>{{ formattedJoinDate }}</p>
        </div>
        <div class="account-edit">
            <BaseTabs :tabs="tabs" v-model="activeTab">
            </BaseTabs>
            <div class="tabs-content">
                <div v-if="activeTab === 'edit-profile'">
                    <div class="edit-section">
                        <div class="edit-photo-section">
                            <img class="avatar-edit" :src="userAvatar" alt="Current Avatar" />
                            <BaseButton variant="secondary" class="ml-md px-md py-sm" @click="changeAvatar">Change Avatar</BaseButton>
                        </div>
                    </div>
                    <div class="edit-section">
                        <form @submit.prevent="updateProfile">
                            <BaseInput label="Username" v-model="editableUsername" placeholder="New username" />
                            <BaseInput label="E-mail" v-model="editableEmail" placeholder="New email address" />
                            <BaseButton variant="primary" class="px-md py-sm" type="submit">Save Changes</BaseButton>
                        </form>
                    </div>
                    <hr>
                    <div class="edit-section">
                        <h3>Delete Account</h3>
                        <p>Deleting your account is permanent and cannot be undone.</p>
                        <BaseButton variant="danger" class="px-md py-sm" @click="deleteAccount">Delete Account</BaseButton>
                    </div>
                </div>
                <div v-if="activeTab === 'password'">
                    <h3>Change Password</h3>
                    <form @submit.prevent="changePassword">
                        <BaseInput label="Current Password" type="password" v-model="currentPassword"
                            placeholder="Enter current password" />
                        <BaseInput label="New Password" type="password" v-model="newPassword"
                            placeholder="Enter new password" />
                        <BaseInput label="Confirm New Password" type="password" v-model="confirmNewPassword"
                            placeholder="Confirm new password" />
                        <BaseButton variant="primary" type="submit">Update Password</BaseButton>
                    </form>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import BaseInput from '@/components/base/BaseInput.vue';
import BaseButton from '@/components/base/BaseButton.vue';
import BaseTabs from '@/components/base/BaseTabs.vue';

export default {
    name: 'AccountView',
    components: {
        BaseInput,
        BaseButton,
        BaseTabs
    },
    data() {
        return {
            activeTab: 'edit-profile',
            tabs: [
                { label: 'Edit Profile', value: 'edit-profile' },
                { label: 'Password', value: 'password' }
            ],
            // Mock user data - in a real app, this would come from a store or API
            user: {
                username: 'John Doe',
                email: 'john.doe@example.com',
                avatarIndex: 1,
                joinDate: '2024-11-24'
            },
            editableUsername: '',
            editableEmail: '',
            currentPassword: '',
            newPassword: '',
            confirmNewPassword: ''
        };
    },
    computed: {
        userAvatar() {
            // Just an example: requires avatar images at certain paths
            return require(`@/assets/images/avatar-${this.user.avatarIndex}.png`);
        },
        formattedJoinDate() {
            const date = new Date(this.user.joinDate);
            return date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        }
    },
    methods: {
        logout() {
            // Implement logout logic
            console.log("Logged out");
        },
        changeAvatar() {
            // Implement avatar change logic
            console.log("Change Avatar clicked");
        },
        updateProfile() {
            // Implement profile update logic (username/email)
            console.log("Profile updated with:", this.editableUsername, this.editableEmail);
        },
        deleteAccount() {
            // Implement delete account logic
            console.log("Account deleted");
        },
        changePassword() {
            // Implement password change logic
            if (this.newPassword !== this.confirmNewPassword) {
                console.error("Passwords do not match");
                return;
            }
            console.log("Password changed");
        }
    },
    mounted() {
        // Initialize editable fields with current user values
        this.editableUsername = this.user.username;
        this.editableEmail = this.user.email;
    }
};
</script>

<style scoped>
.account-view {
    margin-top: 1.5rem;
}

.title {
    text-align: center;
    margin-bottom: 1.5rem;
}

.profile-section,
.membership-info {
    background: #f6f6f6;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    text-align: center;
}

.avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}

.profile-details {
    margin-top: 1rem;
}

.username {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.logout-link {
    color: #007bff;
    text-decoration: none;
    cursor: pointer;
}

/* Tabs and Edit Section */
.account-edit {
    flex: 1;
}

.tabs-content {
    background: #f9f9f9;
}

.edit-section {
    margin-bottom: 1.5rem;
}

.edit-section h4 {
    margin-bottom: 0.5rem;
}

.edit-photo-section {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.avatar-edit {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}

/* On mobile hide sidebar by default */
@media (max-width: 600px) {
    .tabs-content {
        padding: 1rem;
        border-radius: 8px;
    }

    .account-edit {
        margin: 1.5rem;
    }
}
</style>