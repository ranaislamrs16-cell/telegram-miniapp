let balance = 0;
const balanceElement = document.getElementById('balance');
const tapBtn = document.getElementById('tap-btn');

tapBtn.addEventListener('click', (e) => {
  balance += 1;
  balanceElement.innerText = balance;

  // Floating text (+1) effect
  const floatingText = document.createElement('div');
  floatingText.innerText = '+1';
  floatingText.className = 'floating-text';
  
  const rect = tapBtn.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  floatingText.style.left = `${e.clientX}px`;
  floatingText.style.top = `${e.clientY}px`;
  
  document.body.appendChild(floatingText);

  setTimeout(() => {
    floatingText.remove();
  }, 800);
});

// Initialize Telegram WebApp
if (window.Telegram && window.Telegram.WebApp) {
  window.Telegram.WebApp.ready();
}
