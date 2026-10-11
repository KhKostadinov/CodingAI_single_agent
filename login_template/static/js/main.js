/**
 * main.js
 * -------
 * Frontend JavaScript for the SecureAuth login system.
 * Handles form validation, password toggle, flash messages,
 * password strength meter, and UX enhancements.
 * No external dependencies.
 */

(function () {
    'use strict';

    // =========================================================================
    // Flash Messages
    // =========================================================================
    /**
     * Render flash messages from the server into the DOM.
     * Expects a hidden <script> tag with JSON data or reads from data attributes.
     */
    function renderFlashMessages() {
        const container = document.getElementById('flashMessages');
        if (!container) return;

        // Check for flash messages passed via data attribute or inline script
        const flashData = document.querySelector('[data-flash-messages]');
        if (flashData) {
            try {
                const messages = JSON.parse(flashData.getAttribute('data-flash-messages'));
                messages.forEach(function (msg) {
                    const div = document.createElement('div');
                    div.className = 'flash-msg ' + msg.category;
                    div.textContent = msg.message;
                    container.appendChild(div);
                });
            } catch (e) {
                // Silently ignore parse errors
            }
        }

        // Auto-dismiss after 5 seconds
        const msgs = container.querySelectorAll('.flash-msg');
        if (msgs.length > 0) {
            setTimeout(function () {
                msgs.forEach(function (m) {
                    m.style.transition = 'opacity 0.5s ease';
                    m.style.opacity = '0';
                    setTimeout(function () { m.remove(); }, 500);
                });
            }, 5000);
        }
    }

    // =========================================================================
    // Password Toggle
    // =========================================================================
    function initPasswordToggle() {
        const toggleBtn = document.getElementById('togglePassword');
        if (!toggleBtn) return;

        const passwordInput = document.getElementById('password');

        toggleBtn.addEventListener('click', function () {
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';
            toggleBtn.classList.toggle('active', isPassword);
        });
    }

    // =========================================================================
    // Password Strength Meter
    // =========================================================================
    function initPasswordStrength() {
        const passwordInput = document.getElementById('password');
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');

        if (!passwordInput || !strengthFill || !strengthText) return;

        passwordInput.addEventListener('input', function () {
            const password = passwordInput.value;
            let score = 0;

            if (password.length >= 6) score++;
            if (password.length >= 10) score++;
            if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
            if (/[0-9]/.test(password)) score++;
            if (/[^A-Za-z0-9]/.test(password)) score++;

            strengthFill.className = 'strength-fill';
            strengthText.textContent = '';

            if (password.length === 0) return;

            if (score <= 2) {
                strengthFill.classList.add('weak');
                strengthText.textContent = 'Weak';
            } else if (score <= 3) {
                strengthFill.classList.add('medium');
                strengthText.textContent = 'Medium';
            } else {
                strengthFill.classList.add('strong');
                strengthText.textContent = 'Strong';
            }
        });
    }

    // =========================================================================
    // Form Validation
    // =========================================================================
    function validateLoginForm() {
        const form = document.getElementById('loginForm');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            let valid = true;

            // Username
            const username = document.getElementById('username');
            const usernameError = document.getElementById('usernameError');
            if (!username.value.trim()) {
                usernameError.textContent = 'Username is required.';
                username.classList.add('input-error');
                valid = false;
            } else {
                usernameError.textContent = '';
                username.classList.remove('input-error');
            }

            // Password
            const password = document.getElementById('password');
            const passwordError = document.getElementById('passwordError');
            if (!password.value) {
                passwordError.textContent = 'Password is required.';
                password.classList.add('input-error');
                valid = false;
            } else {
                passwordError.textContent = '';
                password.classList.remove('input-error');
            }

            if (!valid) {
                e.preventDefault();
            } else {
                // Show loading state
                const btn = document.getElementById('loginBtn');
                if (btn) btn.classList.add('loading');
            }
        });
    }

    function validateRegisterForm() {
        const form = document.getElementById('registerForm');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            let valid = true;

            // Username
            const username = document.getElementById('username');
            const usernameError = document.getElementById('usernameError');
            if (username.value.trim().length < 3) {
                usernameError.textContent = 'Username must be at least 3 characters.';
                username.classList.add('input-error');
                valid = false;
            } else {
                usernameError.textContent = '';
                username.classList.remove('input-error');
            }

            // Email
            const email = document.getElementById('email');
            const emailError = document.getElementById('emailError');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value.trim())) {
                emailError.textContent = 'Please enter a valid email address.';
                email.classList.add('input-error');
                valid = false;
            } else {
                emailError.textContent = '';
                email.classList.remove('input-error');
            }

            // Password
            const password = document.getElementById('password');
            const passwordError = document.getElementById('passwordError');
            if (password.value.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters.';
                password.classList.add('input-error');
                valid = false;
            } else {
                passwordError.textContent = '';
                password.classList.remove('input-error');
            }

            // Confirm Password
            const confirm = document.getElementById('confirm_password');
            const confirmError = document.getElementById('confirmError');
            if (confirm.value !== password.value) {
                confirmError.textContent = 'Passwords do not match.';
                confirm.classList.add('input-error');
                valid = false;
            } else {
                confirmError.textContent = '';
                confirm.classList.remove('input-error');
            }

            if (!valid) {
                e.preventDefault();
            } else {
                const btn = document.getElementById('registerBtn');
                if (btn) btn.classList.add('loading');
            }
        });

        // Real-time confirm password check
        const confirmInput = document.getElementById('confirm_password');
        if (confirmInput) {
            confirmInput.addEventListener('input', function () {
                const password = document.getElementById('password').value;
                const confirmError = document.getElementById('confirmError');
                if (confirmInput.value && confirmInput.value !== password) {
                    confirmError.textContent = 'Passwords do not match.';
                    confirmInput.classList.add('input-error');
                } else {
                    confirmError.textContent = '';
                    confirmInput.classList.remove('input-error');
                }
            });
        }
    }

    // =========================================================================
    // Input Focus Enhancements
    // =========================================================================
    function initInputFocus() {
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(function (input) {
            input.addEventListener('focus', function () {
                input.parentElement.style.transform = 'scale(1.01)';
            });
            input.addEventListener('blur', function () {
                input.parentElement.style.transform = 'scale(1)';
            });
        });
    }

    // =========================================================================
    // Keyboard Shortcuts
    // =========================================================================
    function initKeyboardShortcuts() {
        document.addEventListener('keydown', function (e) {
            // Ctrl/Cmd + Enter to submit form
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const form = document.querySelector('.auth-form');
                if (form) form.requestSubmit();
            }
        });
    }

    // =========================================================================
    // Initialize
    // =========================================================================
    document.addEventListener('DOMContentLoaded', function () {
        renderFlashMessages();
        initPasswordToggle();
        initPasswordStrength();
        validateLoginForm();
        validateRegisterForm();
        initInputFocus();
        initKeyboardShortcuts();
    });

})();
