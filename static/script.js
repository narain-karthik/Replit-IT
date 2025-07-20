// GTN Engineering IT Helpdesk - Client-side JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('GTN Engineering IT Helpdesk loaded successfully');
    
    // Initialize source code protection
    initializeSourceProtection();

    // Initialize all components
    initializeAlerts();
    initializeTooltips();
    initializeFormValidation();
    initializeSearch();
    initializeAutoRefresh();

    // Custom nl2br filter for displaying text with line breaks
    applyNl2br();
});

/**
 * Initialize source code protection measures
 */
function initializeSourceProtection() {
    // Disable right-click context menu
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        showNotification('Right-click is disabled for security reasons', 'warning');
        return false;
    });

    // Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U, Ctrl+Shift+C
    document.addEventListener('keydown', function(e) {
        // F12 - Developer Tools
        if (e.key === 'F12') {
            e.preventDefault();
            showNotification('Developer tools access is restricted', 'warning');
            return false;
        }

        // Ctrl+Shift+I - Developer Tools
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            showNotification('Developer tools access is restricted', 'warning');
            return false;
        }

        // Ctrl+Shift+J - Console
        if (e.ctrlKey && e.shiftKey && e.key === 'J') {
            e.preventDefault();
            showNotification('Console access is restricted', 'warning');
            return false;
        }

        // Ctrl+U - View Source
        if (e.ctrlKey && e.key === 'u') {
            e.preventDefault();
            showNotification('View source is disabled for security reasons', 'warning');
            return false;
        }

        // Ctrl+Shift+C - Element Inspector
        if (e.ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            showNotification('Element inspector is restricted', 'warning');
            return false;
        }

        // Ctrl+A - Select All (prevent copying entire page)
        if (e.ctrlKey && e.key === 'a') {
            e.preventDefault();
            showNotification('Select all is restricted', 'warning');
            return false;
        }
    });

    // Disable text selection on sensitive elements
    const sensitiveElements = document.querySelectorAll('script, style, .header, .footer, .navbar');
    sensitiveElements.forEach(function(element) {
        element.style.userSelect = 'none';
        element.style.webkitUserSelect = 'none';
        element.style.mozUserSelect = 'none';
        element.style.msUserSelect = 'none';
    });

    // Detect developer tools
    let devtools = {
        open: false,
        orientation: null
    };

    setInterval(function() {
        if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200) {
            if (!devtools.open) {
                devtools.open = true;
                showNotification('Developer tools detected - session will be logged', 'danger');
                // Log the attempt (in production, this could send to server)
                console.warn('Developer tools opened at:', new Date().toISOString());
            }
        } else {
            devtools.open = false;
        }
    }, 1000);

    // Disable drag and drop
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });

    // Disable image saving
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault();
            return false;
        }
    });

    // Clear console periodically
    setInterval(function() {
        if (typeof console !== 'undefined') {
            console.clear();
        }
    }, 10000);

    // Obfuscate sensitive data in DOM
    obfuscateSensitiveData();
}

/**
 * Initialize auto-dismissing alerts
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success')) {
            // Auto-dismiss success alerts after 5 seconds
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }

      //  if (alert.classList.contains('alert-info')) {
            // Auto-dismiss info alerts after 8 seconds (example)
        //    setTimeout(function() {
       //         const bsAlert = new bootstrap.Alert(alert);
       //         bsAlert.close();
       //     }, 9999); // you can change this to any time you prefer
       // }
    });
}


/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation and enhancements
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // Character counter for text fields
    const textFields = document.querySelectorAll('input[type="text"], textarea');
    textFields.forEach(function(field) {
        if (field.hasAttribute('maxlength')) {
            addCharacterCounter(field);
        }
    });
}

/**
 * Add character counter to form fields
 */
function addCharacterCounter(field) {
    const maxLength = field.getAttribute('maxlength');
    const counter = document.createElement('div');
    counter.className = 'form-text text-muted';
    counter.id = field.id + '_counter';

    function updateCounter() {
        const remaining = maxLength - field.value.length;
        counter.textContent = `${field.value.length}/${maxLength} characters`;

        if (remaining < 10) {
            counter.classList.add('text-warning');
            counter.classList.remove('text-muted');
        } else {
            counter.classList.remove('text-warning');
            counter.classList.add('text-muted');
        }
    }

    field.addEventListener('input', updateCounter);
    field.parentNode.appendChild(counter);
    updateCounter();
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(function(input) {
        let searchTimeout;

        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);

            // Add loading state
            input.classList.add('loading');

            searchTimeout = setTimeout(function() {
                input.classList.remove('loading');
                // Auto-submit form after 500ms of no typing
                if (input.value.length > 2 || input.value.length === 0) {
                    input.closest('form').submit();
                }
            }, 500);
        });
    });
}

/**
 * Initialize auto-refresh for dashboards
 */
