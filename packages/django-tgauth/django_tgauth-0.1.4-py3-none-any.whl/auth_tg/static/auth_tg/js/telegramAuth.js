window.TelegramAuth = {
    authCheckInterval: null,
    authCode: null,

    async initTelegramAuth() {
        try {
            const response = await fetch('/auth/api/telegram/login/', {
                credentials: 'include'
            });
            const data = await response.json();

            this.authCode = data.auth_code;
            window.open(data.auth_url, '_blank');
            this.startAuthCheck();
        } catch (error) {
            console.error('Error starting auth:', error);
        }
    },

    startAuthCheck() {
        if (this.authCheckInterval) {
            clearInterval(this.authCheckInterval);
        }
        this.authCheckInterval = setInterval(() => this.checkAuthStatus(), 2000);

        setTimeout(() => {
            if (this.authCheckInterval) {
                clearInterval(this.authCheckInterval);
                console.log('Auth check timeout');
            }
        }, 30000);
    },

    async checkAuthStatus() {
        try {
            const response = await fetch(`/auth/api/telegram/check-auth-status/?auth_code=${this.authCode}`, {
                credentials: 'include',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            const data = await response.json();

            if (data.authenticated) {
                clearInterval(this.authCheckInterval);
                window.location.reload();
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
            clearInterval(this.authCheckInterval);
        }
    },

    logout() {
        fetch('/auth/logout/', {
            method: 'GET',
            credentials: 'include'
        }).then(() => {
            window.location.href = '/';
        }).catch(error => {
            console.error('Logout error:', error);
        });
    }
};