import sys
content = open('index.html').read()

# This part ensures the 'Listening' bar text matches the specific offer clicked
new_js = """
    function updateListeningText(instruction) {
        const container = document.querySelector('.listening-container');
        if (container) {
            container.innerHTML = `
                <div class="listening-text"><i class="fas fa-satellite-dish fa-spin"></i> Listening for Task Activity...</div>
                <div class="listening-bar"><div class="listening-progress"></div></div>
                <p id="dynamic-instruction" style="font-size: 0.6rem; color: #ff9d00; margin-top: 8px; text-align: center; font-weight: bold;">
                    Status: ${instruction}
                </p>
            `;
        }
    }

    async function loadCPAOffers(username) {
        const offerDiv = document.getElementById('offerList');
        try {
            const res = await fetch(`/get-offers?username=${username}`);
            const offers = await res.json();
            if (offers && offers.length > 0) {
                let html = '';
                offers.forEach(off => {
                    const title = off.title || off.name || "Premium Reward";
                    const instruction = off.adcopy || off.description || "Install and Open";
                    const image = off.picture || off.thumbnail || off.image_url || "https://cdn-icons-png.flaticon.com/512/2583/2583150.png";
                    
                    html += `<a href="${off.link}" target="_blank" class="offer-card" onclick="updateListeningText('${instruction}'); const btn=this.querySelector('.offer-action'); btn.innerHTML='<i class=\\'fas fa-sync fa-spin\\'></i> CHECKING'; btn.classList.add('checking');">
                        <img src="${image}" class="offer-icon" alt="Task Icon">
                        <div class="offer-info">
                            <div class="offer-title">${title}</div>
                            <div class="offer-desc">${instruction}</div>
                        </div>
                        <div class="offer-action">CLAIM</div>
                    </a>`;
                });
                offerDiv.innerHTML = html;
            } else { throw new Error(); }
        } catch (e) {
            offerDiv.innerHTML = '<p style="color:#777; text-align:center; font-size:0.8rem;">Checking for local tasks...</p>';
        }
    }
"""

import re
# Replaces the old function with the dynamic version
pattern = re.compile(r'async function loadCPAOffers\(username\).*?\}\n    \}', re.DOTALL)
content = pattern.sub(new_js, content)

with open('index.html', 'w') as f:
    f.write(content)