function initializeAutoRefresh() {
    // Auto-refresh dashboard every 30 seconds if on dashboard page
    if (window.location.pathname.includes('dashboard')) {
        let refreshInterval = setInterval(function() {
            // Only refresh if user is still active (not idle)
            if (document.hasFocus()) {
                const currentTime = new Date().getTime();
                const lastActivity = localStorage.getItem('lastActivity') || currentTime;

                // Refresh if user was active in the last 5 minutes
                if (currentTime - lastActivity < 300000) {
                    refreshDashboard();
                }
            }
        }, 30000);

        // Track user activity
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(function(event) {
            document.addEventListener(event, function() {
                localStorage.setItem('lastActivity', new Date().getTime());
            });
        });

        // Clear interval when page is unloaded
        window.addEventListener('beforeunload', function() {
            clearInterval(refreshInterval);
        });
    }
}

/**
 * Refresh dashboard data
 */
function refreshDashboard() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        table.style.opacity = '0.8';
    });

    // Simulate data refresh (in a real app, this would be an AJAX call)
    setTimeout(function() {
        tables.forEach(function(table) {
            table.style.opacity = '1';
        });

        // Show refresh notification
        showNotification('Dashboard updated', 'info');
    }, 1000);
}

/**
 * Apply nl2br filter to elements with line breaks
 */
function applyNl2br() {
    const elements = document.querySelectorAll('[data-nl2br]');
    elements.forEach(function(element) {
        element.innerHTML = element.innerHTML.replace(/\n/g, '<br>');
    });
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';

    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(toast);

    // Auto-dismiss after 3 seconds
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(toast);
        bsAlert.close();
    }, 3000);
}

/**
 * Confirm dialog for destructive actions
 */
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy to clipboard', 'danger');
    });
}

/**
 * Validate form fields
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

/**
 * Handle form submission with loading state
 */
function handleFormSubmit(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Processing...';

        // Re-enable button after 5 seconds as fallback
        setTimeout(function() {
            submitButton.disabled = false;
            submitButton.innerHTML = submitButton.getAttribute('data-original-text') || 'Submit';
        }, 5000);
    }
}

/**
 * Initialize keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Ctrl+/ or Cmd+/ for help
    if ((event.ctrlKey || event.metaKey) && event.key === '/') {
        event.preventDefault();
        showKeyboardShortcuts();
    }

    // Escape key to close modals
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(function(modal) {
            bootstrap.Modal.getInstance(modal).hide();
        });
    }
});

/**
 * Show keyboard shortcuts modal
 */
function showKeyboardShortcuts() {
    const shortcuts = [
        { key: 'Ctrl + /', description: 'Show keyboard shortcuts' },
        { key: 'Escape', description: 'Close modal dialogs' },
        { key: 'Tab', description: 'Navigate between form fields' },
        { key: 'Enter', description: 'Submit forms' }
    ];

    let shortcutsList = shortcuts.map(function(shortcut) {
        return `<tr><td><kbd>${shortcut.key}</kbd></td><td>${shortcut.description}</td></tr>`;
    }).join('');

    const modalHtml = `
        <div class="modal fade" id="keyboardShortcutsModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Keyboard Shortcuts</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Shortcut</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${shortcutsList}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if present
    const existingModal = document.getElementById('keyboardShortcutsModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('keyboardShortcutsModal'));
    modal.show();
}

/**
 * Smooth scroll to features section (for home page)
 */
function scrollToFeatures() {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
        featuresSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Initialize home page specific functionality
 */
function initializeHomePage() {
    // Add parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;

            const heroGradient = document.querySelector('.hero-gradient');
            if (heroGradient) {
                heroGradient.style.transform = `translateY(${parallax}px)`;
            }
        });
    }

    // Animate feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards and role cards
    document.querySelectorAll('.feature-card, .role-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Initialize home page features if on home page
document.addEventListener('DOMContentLoaded', function() {
    const isHomePage = document.querySelector('.hero-section');
    if (isHomePage) {
        initializeHomePage();
    }
});

/**
 * Obfuscate sensitive data in DOM
 */
function obfuscateSensitiveData() {
    // Hide sensitive attributes and data
    const sensitiveAttributes = ['data-user-id', 'data-role', 'data-token'];
    sensitiveAttributes.forEach(function(attr) {
        const elements = document.querySelectorAll(`[${attr}]`);
        elements.forEach(function(element) {
            element.removeAttribute(attr);
        });
    });

    // Remove debug information
    const debugElements = document.querySelectorAll('.debug, .dev-info, [data-debug]');
    debugElements.forEach(function(element) {
        element.remove();
    });
}

/**
 * Advanced protection against inspection
 */
function advancedProtection() {
    // Create invisible overlay to prevent easy inspection
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        background: transparent;
    `;
    document.body.appendChild(overlay);

    // Monitor for tools that might be inspecting the page
    let inspectionCount = 0;
    const originalLog = console.log;
    console.log = function(...args) {
        inspectionCount++;
        if (inspectionCount > 10) {
            showNotification('Unusual activity detected', 'danger');
        }
        originalLog.apply(console, args);
    };
}

// Initialize advanced protection
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(advancedProtection, 1000);
});

// Export functions for global use
window.GTNHelpdesk = {
    showNotification: showNotification,
    confirmAction: confirmAction,
    formatDate: formatDate,
    copyToClipboard: copyToClipboard,
    validateForm: validateForm,
    handleFormSubmit: handleFormSubmit,
    scrollToFeatures: scrollToFeatures
};
