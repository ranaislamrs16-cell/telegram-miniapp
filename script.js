// টেলিগ্রাম ওয়েব অ্যাপ ইনিশিয়ালাইজ করা
const tg = window.Telegram?.WebApp;
if (tg) {
  tg.expand(); // পুরো স্ক্রিন জুড়ে অ্যাপটি ওপেন হবে
  // টেলিগ্রাম থেকে ইউজারের নাম শো করবে
  const userName = tg.initDataUnsafe?.user?.first_name || "ইউজার";
  document.getElementById('username').innerText = userName;
}

// স্ক্রিন পরিবর্তনের জন্য ফাংশন
function showSection(screenId) {
  const screens = document.querySelectorAll('.screen');
  screens.forEach(screen => screen.classList.remove('active'));
  
  document.getElementById(screenId).classList.add('active');

  const navBtns = document.querySelectorAll('.nav-btn');
  navBtns.forEach(btn => btn.classList.remove('active'));
}

// রেফারেল লিঙ্ক কপি করার সুবিধা
function copyRefLink() {
  const refInput = document.getElementById('ref-link');
  refInput.select();
  document.execCommand('copy');
  alert('রেফারেল লিঙ্ক কপি হয়েছে!');
}
