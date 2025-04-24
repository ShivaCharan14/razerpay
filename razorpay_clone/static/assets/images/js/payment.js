// Payment page specific functionality
document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    const paymentStatus = document.getElementById('payment-status');
    
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitButton = paymentForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<img src="/static/assets/images/loading.gif" alt="Processing"> Processing...';
            
            // Simulate API call
            setTimeout(() => {
                paymentForm.submit();
            }, 1500);
        });
    }
    
    if (paymentStatus) {
        // Animate status display
        paymentStatus.style.opacity = 0;
        setTimeout(() => {
            paymentStatus.style.transition = 'opacity 0.5s ease';
            paymentStatus.style.opacity = 1;
        }, 300);
    }
});