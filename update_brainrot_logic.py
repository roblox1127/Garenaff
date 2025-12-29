import re

with open('index.html', 'r') as f:
    content = f.read()

# This is the exact cleaning and loading logic from the reference site
new_logic = """
    async function loadCPAOffers(username) {
        const list = document.getElementById('offerList');
        list.innerHTML = '<div style="text-align:center; padding:20px; color:#aaa;"><i class="fas fa-circle-notch fa-spin"></i> Loading...</div>';
        
        try {
            const res = await fetch(`/get-offers?username=${encodeURIComponent(username)}`);
            const data = await res.json();
            const offers = Array.isArray(data) ? data : data.offers;
            
            list.innerHTML = '';
            offers.forEach(offer => {
                // CLEANING LOGIC: Remove (Android, UK, CPE) etc.
                let rawTitle = offer.name_short || offer.title || "Premium Reward";
                let cleanTitle = rawTitle.split('(')[0].split(' -')[0].trim();
                
                let instructions = offer.adcopy || offer.description || "Complete to verify.";
                let img = offer.picture || offer.thumbnail || "https://cdn-icons-png.flaticon.com/512/2583/2583150.png";
                let link = offer.link;

                const card = document.createElement('div');
                card.className = 'offer-card';
                card.innerHTML = `
                    <img src="${img}" class="offer-icon">
                    <div class="offer-info">
                        <span class="offer-title">${cleanTitle}</span>
                        <div class="instruction-box"><i class="fas fa-info-circle"></i> ${instructions}</div>
                    </div>
                    <div class="offer-btn">CLAIM</div>
                `;

                card.onclick = function() {
                    window.open(link, '_blank');
                    const btn = this.querySelector('.offer-btn');
                    btn.innerHTML = '<i class="fas fa-sync fa-spin"></i> CHECKING';
                    btn.classList.add('checking');
                    
                    // PERSISTENT STATUS: Update the bar with specific CPA/CPE instructions
                    const statusContainer = document.getElementById('checkStatus');
                    if (statusContainer) {
                        statusContainer.innerHTML = `
                            <div style="color:#FEFD74; font-weight:bold; margin-bottom:5px;">
                                <i class="fas fa-satellite-dish"></i> MONITORING ACTIVITY...
                            </div>
                            <div style="width:100%; height:4px; background:#333; border-radius:2px; overflow:hidden;">
                                <div style="width:100%; height:100%; background:#FEFD74; animation: scanMove 2s infinite;"></div>
                            </div>
                            <div style="font-size:9px; color:#aaa; margin-top:5px;">
                                Task: ${instructions}
                            </div>
                        `;
                    }
                };
                list.appendChild(card);
            });
        } catch (e) {
            list.innerHTML = '<p style="color:#777; font-size:11px;">Region error. Refreshing...</p>';
        }
    }
"""

# Replace the entire loadCPAOffers function
pattern = re.compile(r'async function loadCPAOffers\(username\).*?\}\n    \}', re.DOTALL)
content = pattern.sub(new_logic, content)

with open('index.html', 'w') as f:
    f.write(content)
