document.addEventListener('DOMContentLoaded', () => {
    // Handle popup
    const popup = document.getElementById('sacha-popup');
    const pokeball = document.getElementById('pokeball');
    const pokemonDisplay = document.getElementById('pokemon-display');
    const themeMusic = document.getElementById('theme-music');

    // Ensure music starts on page load (requires user interaction for autoplay)
    document.addEventListener('click', () => {
        if (themeMusic.paused) {
            themeMusic.play().catch(err => console.warn("Autoplay failed:", err));
        }
    }, { once: true });

    // Close popup when clicked
    popup.addEventListener("click", function () {
        popup.style.display = "none";
    });

    // Pokeball remains clickable even when popup is open
    pokeball.addEventListener("click", function (event) {
        event.stopPropagation();
        console.log("Pokeball clicked!");
        
        const pokemon = ['Pikachu', 'Charmander', 'Bulbasaur', 'Squirtle'];
        const randomPokemon = pokemon[Math.floor(Math.random() * pokemon.length)];

        pokemonDisplay.innerHTML = `
            <div class="pokemon-card">
                <h2>${randomPokemon} appeared!</h2>
                <div class="sprite"></div>
            </div>
        `;

        // Ensure text appears on top of background logo
        pokemonDisplay.style.zIndex = "1001";
        pokemonDisplay.style.position = "relative";
    });

    // Add hover effects
    document.querySelectorAll('.interactive-section div').forEach(element => {
        element.addEventListener('mouseover', () => {
            element.style.transform = 'scale(1.1)';
        });

        element.addEventListener('mouseout', () => {
            element.style.transform = 'scale(1)';
        });
    });

    // Add particle effect on pokeball click
    import('https://cdn.jsdelivr.net/npm/party-js@latest/bundle/party.min.js').then(() => {
        pokeball.addEventListener('click', (e) => {
            party.confetti(e.clientX, e.clientY);
        });
    });

    // Add hover tooltips
    tippy('[data-tippy-content]', {
        theme: 'pokemon',
        animation: 'scale'
    });
});
