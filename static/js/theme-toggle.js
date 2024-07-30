document.addEventListener('DOMContentLoaded', (event) => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        body.classList.toggle('light-mode');

        // Salva a preferência do usuário no localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });

    // Verifica a preferência do usuário no localStorage ao carregar a página
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme === 'dark' ? 'dark-mode' : 'light-mode');
        body.classList.add(savedTheme === 'light' ? 'light-mode' : 'dark-mode');
    } else {
        body.classList.add('light-mode'); // Modo padrão
    }
});
