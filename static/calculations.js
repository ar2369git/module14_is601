// static/calculations.js
import { getToken, apiFetch } from "./auth.js";

async function reloadList() {
  const res = await apiFetch("/calculations", { method: "GET" });
  const list = document.getElementById("calc-list");
  list.innerHTML = "";
  for (let c of await res.json()) {
    const li = document.createElement("li");
    li.textContent = `(${c.id}) ${c.a} ${c.type} ${c.b} = ${c.result}`;
    // add edit & delete buttons…
    list.appendChild(li);
  }
}

document.getElementById("add-form").addEventListener("submit", async e => {
  e.preventDefault();
  const f = e.target;
  const payload = {
    a: parseFloat(f.a.value),
    b: parseFloat(f.b.value),
    type: f.type.value,
  };
  const res = await apiFetch("/calculations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  const msg = document.getElementById("message");
  if (res.ok) {
    msg.textContent = "Calculation added";
    f.reset();
    await reloadList();
  } else {
    const err = await res.json();
    msg.textContent = err.detail || err.error;
  }
});

window.addEventListener("DOMContentLoaded", reloadList);