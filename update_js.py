import sys
content = open('index.html').read()
old_template = 'html += `<a href="${off.link}" target="_blank" class="offer-card">'
new_template = 'html += `<a href="${off.link}" target="_blank" class="offer-card" onclick="const btn=this.querySelector(\'.offer-action\'); btn.innerHTML=\'CHECKING...\'; btn.classList.add(\'checking\');">'
content = content.replace(old_template, new_template)
with open('index.html', 'w') as f:
    f.write(content)
