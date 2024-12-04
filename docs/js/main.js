// Données statiques (à remplacer par vos vraies données)
const sportsData = [
    {
        name: "Football",
        clubs: [
            {
                name: "Club de Football Albi",
                address: "1 rue du Sport, 81000 Albi",
                phone: "05.XX.XX.XX.XX"
            }
        ]
    },
    // Ajoutez d'autres sports et clubs ici
];

function displaySports() {
    const sportsList = document.getElementById('sports-list');
    
    sportsData.forEach(sport => {
        const sportSection = document.createElement('div');
        sportSection.className = 'mb-4';
        
        sportSection.innerHTML = `
            <h2 class="mb-3">${sport.name}</h2>
            <div class="row">
                ${sport.clubs.map(club => `
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${club.name}</h5>
                                <p class="card-text">
                                    <strong>Adresse:</strong> ${club.address}<br>
                                    <strong>Téléphone:</strong> ${club.phone}
                                </p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        sportsList.appendChild(sportSection);
    });
}

// Charger les données au chargement de la page
document.addEventListener('DOMContentLoaded', displaySports);
