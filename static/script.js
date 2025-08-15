document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
        const li = checkbox.closest('li');
        li.classList.toggle('done'); // toggle done class for immediate visual feedback

        // Optional: small delay to see effect before submitting
        setTimeout(() => {
            checkbox.parentElement.submit();
        }, 150); // 150ms delay
    });
});

