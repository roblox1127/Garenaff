import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update the Fetch Offers URL
content = content.replace('fetch(API_URL)', 'fetch(`/get-offers?username=${encodeURIComponent(username)}`)')

# 2. Update the Click & Polling Logic
new_click_logic = """
    card.onclick = function() {
        window.open(link, '_blank');
        const btn = this.querySelector('.offer-btn');
        btn.innerHTML = '<i class="fas fa-sync fa-spin"></i> CHECKING';
        
        // Status Bar Update
        const statusContainer = document.getElementById('checkStatus');
        let lowerInstr = instructions.toLowerCase();
        let statusTitle = "MONITORING...";
        let statusSub = "Waiting for completion...";
        
        if (lowerInstr.includes('run') || lowerInstr.includes('install')) {
            statusTitle = "LISTENING FOR APP...";
            statusSub = "Keep open for 30s to trigger transfer.";
        } else if (lowerInstr.includes('email') || lowerInstr.includes('survey')) {
            statusTitle = "VERIFYING SUBMISSION...";
            statusSub = "Finalizing after form completion.";
        }

        if (statusContainer) {
            statusContainer.innerHTML = `<div style="color:#FEFD74; font-weight:bold;">${statusTitle}</div><div style="width:100%; height:4px; background:#333; margin:5px 0;"><div style="width:100%; height:100%; background:#FEFD74; animation: scanMove 2s infinite;"></div></div><div style="font-size:9px; color:#aaa;">${statusSub}</div>`;
        }

        // THE CONNECTION TO YOUR check-status FUNCTION
        if (window.verificationInterval) clearInterval(window.verificationInterval);
        window.verificationInterval = setInterval(async () => {
            try {
                const res = await fetch(`/check-status?username=${encodeURIComponent(username)}`);
                const data = await res.json();
                if (data.completed) {
                    clearInterval(window.verificationInterval);
                    btn.innerHTML = 'VERIFIED';
                    btn.style.background = '#2ecc71';
                    alert("Verification Successful! Redirecting...");
                    window.location.href = "https://your-success-page.com"; 
                }
            } catch (e) { console.error("Polling error"); }
        }, 5000);
    };
"""

# Replace the old card.onclick block
pattern = re.compile(r'card\.onclick = function\(\) \{.*?\}\s+\};', re.DOTALL)
content = pattern.sub(new_click_logic, content)

with open('index.html', 'w') as f:
    f.write(content)
