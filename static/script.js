document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        checkbox.parentElement.submit(); // submits the form when checkbox changes
    });
});
