const $ = (id) => document.getElementById(id);

$("run").onclick = async () => {
  const jd = $("jd").value.trim();
  const resume = $("resume").value.trim();
  if (jd.length < 20 || resume.length < 20) {
    alert("Please provide both a Job Description and Resume.");
    return;
  }

  $("status").textContent = "Running...";
  $("run").disabled = true;

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({job_description: jd, resume_text: resume})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis failed");

    $("results").classList.remove("hidden");
    $("coverage").textContent = data.summary.skill_coverage_percent + "%";
    $("agents").textContent = data.summary.agents_run;

    $("cards").innerHTML = data.agents.map(a => `
      <div class="card">
        <h3>${escapeHtml(a.agent)}</h3>
        <pre>${escapeHtml(JSON.stringify(a.data, null, 2))}</pre>
      </div>
    `).join("");

    $("status").textContent = "Completed";
  } catch (e) {
    $("status").textContent = "Error";
    alert(e.message);
  } finally {
    $("run").disabled = false;
  }
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&","&amp;").replaceAll("<","&lt;")
    .replaceAll(">","&gt;").replaceAll('"',"&quot;");
}
