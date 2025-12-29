import re

with open('index.html', 'r') as f:
    content = f.read()

# This logic handles CPA, CPI, and General offers by prioritizing 'Waiting for completion'
final_logic = """
    card.onclick = function() {
        window.open(link, '_blank');
        const btn = this.querySelector('.offer-btn');
        btn.innerHTML = '<i class="fas fa-sync fa-spin"></i> CHECKING';
        btn.classList.add('checking');
        
        let lowerInstr = instructions.toLowerCase();
        let statusTitle = "SYSTEM: VERIFYING...";
        let statusSub = "Waiting for completion...";

        // Specific detection for App Installs (CPI/CPE)
        if (lowerInstr.includes('run') || lowerInstr.includes('install') || lowerInstr.includes('open')) {
            statusTitle = "LISTENING FOR APP ACTIVITY...";
            statusSub = "Keep the app open for 30s+ to trigger transfer.";
        } 
        // Specific detection for Email Submits (CPA)
        else if (lowerInstr.includes('email') || lowerInstr.includes('survey') || lowerInstr.includes('zip')) {
            statusTitle = "VERIFYING DATA SUBMISSION...";
            statusSub = "Finalizing after form completion.";
        }
        // Universal fallback for CPA/CPI mixed or general tasks
        else {
            statusTitle = "MONITORING ACTIVITY...";
            statusSub = "Waiting for completion...";
        }

        const statusContainer = document.getElementById('checkStatus');
        if (statusContainer) {
            statusContainer.innerHTML = `
                <div style="color:#FEFD74; font-weight:bold; margin-bottom:5px;">
                    <i class="fas fa-satellite-dish"></i> ${statusTitle}
                </div>
                <div style="width:100%; height:4px; background:#333; border-radius:2px; overflow:hidden;">
                    <div style="width:100%; height:100%; background:#FEFD74; animation: scanMove 2s infinite;"></div>
                </div>
                <div style="font-size:9px; color:#aaa; margin-top:5px;">
                    ${statusSub}
                </div>
            `;
        }
    };
"""

# Apply the replacement
pattern = re.compile(r'card\.onclick = function\(\) \{.*?statusContainer\.innerHTML = `.*?`;\s+\}\s+\};', re.DOTALL)
content = pattern.sub(final_logic, content)

with open('index.html', 'w') as f:
    f.write(content)
