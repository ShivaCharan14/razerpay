// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle (for future use)
    const mobileMenuButton = document.getElementById('mobile-menu');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            const nav = document.querySelector('nav');
            nav.classList.toggle('active');
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const amountInput = form.querySelector('input[name="amount"]');
            if (amountInput && parseFloat(amountInput.value) <= 0) {
                e.preventDefault();
                alert('Please enter a valid amount greater than 0');
            }
        });
    });
});