// themeToggle.js
document.getElementById('themeToggle').addEventListener('click', function() {
    var body = document.body;
    body.classList.toggle('bg-dark');
    body.classList.toggle('text-light');
    body.classList.toggle('bg-light');
    body.classList.toggle('text-dark');

    // Additional elements to toggle, if necessary
});