function predictDemand() {
    const year = document.getElementById("year").value;
    const month = document.getElementById("month").value;
    const week = document.getElementById("week").value;

    const resultDiv = document.getElementById("result");
    resultDiv.classList.add("hidden");
    resultDiv.innerHTML = "";

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ year, month, week })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            resultDiv.innerHTML = "❌ Error: " + data.error;
            resultDiv.classList.remove("hidden");
            return;
        }

        let html = `
            <h3>📈 Predicted Weekly Demand</h3>
            <p><strong>${data.prediction.toLocaleString()}</strong> units</p>

            <h4>📅 Next 4 Weeks Forecast</h4>
            <ul>
                ${data.future_predictions.map(
                    (v, i) => `<li>Week +${i + 1}: ${v.toLocaleString()} units</li>`
                ).join("")}
            </ul>

            <h4>🔍 Top Influencing Features</h4>
            <ul>
                ${data.explanation.map(
                    e => `<li>${e.feature}: ${e.importance}%</li>`
                ).join("")}
            </ul>
        `;

        resultDiv.innerHTML = html;
        resultDiv.classList.remove("hidden");
    })
    .catch(err => {
        resultDiv.innerHTML = "❌ Server error";
        resultDiv.classList.remove("hidden");
    });
}
