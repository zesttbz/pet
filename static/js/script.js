async function loadPet() {
    const res = await fetch('/api/pet');
    const pet = await res.json();
    if (pet.name) {
        document.getElementById('pet-name').textContent = pet.name;
        document.getElementById('pet-level').textContent = pet.level;
        document.getElementById('pet-exp').textContent = pet.experience;

        document.getElementById('feed-btn').disabled = pet.fed_today;
        document.getElementById('play-btn').disabled = pet.played_today;
        document.getElementById('bathe-btn').disabled = pet.bathed_today;
    } else {
        const name = prompt("Đặt tên thú cưng của bạn:");
        await fetch('/api/pet', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name })
        });
        loadPet();
    }
}

async function doAction(action) {
    const res = await fetch('/api/pet', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ action })
    });
    const pet = await res.json();
    document.getElementById('pet-level').textContent = pet.level;
    document.getElementById('pet-exp').textContent = pet.experience;

    if (action === 'feed') document.getElementById('feed-btn').disabled = true;
    if (action === 'play') document.getElementById('play-btn').disabled = true;
    if (action === 'bathe') document.getElementById('bathe-btn').disabled = true;
}

document.addEventListener('DOMContentLoaded', loadPet);