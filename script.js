
// Initial User Data
let balance = 0;
let isFirstDeposit = true;

// Dynamic Top 10 Leaderboard Data
const leaderboardData = [
    { name: "Sabbir Hossain", balance: 15400 },
    { name: "Tanvir Ahmed", balance: 12800 },
    { name: "Rahim Sheikh", balance: 9500 },
    { name: "Rakib Hasan", balance: 8200 },
    { name: "Anik Chowdhury", balance: 7100 },
    { name: "Mehedi Hasan", balance: 5900 },
    { name: "Imran Khan", balance: 4800 },
    { name: "Sakib Al Hasan", balance: 3500 },
    { name: "Mahmudul Haq", balance: 2900 },
    { name: "Fahim Shahriar", balance: 1800 }
];

// Load Leaderboard on Startup
document.addEventListener("DOMContentLoaded", () => {
    renderLeaderboard();
});

// UI Toggle Functions
function showDeposit() {
    document.getElementById("depositSection").classList.toggle("active");
    document.getElementById("withdrawSection").classList.remove("active");
}

function showWithdraw() {
    document.getElementById("withdrawSection").classList.toggle("active");
    document.getElementById("depositSection").classList.remove("active");
}

// Deposit Logic
function processDeposit() {
    const amountInput = document.getElementById("depositAmount");
    let amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount < 300 || amount > 10000) {
        alert("⚠️ Please enter a deposit amount between 300 BDT and 10,000 BDT.");
        return;
    }

    if (isFirstDeposit) {
        const bonus = amount * 0.30;
        amount += bonus;
        isFirstDeposit = false;
        alert(`🎉 Congratulations! You received a 30% first deposit bonus (+${bonus} BDT)!`);
    } else {
        alert(`✅ Deposit request of ${amount} BDT submitted successfully!`);
    }

    balance += amount;
    updateBalanceDisplay();
    amountInput.value = "";
    document.getElementById("depositSection").classList.remove("active");
}

// Withdraw Logic
function processWithdraw() {
    const amountInput = document.getElementById("withdrawAmount");
    const methodSelect = document.getElementById("paymentMethod");
    const amount = parseFloat(amountInput.value);
    const method = methodSelect.value.toUpperCase();

    if (isNaN(amount) || amount <= 0) {
        alert("⚠️ Please enter a valid withdrawal amount.");
        return;
    }

    if (amount > balance) {
        alert("❌ Insufficient balance for this withdrawal.");
        return;
    }

    balance -= amount;
    updateBalanceDisplay();
    alert(`✅ Withdrawal request of ${amount} BDT via ${method} is processing!`);
    amountInput.value = "";
    document.getElementById("withdrawSection").classList.remove("active");
}

// Balance Display Update
function updateBalanceDisplay() {
    document.getElementById("balance").innerText = balance.toFixed(2);
}

// Render Top 10 Leaderboard
function renderLeaderboard() {
    const listElement = document.getElementById("leaderboardList");
    listElement.innerHTML = "";

    // Sort descending and slice top 10
    const sorted = leaderboardData.sort((a, b) => b.balance - a.balance).slice(0, 10);

    sorted.forEach((user, index) => {
        const li = document.createElement("li");
        li.className = "leaderboard-item";
        li.innerHTML = `
            <span><strong>#${index + 1}</strong> ${user.name}</span>
            <span>${user.balance} ৳</span>
        `;
        listElement.appendChild(li);
    });
}
