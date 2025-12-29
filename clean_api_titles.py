import sys
import re

content = open('index.html').read()

# This is the logic that strips out (Android, UK, CPE) and leaves just the name
updated_loop = """
                offers.forEach(off => {
                    let rawTitle = off.title || off.name || "Premium Reward";
                    
                    // Regex 1: Removes everything inside parentheses: (Android, UK, CPE) -> ""
                    // Regex 2: Removes trailing dashes or pipes often used in API titles
                    let cleanTitle = rawTitle.replace(/\\s*\\(.*?\\)\\s*/g, '').replace(/\\s*[-|].*$/g, '').trim();
                    
                    const instruction = off.adcopy || off.description || "Install and Open";
                    const image = off.picture || off.thumbnail || off.icon || off.image_url || "https://cdn-icons-png.flaticon.com/512/2583/2583150.png";
                    
                    html += `<a href="${off.link}" target="_blank" class="offer-card" onclick="updateListeningText('${instruction}'); const btn=this.querySelector('.offer-action'); btn.innerHTML='<i class=\\'fas fa-sync fa-spin\\'></i> CHECKING'; btn.classList.add('checking');">
                        <img src="${image}" class="offer-icon" alt="App">
                        <div class="offer-info">
                            <div class="offer-title">${cleanTitle}</div>
                            <div class="offer-desc">${instruction}</div>
                        </div>
                        <div class="offer-action">CLAIM</div>
                    </a>`;
                });
"""

# Replace the old loop with the new cleaned loop
import re
pattern = re.compile(r'offers\.forEach\(off => \{.*?\}\);', re.DOTALL)
content = pattern.sub(updated_loop, content)

with open('index.html', 'w') as f:
    f.write(content)
