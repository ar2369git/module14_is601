

document
  .getElementById("login-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const username_or_email = e.target.username_or_email.value;
    const password = e.target.password.value;

    const resp = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username_or_email, password }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      document.getElementById("message").innerText = err.detail || "Login failed";
      return;
    }

    const { access_token } = await resp.json();
    // save it!
    localStorage.setItem("jwt_token", access_token);

    // redirect to calculator
    window.location.href = "/";
  });